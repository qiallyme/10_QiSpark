---
title: QIServer Private AI Node
status: active
date: 2026-04-19
layer: compute
type: runtime_profile
host: qiserver
tailscale_name: qiserver-1
---

# QIServer Private AI Node

## Purpose

QIServer is the current machine-local QiOS compute node for private AI access, local model execution, and future ingestion/runtime work. It exists to offload AI and document-processing workload from the primary workstation and to serve as the first live QiOS local runtime host.

## Why This Node Exists

This node is the practical execution host for the local-runtime side of QiOS:

- private AI chat access
- local model hosting
- future ingestion and extraction
- future chunking and embeddings
- future local control-plane endpoints
- future graph projection support

It is not the canonical source of truth for records. Canonical truth remains in the cloud-side data model. Derived layers remain downstream.

## Current Role

### Active now

- Tailscale-connected private server
- Ollama running on host
- Open WebUI running in Docker
- Neo4j running in Docker
- Tailscale Serve publishing Open WebUI privately to the tailnet

### Planned next

- local Python API
- inbox watcher
- extraction pipeline
- deterministic chunking
- embedding worker
- Conditional/Future: Supabase/pgvector upsert
- Neo4j projection
- queue/retry/status endpoints

## Runtime Position in QiOS

QIServer implements the **local runtime** side of QiOS, not the canonical cloud data layer.

### Local runtime responsibilities

- file watcher
- ingest pipeline
- OCR
- extraction
- chunking
- embeddings
- local API
- machine-local state

### Cloud-side responsibilities

- canonical metadata
- retrieval index in pgvector
- app-facing APIs
- review surfaces
- Conditional/Future: tenant-aware data serving

### Boundary rule

Local runtime writes registrations, metadata, and embeddings outward.
Cloud runtime serves application surfaces.
Graph, vector, and AI layers do not become canonical truth.

## Current Access

### Private access surface

- Open WebUI: `https://qiserver-1.cerberus-sirius.ts.net`

### Machine identity

- OS hostname: `qiserver`
- Tailscale machine: `qiserver-1`
- Tailscale IPv4: `100.121.111.106`

## Current Local Services

### Host service

- Ollama API: `http://127.0.0.1:11434`

### Docker services

- Open WebUI: `http://127.0.0.1:3000`
- Neo4j Browser: `http://127.0.0.1:7474`
- Neo4j Bolt: `bolt://127.0.0.1:7687`

## Current Service Topology

### Host

- Ubuntu server
- Tailscale
- Ollama

### Containers

- Open WebUI
- Neo4j

### Network pattern

- services bind locally
- Tailscale Serve proxies Open WebUI privately to the tailnet
- raw backend services are not publicly exposed

## Current Paths

### Server paths

- QiOS root: `/srv/qios`
- compose: `/srv/qios/compose`
- server runbook: `/srv/qios/docs/000_RUN_ME_FIRST.md`

### Data paths

- data root: `/srv/qidata`
- inbox: `/srv/qidata/inbox`
- processing: `/srv/qidata/processing`
- reviewed: `/srv/qidata/reviewed`
- failed: `/srv/qidata/failed`
- manifests: `/srv/qidata/manifests`
- extracted text: `/srv/qidata/extracted_text`
- embeddings cache: `/srv/qidata/embeddings_cache`
- logs: `/srv/qidata/logs`
- model cache: `/srv/qidata/model_cache`
- exports: `/srv/qidata/exports`

## Current Models

### Chat model

- `llama3.2:latest`

### Embedding model

- `embeddinggemma:latest`

## Model Rule

`llama3.2` is the chat/default interaction model.

`embeddinggemma` is not a general chat default. It is reserved for embedding, retrieval, and vectorization work.

## Architectural Constraints

1. This node is compute infrastructure, not canonical record authority.
2. Graph and vector outputs are derived.
3. No ingestion flow should bypass canonical registration.
4. No downstream layer should redefine identity.
5. Runtime memory for operation lives both here and in the machine-local runbook.

## Relationship to Existing Blueprint Sections

This node operationalizes the following already-defined blueprint concepts:

- local runtime
- local API
- embeddings as local subprocess
- Neo4j as derived graph
- Local Admin Control Plane
- Spine milestone: local inbox -> registration -> extraction -> embedding -> retrieval

This file does not replace those sections. It records the concrete live node now implementing them.

## Operational Re-entry

If operator context is lost, begin with:

- `/srv/qios/docs/000_RUN_ME_FIRST.md`
- `bash /usr/local/bin/qiserver-status`

## Immediate Next Build

1. create local Python API structure
2. implement `/status`, `/queue`, `/ingest`, `/retry`
3. build inbox watcher against `/srv/qidata/inbox`
4. extract text into canonical pipeline flow
5. chunk deterministically
6. call Ollama embeddings endpoint
7. upsert to canonical retrieval layer
8. project derived graph records into Neo4j

## Change Log

### 2026-04-19

- Ubuntu server brought online
- Tailscale configured
- Docker installed and running
- Ollama installed and serving locally
- `llama3.2` pulled
- `embeddinggemma` pulled
- Open WebUI deployed in Docker
- Neo4j deployed in Docker
- Tailscale Serve configured for private Open WebUI access
- server-local operator runbook created
- status command created
## Active Runtime

- **qiserver** is the current active runtime.

## Path Doctrine

- `/srv/qios/repos`: For cloned Git repos and coding work.
- `/srv/qios/stacks`: For Docker Compose runtime stacks. Do not create nested Git repos inside `/srv/qios/stacks`.
- `/srv/qios/data`: For persistent app data.

## Service / Runtime Facts

- **NocoDB**: Runs locally at `127.0.0.1:8088`.
- **Open WebUI**: Runs locally at `127.0.0.1:3000`.
- **Private Server Launcher (gethomepage)**: Runs locally at `127.0.0.1:3001`. **Warning:** This is for local/tailnet use only and is separate from the public `access.qially.com` portal.
- **Portainer**: Runs locally at `127.0.0.1:9443` and is an admin service.
- **Ollama**: Installed on qiserver and locked to `127.0.0.1:11434`.


