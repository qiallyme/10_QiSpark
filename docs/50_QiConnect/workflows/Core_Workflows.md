# Core Workflows

This document defines the core workflows governing the QiAccess ecosystem, specifying trigger conditions, processing steps, reviews, and fallback models.

---

## 1. Repository Synchronization (Sync Walk & Doc Rebuild)
Maintains alignment across multiple sub-repositories (QiLabs, QiNexus) and updates static markdown indexes/blueprints.

- **Trigger**: Manual instruction from operator or daily cron scheduled via agent.
- **Input**: Local uncommitted changes, updated markdown notes, and schema configs.
- **Processor**: Git engine, `scripts/enforce_structure.py`, and `docs/10_qicore/rebuild.bat`.
- **Output**: Clean git tree status, rebuilt MkDocs site, updated index snapshots, and remote pushes.
- **Source of Truth**: Active local workspaces committed and pushed to remote git repositories.
- **Human Review Step**: Final inspection of Git push status and lint validation output before committing.
- **Failure Handling**: Stoppage on script compilation error or merge conflict. Keeps changes local, quarantines push errors to `repo_push_errors.log`.
- **Automation Readiness Score**: **4.5 / 5** (Highly automated via batch scripts, but requires human approval for resolving conflicts).

---

## 2. Care Schema & Clinical Sync (MomsCare Integration)
Coordinates the sync between the local files (e.g. ADHD clinical vaults, discharge PDFs) and operational backend data.

- **Trigger**: Patient regimen logging or receipt of discharge documents.
- **Input**: Clinical logs, CPAP records, or ADHD markdown files.
- **Processor**: CLI Type Generator and local data syncing script.
- **Output**: Updated TypeScript types, loaded rows in the Care schema, and synced files in the clinical vault.
- **Source of Truth**: Relational Care Schema (Supabase/Postgres) and markdown file logs.
- **Human Review Step**: Manual verification of discharge papers and verification of logged doses via the QiAccess UI.
- **Failure Handling**: Failed sync logs trigger a notification card on the QiAccess homepage; data is quarantined locally.
- **Automation Readiness Score**: **3.5 / 5** (Schema generation is stable; sync scripts are still custom/ad-hoc).

---

## 3. Service Status & Health Monitoring
Monitors docker container bindings, Tailscale IP connectivity, and alerts on degradation.

- **Trigger**: Five-minute cron job.
- **Input**: Port listening states, DNS reachability, and Tailscale Serve endpoints.
- **Processor**: Uptime Kuma (`uptime.placeholder.qially.internal`) and status widgets.
- **Output**: Status dot updates (green/red) on the QiAccess homepage and alert channels.
- **Source of Truth**: Uptime Kuma database and active server binding facts.
- **Human Review Step**: None for detection; manual intervention needed to launch Cockpit or Portainer for restarts.
- **Failure Handling**: Automatic Docker container restart policy (restart-unless-stopped) followed by local notification.
- **Automation Readiness Score**: **4 / 5** (Detection and alert triggers are fully automated; recovery actions are manual).

---

## 4. Origin-Down Triage (Recovery Fallback)
Restores portal access and triages service interruption when `qiserver` goes offline.

- **Trigger**: Edge connection timeout (Cloudflare Gateway failover).
- **Input**: Cloudflare routing health metrics.
- **Processor**: Cloudflare edge network rules.
- **Output**: Fallback routing redirecting `access.qially.com` to the offline static fallback page.
- **Source of Truth**: Edge configuration rules and recovery notes cached in the browser/CDN.
- **Human Review Step**: Operator manually opens the SSH console or Cockpit recovery console to diagnose machine states.
- **Failure Handling**: Fallback to Tailscale Direct IP connection to bypass DNS/proxy failure.
- **Automation Readiness Score**: **2 / 5** (Failover detection is automated, but origin diagnosis is entirely manual).
