# Data Flow

## Canonical Ingestion Flow

```
SOURCE FILE
    │
    ▼
DEVICE DROP ZONE / ASSIGNED WATCH PATH
    │
    ▼
LOCAL AGENT DETECT
    │
    ▼
RESOLVE DOMAIN (namespace + prefix lookup)
    │
    ▼
REGISTER IN QiARCHIVE
  - assign canonical ID (UUID/ULID)
  - assign short visible code (Q + 6 hex)
  - normalize filename: {domain}_{name}_{QXXXXXX}.ext
  - calculate checksum
    │
    ▼
EXTRACT / INSPECT
  - detect MIME type
  - choose parser
  - extract text
  - OCR if needed
  - store extraction method + raw text
    │
    ▼
ENRICH METADATA
  - infer document type
  - extract entities
  - tag confidence values
  - assign semantic metadata
    │
    ▼
CHUNK
  - split text deterministically
  - assign chunk indices
  - link chunks to archive_id
    │
    ▼
EMBED (local)
  - generate embedding vectors
  - push to pgvector (qiarchive.archive_chunks)
    │
    ▼
INDEX
  - update search index
  - update qigraph.master_index if applicable
    │
    ▼
ROUTE / REVIEW / ACT
  - suggest route based on doc type + confidence
  - human review or auto-confirm
  - finalize placement
  - update archive record
```

## RAG / AI Query Flow

```
USER QUERY
    │
    ▼
Metadata filter in Postgres (Supabase)
    │
    ▼
Semantic retrieval in pgvector
    │
    ▼ (optional)
Graph expansion in Neo4j / qigraph
    │
    ▼
Assemble evidence with provenance references
    │
    ▼
Generate answer citing archive_id / chunk_id / entity_id
```

## Infrastructure Edge Ingress (Local Node Hosting)

```
PUBLIC REQUEST (Internet)
    │
    ▼
EDGE PROVIDER (DNS / Policy / Tunnel Endpoint)
    │
    ▼
OUTBOUND TUNNEL CONNECTOR (Local Node)
    │
    ▼
LOCAL REVERSE PROXY (Routing / Auth Check)
    │
    ▼
TARGET SERVICE (App Container / Webhook)
    │
    ▼
INTERNAL DATA SERVICE (Postgres / Vector DB)
```

## Flow Invariants

* Every record entering the system carries a canonical ID **before** extraction begins
* Derived layers (graph, vector, AI) only receive data **after** the archive ID is assigned
* Failure at any stage is visible, stateful, and retryable — it never silently drops data
* **Provenance**: Every ingest must carry `source_device_id`, `source_agent_id`, `source_path`, and `ingest_mode` because ingestion happens across nodes.
