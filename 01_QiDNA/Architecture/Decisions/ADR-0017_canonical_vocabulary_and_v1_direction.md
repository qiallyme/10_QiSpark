# ADR-0017: Canonical Vocabulary and V1 Direction

## Status

Accepted on 2026-06-10.

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
- SQLite is the current structured-data authority.
- QiNexus owns file, export, reference, and archive storage, not relational data.
- Supabase is legacy import or possible future integration only.
- V1 is manual-first: capture, inbox and triage, QiBit review, timeline projection, actions, documents and evidence links, people and entities, and daily summaries.
- AI may assist but must use review and approval; it is not silent authority.

## Rationale

These choices remove naming ambiguity, separate shell and product responsibilities, and establish a conservative implementation sequence that can be verified against the actual SQLite schema.

## Consequences

- All documents receive an explicit Active, Legacy, Proposed, Generated, or Evidence status.
- Legacy content remains preserved and cannot override Active documentation.
- Broad database or UI implementation remains blocked until the actual schema and approved implementation blueprints are available.
