# QiIngest Ingestion Pipeline

This document defines the architecture of the **QiIngest Pipeline**, the system that manages the ingestion, deduplication, OCR, and classification of documents.

---

## 1. Verified Facts
- **Intake Source**: Raw files are captured in watched folders (e.g., inboxes).
- **Core Processor**: n8n (`100.121.111.106:8001`) and Paperless-ngx (`https://qiserver-1.cerberus-sirius.ts.net:9447`).
- **Ollama Inference**: Ollama (`100.121.111.106:11434`) is active with `embeddinggemma:latest` and `llama3.2:latest` models.
- **Qdrant Vector DB**: Qdrant is online for indexing, but collection configurations are not verified.
- **Neo4j Graph DB**: Currently offline/unreachable on port 7474.

---

## 2. Target Hierarchy
- This file is situated in the authoritative ingestion directory: `docs/30_qiarchive/10_ingestion/qiingest_pipeline.md`.
- Ingested files are moved from `00_inbox` into their permanent domains inside `docs/20_qinexus/` (e.g., `50_business`, `60_finance`, `70_legal`).

---

## 3. Actual Runtime / Storage Locations
- **Watched Inbox**: `g:\My Drive\20_qinexus\00_inbox` (Google Drive) and local directories.
- **Archive Database**: PostgreSQL instance on `qiserver` (Supabase schema tables like `archive_files` and `ingest_jobs` under `qiarchive` namespace).
- **Paperless Documents**: Mounted to local disk on `qiserver` under `/srv/qios/stacks/paperless/data`.
- **Qdrant Indexes**: Storage volumes on `qiserver` under `/srv/qios/stacks/qdrant/storage`.

---

## 4. Unknowns
- How files uploaded via the Google Drive mobile app synchronize to local watcher folders if Google Drive streaming is disconnected.
- The exact volume path configurations in `docker-compose.yml` for the watch folders.

---

## 5. Needs Cody Confirmation
- Does the watch-worker run as a standalone systemd daemon or inside an n8n custom container?
- Is there a size limit for files entering the watched drop zone?

---

## 6. Wiki.js-Ready Summary
> **QiIngest Pipeline** manages the transition of raw documents from watched drop zones (`00_inbox`) to verified nodes in the QiNexus knowledge graph. It leverages Paperless-ngx for OCR, local Ollama LLMs for metadata/filename proposals, and indexes text representations into Qdrant (vectors) and Neo4j (relationship nodes) after mandatory human review.

---

## 7. Implementation Notes
- **Webhooks**: n8n workflows should listen for watch folder events, invoke the hash scanner, and push metadata proposals to the QiAccess queue.
- **Deduplication**: Reject ingestion if SHA-256 is already recorded in the `archive_files` table.
- **Quarantine**: Maintain `00_inbox/quarantine` to isolate damaged or duplicate files.
