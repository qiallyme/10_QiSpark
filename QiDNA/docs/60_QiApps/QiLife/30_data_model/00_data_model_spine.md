# QiLife Data Model Spine

This document outlines the core SQLite database tables and fields for the **QiLife** V1 system. 

> [!NOTE]
> All tables (except static tables like `buckets`) utilize **ULIDs** as primary keys to ensure lexicographical time-sorting. For more details on the database architecture, layers, and safeguards, see the [Database Stability Strategy](file:///c:/QiLabs/60_QiApps/_qilife/docs/30_data_model/06_database_stability_strategy.md).

---

## Core Tables for V1

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

## Canonical V1 Conventions

- IDs use **ULIDs** everywhere except static lookup tables such as `buckets`.
- `note` and `reflection` are **QiBit types**, not separate tables.
- Monetary amounts are stored as **integer cents**.
- Timeline is a **projection** over timestamped records, not its own table.
- Repo docs imported into `knowledge_items` are **read-only** in-app.

## Timeline Projection Rules

The feed uses these timestamp rules:

| Record Type | Timeline Timestamp Rule |
|---|---|
| QiBit | `COALESCE(happened_at, captured_at, created_at)` |
| Action | `completed_at` if present, else `scheduled_for`, else `created_at` |
| Transaction | `date` |
| Event | `start_time` |
| Daily Summary | `date` |

Documents, people, and knowledge items can appear in context panes and search results without needing to be first-class timeline rows.

---

## 1. `qibits`
The atomic captured life item.

```text
qibits
├── id (ULID, PK)
├── title (Text)
├── raw_capture (Text, Sacred Original Input)
├── summary (Text)
├── meaning (Text)
├── qibit_type (Text)
├── bucket_code (Text, FK)
├── thread_id (ULID, Nullable, FK)
├── status (Text)
├── priority (Text)
├── importance (Text)
├── emotional_load (Text)
├── action_required (Boolean)
├── suggested_action (Text, Nullable)
├── future_slot (Text)
├── happened_at (DateTime)
├── captured_at (DateTime)
├── resolved_at (DateTime, Nullable)
├── retrieval_summary (Text, Nullable)
├── reflection (Text, Nullable)
├── tags_json (JSON)
├── metadata_json (JSON)
├── created_at (DateTime)
├── updated_at (DateTime)
├── archived_at (DateTime, Nullable)
└── deleted_at (DateTime, Nullable)
```

### Types
`event`, `note`, `message`, `call`, `problem`, `idea`, `decision`, `task_seed`, `transaction_seed`, `obligation_seed`, `document_seed`, `appointment`, `receipt`, `knowledge`, `reflection`, `other`

### Statuses
`new`, `triaged`, `open`, `in_progress`, `waiting_on`, `scheduled`, `resolved`, `closed`, `reference`, `ignored`, `archived`

---

## 2. `buckets`
The top-level categorization domain matching the physical folder hierarchy.

```text
buckets
├── code (Text, PK, e.g., '00', '10')
├── name (Text)
├── slug (Text)
├── folder_path (Text)
├── sort_order (Integer)
├── description (Text)
├── is_system (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Seed Buckets
*   `00` Inbox (unprocessed QiBits)
*   `10` Workbench (active work)
*   `20` Timeline (chronological feed)
*   `30` Life (personal / household)
*   `40` People (directory / contact log)
*   `50` Business (freelance / ventures)
*   `60` Finance (ledgers / transactions)
*   `70` Legal (evidence / housing disputes)
*   `80` Tech (automation / config / repos)
*   `90` Assets (media / designs / templates)
*   `100` Data (schemas / backups)
*   `110` Reference (knowledge items / templates)
*   `900` Archive (historical records)
*   `990` System (app logs / index manifests)

---

## 3. `threads`
Ongoing cases, projects, storylines, or situations.

```text
threads
├── id (ULID, PK)
├── title (Text)
├── description (Text)
├── bucket_code (Text, FK)
├── status (Text)
├── priority (Text)
├── next_action (Text, Nullable)
├── due_date (DateTime, Nullable)
├── started_at (DateTime)
├── closed_at (DateTime, Nullable)
├── tags_json (JSON)
├── metadata_json (JSON)
├── created_at (DateTime)
├── updated_at (DateTime)
├── archived_at (DateTime, Nullable)
└── deleted_at (DateTime, Nullable)
```

### Statuses
`open`, `active`, `waiting_on`, `resolved`, `closed`, `archived`

---

## 4. `actions`
The task / work order table.

```text
actions
├── id (ULID, PK)
├── title (Text)
├── description (Text)
├── source_qibit_id (ULID, Nullable, FK)
├── bucket_code (Text, FK)
├── thread_id (ULID, Nullable, FK)
├── status (Text)
├── priority (Text)
├── energy (Text)
├── context (Text)
├── due_date (DateTime, Nullable)
├── scheduled_for (DateTime, Nullable)
├── completed_at (DateTime, Nullable)
├── resolution_note (Text, Nullable)
├── tags_json (JSON)
├── metadata_json (JSON)
├── created_at (DateTime)
├── updated_at (DateTime)
├── archived_at (DateTime, Nullable)
└── deleted_at (DateTime, Nullable)
```

### Statuses
`open`, `in_progress`, `waiting_on`, `scheduled`, `completed`, `cancelled`, `archived`

---

## 5. `action_steps`
Subtasks / steps within an action.

```text
action_steps
├── id (ULID, PK)
├── action_id (ULID, FK)
├── title (Text)
├── description (Text, Nullable)
├── status (Text)
├── sort_order (Integer)
├── completed_at (DateTime, Nullable)
├── created_at (DateTime)
└── updated_at (DateTime)
```

---

## 6. `people`
Lightweight records for external contacts and entities.

```text
people
├── id (ULID, PK)
├── display_name (Text)
├── legal_name (Text)
├── type (Text)
├── relationship (Text)
├── email (Text, Nullable)
├── phone (Text, Nullable)
├── address (Text, Nullable)
├── notes (Text, Nullable)
├── tags_json (JSON)
├── metadata_json (JSON)
├── created_at (DateTime)
├── updated_at (DateTime)
├── archived_at (DateTime, Nullable)
└── deleted_at (DateTime, Nullable)
```

---

## 7. `transactions`
Log of actual financial movements.

```text
transactions
├── id (ULID, PK)
├── date (Date)
├── amount_cents (Integer, e.g. 4000 for $40.00)
├── currency (Text)
├── direction (Text)
├── from_label (Text)
├── to_label (Text)
├── category (Text)
├── bucket_code (Text, FK)
├── thread_id (ULID, Nullable, FK)
├── status (Text)
├── notes (Text, Nullable)
├── evidence_document_id (ULID, Nullable, FK)
├── source_qibit_id (ULID, Nullable, FK)
├── created_at (DateTime)
├── updated_at (DateTime)
├── archived_at (DateTime, Nullable)
└── deleted_at (DateTime, Nullable)
```

---

## 8. `obligations`
Tracks who owes what (money, response, decision).

```text
obligations
├── id (ULID, PK)
├── owed_by_label (Text)
├── owed_to_label (Text)
├── obligation_type (Text)
├── amount_cents (Integer, Nullable)
├── currency (Text, Nullable)
├── reason (Text)
├── status (Text)
├── due_date (DateTime, Nullable)
├── related_transaction_id (ULID, Nullable, FK)
├── source_qibit_id (ULID, Nullable, FK)
├── created_at (DateTime)
├── updated_at (DateTime)
├── resolved_at (DateTime, Nullable)
├── archived_at (DateTime, Nullable)
└── deleted_at (DateTime, Nullable)
```

### Statuses
`open`, `partial`, `waiting_on`, `resolved`, `disputed`, `archived`

---

## 9. `knowledge_items`
Durable reference articles and templates.

```text
knowledge_items
├── id (ULID, PK)
├── title (Text)
├── body_markdown (Text)
├── bucket_code (Text, FK)
├── module_key (Text, Nullable)
├── knowledge_type (Text)
├── source_type (Text)
├── source_path (Text, Nullable)
├── confidence (Text)
├── visibility (Text)
├── tags_json (JSON)
├── metadata_json (JSON)
├── last_synced_at (DateTime, Nullable)
├── sync_hash (Text, Nullable)
├── created_at (DateTime)
├── updated_at (DateTime)
├── archived_at (DateTime, Nullable)
└── deleted_at (DateTime, Nullable)
```

---

## 10. `documents`
File metadata for items stored on disk.

```text
documents
├── id (ULID, PK)
├── title (Text)
├── file_path (Text)
├── source (Text)
├── document_type (Text)
├── bucket_code (Text, FK)
├── thread_id (ULID, Nullable, FK)
├── file_hash (Text)
├── mime_type (Text)
├── size_bytes (Integer)
├── notes (Text, Nullable)
├── created_at (DateTime)
├── updated_at (DateTime)
├── archived_at (DateTime, Nullable)
└── deleted_at (DateTime, Nullable)
```

---

## 11. `events`
Schedule items visible in the Calendar.

```text
events
├── id (ULID, PK)
├── title (Text)
├── description (Text, Nullable)
├── start_time (DateTime)
├── end_time (DateTime)
├── location (Text, Nullable)
├── bucket_code (Text, FK)
├── thread_id (ULID, Nullable, FK)
├── status (Text)
├── source_qibit_id (ULID, Nullable, FK)
├── created_at (DateTime)
├── updated_at (DateTime)
├── archived_at (DateTime, Nullable)
└── deleted_at (DateTime, Nullable)
```

### Statuses
`scheduled`, `completed`, `cancelled`, `missed`, `archived`

---

## 12. `links`
The polymorphic join table mapping relationships between any database items.

```text
links
├── id (ULID, PK)
├── source_type (Text)
├── source_id (ULID/Text)
├── target_type (Text)
├── target_id (ULID/Text)
├── relationship (Text)
├── created_at (DateTime)
└── updated_at (DateTime)
```

---

## 13. `activity_log`
Append-only log of modifications to power summaries and histories.

```text
activity_log
├── id (ULID, PK)
├── occurred_at (DateTime)
├── actor (Text)
├── action (Text)
├── entity_type (Text)
├── entity_id (ULID/Text)
├── summary (Text)
├── before_json (JSON)
├── after_json (JSON)
├── source (Text)
└── created_at (DateTime)
```

---

## 14. `ai_outputs`
AI recommendations stored separately to enable the Human-in-the-Loop flow.

```text
ai_outputs
├── id (ULID, PK)
├── source_type (Text)
├── source_id (ULID/Text)
├── ai_task (Text)
├── prompt_snapshot (Text)
├── output_json (JSON)
├── confidence (Real)
├── accepted (Boolean)
├── created_records_json (JSON)
├── created_at (DateTime)
└── updated_at (DateTime)
```

---

## 15. `daily_summaries`
Synthesized day-level summaries distinct from the append-only activity log and from reflection-type QiBits.

```text
daily_summaries
├── id (ULID, PK)
├── date (Date)
├── summary_markdown (Text)
├── ai_summary_json (JSON)
├── reviewed (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)
```

## Activity Log vs Daily Summaries

- `activity_log` is append-only operational history of record changes.
- `daily_summaries` are synthesized day-level summaries for review and retrieval.
- QiBit reflections remain user-authored or AI-assisted reflections tied to life events, not replacements for either table above.
