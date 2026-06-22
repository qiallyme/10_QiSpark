# QISERVER — RUN ME FIRST

## What this machine is
This is the private QiOS AI/ingest node.

## Current role
- Host OS: Ubuntu
- Private network access: Tailscale
- Private AI chat UI: Open WebUI via Tailscale Serve
- Local model runtime: Ollama
- Derived graph store: Neo4j
- Future role: ingestion, extraction, chunking, embeddings, graph projection, local control plane

## Main URLs
- Open WebUI: https://qiserver-1.cerberus-sirius.ts.net
- Tailscale machine name: qiserver-1
- Tailscale IP: 100.121.111.106

## Local services
- Ollama API: http://127.0.0.1:11434
- Open WebUI: http://127.0.0.1:3000
- Neo4j Browser: http://127.0.0.1:7474
- Neo4j Bolt: bolt://127.0.0.1:7687

## Paths
- QiOS root: /srv/qios
- Compose dir: /srv/qios/compose
- Docs dir: /srv/qios/docs
- Data root: /srv/qidata
- Open WebUI data: /srv/qios/open-webui
- Neo4j data: /srv/qios/neo4j

## What is running right now
- Ollama runs on host via systemd
- Open WebUI runs in Docker
- Neo4j runs in Docker
- Tailscale Serve publishes Open WebUI privately to the tailnet

## Docker stack
Compose file:
- /srv/qios/compose/docker-compose.yml

Env file:
- /srv/qios/compose/.env

## Models currently installed
- llama3.2:latest  -> chat
- embeddinggemma:latest -> embeddings only

## Important rule
Do NOT use embeddinggemma as the default chat model.
Use llama3.2 for chat.
Use embeddinggemma for vectorization/RAG.

## Core commands
### Check overall status
bash /usr/local/bin/qiserver-status

### Go to compose folder
cd /srv/qios/compose

### Restart Ollama
sudo systemctl restart ollama

### Check Ollama
sudo systemctl status ollama --no-pager
curl http://127.0.0.1:11434/api/tags

### Check Docker containers
docker ps
docker logs open-webui --tail 50
docker logs neo4j --tail 50

### Restart Docker stack
cd /srv/qios/compose && docker compose up -d

### Stop Docker stack
cd /srv/qios/compose && docker compose down

### Check Tailscale Serve
tailscale serve status

## What this server is NOT
- Not the canonical source of truth for records
- Not where random manual edits should live
- Not where graph/vector should become truth

## Architectural rule
Canonical truth stays in the real data model.
Graph and embeddings are derived layers.
This box is compute + local runtime + private AI surface.

## Next planned build
1. Python local API
2. inbox watcher
3. extraction pipeline
4. chunking
5. embedding worker
6. Supabase upsert
7. Neo4j projection
8. status/retry endpoints

## If I come back later and forget
Start here:
1. Open this file
2. Run: bash /usr/local/bin/qiserver-status
3. Open: https://qiserver-1.cerberus-sirius.ts.net
4. Check: docker ps
5. Check: sudo systemctl status ollama --no-pager
