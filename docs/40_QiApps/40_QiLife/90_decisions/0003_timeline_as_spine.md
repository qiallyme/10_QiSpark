# ADR 0003: Timeline as the Spine

## Status
Accepted

---

## Context
When reviewing tasks, logs, or transactions, we often lose the surrounding context of *when* things occurred in relation to other events. For example, knowing that a gas bill was paid on May 15 is useful, but seeing it on a visual timeline next to a Lyft driving log and a chat summary from that same day provides immediate explanatory value.

---

## Decision
We will establish the **Timeline** as the spinal core of the **QiLife** interface and data queries.
*   Every record that participates in the timeline must expose either a canonical timestamp field or a deterministic projection rule.
*   The primary interface view is a chronological feed where QiBits, note/reflection-type QiBits, transactions, completed actions, events, and daily summaries can be displayed sequentially.
*   The UI must support unified filtering across all entity types based on temporal queries.

---

## Consequences
*   **Contextual Coherence**: Cody can scroll back to any date and see a comprehensive picture of what happened, who was involved, and what money moved on that specific day.
*   **Projection Rules**: The backend must define which timestamp each entity uses when rendered in the feed.
*   **Interface Unity**: Rather than having isolated dashboard silos, the various modules feed their output into the Timeline.
