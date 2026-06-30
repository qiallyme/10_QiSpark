# Gina Core n8n Workflow Specs (v0)

These workflows provide the automation bridge between the Gina Core API and external services like Google Calendar.

## WF-01: `gina_actions_webhook`

**Trigger:** Webhook (POST) `/webhook/gina-actions`
**Source:** Gina Core `POST /capture`

### Payload from Gina Core
```json
{
  "request_id": "QI-000123",
  "actions": [
    {"type":"calendar.upsert", "event_qid":"QI-000125"},
    {"type":"reminder.schedule", "reminder_qids":["QI-000126","QI-000127","QI-000128"]}
  ]
}
```

### Steps

1. **Webhook Node**: Receives the payload.
2. **HTTP Request Node**: `GET Gina Core /event?qid={{ $json.actions[0].event_qid }}` (or query DB directly if n8n has access).
3. **Google Calendar Node**: `Upsert Event`. Use `external_event_id` if present in metadata to update; otherwise create.
4. **HTTP Request Node**: `POST Gina Core /event/external_id` (Record the Google Event ID back to Gina).
5. **Split In Batches**: For each `reminder_qid`:
   - **HTTP Request Node**: `GET Gina Core /reminder?qid={{ $json.reminder_qid }}`.
   - **Wait Node**: Wait until `remind_at`.
   - **Delivery Node**: Send via Push/Email/SMS.
   - **HTTP Request Node**: `POST Gina Core /reminder/mark_sent`.

---

## WF-02: `daily_digest` (Schedule)

**Trigger:** Cron (Daily at 9:00 PM)

1. **HTTP Request Node**: `GET Gina Core /agenda?from=today&to=tomorrow`.
2. **GPT/LLM Node (Optional)**: "Summarize today's achievements and tomorrow's focus."
3. **HTTP Request Node**: `POST Gina Core /capture`.
   - **Payload**: `{ "text": "Daily Digest: ...", "realm_hint": "QiLife", "classification_hint": "system" }`
4. **Email Node**: Send digest to user.

---

## WF-03: `weekly_digest` (Schedule)

**Trigger:** Cron (Sundays at 6:00 PM)

1. **HTTP Request Node**: `GET Gina Core /agenda?from=last_week&to=next_week`.
2. **Email Node**: Send weekly review and preview.
