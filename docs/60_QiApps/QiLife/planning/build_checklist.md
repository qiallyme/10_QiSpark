# Build Checklist

## Phase 1: Core Scaffold & First Vertical Slice
- [ ] Scaffold `frontend/src/config/features.ts` (Feature Registry)
- [ ] Scaffold SQLite DB with migrations for core tables (`activity_log`, `qibits`, `file_objects`, `spaces`, etc.)
- [ ] Implement Capture Module (UI intake for text/files)
- [ ] Implement Ingestion Module (dedupe checks, text extraction)
- [ ] Implement Mock Agent Draft (generate mock drafts from ingestion items)
- [ ] Implement Draft Review UI
- [ ] Implement Approval Flow (saving to QiBits, Actions, Timeline)
- [ ] Implement Context Dock Placeholder

## Phase 2: Spaces and Storage
- [ ] Implement Storage & Sync settings UI
- [ ] Build Document Vault UI and hashing logic
- [ ] Implement Space switcher and Mom Care scoped access

## Phase 3: Legacy Bridge
- [ ] Create legacy bridge tables
- [ ] Implement import script/UI for Supabase legacy data
