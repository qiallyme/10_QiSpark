---
title: Service Map
status: active
updated: 2026-05-29
---

# Service Map

This map separates server-verified runtime facts from repo planning notes. Server-verified facts win when they differ from older repo assumptions.

## Verified Runtime Sources

- Runtime stack: `/srv/qios/stacks/_qiaccess_start`
- Runtime compose file: `/srv/qios/stacks/_qiaccess_start/docker-compose.yml`
- Runtime container: `homepage`
- Runtime image: `ghcr.io/gethomepage/homepage:latest`
- Runtime config: `/srv/qios/stacks/_qiaccess_start/config`
- Repo config source: `/srv/qios/apps/_QiAccess_Start/qiaccess/config`
- Public restricted entrypoint: `https://access.qially.com`
- Tailnet entrypoint: `https://qiserver-1.cerberus-sirius.ts.net`

## Access Classes

- Private Only: local host or tailnet only.
- Public Restricted: internet reachable but protected by Cloudflare Access or equivalent.
- Public Safe: intended unauthenticated public surface.

## Verified Services

| Service | Purpose | Stack / container | Compose path | Internal URL / port | Public or Tailscale URL | Access class | Data path | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QiAccess Home | Start page and service dashboard | `qiaccess_start` / `homepage` | `/srv/qios/stacks/_qiaccess_start/docker-compose.yml` | `127.0.0.1:3001 -> 3000` | `https://access.qially.com`, `https://qiserver-1.cerberus-sirius.ts.net` | Public Restricted, Private Only | `/srv/qios/stacks/_qiaccess_start/config`, `/srv/qios/stacks/_qiaccess_start/public` | active |
| Portainer | Container administration | `portainer` / `portainer` | `/srv/qios/stacks/portainer/docker-compose.yml` | `127.0.0.1:9443 -> 9443` | `https://qiserver-1.cerberus-sirius.ts.net:9449` | Private Only | Docker volume `portainer_data` | active |
| Cockpit | Host administration | systemd `cockpit.socket` | systemd | `*:9090` | `https://qiserver-1.cerberus-sirius.ts.net:9090` | Private Only | system service | active |
| Wiki.js | Knowledge base | `wikijs` / `wikijs`, `wikijs-db` | `/srv/qios/stacks/wikijs/docker-compose.yml` | `127.0.0.1:3002 -> 3000` | `https://qiserver-1.cerberus-sirius.ts.net:9448` | Private Only | `/srv/qios/wiki-export/current`, `/srv/qios/wiki-import/QiDocs`, Docker volume `wikijs_wikijs-db-data` | active |
| Paperless-ngx | Document intake and OCR | `paperless` / `paperless`, `paperless-postgres`, `paperless-redis` | `/srv/qios/stacks/paperless/docker-compose.yml` | `127.0.0.1:8010 -> 8000` | `https://qiserver-1.cerberus-sirius.ts.net:9447` | Private Only | `/srv/qios/data/paperless` | active |
| Open WebUI | Local AI workspace | `compose` / `open-webui` | `/srv/qios/compose/docker-compose.yml` | `127.0.0.1:3000 -> 8080` | `https://qiserver-1.cerberus-sirius.ts.net:9446` | Private Only | `/srv/qios/open-webui` | active |
| Ollama | Local model runtime | systemd `ollama.service` | systemd | `127.0.0.1:11434` | `http://qiserver-1.cerberus-sirius.ts.net:11434` | Private Only | service-managed model store | active |
| NocoDB | Structured tables and registry | `nocodb` / `nocodb`, `nocodb-db`, `nocodb-redis` | `/srv/qios/stacks/nocodb/docker-compose.yml` | `127.0.0.1:8088 -> 8080` | `https://qiserver-1.cerberus-sirius.ts.net:8443` | Private Only | Docker volumes `nocodb_nocodb_data`, `nocodb_nocodb_pg_data`, `nocodb_nocodb_redis_data` | active |
| Firefly III | Personal finance ledger | `firefly` / `firefly_iii_core`, `firefly_iii_db`, `firefly_iii_cron` | `/srv/qios/stacks/firefly/docker-compose.yml` | `127.0.0.1:6877 -> 8080` | `http://qiserver-1.cerberus-sirius.ts.net:6877` | Private Only | Docker volumes `firefly_firefly_iii_upload`, `firefly_firefly_iii_db` | active |
| Firefly Importer | Finance import workflow | `firefly` / `firefly_iii_importer` | `/srv/qios/stacks/firefly/docker-compose.yml` | `127.0.0.1:6878 -> 8080` | `http://qiserver-1.cerberus-sirius.ts.net:6878` | Private Only | `/srv/qios/stacks/firefly/import` | active |
| Qdrant | Vector database | `qdrant` / `qdrant` | `/srv/qios/stacks/qdrant/docker-compose.yml` | `127.0.0.1:6333-6334` | `https://qiserver-1.cerberus-sirius.ts.net:9452/dashboard` | Private Only | `/srv/qios/data/qdrant/storage` | active |
| Neo4j | Graph database browser and Bolt endpoint | `compose` / `neo4j` | `/srv/qios/compose/docker-compose.yml` | `127.0.0.1:7474`, `127.0.0.1:7687` | `http://qiserver-1.cerberus-sirius.ts.net:7474` | Private Only | `/srv/qios/neo4j` | active |
| Uptime Kuma | Health monitoring | `uptime-kuma` / `uptime-kuma` | `/srv/qios/stacks/uptime-kuma/docker-compose.yml` | `127.0.0.1:3005 -> 3001` | `https://qiserver-1.cerberus-sirius.ts.net:9451` | Private Only | `/srv/qios/data/uptime-kuma` | active |
| SolidTime | Project and time ledger | `solidtime` / `solidtime`, `solidtime-db` | `/srv/qios/stacks/solidtime/docker-compose.yml` | `127.0.0.1:8095 -> 8000` | `https://qiserver-1.cerberus-sirius.ts.net:9453` | Private Only | `/srv/qios/data/solidtime` | active |
| Cloudflared | Cloudflare tunnel for public restricted access | `cloudflared` / `cloudflared` | `/srv/qios/stacks/cloudflared/docker-compose.yml` | no host port | `https://access.qially.com` | Public Restricted | token-based tunnel config in compose; do not copy token | active |
| Tailscale | Tailnet access and service proxy | systemd `tailscaled.service` | systemd | UDP `41641`; Tailscale Serve ports listed separately | `qiserver-1.cerberus-sirius.ts.net`, `100.121.111.106` | Private Only | `/var/lib/tailscale` | active |
| DailyWave | Flow planner and next-step dashboard | `dailywave` / `dailywave-frontend-1`, `dailywave-backend-1` | `/srv/qios/stacks/dailywave/docker-compose.yml` | frontend `127.0.0.1:3020`, backend `127.0.0.1:8020` | frontend `https://qiserver-1.cerberus-sirius.ts.net:9454`, backend health `https://qiserver-1.cerberus-sirius.ts.net:9455/health` | Private Only | `/srv/qios/stacks/dailywave/backend/data` | active |
| n8n | Automation switchboard | `n8n` / `n8n` | `/srv/qios/stacks/n8n/docker-compose.yml` | `127.0.0.1:5678 -> 5678` | `https://qiserver-1.cerberus-sirius.ts.net:9450` | Private Only | `/srv/qios/data/n8n` | active |
| BookStack | Operational documentation | `bookstack` / `bookstack`, `bookstack-db` | `/srv/qios/stacks/bookstack/docker-compose.yml` | `127.0.0.1:6875 -> 80` | `http://qiserver-1.cerberus-sirius.ts.net:6875` | Private Only | `/srv/qios/data/bookstack` | active |
| QI Transcribe | Whisper transcription UI | `qitranscribe` / `qitranscribe-whisper-webui` | `/srv/qios/stacks/qitranscribe/docker-compose.yml` | no current host port | listed in QiAccess as attention item | Private Only | `/srv/qios/data/qitranscribe` | broken |
| QI TTS | Local TTS API and Kokoro backend | `qitts` / `qitts-api`, `qitts-kokoro` | `/srv/qios/stacks/qitts/docker-compose.yml` | API `127.0.0.1:8890 -> 8890`; Kokoro internal `8880` | none discovered | Private Only | `/srv/qios/data/qitts/output` | active |

## Repo Planning Notes

- The repo has carried parallel service representations in Homepage YAML and TypeScript registry data.
- Older placeholder URLs in `qiaccess/config/services.yaml` have been replaced with verified qiserver routes.
- Wiki.js can consume this map, but should not be treated as the canonical source for runtime deployment facts.
- Future automation should generate this map from checked runtime receipts and committed config.
