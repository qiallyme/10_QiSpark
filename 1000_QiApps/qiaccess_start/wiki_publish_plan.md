# Wiki.js Publish Plan

This document details the plan to automatically synchronize static markdown files from the local Git repository to the operational **Wiki.js** database.

---

## 1. Verified Facts
- **Wiki.js Endpoint**: The active internal endpoint is `https://qiserver-1.cerberus-sirius.ts.net:9448` (Tailscale Serve route).
- **Public Domain**: `https://wiki.qially.com` exists but suffers from degraded tunnel routing (needs repair).
- **API Availability**: Wiki.js exposes a GraphQL API for page creations, updates, and indexing.

---

## 2. Target Hierarchy
- This file is situated in: `docs/60_qiapps/qiaccess_start/wiki_publish_plan.md`.
- Interacts with system rebuild scripts in `docs/10_qicore/` (e.g. `rebuild.bat`).

---

## 3. Actual Runtime / Storage Locations
- **Sync script**: Planned to run under `_QiAccess_Start/scripts/publish_wiki.py` or as an n8n workflow.
- **Source Files**: Static markdown folders (`10_qicore`, `20_qinexus`, `30_qiarchive`) under `docs/`.
- **Target Database**: PostgreSQL instances feeding the Wiki.js container on `qiserver`.

---

## 4. Unknowns
- How Wiki.js GraphQL mutations handle page assets (images, pdfs) when referencing local relative directories.
- Best formatting style to map custom front-matter tags (YAML blocks) to Wiki.js tags.

---

## 5. Needs Cody Confirmation
- Do we write a custom python synchronization script using requests, or do we implement this as an n8n webhook workflow?
- How frequently should the sync run (e.g. on every Git push or hourly)?

---

## 6. Wiki.js-Ready Summary
> **Wiki.js Publish Plan** establishes the requirements and architecture for importing markdown blueprint documents into Wiki.js. It details the GraphQL payload structures, path resolution logic, and edge proxy mappings required to publish governance, schemas, and operational checklists automatically.

---

## 7. Implementation Notes
- **API Authentication**: Requires a Wiki.js API Token with `write:pages` permission scope.
- **Path Translation**:
  - Local path `docs/10_qicore/10_governance/10_principles/_index.md`
  - Maps to Wiki.js route `/qicore/governance/principles`
- **Payload Structure**:
  - Query: `mutation ($title: String!, $content: String!, $path: String!) { pages { create(title: $title, content: $content, path: $path, description: "Synced doc", editor: "markdown", locale: "en") { page { id } } } }`
