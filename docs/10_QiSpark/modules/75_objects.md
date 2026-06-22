# Objects

## Current Doctrine

Current active doctrine centers on QiAccess Start, qiserver, QiNexus, and Markdown/YAML records. The relational object families below are retained as a reference model for future/conditional database work rather than current live platform requirements.

## Core Object Families

| Object | Home Schema | Notes |
|---|---|---|
| files | `qiarchive` | Primary archive records - the Spine |
| chunks | `qiarchive` | Derived from files, linked by `archive_id` |
| notes | `qiknowledge` | Local-first knowledge layer |
| documents | `qivault` | Secure document references; tenant-scoped assumptions are legacy/future only |
| entities | `qigraph` | Extracted and projected (derived) |
| clients | `qicase` | Legacy/reference operational domain objects |
| contacts | `qicase` | Legacy/reference operational contacts |
| cases | `qicase` | Core legal/operational unit |
| tasks / jobs | `qisys` | System and workflow jobs |
| events | `qichronicle` | Time-anchored records |
| contracts | `qivault` | Secure contract records |
| prompts | `qially` | AI prompt records |
| memories | `qially` | AI memory references; embeddings remain future/conditional |
| routes | `qiarchive` | Archive routing state records |
| posts | `qicms` | Content management objects |
| tenants | `qione` | Legacy/future top-level containers |
| modules | `qione` | Platform feature-toggle reference |

## Object Identity Requirements

Every object must carry:

1. A **canonical ID** (assigned at registration, never changed)
2. A **domain assignment** (one schema, one band)
3. A **status** (lifecycle state)
4. **Timestamps** (`created_at`, `updated_at` where mutable)

If a future shared-container relational model is activated, domain-scoped objects may additionally require:
- `tenant_id` FK to `qione.tenants`

File-derived objects additionally require:
- `archive_id` FK to `qiarchive.archive_files`

## Object Lineage Rule

> Derived records must not invent disconnected truth.

* Chunks must reference `archive_id`
* Graph nodes must reference canonical object IDs
* AI evidence must reference `archive_id` / `chunk_id` / `entity_id`
* Memories must reference source provenance where possible
