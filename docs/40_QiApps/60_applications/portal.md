# QiAccess Start Portal

QiAccess Start is Cody's cognitive front door.

It is not just a dashboard, launcher, or control panel.
It is the active portal doctrine for this master blueprint.

## Two Launch Surfaces

It is critical to distinguish between the two distinct launchers used in this architecture. They are not the same, and updating one does not update the other:

1. **`access.qially.com` (The Public Portal)**
   - **Role:** External/public QiAccess landing page and primary user-facing front door when away from home/server.
   - **Tech:** Static/React app deployed through Cloudflare.
   - **Config:** Service links must be maintained directly in the app source data files. It does *not* read from the server's `services.yaml`.

2. **`qiserver-1.cerberus-sirius.ts.net` (The Private Server Utility)**
   - **Role:** Private Tailscale/server launcher, useful strictly for local/tailnet access.
   - **Tech:** `gethomepage` local server utility.
   - **Config:** Configuration lives at `/srv/qios/stacks/_qiaccess_start/config/services.yaml`. Editing this file updates the local utility, *not* the public landing page.

## Portal Contract

The portal has seven roots only:

1. `Home`
2. `Start`
3. `Capture`
4. `Knowledge`
5. `Memory`
6. `Insights`
7. `System`

## Root Intent

- `Home`: orient the day and show the next useful actions
- `Start`: open tools, services, projects, and working surfaces
- `Capture`: get notes, links, reminders, files, and observations out fast
- `Knowledge`: point to docs, runbooks, manuals, and references
- `Memory`: preserve continuity, decisions, and context once ingestion exists
- `Insights`: hold summaries, patterns, reports, and future analysis
- `System`: hold nested access, server, storage, governance, and diagnostics surfaces

## Routes

Use this route model:

- `/` = Home
- `/start` = Start
- `/capture` = Capture
- `/quick` = mobile quick capture
- `/knowledge` = Knowledge
- `/memory` = Memory
- `/insights` = Insights
- `/system` = System

System subroutes:

- `/system/access`
- `/system/server`
- `/system/storage`
- `/system/integrations`
- `/system/settings`
- `/system/blueprint`
- `/system/roadmap`
- `/system/security`
- `/system/diagnostics`

## Current Phase

The current phase is stabilization and prototype flow validation.

The shortest path to daily usefulness is:

1. Start opens real tools
2. Capture reduces friction
3. Knowledge points to real docs
4. System keeps infrastructure honest and visible
5. Storage maps QiNexus targets
6. Memory and Insights stay clearly marked until they are real

## Design Rule

The portal should feel like a deliberate entry point into a real operating environment.

- modern
- fast
- low-friction
- visually distinct by root
- no dead controls
- no fake intelligence claims

## Legacy Disposition

The older QiPortals and multi-tenant client portal material is not active doctrine for this page.

Useful governance fragments may be retained, but legacy platform assumptions belong in:

- `08_appendices/20_legacy/legacy_salvage.md`
- `08_appendices/20_legacy/qiaccess_start_legacy_quarantine.md`

## Daily-use priority

The shortest path to daily use is:

1. Start opens tools
2. Capture reduces friction
3. Knowledge points to real docs
4. System keeps private infrastructure visible
5. Storage shows QiNexus targets
6. Memory and Insights remain honest placeholders
7. Paperless ingestion becomes the first proven intake pipeline

## Current Build Rule

Prototype inside the existing repo and preserve what already works.

- no repo split
- no auth rebuild
- no deployment churn before flow is validated
- no fake intelligence claims
- static or honest placeholder content is acceptable during stabilization

