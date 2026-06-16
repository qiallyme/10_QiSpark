# ADR 0002: QiBit as the Atomic Unit

## Status
Accepted

---

## Context
User inputs vary drastically in format (a text message, a scan of a legal notice, a voice memo, a transaction log). Attempting to immediately force these into rigid schemas (like forcing a vague text "Zai gas $40" directly into a double-entry accounting ledger or a calendar deadline) leads to capture friction. People stop capturing items if the entry form is too demanding.

---

## Decision
We will establish the **QiBit** as the atomic unit of all data within **QiLife**.
*   Every capture action creates a QiBit first.
*   A QiBit contains a `raw_capture` field to preserve the exact raw input text, and metadata tracking when and how it was captured.
*   All structured operational records (Actions, Obligations, Transactions, Documents) must link back to a parent QiBit to preserve historical provenance.

---

## Consequences
*   **Zero-Friction Ingestion**: Cody can capture thoughts or logs in a single input field.
*   **Staged Structure**: Separation of capture from organization. AI or manual triage processes run asynchronously or semi-synchronously to unpack the QiBit into structured tables without blocking ingestion.
*   **Provenance Retention**: Clicking on any Action or Transaction allows Cody to trace it back to the exact raw text or situation that triggered it.
