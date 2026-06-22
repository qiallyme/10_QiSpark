# ADR-0017: Canonical Vocabulary and V1 Direction

## Status

Accepted on 2026-06-10. Database-authority bullets superseded by ADR-0018 on 2026-06-14; all other decisions remain active.

## Context

QiDNA contained competing top-level names, overlapping app locations, and inconsistent data and product direction. Database and UI work require one vocabulary and one approved v1 boundary.

## Decision

The canonical roots are:

```text
01_QiDNA
10_QiAccess
20_QiSystem
30_QiServer
40_QiCapture
50_QiNexus
60_QiApp_QiLife
70_QiConnect
```

- Older roots such as `00_QiEOS`, `10_QiOS_Start`, and `60_QiApps` are Legacy or Evidence unless reviewed content is promoted.
- QiEOS is doctrine inside `01_QiDNA`, not a top-level root.
- QiAccess is the canonical front-door name and remains separate from QiLife.
- QiApp QiLife and `60_QiApp_QiLife` are the canonical app name and root.
- Supabase Postgres is the canonical structured-data authority under ADR-0018.
- QiNexus owns file, export, reference, archive, and backup storage, not relational data.
- SQLite is deprecated and limited to legacy, local, or transitional use.
- V1 is manual-first: capture, inbox and triage, QiBit review, timeline projection, actions, documents and evidence links, people and entities, and daily summaries.
- AI may assist but must use review and approval; it is not silent authority.

## Verified Implementation

QiLife commit `c589e1e` implements the legacy 15-table SQLite catalog. ADR-0018 replaces it with the minimal Supabase Entity/QiBit spine documented in `20_QiSystem/schemas/QiLife_Data_Spine.mdx`.

## Consequences

- All documents receive an explicit Active, Legacy, Proposed, Generated, or Evidence status.
- Legacy content remains preserved and cannot override Active documentation.
- The missing-schema blocker is closed.
- Schema hardening remains gated on accepted categorical values, constraints, indexes, lifecycle rules, migrations, privacy, retention, and backup contracts.
- UI implementation remains gated on the approved route, screen, workflow, and entity-to-view blueprint.
