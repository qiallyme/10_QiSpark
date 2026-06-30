---
date: 2026-05-17
title: Open Loop Reset and Paperless Ingestion Runbook
category: operations
project_context: QiAccess / QiNexus / Paperless-NGX / MomCare / QiNote
status: active
tags:
  - open-loops
  - paperless-ngx
  - ingestion
  - qinexus
  - qiaccess
  - runbook
---

# Open Loop Reset and Paperless Ingestion Runbook

## Purpose

This page captures the current open loops across active system work and defines the next sane execution order. The goal is to stop context loss, prevent repeated redesign, and move from scattered updates into controlled completion.

This also includes the first working strategy for recursively ingesting eligible files from a folder into Paperless-NGX.

---

# 1. Current Open Loop Map

| Thread | Current State | Next Move |
|---|---|---|
| MomCare App QA Checklist | Markdown checklist was created for MomCare app testing. It covers startup, dashboard, daily care log, vitals, privacy, retest, and AI work-order capture. | Use it during app testing. Every bug becomes an AI work order. |
| QiAccess Start QA Checklist | Markdown checklist was created for QiAccess Start testing. It covers access, service links, docs alignment, build/deploy, regression, and acceptance. | Test QiAccess Start and capture broken links/routes. |
| Supabase Visual / ERD Problem | DBeaver became a distraction because connection/password was blocking progress. Direction changed to direct schema export. | Export all schemas, tables, and fields directly from Postgres/Supabase metadata for Markmind or ERD use. |
| Directory Markmind Mapper Toolbox Tool | Standalone toolbox module was planned, but import error occurred: `ModuleNotFoundError: tools.system.sys_directory_markmind_mapper.SysDirectoryMarkmindMapperTool`. | Fix module path, file name, class name, and import alignment. |
| Paperless-NGX | Paperless is running and should not be rebuilt if healthy. It needs final admin validation. | Confirm login, consume folder, OCR test, and API token. |
| QiAccess / QiNexus / QiNote Architecture | Core doctrine is mostly settled: QiAccess is the front door/interface, QiNexus is storage/assets, QiLabs is code/execution, database is structured confirmed records. | Stop redesigning the universe. Convert decisions into docs, scripts, and tests. |
| QiNexus Folder Numbering | Root folders should be numbered and intentionally ordered, not left to alphabetic sorting. | Lock root numbering and only reopen if there is a real structural conflict. |
| QiCode / File IDs | Direction is path-derived code plus version, with date where useful. | Needs one final naming spec before scripts enforce it. |
| Mom / Caregiver Documentation | Daily logs, vitals, MyChart tasks, safety notes, and PT descriptions are being captured. Manual typing is not sustainable. | Build photo/voice capture flow into spreadsheet/database and Family Wall visibility. |
| Graphify / RAG / Graph Layer | Graphify is useful as a mapping layer, not the source of truth. Markdown/files remain truth. | Test Graphify on repo/docs first, not sensitive personal corpora. |
| Qdrant / Neo4j / Paperless Pipeline | Proposed pipeline: Paperless docs → canonical SQL tables → embeddings/Qdrant → Neo4j graph. | Downstream. Do not touch until Paperless basics are stable. |
| QiAccess Start UI | Route doctrine exists: Home, Start, Capture, Knowledge, Memory, Insights, System. Known bug: public URL may override private/tailnet/local URL. | Fix service URL resolver priority so private/tailnet/local wins in admin/local mode. |

---

# 2. Actual Priority Order

Do not touch all of these at once.

## Priority 1 — Finish Testing Artifacts

Use the existing QA checklists.

- Test MomCare App.
- Test QiAccess Start.
- Convert every bug into an AI work order.

## Priority 2 — Fix Toolbox Import Error

The likely issue is one of these:

- folder path mismatch
- filename mismatch
- class name mismatch
- `__init__.py` imports a file that does not exist
- Windows casing tolerance hiding Linux/package issues

Action:

- Inspect the module folder.
- Align folder name, filename, class name, and import path.
- Retest through `main_ui.py`.

## Priority 3 — Export Supabase Schema Directly

Do not fight DBeaver right now.

Action:

- Use Postgres metadata queries.
- Export all schemas, tables, columns, data types, nullability, defaults, and relationships.
- Feed that into Markmind or an ERD generator.

## Priority 4 — Finish Paperless Basics

Do not rebuild Paperless if it is healthy.

Action:

- Login.
- Confirm consume folder.
- Drop in 1-3 safe test files.
- Confirm OCR.
- Confirm tags/document types/storage paths.
- Create API token.

## Priority 5 — Freeze Structure Decisions

The architecture is sufficiently clear to proceed.

Do not keep reopening the entire QiAccess/QiNexus/QiNote structure unless a real conflict appears.

---

# 3. Today's Execution List

1. Test MomCare App with checklist.
2. Test QiAccess Start with checklist.
3. Fix `sys_directory_markmind_mapper` import error.
4. Run Supabase schema export for all schemas/tables/fields.
5. Confirm Paperless login, OCR, consume behavior, and API token.

Everything else is parked.

---

# 4. Parking Lot

These are valid, but not allowed to hijack the day:

- QiCode final spec
- Graphify integration
- Qdrant/Neo4j ingestion
- Paperless sync worker
- Family Wall automation
- Caregiver AI capture system
- Full QiNote ultimate architecture
- NocoDB/general ledger schema
- Wiki/KB polishing

---

# 5. Where This Page Belongs

For now, place this in:

`docs/10_core/60_operations/03_runbooks/2026-05-17_open_loop_reset_paperless_ingestion_runbook.md`

Why:

- This is not source data.
- This is not a template.
- This is not architecture doctrine.
- This is an operational control document.
- It tells the system what to do next.

If `03_runbooks` does not exist yet, create it under:

`docs/10_core/60_operations/`

Later, if this becomes part of the Paperless ingestion system documentation, split the Paperless portion into:

`docs/10_core/40_compute/03_pipelines/`

Suggested future split:

- Keep open-loop reset in `60_operations/03_runbooks/`
- Move permanent ingestion pipeline docs to `40_compute/03_pipelines/`
- Move script documentation to the owning tool folder README

---

# 6. Paperless Recursive Ingestion Strategy

## Goal

Systematically ingest all eligible files inside a folder recursively into Paperless-NGX without losing track of what was ingested, what failed, or what should be excluded.

Paperless should be treated as an ingestion engine, not as a general file browser. Files placed into the Paperless consume folder are temporary. Once consumed, Paperless stores them in its own media/archive structure and removes them from the consume folder.

---

# 7. Important Paperless Behavior

Paperless-NGX consumes documents from its consumption directory. After consumption, files are stored inside Paperless and are not retained in the consumption directory.

This means:

- Do not point Paperless directly at your only copy of an important archive.
- Do not use the consume folder as permanent storage.
- Stage copies into consume.
- Keep your original source folder intact until ingestion is verified.

Recommended principle:

> Source folder is truth until verified. Consume folder is a temporary loading dock.

---

# 8. Recommended Folder Flow

Use a staging workflow instead of dragging the original archive directly into Paperless.

## Proposed Local Flow

Source archive:

`/srv/qios/imports/paperless_source/`

Staging queue:

`/srv/qios/imports/paperless_stage/`

Paperless consume folder:

`/srv/qios/data/paperless/consume/`

Processed manifest/logs:

`/srv/qios/imports/paperless_logs/`

Rejected/unsupported files:

`/srv/qios/imports/paperless_rejected/`

Do not dump random folders straight into consume until recursive handling has been tested.

---

# 9. Confirm the Actual Consume Folder

Run:

```bash
sudo docker inspect paperless --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'
```

Look for the host path mapped to the container consume directory.

Expected pattern:

```text
/srv/qios/data/paperless/consume -> /usr/src/paperless/consume
```

If the host consume path is different, use the actual mounted host path.

---

# 10. Enable Recursive Consume If Desired

Paperless has a setting for recursive consumption:

```env
PAPERLESS_CONSUMER_RECURSIVE=true
```

Optional setting to turn subfolders into tags:

```env
PAPERLESS_CONSUMER_SUBDIRS_AS_TAGS=true
```

Use this carefully.

## Recommendation

For your system, do not rely only on Paperless recursive consume at first.

Use a controlled staging script that:

1. recursively scans the source folder,
2. filters ingestible file types,
3. copies eligible files into the consume folder,
4. writes a manifest,
5. moves unsupported files to a rejected list/folder,
6. avoids duplicates by checksum.

This gives you auditability and prevents chaos.

---

# 11. Supported File Types to Start With

Start conservative.

Recommended ingestible extensions:

- `.pdf`
- `.jpg`
- `.jpeg`
- `.png`
- `.tif`
- `.tiff`
- `.txt`
- `.doc`
- `.docx`
- `.odt`
- `.xls`
- `.xlsx`
- `.ods`
- `.ppt`
- `.pptx`
- `.odp`
- `.eml`

Paperless support depends on installed services and configuration. PDFs and images are the safest first test set.

For the first pass, use only:

- `.pdf`
- `.jpg`
- `.jpeg`
- `.png`
- `.tif`
- `.tiff`

Then expand after testing.

---

# 12. Safe First Test

Create a small test source folder:

```bash
mkdir -p /srv/qios/imports/paperless_source_test
mkdir -p /srv/qios/imports/paperless_logs
```

Copy 3-5 safe documents into it.

Then stage only PDFs/images first.

---

# 13. Dry Run Command

Use this to preview ingestible files recursively:

```bash
find /srv/qios/imports/paperless_source_test \
  -type f \
  \( -iname "*.pdf" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.tif" -o -iname "*.tiff" \) \
  -print
```

If this list looks correct, proceed.

---

# 14. Controlled Copy Into Consume Folder

Use `rsync` to copy files while preserving relative paths:

```bash
sudo rsync -av --progress \
  --include='*/' \
  --include='*.pdf' \
  --include='*.PDF' \
  --include='*.jpg' \
  --include='*.JPG' \
  --include='*.jpeg' \
  --include='*.JPEG' \
  --include='*.png' \
  --include='*.PNG' \
  --include='*.tif' \
  --include='*.TIF' \
  --include='*.tiff' \
  --include='*.TIFF' \
  --exclude='*' \
  /srv/qios/imports/paperless_source_test/ \
  /srv/qios/data/paperless/consume/
```

Then watch Paperless logs:

```bash
sudo docker logs -f paperless
```

---

# 15. Better Long-Term Method: Staging Script

A real ingestion script should create a manifest before copying files.

Manifest fields:

| Field | Purpose |
|---|---|
| source_path | Original file path |
| staged_path | Where the file was copied |
| filename | Original filename |
| extension | File type |
| size_bytes | File size |
| sha256 | Duplicate detection |
| status | staged, skipped, rejected, failed |
| reason | Why skipped/rejected/failed |
| staged_at | Timestamp |

This lets you later answer:

- What did I ingest?
- What failed?
- What was skipped?
- What needs manual review?
- Did I accidentally duplicate a folder?

---

# 16. Suggested Script Location

This should become a standalone runnable tool because it can work independently.

Place it here:

`c:\QiLabs\toolbox\tools\system\sys_paperless_recursive_ingestor\`

Required files:

```text
sys_paperless_recursive_ingestor/
├── README.md
├── manifest.json
├── sys_paperless_recursive_ingestor.py
└── __init__.py
```

The script should include a commented intro immediately after the first line/shebang:

```python
# sys_paperless_recursive_ingestor.py
# Purpose: Recursively scans a source folder, identifies Paperless-ingestible files,
# creates a manifest with checksums, and stages safe copies into the Paperless consume folder.
```

---

# 17. Minimum Script Behavior

The script should support:

```bash
python sys_paperless_recursive_ingestor.py \
  --source "/srv/qios/imports/paperless_source" \
  --consume "/srv/qios/data/paperless/consume" \
  --log-dir "/srv/qios/imports/paperless_logs" \
  --mode dry-run
```

Then:

```bash
python sys_paperless_recursive_ingestor.py \
  --source "/srv/qios/imports/paperless_source" \
  --consume "/srv/qios/data/paperless/consume" \
  --log-dir "/srv/qios/imports/paperless_logs" \
  --mode stage
```

Modes:

| Mode | Behavior |
|---|---|
| dry-run | Scan and report only |
| manifest | Write manifest only |
| stage | Copy eligible files to consume |
| reject-report | Report unsupported files |
| verify | Compare manifest to Paperless API after ingest |

---

# 18. Paperless API Verification Later

After API token is created, the script can verify imported documents by checking the Paperless API.

Future verification fields:

- title
- original filename
- created date
- correspondent
- document type
- storage path
- tags
- archive serial number
- checksum if exposed/available

This comes later. First prove the consume flow works.

---

# 19. Current Recommendation

Do not start with full automation.

Do this sequence:

1. Confirm actual consume folder mount.
2. Test 3-5 files manually.
3. Enable recursive consume only if needed.
4. Run dry-run against a small source folder.
5. Stage only PDFs/images first.
6. Watch logs.
7. Confirm documents appear correctly in Paperless.
8. Only then run a larger batch.
9. Build the standalone toolbox ingestor after the manual pattern is proven.

---

# 20. Immediate Commands

## Inspect mounts

```bash
sudo docker inspect paperless --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'
```

## Create import folders

```bash
sudo mkdir -p /srv/qios/imports/paperless_source
sudo mkdir -p /srv/qios/imports/paperless_source_test
sudo mkdir -p /srv/qios/imports/paperless_logs
sudo mkdir -p /srv/qios/imports/paperless_rejected
```

## Confirm consume folder exists

```bash
sudo ls -lah /srv/qios/data/paperless/consume
```

## Preview ingestible test files

```bash
find /srv/qios/imports/paperless_source_test \
  -type f \
  \( -iname "*.pdf" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.tif" -o -iname "*.tiff" \) \
  -print
```

## Copy test files into consume

```bash
sudo rsync -av --progress \
  --include='*/' \
  --include='*.pdf' --include='*.PDF' \
  --include='*.jpg' --include='*.JPG' \
  --include='*.jpeg' --include='*.JPEG' \
  --include='*.png' --include='*.PNG' \
  --include='*.tif' --include='*.TIF' \
  --include='*.tiff' --include='*.TIFF' \
  --exclude='*' \
  /srv/qios/imports/paperless_source_test/ \
  /srv/qios/data/paperless/consume/
```

## Watch Paperless

```bash
sudo docker logs -f paperless
```

---

# 21. Decision

For now:

- Keep this page as the operating checkpoint.
- Do not redesign the whole system.
- Validate Paperless ingestion manually.
- Then build the recursive ingestor as a standalone toolbox tool.

The system moves forward when the ingest path is proven, not when the architecture is prettier.
