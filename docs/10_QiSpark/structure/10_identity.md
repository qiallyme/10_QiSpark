# Identity and Multi-Tenancy Architecture

> Quarantine notice: this page preserves older platform and tenant-model doctrine. Treat it as reference-only until it is rewritten to match the active QiAccess Start runtime. See `08_appendices/20_legacy/qiaccess_start_legacy_quarantine.md`.

## Single Source of Truth
Auth and Identity are completely delegated to **Supabase Auth**.

## Namespace Isolation & Schema Separation
Do **not** store tenant isolation logic or multi-tenant domain data in the `public` schema.
* **`public`**: Reserved only for global operational data, internal system profiles, and generalized reference tables (e.g., `profiles`, `todos`).
* **`qione` (or `tenant_data`)**: A separate schema for all multi-tenant customer data, keeping domains strictly isolated.

## The RBAC & Tenant Structure
Identity operates through three primary tables:

1. **`auth.users`**: Managed natively by Supabase.
2. **`public.organizations` (or `tenants`)**: The canonical parent for a given tenant instance.
3. **`public.tenant_members`**: The mapping layer that ties `auth.users.id` to `tenants.id` with a specific `role` (e.g., Owner, Admin, Member).

## Row Level Security (RLS) Strategy
Every mapped table in the tenant domain must contain a `tenant_id`.
RLS must be universally enforced utilizing a Supabase Postgres function that pulls the resolved `tenant_id` out of the user's secure bounded context (either via a JWT claim `app_metadata` or a secure database hook `auth.uid() -> tenant_members`).
