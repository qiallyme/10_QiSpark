---
title: QiIngest Pipeline
status: planned
updated: 2026-05-26
---

# QiIngest Pipeline

## Purpose

QiIngest Pipeline is the future local-first ingestion workflow for documents and document-like artifacts. This page is architecture and planning only. It does not claim that the full pipeline already exists in this repo.

## Goal

Build a controlled local-first path that can:

1. watch selected folders
2. hash files
3. detect duplicates
4. import documents into Paperless
5. extract text and OCR results
6. classify documents by content and context
7. propose cleaned filenames
8. propose metadata, tags, correspondents, and document types
9. update a file inventory
10. embed document text into a vector store such as Qdrant
11. optionally map entities and relationships into Neo4j
12. create an approval queue for Cody
13. update routing rules based on Cody-approved corrections
14. improve routing accuracy over time

## Current Repo Reality

### What Exists

- Paperless is already treated in repo docs as the first real ingestion target.
- `docs/10_qicore/50_operations/20_qiserver/_index.md` documents the Paperless 10-document test rule before bulk import.
- `docs/10_qicore/50_operations/30_dev_history/2026-05-17_open_loop_reset_paperless_ingestion_runbook.md` outlines a controlled staging and manifest concept for Paperless.
- `docs/30_qiarchive/10_ingestion/`, `20_extraction/`, `40_embeddings/`, and `50_graphs/` contain placeholder planning folders.

### What Does Not Exist In This Repo

- no committed folder watcher for QiIngest
- no committed duplicate-detector for QiIngest
- no committed Paperless staging script for QiIngest
- no committed OCR or text extraction worker for QiIngest
- no committed classifier or filename-normalizer for QiIngest
- no committed inventory database or inventory writer for QiIngest
- no committed Qdrant writer for QiIngest
- no committed Neo4j mapper for QiIngest
- no committed approval queue implementation for QiIngest

### Important Non-Match To Avoid

- `src/pages/api/hash.js` is a Homepage config hash endpoint, not a file-ingest hashing pipeline.

## Proposed Pipeline Stages

### Stage 1: Watch And Register

Input:
- approved local folders
- manual drop zones
- optionally exported document batches

Actions:
- detect new or changed files
- compute stable hash values
- record source path, timestamps, size, and file type
- check duplicate history before deeper processing

Output:
- inventory registration record
- staging decision: new, duplicate, skip, manual review

### Stage 2: Paperless Intake

Actions:
- stage safe copies into Paperless consume flow
- keep originals untouched until verified
- follow the 10-document maximum proof step before bulk import

Output:
- Paperless import receipt
- initial document identity linkage back to the local inventory

### Stage 3: OCR And Text Extraction

Actions:
- capture OCR text from scans
- extract text from native digital documents when available
- preserve raw extracted text plus cleaned text

Output:
- raw text
- cleaned text
- extraction status

### Stage 4: Classification And Naming Suggestions

Actions:
- classify by content, source context, and historical routing patterns
- propose cleaned filenames
- propose tags, correspondents, document types, and routing targets

Output:
- suggestion set, not silent auto-rename

### Stage 5: Inventory And Derived Layers

Actions:
- update the file inventory with canonical facts
- write embeddings to Qdrant or another approved vector store
- optionally create Neo4j entity and relationship projections

Rule:
- inventory facts stay canonical
- vectors and graph remain derived

### Stage 6: Approval Queue And Learning Loop

Actions:
- queue proposed corrections for Cody review
- record Cody-approved edits
- update routing rules from approved corrections only
- keep audit trail of changed rules and their source decisions

## Suggested Data Artifacts

| Artifact | Purpose |
|---|---|
| file inventory record | canonical record of source file and ingest state |
| content hash | duplicate detection and lineage |
| Paperless receipt | proof of import or failure |
| OCR text | raw extraction output |
| cleaned text | downstream classification/search input |
| suggestion payload | proposed filename, tags, document type, correspondent, route |
| approval decision record | Cody review outcome |
| routing rule update receipt | record of what learning rule changed and why |

## Verified Facts

- The repo already documents Paperless as the first real ingest lane.
- The repo already documents vector and graph layers as downstream/derived concepts.
- No full QiIngest implementation scripts are committed here today.
- Existing related tooling in this repo is limited to documentation audit and Homepage config-map generation.

## Assumptions

- Local-first means the first detection, hashing, staging, and approval loop should start from Cody-controlled folders or drop zones.
- Paperless should be the first durable document-ingest system before vector or graph expansion.
- Qdrant and Neo4j should remain optional downstream layers, not required first milestones.

## Unknowns

- Which local folders should be watched first.
- Where the inventory should live.
- Which approval queue surface Cody wants to use.
- Whether filename cleanup should happen before or after Paperless import.
- Whether routing rules should stay file-based, database-backed, or both.

## Needs Cody Confirmation

- Initial watch-folder set.
- Preferred approval queue surface.
- Preferred inventory location.
- Whether Paperless should stay the first mandatory destination for all document-like material or only a subset.

## Repo-Only Content

- Exact source references to current runbook docs and placeholder archive folders.
- Warning that `src/pages/api/hash.js` is unrelated to QiIngest.
- Local implementation gap inventory.

## Wiki.js-Ready Content

- Stage-by-stage ingest overview.
- Manual-approval rule.
- Canonical-versus-derived rule.
- Paperless-first validation rule.

## Future Automation Candidates

- folder watcher
- duplicate detector
- Paperless staging script
- OCR/extraction worker
- classifier and metadata suggester
- inventory writer
- Qdrant writer
- optional Neo4j mapper
- approval queue UI or CLI
- correction-to-routing-rule updater
