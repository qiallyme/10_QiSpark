# QiServer Runbook

This document details the operational triage, monitoring, and recovery runbooks for **QiServer**, the central host of the QiAccess ecosystem.

---

## 1. Verified Facts
- **Host System**: A local server node at `100.121.111.106` running on the Tailnet.
- **Port Bindings**:
  - SSH: `22`
  - Cockpit Administration: `9090`
  - Open WebUI: `9446`
  - Paperless-ngx Serve Proxy: `9447`
  - Wiki.js Serve Proxy: `9448`
  - Portainer Container Admin: `9449`
  - Firefly III: `6877` (HTTP)
  - Firefly Importer: `6878` (HTTP)
  - SolidTime: `9453` (HTTPS)
  - Neo4j: `7474` (HTTP)
- **Repo-side Canonical Homepage Config Source**: `c:\QiLabs\_QiAccess_Start\qiaccess\config\`
- **Docker Compose Stack Path**: `/srv/qios/stacks/` or `/srv/qios/stacks/_qiaccess_start/` on the server.
- **Deployment Boundary**: Local repo edits are not live until Server Codex pulls the repo and syncs the config files into `/srv/qios/stacks/_qiaccess_start/config/`.

---

## 2. Target Hierarchy
- This file is situated in: `docs/50_qiserver/qiserver_runbook.md`.
- Works in conjunction with system status monitoring pages and Uptime Kuma alerts.

---

## 3. Actual Runtime / Storage Locations
- **Server Host**: Physical system or VM managed via Tailscale.
- **Config Backup Destination**: Synced to `docs/10_qicore/10_governance/60_registry/` and backup drives.
- **Compose Files**: Kept in local repository stack folders on the host machine.
- **Homepage Config Sync Target**: `/srv/qios/stacks/_qiaccess_start/config/`

---

## 4. Unknowns
- Exact root partition structure and disk utilization alert thresholds on the host.
- The credentials required to access the Portainer dashboard stack if credentials lose sync.

---

## 5. Needs Cody Confirmation
- How are system credentials backed up for offline emergency access?
- Is there a hardware-level IP KVM (like Pi-KVM) connected to the host for origin down triage?

---

## 6. Wiki.js-Ready Summary
> **QiServer Runbook** provides step-by-step procedures for origin-down recovery, SSH diagnostic routines, Docker stack restarts, and port mapping checks. It serves as the authoritative operational manual for maintaining local AI model inference (Ollama), document intake (Paperless), and database runtimes.

---

## 7. Implementation Notes
- **Emergency SSH**:
  ```bash
  ssh qiadmin@qiserver-1.cerberus-sirius.ts.net
  ```
- **Repo-to-Server Sync Rule**:
  - Update repo-side canonical config in `c:\QiLabs\_QiAccess_Start\qiaccess\config\`
  - Push to GitHub from the local PC repo
  - Have Server Codex pull the repo on qiserver
  - Sync the config files into `/srv/qios/stacks/_qiaccess_start/config/`
  - Only then restart or reload the private Homepage stack if needed
- **Service Recovery Steps**:
  1. Ping the host over Tailscale: `ping 100.121.111.106`.
  2. Access the Cockpit console on `https://100.121.111.106:9090`.
  3. Inspect container states: `docker ps` or log in to Portainer on port `9449`.
  4. Restart compose stacks:
     ```bash
     cd /srv/qios/stacks/_qiaccess_start
     docker compose down && docker compose up -d
     ```
