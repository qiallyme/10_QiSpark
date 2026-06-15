# Integrations

Integrations are connections to external systems. They are not canonical data sources — they are inputs that feed into the Spine.

## Integration Rule

> All external data entering QiOS must pass through the registration pipeline. No integration may write directly to canonical tables.

```
External System → Integration API → Pipeline → QiArchive → Canonical Record
```

## Planned Integrations

| Integration | Status | Entry point |
|---|---|---|
| Assigned watch folders | Active | Active via enrolled device agent |
| Device drop zone | Active | Active via enrolled device agent |
| Local file watcher | Active | `C:/QiLabs/QiData/inbox/` |
| Manual file upload | Active | App API → pipeline |
| Synced cloud storage | Planned | Non-canonical until registered via sync worker |
| Email intake | Future | Connector service |
| Webhook intake | Future | Integration API |
| Calendar sync | Future | `qichronicle` connector |

*Note: A device-assigned folder or drop zone is merely an **ingress mechanism**, not a canonical source itself. The integration law explicitly remains intact.*

## Integration Contract

Every integration must define:

* **Trigger**: what initiates the intake
* **Format**: what data arrives and in what shape
* **Entry point**: which API or queue receives the data
* **Output**: what canonical record is created
* **Failure handling**: what happens if the integration drops data

## Auth for Integrations

External integrations must authenticate using:
* **Service role key** for server-to-server (never expose to client)
* **Scoped API key** for third-party connectors
* **JWT** for user-context integrations

Integrations may never bypass tenant isolation — every record created via integration must carry a `tenant_id`.

## Email Pipeline Flow Contract

Email intake is considered a complex integration that must strictly obey the canonical registration pipeline:

* **Source**: Gmail / Outlook / IMAP / webhook providers
* **Entry**: Integration API or background connector worker
* **Flow**:
  1. `Connector Pull or Webhook`
  2. `→ qisys Job / Event`
  3. `→ qiarchive Registration`
  4. `→ Extraction & Attachments`
  5. `→ Chunking & Embedding`
  6. `→ Routing/Review/Action`
* **Worker Rule**: All asynchronous worker inputs and outputs must pass and reference canonical IDs.
* **Failure Rule**: Failures must be visible, stateful, and cleanly retryable via `qisys`.
* **Provenance Rule**: The integration must NEVER bypass explicit `qiarchive` registration.
* **Isolation Rule**: Every derived email record must preserve `tenant_id` and obey Row-Level Security.

## Specific Service Integrations

- **Wiki.js**: Runs locally at `127.0.0.1:3002`. Verified internal/admin route via Tailscale Serve: `https://qiserver-1.cerberus-sirius.ts.net:9448`. Public Cloudflare route `https://wiki.qially.com` currently returns Bad Gateway and should be labeled degraded until the tunnel route is repaired. Future Wiki.js sync may happen by script or workflow, but do not build it now.
- **Paperless-ngx**: Runs locally at `127.0.0.1:8010`. Paperless metadata must be configured before bulk import. Paperless should be tested with 10 documents max before large ingestion.
