# File Inventory Scanner

This document describes the design of the **File Inventory Scanner**, the background utility responsible for detecting new files, generating inventory records, and computing deduplication hashes.

---

## 1. Verified Facts
- **Hashing Algorithm**: SHA-256 is the ecosystem standard for file identity.
- **Python Runtime**: Python 3 is active in the repository for helper scripts.
- **Git Syncing**: `justfile` and python scripts normalize and enforce files in the workspace directory.

---

## 2. Target Hierarchy
- This file is situated in: `docs/30_qiarchive/10_ingestion/file_inventory_scanner.md`.
- Relates directly to data models mapped under `docs/10_qicore/20_structure/50_data_flow.md` and `docs/10_qicore/10_governance/60_registry/folder_registry.yaml`.

---

## 3. Actual Runtime / Storage Locations
- **Scanner Service**: Planned to run on `qiserver` (origin server).
- **Inventory Database Table**: `archive_files` table in the database.
- **Obsidian Index**: Saved to `g:\My Drive\20_qinexus\100_data\inventory_index.json` or equivalent file catalog.

---

## 4. Unknowns
- Does the scanner compute hashes locally before uploading, or does it trigger hash calculation on `qiserver` after file transfer?
- How to handle files that are modified in-place vs. deleted and re-created (re-hashing rules).

---

## 5. Needs Cody Confirmation
- Do we use Node.js (`chokidar`) or Python (`watchdog`) to monitor the directories?
- Should we write scanner logs directly to syslog or save them to `docs/40_qisystem/10_logs/`?

---

## 6. Wiki.js-Ready Summary
> **File Inventory Scanner** monitors target folders for additions and changes. It computes unique SHA-256 identifiers for each file, records their initial metadata in the inventory, and cross-checks them against the database to prevent duplicate processing.

---

## 7. Implementation Notes
- **Deduplication Check**: Run a database query checking for the calculated SHA-256. If a record is found, log it as a duplicate and skip ingestion.
- **Incremental Scans**: The scanner must maintain a state file of last-modified timestamps to recover quickly after server restarts.
- **File Locks**: Verify that write operations are complete before calculating the hash to avoid partial hashes.
