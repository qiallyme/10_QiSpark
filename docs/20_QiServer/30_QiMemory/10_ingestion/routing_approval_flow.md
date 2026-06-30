# Routing & Approval Flow

This document details the **Routing and Approval Flow**, the human-in-the-loop mechanism that validates filename proposals, metadata tags, and target directories before files are archived.

---

## 1. Verified Facts
- **QiAccess Frontend**: Contains views for managing resources and editing registry entries.
- **Obsidian Folders**: Categorized into bands (e.g., `50_business`, `60_finance`, `70_legal`) under `docs/20_qinexus/`.
- **Database Tables**: Schema definitions for jobs and worker statuses exist in the active domain registry.

---

## 2. Target Hierarchy
- This file is situated in: `docs/30_qiarchive/10_ingestion/routing_approval_flow.md`.
- Works in tandem with classification rules defined in `docs/10_qicore/10_governance/60_registry/sensitivity_classification.yaml`.

---

## 3. Actual Runtime / Storage Locations
- **Approval UI**: Rendered as a dashboard page in QiAccess (`access.qially.com`).
- **Correction Logs**: Saved to `docs/10_qicore/30_data/correction_memory.json` or in a PostgreSQL table on the server.
- **Routing Rules**: Maintained in `docs/10_qicore/10_governance/60_registry/folder_registry.yaml`.

---

## 4. Unknowns
- How to notify the human operator when new documents are pending approval (e.g., email alerts, browser notifications, or simple dashboard alerts).
- The exact format of the correction log structure.

---

## 5. Needs Cody Confirmation
- Do we want automatic routing for certain highly-predictable documents (e.g. utility bills), or must *every* document pass through manual review?
- Should correction memory update the LLM prompt directly or update a set of strict regex rules?

---

## 6. Wiki.js-Ready Summary
> **Routing & Approval Flow** enforces human oversight during document classification. The AI proposes standard names and target folders, which are queued in the QiAccess UI. Once approved or corrected, the document is moved to its final directory in the Obsidian vault, and any manual edits are saved to correction memory.

---

## 7. Implementation Notes
- **UI Queue**: A card list in QiAccess shows: original name, AI proposed name, proposed tags, proposed folder, and actions (Approve / Edit / Discard).
- **Rule Enforcement**: Ensure that filenames follow the schema `YYYY-MM-DD_[Category]_[Descriptor]`.
- **Destination Validation**: Verify that the selected destination folder exists in `folder_registry.yaml` before moving the file.
