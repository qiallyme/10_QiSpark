---
uid:
  9138f16a-3e33-440d-9133-98d6b5964d2a ...
  ...
---
# APIs

Current active doctrine centers on qiserver local runtime surfaces, QiAccess Start as the cognitive/operational front door, and Markdown/YAML files as the source of truth. Old cloud-hosted Supabase admin/app API assumptions below are retained as legacy/reference-only or future/conditional patterns.

## API Categories

QiOS has four distinct API categories. Each has a defined scope and must not cross into another's responsibility.

| Category | Scope | Location |
|---|---|---|
| **Local Agent API** | Machine-local control — pipeline state, local config | Python (local machine) |
| **Hosted Admin API** | Fleet control — enrollment, dispatch, health | Future / conditional hosted layer |
| **App APIs** | Frontend interaction — route-safe reads/writes against approved services | QiAccess Start and future adapters |
| **Integration APIs** | External system connectors — future email, webhooks, Zapier | Local or future hosted connectors |
| **Worker APIs / Events** | Async job triggers and continuation signals | Local runtime first; future hosted queue optional |

## Local Agent API (Machine-internal)

The local Python API controls engine-side operations strictly for the node:

```
GET  /status              -> local agent health and pipeline state
GET  /watchers            -> return current active filesystem assigned paths
POST /scan                -> trigger a directory scan
POST /ingest              -> manually push a single file
POST /job/execute         -> accept and execute a dispatched command
POST /update              -> receive configuration updates
GET  /health              -> basic node liveness check
```

## Hosted Fleet / Admin API (Server-side, Future / Conditional)

The Cloud-hosted orchestration surface commands the fleet:

```
POST /fleet/enroll        -> enroll a new machine device
POST /fleet/assign        -> map a watch folder to a device node
POST /fleet/tokens        -> issue or revoke access credentials
PUT  /fleet/config        -> push configurations downward
POST /fleet/jobs          -> queue execution task for a node
GET  /fleet/heartbeats    -> fetch liveness matrix of devices
GET  /fleet/audit         -> view action history for operations
```

## App API Responsibilities

App APIs must:
* Respect current source-of-truth boundaries in Markdown/YAML docs and approved runtime services
* Treat tenant-scoped Supabase JWT patterns as legacy/future only unless a specific job requires them
* Avoid cross-boundary reads/writes that bypass the owning domain or pipeline
* Never accept writes that bypass the pipeline (no raw archive inserts from frontend)

## Worker Events Contract

Each async worker must define:
* **Input**: what payload it receives (always includes a canonical ID)
* **Output**: what it writes back (always references the same canonical ID)
* **Failure handling**: retryable error state written to `qisys.jobs`

## API Law

> No frontend or integration API may write directly to `qiarchive` records without going through the pipeline. The pipeline owns archive record state.
