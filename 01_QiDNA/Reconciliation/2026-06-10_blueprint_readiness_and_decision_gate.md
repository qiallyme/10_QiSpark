# QiDNA Blueprint Readiness and Decision Gate

## Purpose

This document states whether QiDNA is ready to govern database and UI implementation and identifies the decisions required before that work continues.

Assessment date: 2026-06-10.

## Current Position

QiDNA has a sound governance foundation, but it is not yet a contradiction-free or implementation-complete master blueprint.

The repository is synchronized, the active `01-70` domains are documented, the architecture ADRs are in place, and the single-page site builds successfully. Structural reconciliation and implementation specifications remain incomplete.

## Established Foundations

- Eight primary domains define the current system boundary.
- ADRs define data strategy, folder documentation, topology, build strategy, and the AI auditor role.
- The reconciliation report records naming, ownership, topology, and persistence conflicts.
- SQLite, QiNexus, and legacy Supabase have separate intended responsibilities.
- The generated site provides a searchable single-page documentation reader.

## Blocking Issues

### 1. Competing Root Models

The repository still presents two architectures as if both are current:

```text
Current: 01_QiDNA, 10_QiAccess, 60_QiApp_QiLife
Legacy:  00_QiEOS, 10_QiOS_Start, 60_QiApps
```

`README.md`, `docs.json`, doctrine, manifests, and module documents do not yet use one canonical vocabulary.

### 2. Incomplete Site Coverage

The current Node builder renders `.md` files but omits `.mdx` files. Fourteen MDX documents are absent from the site, including the historical master map, source-of-truth rules, QiLife data spine, and several module pages.

The site also renders current and legacy Markdown together without visible status labels.

### 3. Incomplete Database Blueprint

The entity catalog exists, but the following are not yet canonical and complete:

- field definitions and types
- primary and foreign keys
- relationship cardinality
- status values and transition rules
- uniqueness and validation constraints
- indexes and query requirements
- ownership and provenance rules
- retention, archive, and deletion behavior
- migration and backup rules
- authorization and sensitive-data boundaries

The actual QiLife SQLite schema and legacy Supabase schema were not available for comparison.

### 4. Incomplete UI Blueprint

Module flows exist, but the following are not yet unified:

- application route map
- screen and view inventory
- component ownership
- navigation hierarchy
- loading, empty, error, and offline states
- create, review, approve, edit, archive, and delete flows
- entity-to-screen and API-to-screen mappings
- permissions and visibility rules
- accessibility and responsive behavior requirements
- acceptance criteria for each workflow

## Readiness Decision

Broad database and UI implementation should not begin from the current documentation alone.

The required sequence is:

1. Select and document the canonical root vocabulary.
2. Label all competing documents as Active, Legacy, Proposed, Generated, or Evidence.
3. Consolidate active domain documentation without deleting historical evidence.
4. Make the generated site include all supported canonical formats and display document status.
5. Complete and verify the database blueprint against the actual implementation schema.
6. Complete the route, screen, workflow, and UI-to-entity blueprint.
7. Implement database changes, then API contracts, then UI behavior.

## Decision Package Required From Cody

Review the documents listed below and provide explicit decisions for each question.

### Canonical Structure

Review:

- `01_QiDNA/_01_QiDNA.md`
- `01_QiDNA/QiEOS/_QiEOS.md`
- `00_QiEOS/system_map/QiOS_Master_Map.mdx`
- `00_QiEOS/doctrine/QiOS_Core_Doctrine.mdx`
- `README.md`

Decision:

- Is the canonical root model the current `01_QiDNA` through `70_QiConnect` structure?
- Is `QiEOS` a doctrine section inside QiDNA rather than a separate top-level root?
- Is the canonical front-door name `QiAccess` rather than `QiOS Start` or `QiAccess Start`?
- Is the canonical application name and root `QiApp QiLife` / `60_QiApp_QiLife`?

### Data Authority

Review:

- `01_QiDNA/Architecture/Decisions/ADR-0012_data_strategy.md`
- `20_QiSystem/schemas/QiLife_Data_Spine.mdx`
- `90_decisions/0006_clean_core_with_legacy_bridge.md`
- `70_deployment/00_local_dev.md`

Decision:

- Confirm SQLite as the current QiLife structured-data authority.
- Confirm QiNexus as file, export, reference, and archive storage rather than a database.
- Confirm Supabase as legacy/import or future integration only.
- Provide or identify the actual QiLife schema repository and database path.

### Product Scope

Review:

- `60_QiApp_QiLife/_60_QiApp_QiLife.md`
- `90_decisions/0001_personal_lifedesk_model.md`
- `90_decisions/0002_qibit_as_atomic_unit.md`
- `90_decisions/0003_timeline_as_spine.md`
- `90_decisions/0009_agent_first_copilot_cockpit.md`
- `90_decisions/0010_spaces_for_scoped_shared_access.md`

Decision:

- Confirm which entities and modules are required for v1.
- Confirm whether Spaces and shared access are v1 or later.
- Confirm whether AI is central to v1 or staged after manual workflows.

### UI Direction

Review:

- `10_QiAccess/_10_QiAccess.md`
- `60_QiApp_QiLife/_60_QiApp_QiLife.md`
- `50_modules/*/overview.md`
- `50_modules/*/ui_flow.md`
- `60_ai_layer/02_ai_review_workflow.md`

Decision:

- Confirm the primary navigation and first screens to implement.
- Confirm whether QiAccess and QiLife are separate applications or one shell with embedded modules.
- Confirm the minimum capture, inbox, timeline, action, and review workflows for v1.

## Exit Criteria

Database and UI work may proceed when:

- one root vocabulary is accepted
- contradictory documents are labeled or reconciled
- the actual database schema is available and mapped to the entity catalog
- v1 entities, statuses, and relationships are approved
- v1 routes, screens, and workflows are approved
- the generated site contains the complete active blueprint without presenting legacy material as current authority

## Readiness Estimate

- Governance and architecture foundation: approximately 70 percent.
- Implementation-level database and UI specification: approximately 40-50 percent.
- Current status: documentation consolidation and decision review required before implementation expansion.
