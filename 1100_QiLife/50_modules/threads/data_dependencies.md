# Threads: Data Dependencies
*   **Reads/Writes**: Writes to the `threads` table.
*   **Foreign Keys**: Actions, QiBits, and Transactions possess a nullable `thread_id` pointing directly to this table.
