---
title: Access And Exposure Rules
status: active
updated: 2026-05-29
---

# Access And Exposure Rules

## Current Exposure Pattern

QiAccess Home has two confirmed access paths:

- Public restricted: `https://access.qially.com`
- Tailnet private: `https://qiserver-1.cerberus-sirius.ts.net`

The public path is protected by Cloudflare Access. An unauthenticated request to `https://access.qially.com` returns a Cloudflare Access login redirect, not dashboard content.

Most operational services are exposed only through Tailscale Serve on `qiserver-1.cerberus-sirius.ts.net` and local loopback Docker bindings. The Docker host port bindings for service containers are on `127.0.0.1` unless otherwise noted.

## Classes

| Class | Meaning | Examples |
| --- | --- | --- |
| Private Only | Localhost-only or tailnet-only access | Portainer, Cockpit, NocoDB, Firefly, Paperless, Open WebUI, Ollama, Qdrant, Neo4j, Uptime Kuma, SolidTime, Wiki.js, n8n |
| Public Restricted | Internet reachable but protected by Cloudflare Access or equivalent | `https://access.qially.com` |
| Public Safe | Intended unauthenticated public surface | none confirmed for QiAccess |
| Placeholder | A repo or planning URL that must not be treated as live truth | superseded placeholder URLs in older config |

## Rules

1. Do not expose admin/control surfaces publicly by default.
2. Do not treat placeholder URLs as verified routes.
3. Do not commit secrets, tokens, passwords, or embedded credentials into Homepage YAML.
4. Do not expose admin tools publicly without Cloudflare Access or stronger controls.
5. Keep Docker service host bindings on `127.0.0.1` unless there is an explicit exposure decision.
6. Treat Tailscale URLs as private operational access, not public product URLs.
7. Do not document Cloudflare tunnel tokens or service credentials.
8. Do not change Cloudflare, Tailscale, compose, or `.env` configuration without backing up the file and showing a diff first.

## Verification Commands

```bash
curl -fsS -I http://127.0.0.1:3001
curl -kfsS -I https://qiserver-1.cerberus-sirius.ts.net
curl -fsS -I https://access.qially.com
tailscale serve status
docker ps --format '{{.Names}}|{{.Image}}|{{.Status}}|{{.Ports}}'
ss -tulpen
```

Expected:

- Local QiAccess returns `200 OK`.
- Tailscale QiAccess returns `200 OK`.
- Public QiAccess returns a Cloudflare Access redirect when unauthenticated.
- Admin services appear only on loopback or Tailscale Serve.

## Future Automation Candidates

- Exposure-label linting across YAML and TypeScript.
- A route-verification receipt generated from Server Codex checks.
- Automatic warning when a public URL points to a private/admin-class service.
