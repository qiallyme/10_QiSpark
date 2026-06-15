# ADR-0004: Single-Account Modular Mode

Date: 2026-04-04
Status: Proposed

## Context

QiOS v0.4 currently defines a Platform layer centered on multi-tenancy through the `qione` schema, including `tenants`, `tenant_members`, `member_roles`, `tenant_modules`, and `module_role_access`.

That model is valid for a hosted multi-tenant portal, but it adds significant implementation overhead for the current runtime goal: a standard authenticated app with strict per-user isolation and incremental module growth.

The current system does not require organization containers, cross-user shared workspaces, tenant billing, or tenant-scoped administration in order to deliver the first working product.

At the same time, the Core Spine remains correct and should be preserved:

- canonical identity
- archive-first registration
- lineage continuity
- modular domains
- applications as delivery surfaces rather than schema owners

## Decision

QiOS adopts a **Single-Account Modular Mode** for the current implementation.

### 1. Runtime mode

The active runtime is **single-account / user-scoped**, not multi-tenant.

### 2. Ownership model

For current domain-scoped records, `tenant_id` is replaced by `owner_user_id` referencing `auth.users(id)`.

### 3. Platform simplification

The following `qione` concerns are deferred from the active runtime:

- tenants
- tenant membership
- tenant role mapping
- tenant module assignment
- tenant-scoped access resolution

`qione` is no longer required as the active container model for the first working app.

### 4. Module model

Modules remain valid, but are redefined as:

- domain packages
- navigation surfaces
- optional user-level feature flags or app-level config

Modules do **not** require tenant infrastructure.

### 5. Preserved architecture

The following remain mandatory:

- one canonical identity per object
- one canonical schema home per concern
- archive registration before advanced automation
- derived layers remain non-canonical
- applications do not redefine business logic or schema truth

### 6. Future compatibility

Multi-tenancy is **deferred**, not rejected.
If later required, the system may introduce an account/container layer above user-owned records through a future ADR and migration plan.

## Consequences

### Positive

- faster implementation
- simpler RLS
- fewer joins
- simpler auth resolution
- easier debugging
- modules can ship independently

### Tradeoffs

- no shared tenant workspace model yet
- no org-level RBAC yet
- future collaboration features require later migration

### Implementation rule changes

Replace:

- "All domain tables must carry `tenant_id`"

With:

- "All user-scoped domain tables must carry `owner_user_id`"

Replace:

- "Cross-band data access must go through Platform RBAC"

With:

- "Current runtime access is enforced through `auth.uid()` ownership policies; any future shared-container access model requires a new ADR."

## Follow-up actions

1. Update docs that describe the active runtime as multi-tenant.
2. Mark hosted multi-tenant portal language as future-state only.
3. Update schema guidance from `tenant_id` to `owner_user_id` for current implementation.
4. Simplify RLS examples accordingly.
5. Create migration files for active domain schemas.
