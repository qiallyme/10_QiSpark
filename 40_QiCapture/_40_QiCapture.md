# QiCapture

## Overview

QiCapture is the data intake and ingestion pipeline of QiOS. It handles messy life data (exports, receipts, documents) and turns it into clean, structured, and searchable materials.

## Responsibilities

- Clean and parse raw intake.
- Index and extract metadata from documents (via OCR or scripts).
- Chunk and embed clean text for semantic search.
- Form entity relationships and graphs from text.
- Synchronize indices and manage backups.

## Flows

```text
Intake raw file 
  -> profile & inspect 
  -> clean & normalize 
  -> produce staging import 
  -> Supabase import
```

## Folder Structure & Table of Contents

### Intake Pipeline Stages
- [10 Ingestion](10_ingestion/): Raw intake from various sources (Paperless, drive imports, manual uploads, email exports, web clips).
- [20 Extraction](20_extraction/): OCR processing, text extraction, markdown exports, and transcripts.
- [30 Chunking](30_chunking/): Processing clean text into chunks, manifest records, and source mapping.
- [40 Embeddings](40_embeddings/): Embedding models, Qdrant setup, collections, and vector quality tests.
- [50 Graphs](50_graphs/): Entity extraction, relationship graphs, and entity maps.
- [60 Retrieval](60_retrieval/): Semantic search profiles, query logs, retrieval tests, and context packaging.
- [70 Memory](70_memory/): facts storage, session summaries, user preference maps.
- [80 Sync & Backups](80_sync_backups/): Snapshot logs, restore points, and synchronization manifests.

### Tools & System References
- [NocoDB](nocodb.md): Intake tracking database interface.
- [Obsidian QiDocs](obsidian_qidocs.md): Vault indexing rules and guidelines for local notes.
- [WikiJS](wikijs.md): Ingest documentation library.
- [Paperless-ngx](paperless/): Document management setup and indexing rules.
