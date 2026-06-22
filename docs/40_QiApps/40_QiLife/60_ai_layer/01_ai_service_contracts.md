# QiLife AI Service Contracts

This document defines the v1 AI service interfaces. The contracts must align with the canonical SQLite schema so that mocked AI behavior can graduate cleanly into live AI later.

## Contract Rules

- Use ULID strings for record identifiers.
- Monetary values returned for structured writes should include `amount_cents`.
- AI suggestions write to `ai_outputs` first and only reach primary tables after approval.
- AI can suggest note/reflection content as QiBit payloads; there are no dedicated `notes` or `reflections` tables in v1.

## 1. QiBit Interpretation

### `interpret_qibit`

Request:

```json
{
  "raw_capture": "string (max 1000 chars)",
  "captured_at": "datetime (ISO 8601)"
}
```

Response:

```json
{
  "title": "string",
  "summary": "string",
  "meaning": "string",
  "suggested_qibit_type": "string",
  "suggested_bucket_code": "string",
  "importance": "string",
  "priority": "string",
  "emotional_load": "string",
  "action_required": true,
  "suggested_action": "string | null",
  "suggested_future_slot": "string (today | this_week | scheduled | waiting_on | someday | knowledge_base)"
}
```

### `extract_related_entities`

Request:

```json
{
  "qibit_id": "string (ULID)",
  "content": "string"
}
```

Response:

```json
{
  "people": [
    {
      "display_name": "string",
      "relationship_hint": "string | null"
    }
  ],
  "organizations": ["string"],
  "financials": [
    {
      "amount_cents": 4000,
      "currency": "USD",
      "type": "obligation"
    }
  ],
  "dates": [
    {
      "extracted_date": "2026-05-29",
      "label": "occurred_date"
    }
  ]
}
```

## 2. Action Generation

### `generate_action_steps`

Request:

```json
{
  "action_id": "string (ULID)",
  "action_title": "string",
  "action_description": "string"
}
```

Response:

```json
{
  "steps": [
    {
      "title": "string",
      "description": "string | null",
      "sort_order": 1
    }
  ]
}
```

## 3. Financial Extraction

### `extract_transaction_from_text`

Response:

```json
{
  "date": "2026-05-29",
  "amount_cents": 6523,
  "currency": "USD",
  "direction": "out",
  "from_label": "Cody",
  "to_label": "Shell Gas Station",
  "category": "gas",
  "notes": "string | null"
}
```

### `extract_obligation_from_text`

Response:

```json
{
  "owed_by_label": "Zai",
  "owed_to_label": "Cody",
  "obligation_type": "money",
  "amount_cents": 4000,
  "currency": "USD",
  "reason": "Gas payment share for Lyft driving run",
  "due_date": "2026-05-30 | null"
}
```

## 4. Ask QiLife

### `answer_life_query`

Request:

```json
{
  "query": "string",
  "active_bucket_code": "string | null",
  "active_thread_id": "string | null"
}
```

Response:

```json
{
  "answer": "string (Markdown)",
  "confidence": 0.86,
  "supporting_records": [
    {
      "record_type": "obligations",
      "record_id": "01JWNZ4M5N6P7Q8R9S0T1U2V3A",
      "relevance_reason": "Open money obligation for Zai"
    }
  ],
  "suggested_actions": ["Send a follow-up message to Zai"],
  "related_people_ids": ["01JWNX2D3Q4A5B6C7D8E9F0G1J"],
  "related_thread_ids": ["01JWNX8F6R7S8T9U0V1W2X3Y4A"]
}
```

Saving an answer can create:

- a QiBit of type `note`
- a QiBit of type `reflection`
- an action
- a knowledge item

It should not create a record in a non-existent `notes` table.

## 5. Reflection Prompt

### `generate_reflection_prompt`

Request:

```json
{
  "date": "2026-05-29",
  "completed_actions_count": 2,
  "open_loops_count": 3,
  "daily_summary": "string"
}
```

Response:

```json
{
  "reflection_prompt": "string",
  "cognitive_load_estimate": "high"
}
```
