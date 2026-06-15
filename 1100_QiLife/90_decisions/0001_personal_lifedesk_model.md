# ADR 0001: Personal LifeDesk Model

## Status
Accepted

---

## Context
Cody's daily life operations (LifeOps) involve tasks, legal issues, financial obligations, documentation, and relationships. Managing these using generic tools (Trello, standard todo apps, spreadsheets) creates fragmentation and cognitive overload. There is no unified metaphor that brings these elements together in a way that respects their interconnected nature (e.g., how a financial loan relates to a specific person and a legal dispute).

---

## Decision
We will standardize the entire application architecture on the **Personal LifeDesk** model. Under this model:
*   The application behaves like an IT/customer helpdesk console.
*   **Cody** is the sole "agent" (the one resolving items) and the primary "customer" (the one whose life is being managed).
*   All other individuals, agencies, and vendors are treated as external requesters/contacts.
*   The data model maps exactly to helpdesk concepts:
    *   Ticket = **QiBit**
    *   Queue/Department = **Bucket**
    *   Case/Project = **Thread**
    *   Work Order = **Action**
    *   Subtask = **Step**
    *   Sidebar widget = **Context Dock**

---

## Consequences
*   **Simplicity**: The backend database and routing are simplified. There is no need for complex multi-tenant row-level security or multi-user permission roles in V1.
*   **Strict Vocabulary**: Developers and AI agents must strictly use the terms: QiLife, QiBit, Personal LifeDesk, Timeline, Bucket, Thread, Action, Step, Context Dock, and Ask QiLife.
*   **Narrow Scope**: We will not build complex Customer Relationship Management (CRM) sales pipelines or client portals.
