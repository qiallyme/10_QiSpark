# Object Model

## Core Object Families

The system supports these canonical object families:

| Object | Home Schema | Notes |
|---|---|---|
| files | `qiarchive` | Primary archive records |
| chunks | `qiarchive` | Derived from files |
| notes | `qiknowledge` | Local-first knowledge layer |
| documents | `qivault` | Secure document vault |
| entities | `qigraph` | Extracted and projected |
| clients | `qicase` | Operational domain |
| contacts | `qicase` | Associated with clients |
| cases | `qicase` | Core legal/ops unit |
| tasks | `qisys` | Jobs and system tasks |
| events | `qichronicle` | Time-anchored records |
| contracts | `qivault` | Secure contract records |
| prompts | `qially` | AI prompt records |
| memories | `qially` | AI memory embeddings |
| routes | `qiarchive` | Archive routing states |
| projects | `qisys` | Grouped work units |
| modules | `qione` | Platform feature toggles |
| tenants | `qione` | Top-level containers |
| email_accounts | `qione` | Email platform configuration and ownership |
| email_messages | `qiarchive` | Canonical registered email records |
| email_threads | `qiarchive` | Grouped email conversations |
| email_participants | `qiarchive` | Canonical sender/recipient records |
| email_attachments| `qiarchive` | Files attached to registered emails |
| email_sync_jobs | `qisys` | Connector sync processing |
| email_connector_events | `qisys` | Integration ingress events |
| email_sync_cursors | `qisys` | Provider sync state tracking |

## Structural Layers

Objects exist across these structural tiers:

| Layer | Purpose |
|---|---|
| **Archive layer** | Files and registration records |
| **Semantic layer** | Entities and enriched meaning |
| **Workflow layer** | Routing, review, and actions |
| **Knowledge layer** | Notes, memory, and recall |
| **Graph layer** | Derived relationships (never canonical) |
| **Delivery layer** | Portals, reports, chatbot output |

## Placement Rule

Every object must have:
1. A **canonical schema** home
2. A **band** assignment
3. A **tenant_id** if it is domain-scoped
4. An **archive_id** if it is derived from a registered file

Objects that violate these rules are considered unregistered and must not be used in automation or AI retrieval.
