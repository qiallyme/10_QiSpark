# Non-Destructive QiDNA Reconciliation Plan

## Rule

No legacy evidence is deleted during reconciliation. Promotion copies or merges reviewed meaning into the canonical root, records provenance, and leaves the source available until a later explicit archive or deletion decision.

## Phase 1: Canonical Vocabulary

Status: accepted through ADR-0017.

- Use the eight canonical roots.
- Treat QiEOS as doctrine inside QiDNA.
- Use QiAccess and QiApp QiLife as canonical names.
- Keep QiAccess and QiLife as separate layers.

## Phase 2: Status Labeling

Status: implemented in the site classifier.

- Label every Markdown and MDX document.
- Default the site to Active.
- Keep Legacy, Proposed, Generated, and Evidence searchable through filters.
- Never infer authority from file age or build visibility.

## Phase 3: Content Promotion

Status: in progress. The `00_QiEOS` doctrine, master map, and ADR-0001 set was reconciled on 2026-06-12.

For each legacy document:

1. Identify unique claims.
2. Compare them with Active doctrine and runtime evidence.
3. Classify each claim as compatible, conflicting, stale, or unknown.
4. Merge compatible unique content into one canonical destination.
5. Record the legacy source path in the reconciliation receipt.
6. Resolve conflicts through an ADR or explicit owner decision.
7. Add an explicit supersession notice to the legacy source and retain it in place as hierarchy-preserving archive evidence unless a later approved move preserves its source path and provenance.

Priority promotion sets:

- `00_QiEOS` doctrine and master map into `01_QiDNA`
- `10_QiOS_Start` and `60_qiapps/qiaccess_start` into `10_QiAccess`
- `60_QiApps/QiLife`, approved `50_modules`, and approved `60_ai_layer` content into `60_QiApp_QiLife`
- `50_qiserver` into `30_QiServer`
- `70_qiconnect` into `70_QiConnect`
- reviewed `20_qinexus` content into `50_QiNexus`

## Phase 4: Site Coverage

Status: builder updated.

- Render Markdown and MDX.
- Show document status.
- Keep Active as the default.
- Validate canonical required documents.
- Regenerate after every accepted documentation change.

## Phase 5: Database Blueprint

Status: physical schema inventory complete; behavioral contracts remain open.

- The QiLife repository, SQLModel metadata, and canonical SQLite database were inspected on 2026-06-12.
- Tables, columns, keys, relationships, indexes, constraints, and migration state are mapped in `20_QiSystem/schemas/QiLife_Data_Spine.mdx`.
- Produce ADD, MERGE, UPDATE, or DELETE recommendations.
- Approve v1 schema before migration or application changes.

## Phase 6: UI Blueprint

Status: pending database mapping.

- Define route and screen catalog.
- Define workflow state machines.
- Map screens to entities and mutations.
- Define errors, permissions, offline behavior, accessibility, and acceptance criteria.
- Approve the manual-first v1 sequence before broad UI implementation.

## Completion Gate

Reconciliation is complete when one active document answers each architectural question, all alternatives are visibly non-active, the database and UI blueprints match verified implementation, and the generated site presents the complete active blueprint without hiding preserved evidence.
