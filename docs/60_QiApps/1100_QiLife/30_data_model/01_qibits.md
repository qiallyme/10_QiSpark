# QiBits Data Model

QiBits are the atomic capture records in QiLife. They preserve the original life input first, then accumulate structure and interpretation over time.

## Canonical Fields

- `id`: ULID
- `title`: short summary line
- `raw_capture`: original captured text or normalized import payload
- `summary`: cleaned summary of the capture
- `meaning`: interpreted significance
- `qibit_type`: canonical type
- `bucket_code`: two- or three-digit bucket code
- `thread_id`: optional thread ULID
- `status`: canonical lifecycle status
- `priority`: consequence-based priority
- `importance`: overall significance
- `emotional_load`: low / normal / high
- `action_required`: boolean
- `suggested_action`: nullable suggestion field
- `future_slot`: routing/scheduling intent
- `happened_at`: when the underlying event happened, if known
- `captured_at`: when Cody or an importer captured the item
- `resolved_at`: nullable resolution timestamp
- `retrieval_summary`: optional retrieval-facing synopsis
- `reflection`: optional attached reflection text
- `tags_json`: flexible retrieval tags
- `metadata_json`: importer or UI metadata
- `created_at`
- `updated_at`
- `archived_at`
- `deleted_at`

## Canonical QiBit Types

```text
event
note
message
call
problem
idea
decision
task_seed
transaction_seed
obligation_seed
document_seed
appointment
receipt
knowledge
reflection
other
```

## Canonical QiBit Statuses

```text
new
triaged
open
in_progress
waiting_on
scheduled
resolved
closed
reference
ignored
archived
```

## Provenance Rule

QiBits are the source-of-truth capture layer. Downstream records such as actions, obligations, transactions, documents, or events should link back to a QiBit directly through a foreign key when the table supports it, or through `links` when the relationship is many-to-many or indirect.

## Timeline Rule

QiBits appear on the Timeline using `COALESCE(happened_at, captured_at, created_at)`.
