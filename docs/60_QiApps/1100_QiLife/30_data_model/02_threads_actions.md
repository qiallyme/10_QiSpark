# Threads & Actions Data Model

## Thread

Threads represent cases, projects, storylines, or ongoing situations.

Canonical fields:

- `id`: ULID
- `title`
- `description`
- `bucket_code`
- `status`
- `priority`
- `next_action`
- `due_date`
- `started_at`
- `closed_at`
- `tags_json`
- `metadata_json`
- `created_at`
- `updated_at`
- `archived_at`
- `deleted_at`

Canonical statuses:

```text
open
active
waiting_on
resolved
closed
archived
```

## Action

Actions are work orders derived from QiBits or created directly during triage/planning.

Canonical fields:

- `id`: ULID
- `title`
- `description`
- `source_qibit_id`
- `bucket_code`
- `thread_id`
- `status`
- `priority`
- `energy`
- `context`
- `due_date`
- `scheduled_for`
- `completed_at`
- `resolution_note`
- `tags_json`
- `metadata_json`
- `created_at`
- `updated_at`
- `archived_at`
- `deleted_at`

Canonical statuses:

```text
open
in_progress
waiting_on
scheduled
completed
cancelled
archived
```

## Step

Action steps are structured subtasks.

Canonical fields:

- `id`: ULID
- `action_id`
- `title`
- `description`
- `status`
- `sort_order`
- `completed_at`
- `created_at`
- `updated_at`

## Timeline Rule

Actions are projected into Timeline using:

1. `completed_at` when the action is finished
2. `scheduled_for` when it is scheduled but not completed
3. `created_at` as a fallback
