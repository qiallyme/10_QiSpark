# ADR-0018: Supabase as QiLife Data Authority

## Status

Accepted on 2026-06-14.

## Context

QiLife needs centralized, queryable, cross-device structured data and a stable API surface for normalized imports. The existing SQLite implementation proved the earlier 15-table model, but it is no longer the canonical direction.

## Decision

- Supabase Postgres is the canonical QiLife structured-data authority.
- SQLite is deprecated and may be used only for legacy, local, or transitional operation.
- The canonical minimum model has two concepts: an **Entity** is a who or what; a **QiBit** is an event or unit of reality.
- Every canonical structured record is represented as an Entity or QiBit.
- QiBits may reference one primary Entity in the baseline. Additional participation models require a later decision.
- Entity-to-Entity meaning is stored in `qi_entities.relationships`.
- Files remain outside the relational spine in QiNexus. Paperless may process and manage documents but does not replace QiNexus authority.
- The baseline contains only `qi_entities.entities`, `qi_entities.relationships`, and `qi_events.qibits`.

## Security Boundary

The custom schemas are private by default. Row-level security is enabled, but no client policies or schema grants are created until identity and authorization rules are approved.

## Migration Boundary

This decision authorizes a migration-ready baseline, not deployment or automatic SQLite conversion. Cutover, data mapping, validation, backup, rollback, and application integration remain separate work.

## Supersedes

- ADR-0012's SQLite/Supabase authority decision.
- ADR-0017's SQLite/Supabase authority bullets.
- Decision 0006's SQLite clean-core direction.

All unrelated vocabulary, hierarchy, QiNexus, manual-first, and review requirements remain in force.
