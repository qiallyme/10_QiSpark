# Money: Data Dependencies
*   **Reads/Writes**: Writes to `transactions` and `obligations` tables.
*   **Foreign Keys**: Connects to `people` (via label or link) and `threads` (via `thread_id`).
