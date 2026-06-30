# Actions: Data Dependencies
*   **Reads/Writes**: Writes to `actions` and `action_steps` tables.
*   **Foreign Keys**: Relates to `qibits` via `source_qibit_id`, and `threads` via `thread_id`.
*   **Links**: Integrates with `people`, `money`, and `documents` tables via the central `links` schema.
