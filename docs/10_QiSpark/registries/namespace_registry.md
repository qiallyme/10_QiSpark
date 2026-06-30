# Namespace Registry

Status: Active  
Version: 1.0

## Purpose

QiOS uses a governed namespace registry to route work, artifacts, and workspace containers.

Namespace codes are routing allocations for governed containers of work, not identifiers for every person, contact, login, or raw database row.

Current active doctrine uses these routes to organize QiNexus work, QiAccess Start documentation, and related local operational containers. Old tenant/platform language below is reference-only unless a future shared-container model is explicitly activated.

Relational identity and namespace routing are separate concerns:

- relational IDs answer: "what is this?"
- namespace codes answer: "where does this work belong?"

---

## Core Doctrine

1. Namespace codes are container routes, not universal entity identifiers.
2. Contacts, users, clients, vendors, and organizations must exist as relational records first.
3. Namespace allocation occurs only when a governed workspace, matter, project, legacy tenant container, archive block, or other approved routed container is required.
4. Namespace bands are finite, explicit, and registry-controlled.
5. No new top-level band may be created without blueprint update or ADR approval.
6. Namespace aliases may exist for legacy interpretation, but full canonical names remain authoritative in blueprint doctrine.

---

## Structural Syntax

- `####AAA` = structural node
- `####AAA.###` = subgroup, child route, bucket, or artifact route

Examples:

- `0300LGL`
- `0330LGL.010`
- `5120TNT`
- `5441MAT.020`

---

## Naming Rules

### Structural Nodes
`####AAA_Label_Name`

### Artifact Files
`####AAA.###_YYYY-MM-DD_title_detail.ext`

---

## Decimal Rules

- `.000` = base/default/index under node
- `.010`, `.020`, `.030` = grouping buckets
- `.011-.019` = descendants/items under `.010`
- `.021-.029` = descendants/items under `.020`

Trailing zeroes are reserved for grouping buckets unless explicitly used as an index node.

---

## Rollup Rule

Descendants roll up numerically.

Example:

`0330LGL.011` -> `0330LGL.010` -> `0330LGL` -> `0300LGL`

---

## Allocation Rule

Namespace blocks are assigned only to governed containers requiring durable routing.

Approved allocation targets include:

- system roots
- official bands
- governed workspaces
- matters
- projects
- archival containers
- approved operational partitions

Namespace blocks must NOT be assigned to:

- every contact
- every portal login
- every CRM row
- every raw record
- every message or event
- every client unless a governed workspace exists

---

## Registry Bands

### 0000–1999 — Global / Shared Constitutional Bands
Reserved for stable top-level routing bands.

### 2000–4999 — Future Shared Domain Expansion
Reserved for future major approved domains.

### 5000-7999 - Workspace Allocation Bands
Reserved for matter, project, governed workspace, or equivalent routed allocation. Tenant wording here is legacy/future only.

### 8000–8999 — Lab / Sandbox
Reserved for experimental and non-canonical routing.

### 9000–9999 — Archive / Legacy
Reserved for deprecated, frozen, migrated, or cold-storage routing.

---

## Canonical Band Manifest

| Range | Code | Canonical Name | Role |
|---|---|---|---|
| 0000 | ROOT | Root | system root |
| 0100 | KBS | Knowledge Base | doctrine, references, templates |
| 0200 | VLT | Vault | records, entities, durable holdings |
| 0300 | LGL | Legal | legal work and litigation support |
| 0400 | FIN | Finance | financial routing and financial artifacts |
| 0500 | OPS | Operations | tasks, projects, requests, schedules |
| 0600 | SYS | Systems | architecture, schemas, automations, deployments |
| 0700 | HUM | Human | household, support, relationships, routines |
| 0800 | HLT | Health | logs, care, regulation, recovery |
| 0900 | MED | Media | writing, publishing, campaigns, assets |
| 1000 | CRM | CRM | leads, active clients, engagements, closeout |
| 1100 | TPL | Templates | prompts, forms, packets, boilerplates |
| 1200 | REF | Reference | laws, cases, snapshots, citations |
| 8000 | LAB | Lab | experiments and prototypes |
| 9000 | ARC | Archive | legacy and frozen materials |

---

## Workspace Allocation Bands

Workspace allocations must use controlled registry assignment from the 5000–7999 range.

Recommended patterns:

- `5xxxTNT` = legacy/future tenant workspace alias
- `54xxMAT` = matter workspace
- `56xxPRJ` = project workspace
- `58xxORG` = organization-specific governed workspace

These are routing classes, not relational identity classes.

---

## Alias Policy

Abbreviated legacy codes may be recognized as aliases for interpretation only.

Examples:

- `ARC` -> `QiArchive` alias only
- `ALY` -> `QiAlly` alias only
- `CAS` -> `QiCase` alias only

Aliases are not canonical replacements for official blueprint names.

---

## ADHD-Safe Structural Constraint

- maximum structural folder depth = 3 levels from root
- use decimal buckets before adding new folders
- avoid sibling overlap
- organize by function, not theme

---

## Compliance Requirement

All namespace allocations must be:

- registry-valid
- unique within scope
- mapped to an approved owner type
- documented in the allocation registry
- consistent with blueprint band doctrine
