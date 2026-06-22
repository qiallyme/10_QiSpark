# Timeline: Data Dependencies

- **Reads**:
  - `qibits`
  - `actions`
  - `transactions`
  - `events`
  - `daily_summaries`
- **Projection rules**:
  - QiBits by `COALESCE(happened_at, captured_at, created_at)`
  - Actions by `completed_at`, else `scheduled_for`, else `created_at`
  - Transactions by `date`
  - Events by `start_time`
  - Daily summaries by `date`
- **Writes**: none directly; Timeline is a read model built from other tables.
