---
title: 'ADR-0006: Narrative and Knowledge Layer Consolidation'
status:
  accepted ...
  ...

created_at: '2026-03-30'
updated_at: '2026-03-30'
author:
  Antigravity ...
  ...

source_type:
  manual ...
  ...

supersedes: ''

id: '0006'
short_code:
  NARRATIVE_CONSOLIDATION ...
  ...
domain_prefix:
  core ...
  ...
document_type:
  adr ...
  ...
context_domain:
  core ...
  ...
---

# ADR-0006: Narrative and Knowledge Layer Consolidation

**Status:** Accepted
**Date:** 2026-03-30

## Context
The QiOS / QiOne ecosystem has accumulated overlapping top-level product namespace terminology over time, leading to collisions and lack of clarity. Concepts like `QiHistory`, `QJournal`, `QsaysIt`, `Qistory`, `QiArchive`, `QiNote`, `QiNode`, and `QiObjects` have been used inconsistently. To formalize the QiOS ontology and comply with the Master Blueprint rules (one canonical home per concern, no silent duplication), we must officially define the canonical roles of these concepts and retire redundancies.

## Decision
We establish the following canonical merge map and definitions:
- **QiArchive**: The exclusive canonical archival identity spine and raw file ingest layer.
- **QiNote**: The exclusive canonical knowledge and local-first markdown note layer.
- **QiNode**: The derived semantic and structural intelligence layer (never a canonical source of truth for records).
- **QiHistory**: The consolidated top-level narrative/history umbrella and chronological event log. 

The following terms are formally retired and stripped from the active ontology:
- **QJournal** (Merged into `QiHistory`)
- **Qistory** (Merged into `QiHistory`)
- **QsaysIt** (Retired / Out of Scope for canonical ontology)
- **QiObjects** (Retired as a top-level functional namespace)

## Consequences
### Positive
* Eliminates conceptual duplication and namespace collisions.
* Reinforces the "single domain rule" by giving chronological events, knowledge, and archives explicitly unique, non-overlapping names.
* Simplifies onboarding and architectural referencing.

### Negative (Ripple Effects)
* Any existing code, scripts, or legacy `.legacy` folders using the retired terms might need renaming or archival, causing minor path update friction.
* Users accustomed to the old nomenclature will need to adopt the canonical terms.

## Affected Documents
* `docs/02_architecture/index.md`
* `docs/02_architecture/system_model.md`
* `docs/appendices/changelog.md`
