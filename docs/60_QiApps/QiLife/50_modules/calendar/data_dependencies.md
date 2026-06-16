# Calendar: Data Dependencies
*   **Reads**: Queries `actions` where `scheduled_for` is not null, `obligations` with due dates, and `events`.
*   **Writes**: Updates `scheduled_for` or `due_date` on `actions` and `obligations`.
