# Schema

## Current Doctrine

QiAccess Start currently operates as a Markdown/YAML doctrine vault rooted in `docs/`, with qiserver as the active runtime host and QiNexus as the storage backbone.

Relational schema material below is retained as legacy/reference-only or future/conditional architecture guidance. Supabase is not active unless it has a specific job. `pgvector` is not active unless a future retrieval pipeline explicitly needs it.

## Schema Philosophy

If a future relational layer is activated for a specific job, the schema should reflect the fact that the system is:

* **modular** — each domain lives in its own Postgres schema
* **identity-driven** — every record has a canonical ID that survives transformation
* **archive-aware** — ingested files register in `qiarchive` before downstream processing
* **retrieval-oriented** — embeddings and vector search are future/conditional rather than current doctrine
* **graph-projectable** — `qigraph` is always derived from, never the source of, canonical records

The active doctrine in this repo is not a live relational platform. If a relational layer is reactivated, it should remain relational at the core, with vector and graph layers derived from stable canonical records.

## Legacy / Conditional Namespace Map (Reference Only)

| Schema | Band | Role |
| --- | --- | --- |
| `qione` | Platform | Modular registry and app config reference only; tenants/RBAC remain future/conditional |
| `qiarchive` | Core | File registration, archive spine |
| `qigraph` | Core | Derived knowledge graph |
| `qially` | Core | AI sessions, messages, memory |
| `qisys` | Core | Jobs, events, worker status |
| `qievidence` | Domain | Local-first evidence intelligence |
| `qicase` | Domain | Legal case management |
| `qichronicle` | Domain | Events and calendar |
| `qicms` | Domain | Content and posts |
| `qihome` | Domain | Household and finances |
| `qiknowledge` | Domain | Notes and writing |
| `qitax` | Domain | Tax returns |
| `qivault` | Domain | Secure documents |
| `qicare` | Domain | Respiratory and health care management |
| `public` | Platform | Legacy stubs only - no new tables |

## Reconciliation: Schema vs Data vs Object

These three things are distinct. Conflating them creates drift.

| Term | Definition |
| --- | --- |
| **Schema** | The structural shape defined in Postgres (columns, types, constraints) |
| **Data** | The raw or unstructured payload stored at ingest |
| **Object** | The domain-level entity mapped from schema + enriched data |

**Rule**: Never let a downstream object layer redefine what the schema says is true.

## Core Early Tables (Spine-Required)

As defined in the QiOS Master Blueprint genesis:

* `qiarchive.archive_files` — canonical file registration ✅
* `qiarchive.archive_chunks` — chunked text records ✅
* `qiarchive.ingest_jobs` — pipeline state tracking ✅
* `qiarchive.file_history` — lineage and rename tracking ✅
* `qione.app_module_registry` — modular capability tracking ✅
* `qione.tenants` — tenant identity (Platform-Future) ✅
* `qigraph.master_index` — cross-domain object index ✅
* `qisys.devices` — enrolled machine identities
* `qisys.device_agents` — local agent service states
* `qisys.device_heartbeats` — node health checks
* `qisys.device_jobs` — dispatched node tasks
* `qisys.device_events` — fleet audit trail
* `qisys.device_capabilities` — node role and hardware spec
* `qisys.device_watch_assignments` — folder and drop zone policies

## Email Intake Schema Contract

Email is modeled as an integration feeding the master archival spine, avoiding a separate schema. It is bounded by these core table definitions:

* `qione.email_accounts` — user-owned integration integration ownership and IMAP/Gmail/connector configuration.
* `qiarchive.archive_messages` — canonical registration for individual email payloads.
* `qiarchive.archive_message_threads` — canonical grouping of related messages.
* `qiarchive.archive_message_participants` — sender/recipient edge metadata.
* `qiarchive.archive_message_attachments` — canonical attachment metadata. Email attachments processed as robust files must receive an `archive_id`.
* `qisys.email_sync_cursors` — connector synchronization state, jobs, and webhook checkpoints.
* `qially` tracking — provenance-aware memory and embeddings for email-derived knowledge chunks must link back to their canonical archive IDs.

---

## Canonical Record Invariants

QiOS supports modular, domain-specific schemas. Canonical records should conform to a shared minimum invariant set unless the table's purpose or an approved ADR justifies an exception. Every record passing through the intake pipeline must also capture fleet provenance fields (`owner_user_id`, `source_device_id`, `source_agent_id`, `source_path`, `ingest_mode`) so ingestion is fully traceable and isolated.

### Common Field Invariants

Canonical domain records should implement the following common fields unless the table serves a narrowly scoped structural purpose or an approved ADR defines an exception:

| Field | Type | Role |
| --- | --- | --- |
| `id` | `uuid` | Canonical unique identifier for the record. |
| `owner_user_id` | `uuid` | Reference to the owning user identity in a future relational/auth-backed layer. |
| `status` | `text` | Lifecycle state for governance, routing, or operational control. |
| `visibility` | `text` | Visibility or access classification for governed read exposure. |
| `metadata` | `jsonb` | System-governed provenance, lineage, and auxiliary indexing metadata. |
| `source_device_id` | `uuid` | Identifying the enrolled ingestion node. |
| `source_agent_id` | `uuid` | Identifying the agent runner instance. |
| `source_path` | `text` | Original ingress pathway or drop zone. |
| `ingest_mode` | `text` | e.g. `drop_zone`, `watcher`, `manual_upload`, `sync_worker` |

Domain-specific fields should be modeled as typed relational columns by default. An `attributes` or equivalent extensibility field may be used only where flexibility is justified and does not replace stable schema design.

## Schema Governance Invariants

* **Migration-as-Truth**: If a relational schema is activated for a specific job, database migrations are the canonical schema authority for that layer. ORMs and client models may reflect the schema, but they do not define it.
* **Relational Core**: If used, the relational layer remains downstream-safe. Vector, graph, and AI-derived structures must remain downstream of stable canonical records and preserve traceable linkage back to them.
* **Domain Isolation**: Domain ownership must remain local to the owning schema. Cross-domain dependencies must not create hidden coupling or competing sources of truth. Inter-domain resolution should occur through governed registry patterns, approved interfaces, or the application layer unless an ADR explicitly permits tighter database-level integration.
* **Audit Requirements**: Canonical tables should maintain `created_at` and `updated_at` timestamps unless the table is append-only, purely structural, or explicitly exempted by doctrine or ADR.

## Namespace Allocation Governance

Namespace routing is governed separately from relational identity.

Canonical records such as contacts, users, clients, cases, and matters must use relational identifiers as their source of truth. Namespace codes may be attached only when a governed routed container is required.

### Minimum Registry Requirements

A namespace allocation system must record:

* allocation identifier
* namespace code
* owner type
* owner identifier
* band class
* status
* created_at
* updated_at

### Compliance Rules

Namespace allocations must:

* map to an approved band
* remain unique within the allocation registry
* target an approved owner type
* respect reserved ranges
* avoid implicit invention of new band classes or code patterns

### Forbidden Pattern

Do not allocate namespace codes to every contact, login, or row merely for symmetry. Routing allocation is operational and architectural, not ornamental.
