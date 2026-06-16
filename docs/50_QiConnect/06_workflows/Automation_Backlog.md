# Automation Backlog

This backlog tracks automation targets within the QiAccess ecosystem, outlining their implementation priority, dependencies, blockers, and automation readiness scores.

---

## 1. Automated Document watched folders intake (QiIngest Core)
Automate the file system watch triggers in the `00_inbox` and route them to Paperless-ngx.
- **Priority**: **Critical / High**
- **Prerequisites**: Secure Docker volume binds on `qiserver`, verification of Tailscale network persistence.
- **Blockers**: None.
- **Automation Readiness**: **3.5 / 5** (Tools are ready, but container daemon bindings need configuration).

---

## 2. Wiki.js Auto-Publishing API Pipeline
Convert local static Markdown blueprints and records into Wiki.js pages automatically upon push.
- **Priority**: **Medium**
- **Prerequisites**: Wiki.js API token setup and connection path repair on `wiki.qially.com`.
- **Blockers**: Public Cloudflare tunnel routing to Wiki.js is currently degraded; private-only 9448 endpoint must be used.
- **Automation Readiness**: **2.5 / 5** (Wiki.js API is standard, but the connector script needs mapping).

---

## 3. Neo4j Graph Extraction & Sync
Generate entity relationship graph files and seed Neo4j with structural metadata.
- **Priority**: **Medium**
- **Prerequisites**: Bring Neo4j back online.
- **Blockers**: TCP port 7474 did not respond on `100.121.111.106` during the 2026-05-08 audit (marked as `broken` / `offline` in registry).
- **Automation Readiness**: **1.5 / 5** (Database container requires troubleshooting before extraction code can run).

---

## 4. Ollama to Qdrant Vector Sync
Automatically chunk ingested files, run embeddings using Ollama `embeddinggemma:latest`, and upsert vectors to Qdrant collections.
- **Priority**: **High**
- **Prerequisites**: Qdrant collection schemas, chunking rules in `docs/30_qiarchive/30_chunking/20_chunk_rules/`.
- **Blockers**: Qdrant configuration is currently a placeholder (needs initialization).
- **Automation Readiness**: **3 / 5** (Ollama API is verified active; Qdrant container is online but needs collection creation).

---

## 5. Uptime Kuma Automated Container Auto-Healer
Configure webhooks from Uptime Kuma to trigger Docker container restarts on `qiserver` when port monitoring fails.
- **Priority**: **Low**
- **Prerequisites**: Portainer API keys and docker-entrypoint hooks.
- **Blockers**: Access security checks (ensuring container restarts are restricted to non-malicious sources).
- **Automation Readiness**: **2.5 / 5** (n8n hooks can route these, but strict auth guards are missing).
