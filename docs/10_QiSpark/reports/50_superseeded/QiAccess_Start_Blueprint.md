# QiAccess Start Blueprint

QiAccess Start is Cody's cognitive front door.

It has seven roots only:

1. Home
2. Start
3. Capture
4. Knowledge
5. Memory
6. Insights
7. System

## Root intent

- `Home`: orient the day and expose the shortest useful paths
- `Start`: open tools, services, projects, and working surfaces
- `Capture`: get thoughts, links, reminders, observations, and files into an intake path fast
- `Knowledge`: link to manuals, Wiki.js, repo docs, and reference material
- `Memory`: timeline, decisions, and context surfaces once ingestion exists
- `Insights`: summaries, pattern detection, reports, and future analysis layers
- `System`: nested admin, private-only tools, diagnostics, storage, and doctrine

## System subroutes

System owns:

- `/system/access`
- `/system/server`
- `/system/storage`
- `/system/integrations`
- `/system/settings`
- `/system/blueprint`
- `/system/roadmap`
- `/system/security`
- `/system/diagnostics`

## Current phase

Phase 1 is stabilization and prototype flow validation:

- fix the SPA build
- align the current app to the seven roots
- preserve working launcher and link behavior
- freeze legacy surfaces in place
- validate Capture as the first real operational path

## Phase 0 — Freeze and protect (QiNexus)

Goal: prevent accidental loss during reorganization.

**Mandatory Rules:**
- Do not delete anything.
- Do not let an AI move files directly.
- Create and use the `130_system/qinexus_cleanup` folder.
- Generate manifests and reports before any moves.

### Cleanup System Structure
Located at `G:\My Drive\QiNexus\130_system\qinexus_cleanup`:
- `rules/`: Governance and movement criteria.
- `reports/`: Audit results and analysis.
- `manifests/`: Snapshots of directory state.
- `quarantine/`: Staging for disputed or risky items.
- `scripts/`: Automation for audit and verification.
- `approved_moves/`: Verified move instructions for human execution.

## Daily-use priority

The shortest path to daily use is:

1. Start opens tools
2. Capture reduces friction
3. Knowledge points to real docs
4. System keeps private infrastructure visible
5. Storage shows QiNexus targets
6. Memory and Insights remain honest placeholders
7. Paperless ingestion becomes the first proven intake pipeline

## QiNexus Root Bands (Doctrine)

The directory structure is organized into numeric bands to maintain priority and categorization:

| Band | Root | Purpose |
| :--- | :--- | :--- |
| 00 | `00_inbox` | Temporary intake and staging |
| 10 | `10_workbench` | Active projects, tasks, and drafts |
| 20 | `20_timeline` | Journals, logs, and chronological records |
| 30 | `30_life` | Routines, wellness, personal operations |
| 40 | `40_people` | Family, Mom's Care, relationships |
| 50 | `50_business` | Client work, branding, revenue systems |
| 60 | `60_finance` | Bills, budgets, accounts, reports |
| 70 | `70_legal` | Case files, court filings, evidence |
| 80 | `80_tech` | Apps, server configs, architecture |
| 90 | `90_assets` | Media, design templates, branding assets |
| 100 | `100_data` | Datasets, exports, CSV/JSON storage |
| 110 | `110_reference` | Laws, guides, external research |
| 120 | `120_archive` | Frozen, inactive, and legacy records |
| 130 | `130_system` | Manifests, rules, indexes, automation |
