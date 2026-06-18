---
uid:
  49fa3aba-6764-49f2-ba0b-05995fe4d24b ...
  ...
---
# ADR-0002: Single Domain Rule

**Date**: 2026-03-27
**Status**: Accepted

## Context

Early schema design placed domain logic in the `public` schema and mixed concerns across tables. This created unclear ownership and made RLS enforcement fragile.

## Decision

Every domain in QiOS gets **one canonical Postgres schema**. No domain logic lives in `public`. The mapping is enforced in `registry/domain_registry.yaml`.

Rules:
- One schema per domain (e.g., `qicase`, `qivault`, `qihome`)
- All domain tables must carry `tenant_id` for RLS isolation
- `public` schema is reserved for legacy stubs and global auth-adjacent data only
- Cross-domain access must go through the Platform RBAC layer

## Consequences

- All new tables are created in their domain schema, never in `public`
- Domain registry must be updated when a new schema is created
- Existing `public` tables (`todos`, `nods_page`) are marked legacy and will not be extended
