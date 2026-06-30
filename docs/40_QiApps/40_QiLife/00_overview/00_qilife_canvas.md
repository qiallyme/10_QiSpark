# QiLife Canvas

## Product Sentence

QiLife is Cody's private **Personal LifeDesk**: a local-first life operations system that turns messy real-world inputs into structured, traceable **QiBits**, then routes them through timeline, buckets, threads, actions, context, and retrieval.

## Core Doctrine

- **QiBit is the atomic unit.** Every important item starts as a QiBit or links back to one.
- **Timeline is the spine.** Timeline is a chronological projection of timestamped records, not a separate silo.
- **Buckets match the QiNexus/QiAccess hierarchy.** Structural organization should stay legible outside the app.
- **Threads are cases, projects, and storylines.** They group the full situation, not just tasks.
- **Actions are work orders.** They are the executable layer derived from life events and obligations.
- **Context Dock embeds knowledge beside the work.** QiLife does not depend on a separate wiki engine.
- **Repo docs are canonical during build.** `docs/` is authored in git and later imported into in-app knowledge as read-only system knowledge.
- **SQLite is the v1 database.** The schema is designed to migrate later to Postgres without changing product doctrine.

## Core Object Chain

```text
QiBit
  -> Timeline projection
  -> Bucket
  -> Thread
  -> Action
  -> Resolution
  -> Reflection
  -> Retrieval
```

## Timeline Projection

Timeline is a unified feed assembled from existing records:

- QiBits by `COALESCE(happened_at, captured_at, created_at)`
- Actions by `completed_at` when completed, otherwise `scheduled_for` or `created_at`
- Transactions by `date`
- Events by `start_time`
- Daily summaries by `date`

There is no separate `timeline_entries` table in v1.

## Operational Views

```text
Today
Timeline
Inbox
Threads
Actions
Calendar
People
Money
Knowledge
Documents
Ask QiLife
Settings/About
```

## Structural Buckets

```text
00 Inbox
10 Workbench
20 Timeline
30 Life
40 People
50 Business
60 Finance
70 Legal
80 Tech
90 Assets
100 Data
110 Reference
900 Archive
990 System
```
