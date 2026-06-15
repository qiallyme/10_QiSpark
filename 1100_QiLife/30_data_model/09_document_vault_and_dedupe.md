# Managed Document Vault and Dedupe
QiLife eventually replaces Paperless-style intake.

## Doctrine
- QiLife is dup-allergic. Every incoming file must be hashed.
- Exact duplicates should not create duplicate blobs. Near duplicates should be flagged for review.
- Files should be stored as managed file objects.
- Documents are meaning/context records linked to file objects.
- Support document versions.
- File deletion should be safe, logged, and restorable before purge.

## Planned Tables
- `file_objects`
- `documents`
- `document_versions`
- `duplicate_candidates`
- `file_events`
- `text_extractions`
