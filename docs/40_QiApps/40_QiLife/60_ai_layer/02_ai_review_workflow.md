# QiLife AI Review Workflow

To prevent AI hallucinations, model drift, or unintended edits from corrupting Cody's personal ledger, QiLife operates on a strict **Human-in-the-Loop (HITL)** doctrine. The AI proposes; Cody approves or edits.

---

## 1. Core Principles

1.  **No Silent Creation**: The AI service never directly inserts or updates records in primary tables (`actions`, `obligations`, `transactions`, `people`, `threads`) without user intervention.
2.  **Draft / AI Output Staging**: All AI inferences are written to the `ai_outputs` table first. They are displayed in the UI as editable suggestions.
3.  **Explicit Acceptance**: A suggestion only moves to the primary tables when Cody clicks **Accept** (which marks `ai_outputs.accepted = true` and performs the writes) or modifies the values and clicks **Save**.
4.  **Provenance Tracking**: Created items retain a link to their originating `qibit_id` and `ai_output_id` via the `links` table.

---

## 2. The Triage Review Pipeline

The primary review pipeline happens in the **Inbox** during the Triage phase of a QiBit.

```text
  [Raw Capture]
        ↓
   AI Service (Calls interpret_qibit & extract_related_entities)
        ↓
  [Insert into ai_outputs] (State: accepted=false)
        ↓
  [Inbox UI Display] (Show suggested fields side-by-side with original text)
        ├─────────────────────────────┐
        ▼                             ▼
  [Cody clicks Edit]            [Cody clicks Accept]
        ▼                             ▼
   Modifies fields in form      Backend writes direct to primary tables
        └──────────────┬──────────────┘
                       ▼
            [Commit to SQLite]
     - Mark ai_outputs.accepted = true
     - Create records in primary tables
     - Create links for provenance
```

---

## 3. Database State Machine

### The `ai_outputs` Table State
*   `accepted = false` (default): Represents a pending suggestion. It is displayed as a draft card in the inbox or context dock.
*   `accepted = true`: Cody has approved this output. The application logic prevents writing this output to the primary tables again to avoid duplicate creation.

### Provenance Mapping in `links`
When a suggestion is accepted:
*   A link is written: `source_type = 'qibits'`, `source_id = [QiBit ID]`, `target_type = 'actions'`, `target_id = [Created Action ID]`, `relationship = 'created_from'`.
*   If money is extracted: `source_type = 'qibits'`, `source_id = [QiBit ID]`, `target_type = 'obligations'`, `target_id = [Created Obligation ID]`, `relationship = 'created_from'`.

---

## 4. UI Representation of AI State

The frontend must visually distinguish between three categories of data:
1.  **Confirmed Data (User Entered/Approved)**: Standard color coding, fully indexed.
2.  **Suggested Data (AI Drafts)**:
    *   Displayed with dashed borders or light purple background.
    *   Accompanied by a confidence rating indicator (e.g., `Confidence: 85%`).
    *   Features a quick-action checkmark (Accept) and a pencil icon (Edit).
3.  **Contradictions / Flags**: If an AI background process detects an unresolved open loop or a duplicate entry, it places a red warning icon in the Context Dock under "AI Flags".
