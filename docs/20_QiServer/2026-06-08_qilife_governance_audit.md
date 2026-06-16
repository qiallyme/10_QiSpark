# QiLife Governance-First Repository Audit

Date: 2026-06-08

Scope: Read-only audit of the current QiOS DNA repository, its Git history, QiLife planning material, and available persistence evidence. No application or database implementation was performed.

## A. Current Repo State

- Workspace: `/home/qiadmin/qi_workspace/_QiOS_DNA`
- Remote: `https://github.com/qiallyme/_QiOS_DNA.git`
- Branch: `main`, aligned with `origin/main` at audit time.
- Working tree: clean at audit time.
- Latest commit: `0d58afd` (`Fix folder doc naming to _FolderName.md standard`), dated 2026-06-05.
- The current repository is a QiOS documentation shell with a static HTML viewer. It is not a QiLife application codebase.
- Current top-level system layers are `01_QiDNA`, `10_QiAccess`, `20_QiSystem`, `30_QiServer`, `40_QiCapture`, `50_QiNexus`, `60_QiApp_QiLife`, and `70_QiConnect`.

## B. Existing Implemented Pieces

- Governance and system-boundary documentation exists for the active QiOS layers.
- `site/` contains a static single-page documentation viewer.
- QiLife has a documented conceptual lifecycle from capture through retrieval.
- The active QiLife document names proposed v1 entities: `qibits`, `buckets`, `threads`, `actions`, `action_steps`, `people`, `transactions`, `obligations`, `knowledge_items`, `documents`, `events`, `links`, `activity_log`, `ai_outputs`, and `daily_summaries`.
- QiCapture documents intake, interpretation review, and handoff to QiLife.
- QiNexus documents durable storage buckets and folder alignment.
- Historical Git revisions contain detailed planning for the QiBit lifecycle, modules, data fields, seed data, build phases, and a local-first database strategy. Commit `ed32390` removed that planning corpus from the active tree.
- No current or historical matches were found for `KeyLife`, `HumanOps`, `Communication Playbook`, or `Relationship Triage` in the inspected repository revisions.

## C. Existing Database Setup

- Requested database path: `C:\QiLabs\60_QiApps_qilife\data\db\qilife.sqlite`.
- The database was not found at that path or at the corresponding mounted path `/mnt/c/QiLabs/60_QiApps_qilife/data/db/qilife.sqlite`.
- No `qilife.sqlite`, `qilife.sqlite3`, or `qilife.db` was found under the accessible `/home/qiadmin` or `/srv/qios` trees.
- Because the database is missing, it could not be opened and no tables could be inspected.
- The current repository contains no SQLite database, SQL schema, migrations, ORM configuration, backend, API, or database connection configuration.
- The static viewer does not use a backend or persistence layer.
- Historical planning prescribed SQLite for QiLife v1, migrations from day one, and a later migration path to Postgres. One historical document used a different location: `C:\QiLifeData\db\qilife.sqlite`.
- Historical seed records and table definitions are documentation only, not executable database artifacts.

## D. Missing Database Foundation

- No active canonical persistence decision.
- No executable schema, constraints, indexes, or foreign keys.
- No migration framework or initial migration.
- No database initialization or health verification.
- No canonical database path ownership.
- No backend data-access layer.
- No transaction or concurrency policy.
- No backup, restore, export, or migration verification workflow.
- No persistence tests.

The active QiLife documentation names tables but does not define an implementation-ready schema. The project is not currently using persistent, mock, or client-side application data because no current application implementation exists.

## E. Unfinished or Suspicious Tasks

- `docs.json` references `_folder` pages, but the physical documents were renamed to `_FolderName.md` files.
- The README and layer documentation still describe `_folder.md` as the required convention, while no `_folder.md` files remain.
- `site/script.js` embeds copies of the Markdown content instead of loading the physical documents, allowing the viewer and source documents to drift.
- The viewer displays paths ending in `/_folder.md`, although those paths no longer exist.
- `fix_folder_names.sh` remains after the repository-wide rename.
- Detailed schema, module, roadmap, seed, and migration planning was removed from the active tree without equivalent active replacements.

## F. Conflicts and Duplicates

- Documentation naming conflict: `_folder.md` governance versus `_FolderName.md` files.
- Navigation conflict: `docs.json` points to missing page names.
- Source duplication: Markdown documents and embedded copies in `site/script.js`.
- Persistence conflict: historical QiLife plans say SQLite first and Postgres later, while other historical QiOS material alternately describes Supabase/Postgres as canonical, conditional, or legacy.
- Database path conflict: the requested `C:\QiLabs\60_QiApps_qilife\data\db\qilife.sqlite` differs from the historically documented `C:\QiLifeData\db\qilife.sqlite`.
- Product naming conflict remains unresolved because no KeyLife definition exists in the inspected repository.

## G. Recommended Next Step

Do not begin feature implementation until a governance decision record establishes:

1. The canonical product name and repository ownership.
2. SQLite or Postgres authority for v1.
3. The canonical database location.
4. Which removed historical schema material remains valid.
5. Migration ownership and versioning.
6. One documentation filename convention and one documentation source of truth.

After approval, the first implementation should be a migration-backed persistence foundation with schema verification tests, before UI or module development.
