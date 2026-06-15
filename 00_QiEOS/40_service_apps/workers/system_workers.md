---
uid:
  63df3f97-e518-4fd0-b954-da1b5ddba406 ...
  ...
---
# Workers

Workers are async background processes that run **after** canonical registration. They are triggered by events and always operate on canonically-identified records.

## Worker Categories

| Worker | Trigger | Responsibility |
|---|---|---|
| **Graph projection** | New archive record registered | Push entity/object into `qigraph` |
| **Retrieval orchestration** | Query received | Coordinate pgvector + Neo4j |
| **Metadata enrichment** | Extraction complete | Infer entities, doc type, tags |
| **Repair / retry job** | Failed state detected | Retry a failed pipeline stage on specific node |
| **Background embedding** | Chunks ready | Embed and push to pgvector |
| **Sync worker** | Scheduled | Reconcile local ↔ cloud state |
| **Enrollment reconciliation** | Fleet event | Sync config and health state |
| **Config distribution** | Admin action | Push settings to assigned nodes |
| **Folder assignment sync** | Admin action | Attach dropping zones to node |
| **Node update/repair** | Admin action | Instruct agent to patch or restart |

## Worker Contract

Every worker must define:

```yaml
id: worker_slug
trigger: event_type or schedule
input:
  - canonical_id (required for domain records)
  - additional context fields
output:
  - what is written back (always via canonical_id FK)
fleet_context:
  - target_device_id (if a node command)
  - issued_by (identity)
  - result_event_id (event tracking link)
failure:
  - error state written to qisys.jobs
  - retryable: true/false
  - max_retries: N
```

## Worker State

Workers write their state to `qisys.jobs`:

| Status | Meaning |
|---|---|
| `queued` | Job received, not yet started |
| `running` | In progress |
| `completed` | Successfully finished |
| `failed` | Terminal error (retryable or not) |
| `retrying` | Scheduled for retry |

## Workers Law

* Workers **never** redefine canonical identity
* Workers **never** write to `qiarchive` schema directly without going through the pipeline contract
* Workers **always** reference a `canonical_id` in their input and output
* Worker failures are **visible** — silently dropped jobs are a violation
