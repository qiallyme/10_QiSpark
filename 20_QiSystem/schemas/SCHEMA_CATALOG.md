# Schema Catalog

## Status

**Active.** Minimal canonical Supabase catalog accepted by ADR-0018.

| Schema | Table | Purpose |
|---|---|---|
| `qi_entities` | `entities` | Persistent people, organizations, places, objects, systems, and other who/what records |
| `qi_entities` | `relationships` | Typed directed relationships between Entities |
| `qi_events` | `qibits` | Events and units of reality, optionally tied to one primary Entity |

## Deliberately Absent

There is no canonical `qi_capture` schema, tagging engine, automation schema, AI schema, file-blob table, or module-specific table in this baseline.

## Security Posture

All tables have RLS enabled. No client grants or policies are defined until identity and authorization are approved.

## Source

Migration: `supabase/migrations/20260614162319_establish_qilife_entity_qibit_spine.sql`.
