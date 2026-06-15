# QiDNA Blueprint Readiness and Decision Gate

## Status

Original assessment: 2026-06-10. Supabase authority update: 2026-06-14.

QiDNA has one accepted vocabulary, complete Markdown/MDX site coverage, visible document statuses, and an accepted minimal Supabase spine. Database deployment and application cutover remain gated.

## Resolved Gates

- ADR-0017 defines the canonical mirrored roots.
- ADR-0018 defines Supabase Postgres as QiLife's canonical structured-data authority.
- The canonical minimum is Entity, Entity Relationship, and QiBit.
- The local migration contains only `qi_entities.entities`, `qi_entities.relationships`, and `qi_events.qibits`.
- QiNexus remains file/export/reference/archive authority.
- SQLite is legacy, local, or transitional evidence only.

## Open Database Gate

Before deployment:

1. Approve user identity and ownership columns.
2. Approve custom-schema Data API exposure.
3. Define RLS policies and role grants.
4. Define SQLite-to-Supabase mapping and validation.
5. Define backup, rollback, cutover, and offline behavior.
6. Test the migration against a local or linked Supabase project.

## Open UI Gate

The route, screen, workflow, loading, empty, error, offline, permission, visibility, accessibility, and entity-to-view contracts remain incomplete.

## Required Sequence

1. Validate the baseline migration locally.
2. Approve identity, RLS, grants, and access boundaries.
3. Define and test the transitional data mapping.
4. Approve backup, rollback, and cutover.
5. Integrate QiLife against Supabase.
6. Complete the UI blueprint.

## Exit Criteria

The Chronicle becomes implementation-complete when the Supabase access/cutover contracts and the v1 UI contracts are approved, tested, and represented by one canonical document each.
