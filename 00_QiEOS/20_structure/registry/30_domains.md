---
uid:
  cdddc4a1-c802-4c5f-b871-c5ce5d6b5f78 ...
  ...
---
# Domains

Domains in QiOS are ownership boundaries first. Historically they mapped to Postgres schemas in Supabase, but that layer is now legacy/reference-only or future/conditional unless a specific job requires it. No new domain logic belongs in `public`.

## Domain Hierarchy

```text
band -> domain -> subdomain -> object
```

Every object must have a resolved path through this hierarchy before it can be considered registered.

## Live Domain Map

| Domain | Schema | Band | Core Tables |
|---|---|---|---|
| QiOne Platform | `qione` | Platform | legacy/future tenants, tenant_members, member_roles, tenant_modules, module_role_access |
| QiArchive | `qiarchive` | Core | archive_files, archive_chunks, ingest_jobs, file_history |
| QiGraph | `qigraph` | Core | edges, master_index |
| QiAlly (AI) | `qially` | Core | sessions, messages, memory_embeddings |
| QiSys | `qisys` | Core | jobs, system_events, worker_status |
| QiCase | `qicase` | Domain | cases, phases, issues, deadlines, case_documents, document_issues |
| QiChronicle | `qichronicle` | Domain | events, calendar_feeds |
| QiCMS | `qicms` | Domain | posts |
| QiHome | `qihome` | Domain | chores, chore_assignments, expenses, expense_shares, settlements |
| QiKnowledge | `qiknowledge` | Domain | notes |
| QiTax | `qitax` | Domain | returns, return_files |
| QiVault | `qivault` | Domain | documents |

## Domain Rules

* If a relational layer is used, prefer one schema per domain
* Multi-tenant `tenant_id` assumptions are legacy/future only unless a specific job reactivates them
* If a relational layer is used, every domain table should have governed access policy coverage
* Cross-domain reads are reference-only unless an explicit interface or event contract is approved
* New domains require an ADR before any new relational schema is created

## Domain vs Namespace Clarification

Domains and namespaces are not interchangeable.

- Domains define ownership boundaries in the system architecture.
- Namespace codes define routing containers for work, artifacts, and workspace organization.

Examples:
- `QiArchive` is a domain
- `0300LGL` is a namespace band
- `5441MAT` is a namespace allocation

Shorthand legacy codes may exist as aliases in reconciled materials, but they do not replace canonical domain names in the blueprint.
