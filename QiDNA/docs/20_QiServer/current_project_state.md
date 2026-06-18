# Current Project State Report

This document reports the current **repo-side canonical Homepage configuration state** for QiAccess Start on Cody's local PC. It does not claim that qiserver has already been updated.

---

## 1. Verified Facts
- **Canonical Repo Config Path**: `c:\QiLabs\_QiAccess_Start\qiaccess\config\`
- **Homepage Config Files Reviewed**:
  - `services.yaml`
  - `bookmarks.yaml`
  - `settings.yaml`
  - `widgets.yaml`
- **Private Service URLs Now Present In Repo Config**:
  - Open WebUI: `https://qiserver-1.cerberus-sirius.ts.net:9446`
  - Paperless-ngx: `https://qiserver-1.cerberus-sirius.ts.net:9447`
  - Wiki.js: `https://qiserver-1.cerberus-sirius.ts.net:9448`
  - Portainer: `https://qiserver-1.cerberus-sirius.ts.net:9449`
  - n8n: `https://qiserver-1.cerberus-sirius.ts.net:9450`
  - Uptime Kuma: `https://qiserver-1.cerberus-sirius.ts.net:9451`
  - Qdrant: `https://qiserver-1.cerberus-sirius.ts.net:9452`
  - NocoDB: `https://qiserver-1.cerberus-sirius.ts.net:8443`
  - Cockpit: `https://100.121.111.106:9090`
  - Firefly III: `http://qiserver-1.cerberus-sirius.ts.net:6877`
  - Firefly Importer: `http://qiserver-1.cerberus-sirius.ts.net:6878`
  - SolidTime: `https://qiserver-1.cerberus-sirius.ts.net:9453`
  - Neo4j: `http://qiserver-1.cerberus-sirius.ts.net:7474`
- **Deployment Boundary**: Repo config changes still require server pull plus sync into `/srv/qios/stacks/_qiaccess_start/config/`.

---

## 2. Target Hierarchy
- This file is situated in: `docs/40_qisystem/50_generated_reports/current_project_state.md`.
- Derived from active configurations under `qiaccess/config/` and code schemas.

---

## 3. Actual Runtime / Storage Locations
- **Front Door**: `https://access.qially.com` routed via Cloudflare.
- **Private Launcher**: `https://qiserver-1.cerberus-sirius.ts.net/`
- **Docker Compose Stack**: `/srv/qios/stacks/_qiaccess_start/` on `qiserver`.
- **Server Config Sync Target**: `/srv/qios/stacks/_qiaccess_start/config/`
- **Repo Authoring Source**: `c:\QiLabs\_QiAccess_Start\qiaccess\config\`

---

## 4. Unknowns
- Exact live server config drift beyond the routes documented in this repo pass.

---

## 5. Needs Cody Confirmation
- Should recovery/documentation links stay GitHub-based until a stable Wiki.js publish flow exists?

---

## 6. Wiki.js-Ready Summary
> **Current Project State Report** records the repo-side canonical Homepage config after placeholder cleanup. It identifies which private qiserver service URLs are now wired into the repo config, which routes remain unconfirmed, and the fact that Server Codex still has to pull the repo and sync files into `/srv/qios/stacks/_qiaccess_start/config/` before any live dashboard changes occur.

---

## 7. Implementation Notes
- **Audited Discrepancies**:
  - `wiki.qially.com` public tunnel needs repair; private Tailscale route at port `9448` is active.
  - `Neo4j` database container on port `7474` is still documented as unreachable in repo notes.
  - The private Homepage launcher is separate from the public `access.qially.com` front door.
  - Host port `8000` is offline; Paperless-ngx queries should target the Tailscale Serve route at `9447`.
  - Local repo edits do not change the live server until Server Codex performs pull plus config sync.
