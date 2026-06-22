# Install Semantic Ingestion Worker v0.1

## Overview
This prompt installs the Semantic Ingestion Worker, the first "brainstem" worker that processes files from the ingestion queue and creates semantic profile stubs for the embedder/router.

## Prerequisites
- Supabase project configured
- Cloudflare Workers account
- Wrangler CLI installed (`npm install -g wrangler`)

## Installation Steps

### 1. Database Migrations
Run these migrations in your Supabase SQL editor (in order):

```sql
-- Migration 001: ingestion_queue table
-- File: data/migrations/001_ingestion_queue.sql

-- Migration 002: Extend semantic_profile for file-level stubs
-- File: data/migrations/002_semantic_profile_file_level.sql
```

**Note**: The semantic_profile migration makes chunk_id/chunk_text optional and adds file_path as a unique conflict target for file-level stubs.

### 2. Deploy Worker

Navigate to the worker directory:
```bash
cd workers/ingestion
```

Bind Supabase secrets:
```bash
npx wrangler secret put SUPABASE_URL
npx wrangler secret put SUPABASE_SERVICE_ROLE_KEY
```

Deploy:
```bash
npx wrangler deploy
```

### 3. Verify Deployment

Check worker status in Supabase:
```sql
SELECT * FROM public.worker_status WHERE worker_id = 'ingestion';
```

The worker runs on a cron schedule (every 2 minutes) and will:
- Pull pending items from `ingestion_queue`
- Create semantic_profile stubs
- Mark queue items as complete or quarantined
- Update heartbeat in `worker_status`

### 4. Test Queue Insertion

Insert a test item into the queue:
```sql
INSERT INTO public.ingestion_queue (
  file_path,
  slug,
  realm_guess,
  mime_type,
  file_ext,
  status
) VALUES (
  'realms/qivault/kb/test_document.md',
  'test_document',
  'QiVault',
  'text/markdown',
  'md',
  'pending'
);
```

Wait up to 2 minutes for the cron to process. Check:
- `ingestion_queue.status` should be `complete`
- `semantic_profile` should have a record with `file_path` matching
- `worker_status` should show `state = 'green'` for worker_id `ingestion`

## Architecture Notes

### Worker Responsibilities
- **Pull Queue**: Fetches pending items from `ingestion_queue`
- **Extract Text**: Placeholder stub (real extraction via FS adapter later)
- **Create Profile**: Upserts file-level semantic_profile stub
- **Mark Complete**: Updates queue status
- **Heartbeat**: Reports health to `worker_status`

### Queue Status Flow
1. `pending` → inserted by scanner/FS adapter
2. `in_progress` → worker processing
3. `complete` → successfully processed
4. `quarantined` → error occurred, check `meta.error`

### Semantic Profile Structure
File-level stubs include:
- `file_path` (unique, conflict target)
- `qid`, `slug`, `realm`, `realm_slug`
- `mime_type`, `file_ext`, `content_hash`
- `extracted_text` (stub for now)
- `embedding_status = 'pending'` (embedder picks this up)
- `chunk_count = 0` (chunker will populate)

### Next Steps
After ingestion worker is running:
1. **Embedder Worker**: Processes `embedding_status = 'pending'` records
2. **Router Worker**: Uses embeddings to route files to correct realms
3. **FS Adapter**: Real file system integration for text extraction/OCR

## Troubleshooting

### Worker Not Running
- Check `worker_status` table for error codes
- Verify secrets are bound: `npx wrangler secret list`
- Check cron trigger: `npx wrangler deployments list`

### Queue Items Stuck
- Check `ingestion_queue.status` and `meta` for error details
- Verify `semantic_profile` table has file_path unique constraint
- Check Supabase logs for constraint violations

### Migration Errors
- Ensure `semantic_profile` table exists before running migration 002
- Check for existing `file_path` column conflicts
- Verify constraint `semantic_profile_file_or_chunk_check` is valid

## Canon Check
✅ **Layer 6 Compliance**: Worker operates at semantic ingestion layer
✅ **Non-Destructive**: Only creates/updates, never deletes
✅ **Heartbeat Pattern**: Follows established worker_status pattern
✅ **Queue-Based**: Uses ingestion_queue for async processing
✅ **Stub Pattern**: Creates file-level stubs for downstream workers

