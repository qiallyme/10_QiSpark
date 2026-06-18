---
uid:
  5d79cdf1-075f-4fb9-8261-bb9aa725e047 ...
  ...
---
# Admin

> Quarantine notice: this page still reflects the older tenant and client-platform admin model. It is retained for salvage, not as active QiAccess Start doctrine. See `08_appendices/20_legacy/qiaccess_start_legacy_quarantine.md`.

The Admin surface is the internal operational dashboard for system operators and developers.

## Admin vs Portal

| Admin | Portal |
|---|---|
| Operator / developer only | Client-facing |
| All tenants visible | Single tenant context |
| Low-level system controls | Business workflow |
| Pipeline monitoring | Domain data |

## Admin Capabilities

| Capability | Source |
|---|---|
| Tenant management | `qione.tenants` |
| User and role management | `qione.tenant_members`, `qione.member_roles` |
| Module assignment | `qione.tenant_modules` |
| Job queue monitoring | `qisys.jobs` |
| System events log | `qisys.system_events` |
| Worker status | `qisys.worker_status` |
| Archive inspection | `qiarchive.archive_files` |
| Pipeline failure review | `qiarchive.ingest_jobs` |
| Device enrollment | `qisys.devices` |
| Device registry | `qisys.devices`, `qisys.device_capabilities` |
| Node health / heartbeat monitoring | `qisys.device_heartbeats` |
| Assigned watch folder management | `qisys.device_watch_assignments` |
| Drop zone policy | `qisys.device_watch_assignments` |
| Runtime version/config drift | `qisys.device_agents` |
| Job dispatch / retry by node | `qisys.device_jobs` |
| Audit trail for fleet actions | `qisys.device_events` |

## NocoDB as Admin Surface

NocoDB provides a human-friendly admin interface over Supabase Postgres without requiring custom admin app code. It is appropriate for internal operational use but must:

* Never be exposed publicly
* Always use service role access carefully
* Never be used to bypass RLS for tenant data

## Admin Law

* Admin surfaces must authenticate with elevated roles — never anon keys
* Devices authenticate with enrollment/agent credentials
* Admin surfaces must not expose tenant data across tenant boundaries
* All node-orchestration actions must write audit events in `qisys.device_events` or `qisys.system_events`
* Admin must never bypass the explicit `QiArchive` registration contract
