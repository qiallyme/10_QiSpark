# ADR 0004: Context Dock Over Wiki

## Status
Accepted

---

## Context
Durable knowledge (such as operating procedures, billing rules, contact directories, and decision logs) is normally stored in a separate, isolated wiki space (like Notion or Wiki.js). This creates friction because Cody must context-switch to find the relevant instructions while working on a task. Consequently, wiki documentation is rarely read or updated, leading to operational errors.

---

## Decision
We will not build or host a separate wiki engine. Instead, we will store knowledge directly inside the **QiLife** database (`knowledge_items`) and expose it through a persistent, collapsible sidebar panel called the **Context Dock**.
*   The Context Dock automatically queries and displays knowledge, linked documents, related people, and prior resolutions relative to the item Cody has open in the center workspace.
*   Knowledge is co-located with action: Cody can read the guide on how to request a check reissue in the Context Dock while checking the status of his Action in the center workspace.

---

## Consequences
*   **Reduced Context Switching**: Cody has all the information needed to complete a task directly on-screen.
*   **Simpler Architecture**: We avoid the overhead of deploying and maintaining a third-party wiki service (e.g., Wiki.js) and trying to synchronize auth states.
*   **Contextual Queries**: Developers must build relation-based database queries that pull records matching active tags, buckets, threads, or people.
