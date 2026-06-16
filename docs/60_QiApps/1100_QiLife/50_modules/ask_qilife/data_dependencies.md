# Ask QiLife: Data Dependencies

- **Reads**: all primary tables plus `links`, `activity_log`, `ai_outputs`, and `daily_summaries` as needed.
- **Writes**:
  - `ai_outputs` for staged query snapshots or suggestions
  - optionally `actions`
  - optionally `knowledge_items`
  - optionally `qibits` of type `note` or `reflection`

Ask QiLife should not depend on a separate `notes` table.
