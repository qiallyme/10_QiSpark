# Database Blueprint Gap Report

## Status

The 2026-06-12 SQLite inventory is retained as legacy implementation evidence. ADR-0018 superseded it as canonical design on 2026-06-14.

## Canonical Baseline

- Authority: Supabase Postgres.
- Schemas: `qi_entities`, `qi_events`.
- Tables: `entities`, `relationships`, `qibits`.
- Keys: generated UUID primary keys.
- Security: RLS enabled, no permissive client policies.
- Files: QiNexus authority; Paperless processing surface.
- Migration: `supabase/migrations/20260614162319_establish_qilife_entity_qibit_spine.sql`.

## Remaining Gaps

1. User ownership and identity mapping.
2. RLS policies and custom-schema grants.
3. Governed Entity, relationship, and QiBit type vocabularies.
4. SQLite-to-Supabase mapping, validation, and duplicate handling.
5. Backup, rollback, cutover, and offline behavior.
6. Application integration and end-to-end tests.
7. Retention, archive, restoration, and purge rules.

## Legacy Evidence

QiLife commit `c589e1e` contains 15 SQLite tables. Those tables are not automatically recreated or discarded. Their useful data and constraints require an explicit migration map.
