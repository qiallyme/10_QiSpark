# QiAccess Start Overview

> **Legacy - Superseded implementation evidence.** Reconciled on 2026-06-12 against the live Homepage stack. Valid deployment-boundary and no-secrets rules were merged into `10_QiAccess/_10_QiAccess.md`. Recorded URLs and repo assumptions are historical and non-authoritative.

This document provides a high-level overview of the **repo-side canonical QiAccess Homepage configuration** prepared on Cody's local PC. It is not a claim that the live qiserver Homepage config already matches this repo.

---

## 1. Verified Facts
- **Architecture**: Homepage-powered private launcher config under `qiaccess/config/`.
- **Canonical Repo Config Files**:
  - `qiaccess/config/services.yaml`
  - `qiaccess/config/bookmarks.yaml`
  - `qiaccess/config/settings.yaml`
  - `qiaccess/config/widgets.yaml`
- **Private Launcher URL**: `https://qiserver-1.cerberus-sirius.ts.net/`
- **Public Front Door**: `https://access.qially.com`
- **Service URL Set Updated In Repo**:
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
- **Deployment Boundary**: The repo config is not live until Server Codex pulls the repo and syncs it into `/srv/qios/stacks/_qiaccess_start/config/`.

---

## 2. Target Hierarchy
- This file is situated in: `docs/60_qiapps/qiaccess_start/overview.md`.
- References core governance and ADR logs in `docs/10_qicore/10_governance/`.

---

## 3. Actual Runtime / Storage Locations
- **Repo Root**: `c:\QiLabs\_QiAccess_Start\`
- **Canonical Local Config Path**: `c:\QiLabs\_QiAccess_Start\qiaccess\config\`
- **Server Sync Target**: `/srv/qios/stacks/_qiaccess_start/config/`
- **Edge URL**: `https://access.qially.com`
- **Private Launcher URL**: `https://qiserver-1.cerberus-sirius.ts.net/`

---

## 4. Unknowns
- Whether the live server Homepage config still contains custom deviations beyond the URLs captured in this repo pass.

---

## 5. Needs Cody Confirmation
- Should repo-side recovery/documentation links remain GitHub-backed, or should they later point at Wiki.js pages after sync/publish is stable?

---

## 6. Wiki.js-Ready Summary
> **QiAccess Start** is the repo-maintained canonical Homepage launcher config for Cody's private qiserver utility dashboard. It carries the grouped layout, known Tailscale service URLs, and recovery links, but it does not become live until Server Codex pulls the repo and syncs the config into `/srv/qios/stacks/_qiaccess_start/config/`.

---

## 7. Implementation Notes
- **Layout Rule**: Preserve the improved Homepage grouping/layout in `settings.yaml` while using real documented service URLs in `services.yaml`.
- **No Secrets Rule**: Do not commit Homepage widget tokens or credentials into repo YAML.
- **Deployment Rule**: Local repo edits alone do not update qiserver; Server Codex must later pull and sync the config.
