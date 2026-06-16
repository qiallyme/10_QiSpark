# QiLife Master Build Spec

## Working Product Name

**QiLife**

## Operating Model

**Personal LifeDesk**

QiLife is a private, single-agent helpdesk for life. The company is Cody's life. Cody is the agent. Cody is also the primary customer. Everyone else is a related person, vendor, stakeholder, agency, court, client, household member, requester, or external party.

## Product Sentence

QiLife turns life chaos into **QiBits** that can be captured, triaged, routed, acted on, documented, resolved, reflected on, and retrieved with AI.

## Core Unit

### QiBit

A **QiBit** is one captured unit of life data.

A QiBit can become or relate to:

- task
- note
- transaction
- obligation
- calendar event
- document
- knowledge item
- thread update
- reflection
- future reminder
- daily log entry

## Core Pain Points Solved

1. No central task ledger.
2. No central "what happened today" record.
3. No central knowledge base.
4. No central note-taking/capture place.
5. No AI directly connected to the above.
6. Knowledge is separated from tools.
7. Life data is scattered across apps, memory, texts, files, calendars, docs, and panic.

## Core Doctrine

Every important item should either:

1. Start as a QiBit, or
2. Link back to a QiBit.

This preserves provenance:

- Why does this task exist?
- What triggered this obligation?
- Who/what is involved?
- What happened before and after?
- What evidence or knowledge supports this?
- What was resolved?
- What should be retrievable later?

## Lifecycle

A QiBit moves through this lifecycle:

1. Capture — what happened?
2. Bucket — where does it belong?
3. Interpret — what does it mean?
4. Relate — who/what is connected?
5. Slot — when does it matter?
6. Breakdown — how do we act?
7. Enrich — what context matters?
8. Act — what needs doing?
9. Resolve — what happened after action?
10. Reflect — what did we learn?
11. Retrieve — how do we find/use it later?

## Helpdesk Mapping

| Helpdesk Concept | QiLife Concept |
|---|---|
| Ticket | QiBit |
| Queue | Bucket |
| Department | Bucket/domain |
| Case | Thread |
| Task/work order | Action |
| Subtask | Step |
| Customer/requester | Related person/entity |
| Agent | Cody |
| SLA | due date / urgency / consequence |
| Internal note | private note / reflection |
| Knowledge article | contextual knowledge item |
| Resolution | outcome / done log |
| Related tickets | linked QiBits |
| Helpdesk sidebar | Context Dock |

## App Spine

Timeline is the spine.

The core structure is:

QiBit → Timeline → Bucket → Thread → Action → Steps → Context Dock → Resolution → Reflection → Retrieval

## Primary Views

1. Today
2. Timeline
3. Inbox
4. Threads
5. Actions
6. Calendar
7. People
8. Money
9. Knowledge
10. Documents
11. Ask QiLife
12. Settings/About

## Main UX Pattern

QiLife should use an agent-console layout:

- Left: navigation and queues/buckets
- Center: current workspace
- Right: Context Dock
- Top or bottom: persistent "What happened?" quick capture

## Knowledge Doctrine

QiLife should not depend on a separate wiki service for v1.

Knowledge should live inside QiLife and appear next to the tool/item it explains through the **Context Dock**.

Repo docs should be canonical during build and indexed/imported into the in-app knowledge layer later.

Doctrine:

**Write once in Markdown, index everywhere.**

## Build Approach

Build the spine first.

Do not start with:

- multiuser
- public sharing
- bank sync
- calendar sync
- complex permissions
- graph database
- full wiki engine
- full mobile native app
- overbuilt automations

## Initial Stack Recommendation

Frontend:

- React
- Vite
- TypeScript
- Tailwind
- TanStack Router or React Router
- TanStack Query
- Markdown renderer

Backend:

- FastAPI
- SQLite for v1
- SQLModel or SQLAlchemy
- Pydantic schemas
- REST API first

Future:

- Postgres on QiServer
- Docker Compose
- local AI / OpenAI / hybrid AI service
- embeddings and semantic search
- QiNexus Markdown exports
