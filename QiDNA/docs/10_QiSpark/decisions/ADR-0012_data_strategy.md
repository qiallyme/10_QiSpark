# ADR-0012: Data Strategy Across Supabase and QiNexus

## Status

Superseded on 2026-06-14 by ADR-0018 for database authority. Retained as decision history.

## Context

QiDNA references an older Supabase-backed system, current QiLife documentation names SQLite as the v1 runtime database, and QiNexus is defined as durable storage and folder discipline. No Supabase migrations, local configuration, or live schema were available during the 2026-06-10 audit.

Supabase and QiNexus are not interchangeable: one can hold relational application state while the other organizes durable files and exports.

## Decision

- The QiLife application database is authoritative for structured life records. The documented current implementation is SQLite.
- QiNexus is the file, export, reference, and archive layer. It is not the relational system of record.
- Supabase is a legacy source and possible integration or future database target, not a current authority. Imports require an explicit bridge and provenance.
- Replacing SQLite with Supabase requires a separate migration ADR backed by a reviewed schema, access model, backup plan, and cutover procedure.

## Rationale

This matches the accepted clean-core decision and prevents folder placement from competing with database integrity or an unavailable legacy schema.

## Consequences

- QiNexus stores or references blobs and exports while QiLife stores metadata and relationships.
- Supabase connectors belong to QiConnect.
- Supabase data remains non-canonical until mapped and approved.
- Schema docs must identify SQLite, legacy Supabase, or proposed future scope.
