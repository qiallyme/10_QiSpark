# Runtime Zones

QiOS has a clear local/cloud boundary. Crossing that boundary without explicit intent is an architectural violation.

> ⚠️ **Discrepancy Note (v0.4)**: An earlier version of the master README described the cloud runtime as "Railway Postgres / Railway Redis / Railway Neo4j / NocoDB on Railway." The v0.4 blueprint removes Railway branding. The **actual canonical cloud backend is Supabase Postgres** with pgvector, managed via Supabase migrations. Redis and Neo4j remain correct for queue and graph layers respectively. This doc reflects the current actual implementation.

## Local Runtime

Runs on an **enrolled device node** (not necessarily the developer/operator machine):

| Component | Responsibility |
|---|---|
| File watcher | Detect new files in assigned watch paths or drop zones |
| Local Agent | Thin control service for health, assignments, and job taking |
| Ingest pipeline | Orchestrate the full intake flow on that node |
| OCR subprocess | Extract text from scanned documents |
| Extraction subprocess | Parse structured file types |
| Chunking | Split extracted text deterministically |
| Embedding subprocess | Generate vectors locally |
| Local API | Agent execution endpoints (internal node control only) |
| Local state | `C:/QiLabs/QiData/` working directory |

### Local Working Directory

The canonical local root is `C:/QiLabs/`. The runtime state root is `C:/QiLabs/QiData/`.

```
C:/QiLabs/
├── QiData/
│   ├── inbox/
│   ├── processing/
│   ├── reviewed/
│   ├── failed/
│   ├── manifests/
│   ├── extracted_text/
│   ├── embeddings_cache/
│   ├── logs/
│   └── model_cache/
└── _QiOne_MonoRepo/
```

Nodes may be provisioned by role such as `PRIMARY_DEV`, `INGEST_EDGE`, `GPU_WORKER`, or `ARCHIVE_NODE`.

## Cloud Runtime

Runs on hosted infrastructure:

| Component | Technology | Responsibility |
|---|---|---|
| Canonical metadata | **Supabase Postgres** | System of record |
| Vector retrieval | **pgvector** (in Supabase) | Embedding index |
| Queues + cache | **Redis** | Job state and ephemeral control |
| Knowledge graph | **Neo4j** | Derived graph (not canonical) |
| Admin surface | **NocoDB** | Human-friendly ops over Postgres |
| App APIs | Cloud-hosted | Frontend interaction |
| Retrieval orchestration | Cloud-hosted | pgvector + Neo4j coordination |

## Infrastructure Node Runtime Zones (Self-Hosted)

When a node acts as a dedicated infrastructure server (e.g., `infra.backup_server`), it is conceptually divided into four runtime zones to enforce security and operational boundaries.

### Zone A — Private Administration Zone
Private-only services used strictly by the operator for system management.
* **Services**: SSH, container management (Portainer), DB admin tools, system dashboards, backup management.
* **Rule**: No service in this zone is publicly routable. Access is via private network overlay (Tailnet/VPN) only.

### Zone B — Public Application Zone
Services intentionally made reachable from the public internet for authorized external access.
* **Services**: Client portals, public webhooks, exposed app frontends, form endpoints.
* **Rule**: Exposure must occur only through an approved outbound tunnel + reverse proxy path. No direct port forwarding.

### Zone C — Data Services Zone
Persistent system state and memory services.
* **Services**: PostgreSQL, Vector Database (Milvus/Qdrant/etc.), Object storage integrations.
* **Rule**: Internal-only. Accessible only via private admin channels or trusted internal service networks.

### Zone D — AI Execution Zone
Model runtime and AI-specific execution services.
* **Services**: Local model runtime (Ollama/LM Studio), Embeddings pipeline, AI Chat UI.
* **Rule**: AI runtimes are never directly exposed. Access must be mediated through an application layer or private admin layer.

## Boundary Rule

1. Local runtime **writes** to cloud (registrations, embeddings, metadata).
2. Cloud runtime **serves** app surfaces.
3. Derived layers (graph, vector, AI) **never** write back to canonical tables.
4. **Infrastructure Rule**: Publicly exposed services on local nodes must be isolated from administrative and data services by an explicit proxy boundary.
