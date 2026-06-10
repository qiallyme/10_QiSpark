# Database Blueprint Gap Report

## Accepted Direction

- SQLite is the current QiLife structured-data authority.
- QiNexus owns files, exports, references, and archives.
- Supabase is legacy import or possible future integration only.
- V1 is manual-first and AI writes require review and approval.

## Evidence Available

QiDNA names these intended entities:

```text
qibits
buckets
threads
actions
action_steps
people
transactions
obligations
knowledge_items
documents
events
links
activity_log
ai_outputs
daily_summaries
```

Module and decision documents describe provenance, timeline projection, capture, triage, documents, people, actions, and summaries.

## Blocking Evidence Missing

No SQLite database, SQL schema, migration files, ORM model, or database configuration exists in this repository. The actual schema cannot be reconstructed safely from prose.

Required implementation evidence:

- actual `qilife.sqlite` database or a read-only schema dump
- migration directory, if one exists
- ORM or model definitions
- database creation/bootstrap code
- canonical runtime database path
- current application repository and commit
- sample data only if sanitized and necessary for constraint discovery

## Blueprint Gaps

For every v1 entity, approval is still required for:

- table and column names
- types, nullability, and defaults
- primary and foreign keys
- cardinality and delete behavior
- unique and check constraints
- status enums and state transitions
- timestamps and timeline projection field
- indexes and required queries
- provenance and audit fields
- file-reference rules
- archive, retention, restoration, and purge behavior
- backup and migration procedure
- privacy and authorization boundaries

## V1 Mapping Priority

1. QiBit and raw capture provenance.
2. Inbox and triage state.
3. Actions and action steps.
4. Documents and evidence links.
5. People and entity relationships.
6. Timeline projection rules.
7. Daily summaries.
8. AI output staging and approval records.

## Exit Criteria

Database implementation may continue only after the real schema is inspected, mapped to the entity catalog, discrepancies are documented, and v1 fields, statuses, relationships, and migrations are approved.
