---
title: QiAccess Start Blueprint
status: active
updated: 2026-05-26
---

# QiAccess Start Blueprint

## Purpose

QiAccess Start is the local repo that defines the QiAccess deployment layer, service inventory source files, workflow notes, and documentation handoff material. In the current checked-in state, the active deployment model is Homepage-based and the readable knowledge destination is Wiki.js.

## Current Blueprint

### Operating Model

1. `qiaccess/` holds the active Homepage deployment config.
2. The repo root still contains the cloned Homepage source tree and upstream Homepage docs.
3. `docs/` holds QiAccess/QiCore/QiArchive planning and operator notes.
4. `src/data/serviceLinks.ts` carries the app-side service registry and verification labels used by the local SPA source still present in the repo.
5. Wiki.js is the intended readable knowledge surface, but repo markdown remains the source material that should be curated before sync.

### Two-Codex Workflow

- Local PC Codex:
  - edits this repo
  - commits changes when the local working tree is safe
  - pushes to GitHub
- Server Codex:
  - inspects qiserver directly
  - pulls from GitHub
  - deploys or restarts only if needed
- GitHub:
  - handoff layer between local and server

Do not treat a local commit or push as proof that server pull, restart, or deployment already happened.

## Verified Facts

- Local repo root is `C:\QiLabs\_QiAccess_Start`.
- Git remote is `https://github.com/qiallyme/_QiAccess_Start.git`.
- Current branch is `main`.
- `README.md` describes this repo as the canonical Homepage-powered QiAccess workspace.
- `qiaccess/README.md` says `qiaccess/` is the canonical deployment layer for QiAccess.
- `qiaccess/config/services.yaml` is the current Homepage service inventory file, but many URLs are still placeholders.
- `src/features/04_knowledge/KnowledgePage.tsx` says QiAccess should hand off to Wiki.js instead of duplicating the knowledge base in-app.
- `_audit/2026-05-24_qiaccess_homepage_local_validation_report.md` says local build and dev validation succeeded and server deployment was not attempted.

## Assumptions

- Homepage remains the live QiAccess dashboard until Cody explicitly changes the deployment model.
- Repo markdown will continue to be the authoring/source layer even when selected pages are copied into Wiki.js.
- The newer `qiaccess/` deployment layer should be treated as more current than older SPA-only doctrine when the two disagree.

## Unknowns

- Which placeholder service URLs in `qiaccess/config/services.yaml` are already mapped on qiserver today.
- Whether the upstream `mkdocs.yml` docs site is still intended to publish these custom QiAccess docs.
- Which Wiki.js pages already exist and whether they match the current repo doctrine.
- Whether the older SPA source tree in this repo is still used for any live route outside Homepage-related work.

## Needs Cody Confirmation

- Which docs should be pushed into Wiki.js first.
- Whether the repo should keep both Homepage source docs and QiAccess doctrine docs in the same `docs/` tree long term.
- Whether service truth should primarily live in `qiaccess/config/services.yaml`, `src/data/serviceLinks.ts`, or a new single canonical inventory file.

## Repo-Only Content

- Exact repo paths such as `qiaccess/config/services.yaml`, `_audit/`, `tools/audit_docs_alignment.py`, and `tools/qiaccess_map_generator/generate_qiaccess_map.py`.
- Git workflow details for local commit/push handoff.
- Local repo audit notes and conversion receipts.

## Wiki.js-Ready Content

- QiAccess Start role as the operational front door.
- The boundary that Wiki.js is the readable knowledge surface while repo markdown remains the maintained source.
- The two-Codex handoff model.
- High-level service boundary and workflow explanations that do not depend on exact local file paths.

## Future Automation Candidates

- Export selected repo docs into Wiki.js-ready pages.
- Generate a service map from `qiaccess/config/*.yaml` plus verified runtime status.
- Lint docs for stale architecture claims versus current Homepage deployment truth.
- Add a small sync receipt so local pushes and server pulls are clearly distinguishable.
