---
title: QiOS Namespace Registry
version: 2.0
status: Active
owner: Cody
updated: 2026-05-18
canonical_home: docs/10_core/30_data/50_namespace_registry.md
companion_docs:
  - docs/10_core/10_governance/60_registry/band_registry.yaml
  - docs/10_core/30_data/70_object_model.md
  - docs/10_core/30_data/100_metadata.md
  - docs/10_core/30_data/110_front_matter.md
  - docs/10_core/30_data/130_placement_rules.md
  - docs/10_core/10_governance/50_decisions/ADR-0010_qios_namespace_as_routing_metadata_layer.md
scope:
  - QiAccess Start
  - QiNexus
  - Paperless-ngx
  - Wiki.js
  - Google Drive
  - RAG/vector indexing
  - graph indexing
  - manifests
  - automation routing
---

# Namespace Registry

## 00. Operating Decision

The QiOS Namespace Registry is the active routing and metadata layer for QiAccess Start, QiNexus, Paperless-ngx, Wiki.js, Google Drive, RAG/vector indexing, graph indexing, manifests, and automation routing.

It does **not** define the visible folder tree.

QiNexus defines storage placement. The namespace defines machine-readable routing, classification, grouping, and rollup logic.

Plain English:

- **QiNexus answers:** “Where does this live?”
- **Namespace route answers:** “Where does this work belong?”
- **Relational ID answers:** “What exact thing is this?”
- **QID/QiDecimal answers:** “What stable object or artifact is this in the system?”

This prevents the old mistake: turning every useful classification into another folder.

---

## 01. Purpose

QiOS uses a governed namespace registry to route work, artifacts, and workspace containers.

Namespace codes are routing allocations for governed containers of work. They are not identifiers for every person, contact, login, message, raw database row, or random file.

Current active doctrine uses these routes to organize and classify:

- QiNexus work
- QiAccess Start documentation
- Paperless-ngx document tags
- Wiki.js pages
- local operational containers
- graph/RAG records
- project and matter workspaces
- archive blocks
- future automations

Old tenant/platform language is reference-only unless a future shared-container model is explicitly activated by ADR.

---

## 02. Core Doctrine

1. Namespace codes are **container routes**, not universal entity identifiers.
2. Contacts, users, clients, vendors, organizations, and other entities must exist as relational records first.
3. Namespace allocation happens only when a governed workspace, matter, project, archive block, legacy tenant container, or approved routed container is required.
4. Namespace bands are finite, explicit, and registry-controlled.
5. No new top-level band may be created without blueprint update or ADR approval.
6. Namespace aliases may exist for legacy interpretation, but full canonical names remain authoritative.
7. Visible folders should remain shallow. Do not recreate the namespace as a folder cathedral.
8. Metadata can carry more specificity than folders.
9. Machine routing should support human clarity, not replace it.
10. QiAccess Start, QiNexus, and the namespace registry are separate layers of the same system.

---

## 03. Layer Boundaries

### 03.01 QiAccess Start

QiAccess Start is the front door, launcher, dashboard, and control panel.

It answers:

> “Where do I go next?”

### 03.02 QiNexus

QiNexus is the visible storage/workspace model, primarily on Google Drive.

It answers:

> “Where does this live?”

Canonical QiNexus roots remain the active visible storage roots:

1. `00_inbox`
2. `01_workbench`
3. `02_timeline`
4. `03_life`
5. `04_people`
6. `05_business`
7. `06_finance`
8. `07_legal`
9. `08_tech`
10. `09_assets`
11. `10_data`
12. `11_reference`
13. `12_archive`
14. `13_system`

### 03.03 Namespace Registry

The namespace registry is the routing/classification layer.

It answers:

> “Where does this work belong in the governed system?”

Example:

A foreclosure impact summary may live in QiNexus under:

`07_legal/...`

but carry a namespace route like:

`0330LGL.011`

The folder serves human storage. The route serves metadata, indexing, automation, and rollup.

### 03.04 Relational Identity

Relational identity belongs in databases, manifests, indexes, and entity tables.

It answers:

> “What exact person, organization, record, matter, file, or object is this?”

A person is not assigned a namespace just because they exist. A person can be related to a routed matter, project, document, or workspace.

---

## 04. Locked Syntax

| Component | Syntax | Example | Meaning |
|---|---|---|---|
| Structural Node | `####AAA` | `0300LGL` | top-level routed node |
| Section Node / Folder Label | `####AAA_Label_Name` | `0330LGL_Impact` | human-readable routed container |
| Decimal Bucket | `####AAA.###` | `0330LGL.010` | group/bucket under node |
| Artifact Route | `####AAA.###_YYYY-MM-DD_title_detail.ext` | `0330LGL.011_2026-04-04_summary.md` | routed artifact filename pattern |

Rules:

- `####` = four-digit numeric namespace allocation.
- `AAA` = three-letter canonical band or route code.
- `.###` = three-digit decimal bucket or artifact route.
- Use lowercase descriptive file titles after the date.
- Use underscores in routed filenames.
- Do not use namespace routes as a replacement for relational IDs.

---

## 05. Structural Syntax

### 05.01 Structural Node

Pattern:

`####AAA`

Examples:

- `0000ROOT`
- `0300LGL`
- `0400FIN`
- `0600SYS`

### 05.02 Structural Node With Label

Pattern:

`####AAA_Label_Name`

Examples:

- `0330LGL_Impact`
- `0410FIN_Accounts`
- `0610SYS_Architecture`

### 05.03 Decimal Route

Pattern:

`####AAA.###`

Examples:

- `0330LGL.010`
- `0330LGL.011`
- `5441MAT.020`
- `5601PRJ.010`

### 05.04 Artifact File

Pattern:

`####AAA.###_YYYY-MM-DD_title_detail.ext`

Example:

`0330LGL.011_2026-04-04_foreclosure_impact_summary.md`

This pattern is for routed artifacts where the namespace route must be visible in the filename.

It is not required for every file in QiNexus. Many files can carry the route in front matter or metadata only.

---

## 06. Decimal Rules

The three-digit decimal structure allows soft grouping without extra folder depth.

| Decimal | Meaning |
|---|---|
| `.000` | base/default/index under node |
| `.010`, `.020`, `.030`, `.040`, `.050` | grouping buckets |
| `.011-.019` | descendants/items under `.010` |
| `.021-.029` | descendants/items under `.020` |
| `.031-.039` | descendants/items under `.030` |
| `.041-.049` | descendants/items under `.040` |
| `.051-.059` | descendants/items under `.050` |

Trailing zeroes are reserved for grouping buckets unless explicitly used as an index node.

Do not solve ambiguity by creating more folders first. Use decimal groups, metadata, or relational links.

---

## 07. Rollup Rule

Descendants roll up numerically.

Example:

`0330LGL.011` → `0330LGL.010` → `0330LGL` → `0300LGL`

This allows rollups by:

- band
- domain
- routed container
- matter
- project
- bucket
- artifact group
- archive block
- reporting class
- automation target

---

## 08. Allocation Rule

Namespace blocks are assigned only to governed containers requiring durable routing.

Approved allocation targets include:

- system roots
- official bands
- governed workspaces
- matters
- projects
- archival containers
- approved operational partitions
- durable system containers
- reusable routing groups
- automation targets

Namespace blocks must **not** be assigned to:

- every contact
- every portal login
- every CRM row
- every raw record
- every message or event
- every client unless a governed workspace exists
- every file by default
- every thought, note, or capture item
- every database row

The allocation test:

> Does this thing need a durable governed route that multiple systems can use?

If no, use metadata, tags, relational links, or ordinary filenames instead.

---

## 09. Registry Bands

### 09.01 Reserved Ranges

| Range | Role |
|---|---|
| `0000–1999` | Global / shared constitutional bands |
| `2000–4999` | future shared domain expansion |
| `5000–7999` | workspace allocation bands |
| `8000–8999` | lab / sandbox |
| `9000–9999` | archive / legacy |

### 09.02 Range Meanings

#### `0000–1999` — Global / Shared Constitutional Bands

Reserved for stable top-level routing bands.

#### `2000–4999` — Future Shared Domain Expansion

Reserved for future major approved domains.

#### `5000–7999` — Workspace Allocation Bands

Reserved for matter, project, governed workspace, or equivalent routed allocation. Tenant wording is legacy/future only.

#### `8000–8999` — Lab / Sandbox

Reserved for experimental and non-canonical routing.

#### `9000–9999` — Archive / Legacy

Reserved for deprecated, frozen, migrated, or cold-storage routing.

---

## 10. Canonical Band Manifest

| Range | Code | Canonical Name | Role |
|---|---|---|---|
| `0000` | `ROOT` | Root | system root |
| `0100` | `KBS` | Knowledge Base | doctrine, references, templates |
| `0200` | `VLT` | Vault | records, entities, durable holdings |
| `0300` | `LGL` | Legal | legal work and litigation support |
| `0400` | `FIN` | Finance | financial routing and financial artifacts |
| `0500` | `OPS` | Operations | tasks, projects, requests, schedules |
| `0600` | `SYS` | Systems | architecture, schemas, automations, deployments |
| `0700` | `HUM` | Human | household, support, relationships, routines |
| `0800` | `HLT` | Health | logs, care, regulation, recovery |
| `0900` | `MED` | Media | writing, publishing, campaigns, reusable media |
| `1000` | `CRM` | CRM | leads, active clients, engagements, closeout |
| `1100` | `TPL` | Templates | prompts, forms, packets, boilerplates |
| `1200` | `REF` | Reference | laws, cases, snapshots, citations |
| `8000` | `LAB` | Lab | experiments and prototypes |
| `9000` | `ARC` | Archive | legacy and frozen materials |

---

## 11. Active Band Detail

### 11.01 `0000ROOT` — System Root

Purpose: master system control, global registries, indexes, staging, inboxes, exports, and base governance.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0010ROOT` | System | global system records |
| `0020ROOT` | Registry | registries and manifests |
| `0030ROOT` | Indexes | generated indexes |
| `0040ROOT` | Inbox | global intake |
| `0050ROOT` | Staging | temporary staging |
| `0060ROOT` | Exports | system exports |

### 11.02 `0100KBS` — Knowledge Base

Purpose: doctrine, operating manuals, references, standards, and templates.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0110KBS` | Start Here | entry and orientation |
| `0120KBS` | Ops | operating pages |
| `0130KBS` | Systems | system explanations |
| `0140KBS` | Standards | active standards |
| `0150KBS` | References | reference pages |
| `0160KBS` | Templates | knowledge templates |

### 11.03 `0200VLT` — Vault

Purpose: durable records, people, entities, places, assets, documents, and media records.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0210VLT` | People | people records |
| `0220VLT` | Entities | organizations and entities |
| `0230VLT` | Places | locations and places |
| `0240VLT` | Assets | durable asset records |
| `0250VLT` | Documents | document records |
| `0260VLT` | Media | durable media records |

### 11.04 `0300LGL` — Legal

Purpose: legal work, cases, evidence, procedure, filings, orders, and legal impact.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0310LGL` | Case | case/matter work |
| `0320LGL` | Evidence | evidence |
| `0330LGL` | Impact | damages, harm, consequences |
| `0340LGL` | Procedure | procedural notes |
| `0370LGL` | Filings | filed/drafted filings |
| `0380LGL` | Orders | court orders |

### 11.05 `0400FIN` — Finance

Purpose: accounts, bills, income, expenses, tax, reporting, reconciliation, and financial artifacts.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0410FIN` | Accounts | bank/card/account records |
| `0420FIN` | Bills | bills and obligations |
| `0430FIN` | Income | income streams |
| `0440FIN` | Expenses | expenses |
| `0450FIN` | Tax | tax prep and filings |
| `0470FIN` | Reports | reports and dashboards |

### 11.06 `0500OPS` — Operations

Purpose: dashboards, tasks, projects, schedules, logistics, reviews, and operating execution.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0510OPS` | Dashboard | operations overview |
| `0520OPS` | Tasks | task execution |
| `0530OPS` | Projects | project containers |
| `0540OPS` | Schedules | calendars/schedules |
| `0560OPS` | Logistics | movement and coordination |
| `0570OPS` | Reviews | reviews and retrospectives |

### 11.07 `0600SYS` — Systems

Purpose: architecture, automations, schemas, scripts, integrations, deployments, and runtime systems.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0610SYS` | Architecture | system architecture |
| `0630SYS` | Automations | automations |
| `0640SYS` | Schemas | schemas |
| `0650SYS` | Scripts | scripts |
| `0660SYS` | Integrations | integrations |
| `0670SYS` | Deployments | deployments |

### 11.08 `0700HUM` — Human & Household

Purpose: household, relationships, care, communication, routines, and conflict operations.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0710HUM` | Household | household operations |
| `0720HUM` | Relationships | relationship context |
| `0740HUM` | Care | care coordination |
| `0750HUM` | Communication | messages and scripts |
| `0760HUM` | Routines | routines |
| `0770HUM` | Conflict | conflict logs/processes |

### 11.09 `0800HLT` — Health & Regulation

Purpose: logs, symptoms, medical records, mental state, recovery, regulation, and care-related context.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0810HLT` | Logs | health/event logs |
| `0820HLT` | Symptoms | symptom notes |
| `0850HLT` | Medical | medical docs |
| `0860HLT` | Mental State | mental/emotional state logs |
| `0870HLT` | Recovery | recovery plans and notes |

### 11.10 `0900MED` — Media & Publishing

Purpose: writing, audio, video, brands, publishing, campaigns, and reusable media.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `0910MED` | Writing | writing projects |
| `0920MED` | Audio | audio |
| `0930MED` | Video | video |
| `0950MED` | Brands | brand material |
| `0970MED` | Publishing | publishing workflows |

### 11.11 `1000CRM` — CRM

Purpose: leads, active client work, engagements, deliverables, portals, billing, and client closeout.

Important: CRM routing does not make business the center of the system. CRM is only active where business/client work exists.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `1010CRM` | Leads | leads |
| `1020CRM` | Active | active clients |
| `1030CRM` | Engagements | engagement records |
| `1040CRM` | Deliverables | deliverables |
| `1050CRM` | Portal | client portal |
| `1060CRM` | Billing | billing |

### 11.12 `1100TPL` — Templates

Purpose: reusable documents, emails, forms, checklists, prompts, and packets.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `1110TPL` | Documents | document templates |
| `1120TPL` | Emails | email templates |
| `1130TPL` | Forms | forms |
| `1140TPL` | Checklists | checklists |
| `1160TPL` | Prompts | prompts |

### 11.13 `1200REF` — Reference

Purpose: laws, cases, standards, notes, citations, snapshots, and external reference material.

Recommended section routes:

| Route | Name | Purpose |
|---|---|---|
| `1210REF` | Laws | laws/statutes |
| `1220REF` | Cases | case references |
| `1230REF` | Standards | external standards |
| `1240REF` | Notes | reference notes |

---

## 12. Workspace Allocation Bands

Workspace allocations must use controlled registry assignment from the `5000–7999` range.

Recommended patterns:

| Pattern | Meaning |
|---|---|
| `5xxxTNT` | legacy/future tenant workspace alias |
| `54xxMAT` | matter workspace |
| `56xxPRJ` | project workspace |
| `58xxORG` | organization-specific governed workspace |

These are routing classes, not relational identity classes.

Examples:

- `5441MAT` = a specific legal matter workspace route
- `5601PRJ` = a specific project workspace route
- `5801ORG` = a specific organization-governed workspace route

Do not allocate one of these unless there is an actual governed workspace.

---

## 13. Alias Policy

Abbreviated legacy codes may be recognized as aliases for interpretation only.

Examples:

| Alias | Meaning |
|---|---|
| `ARC` | QiArchive alias only |
| `ALY` | QiAlly alias only |
| `CAS` | QiCase alias only |

Aliases are not canonical replacements for official blueprint names.

If an alias is used in old material, preserve it for interpretation, then map it to the canonical route in the registry.

---

## 14. Front Matter Profile

Markdown artifacts that participate in QiOS routing should use front matter.

Minimum recommended fields:

```yaml
---
title: Foreclosure Impact Summary
created: 2026-04-04
updated: 2026-04-04
status: active
qid: QID-EXAMPLE-0001
qid_route: 0330LGL.011
route_band: LGL
route_node: 0330LGL
route_bucket: 0330LGL.010
domain: legal
bucket: impact
artifact_type: summary
source_system: qinexus
storage_path: 07_legal/...
related_entities: []
related_matters: []
tags:
  - legal
  - impact
---
```

Rules:

- `qid` identifies the object/artifact.
- `qid_route` routes the artifact.
- `route_node` identifies the structural node.
- `route_bucket` identifies the grouping bucket.
- `domain` should use plain human-readable naming.
- `bucket` should describe the functional bucket.
- `storage_path` points to the QiNexus location when useful.
- `related_entities` should reference entity IDs, not namespace routes.

---

## 15. Paperless-ngx Tagging Profile

Paperless-ngx should use namespace-aware tags sparingly.

Recommended tag categories:

| Tag Type | Example | Purpose |
|---|---|---|
| Route | `route:0330LGL.011` | exact namespace route |
| Band | `band:LGL` | legal band |
| Domain | `domain:legal` | human-readable domain |
| Bucket | `bucket:impact` | functional bucket |
| Matter | `matter:MAT-2026-001` | relational matter ID |
| Sensitivity | `sensitivity:private` | access classification |

Do not create Paperless tags for every possible route unless they are actively useful. Paperless tag clutter becomes its own little goblin. Starve the goblin.

---

## 16. Wiki.js Profile

Wiki.js pages may reference namespace routes in page metadata or page headers.

Recommended pattern:

```yaml
---
title: Legal Impact Routing
qid_route: 0330LGL.000
route_band: LGL
doc_type: operating_page
source_of_truth: repo
---
```

Wiki.js is the readable operating library. It does not silently override the repo doctrine.

If a Wiki page changes doctrine, update the repo document or create an ADR.

---

## 17. RAG / Graph Indexing Profile

Vector and graph records should preserve namespace metadata.

Recommended fields:

| Field | Purpose |
|---|---|
| `qid` | object/artifact identity |
| `qid_route` | route |
| `route_band` | band code |
| `route_node` | structural node |
| `route_bucket` | decimal bucket |
| `domain` | human-readable domain |
| `artifact_type` | type classification |
| `source_system` | source system |
| `storage_path` | source path |
| `source_uri` | source URI if applicable |
| `related_entities` | relational links |
| `related_matters` | matter links |
| `sensitivity` | access classification |
| `created` | creation date |
| `updated` | last update date |

Graph rule:

- Entities are nodes.
- Documents are nodes.
- Matters/projects/workspaces are nodes.
- Namespace routes are classification/routing properties.
- Do not make every route into a fake entity unless it has operational meaning.

---

## 18. Folder Placement Rule

Namespace bands must not become QiNexus root folders.

Correct:

- QiNexus root: `07_legal`
- Namespace route: `0330LGL.011`
- Front matter: `qid_route: 0330LGL.011`

Wrong:

- Creating a new Drive root folder called `0300LGL`
- Duplicating every namespace node as a folder
- Turning `0330LGL.010` into another folder unless there is a concrete usability reason

Folders are for human retrieval. Namespace routes are for system routing.

---

## 19. ADHD-Safe Structural Constraint

To prevent system rot:

- maximum structural folder depth = 3 levels from root
- use decimal buckets before adding new folders
- avoid sibling overlap
- organize by function, not theme
- do not turn feelings, moods, or vibes into folders
- do not create a new root for a temporary panic
- route first, then place
- when in doubt, ask: “What job does this object do?”

---

## 20. Compliance Requirement

All namespace allocations must be:

- registry-valid
- unique within scope
- mapped to an approved owner type
- documented in the allocation registry
- consistent with blueprint band doctrine
- connected to relational identity when the item is an entity, matter, organization, client, vendor, person, or record
- safe for future automation and indexing

---

## 21. Allocation Review Checklist

Before assigning a namespace route, answer:

1. Is this a governed workspace, matter, project, archive block, or durable routed container?
2. Does it need to be found across multiple systems?
3. Does it need rollup reporting?
4. Does it need automation routing?
5. Is there already a valid route?
6. Is this actually an entity that belongs in a database instead?
7. Is this just a file that only needs front matter?
8. Is this better handled by tags?
9. Would creating this route reduce friction or create future clutter?
10. Is the allocation documented in the registry?

If the answer is not clearly useful, do not allocate a new route.

---

## 22. Implementation Targets

### 22.01 Canonical Document

Save this file as:

`docs/10_core/30_data/50_namespace_registry.md`

### 22.02 Machine Registry

Maintain machine-readable band data at:

`docs/10_core/10_governance/60_registry/band_registry.yaml`

### 22.03 ADR

Create or update:

`docs/10_core/10_governance/50_decisions/ADR-0010_qios_namespace_as_routing_metadata_layer.md`

### 22.04 Related Docs To Update

Update these documents to reference this doctrine:

- `docs/10_core/30_data/20_bands.md`
- `docs/10_core/30_data/30_domains.md`
- `docs/10_core/30_data/40_subdomains.md`
- `docs/10_core/30_data/70_object_model.md`
- `docs/10_core/30_data/100_metadata.md`
- `docs/10_core/30_data/110_front_matter.md`
- `docs/10_core/30_data/130_placement_rules.md`
- `docs/10_core/10_governance/30_standards/metadata_rules.yaml`
- `docs/10_core/10_governance/30_standards/naming_rules.yaml`

---

## 23. Final Operating Rule

Do not build a folder tree for every thought.

QiNexus keeps the visible system navigable.

The namespace keeps the machine-readable system coherent.

Relational identity keeps real-world entities accurate.

The win is not more structure. The win is the right layer doing the right job.
