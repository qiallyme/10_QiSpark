# QiLife Information Architecture

## Core Structure

QiLife is organized around QiBits, timeline, buckets, threads, actions, context, knowledge, and AI retrieval.

## Main Objects

```text
QiLife Data
├── QiBits
├── Buckets
├── Threads
├── Actions
├── Action Steps
├── People
├── Transactions
├── Obligations
├── Knowledge Items
├── Documents
├── Events
├── Links
├── Activity Log
├── AI Outputs
└── Daily Summaries
```

`note` and `reflection` are QiBit types in v1, not separate top-level tables.

## Buckets

Buckets match the real QiNexus/QiAccess folder hierarchy.

| Code | Bucket | Purpose |
|---:|---|---|
| 00 | Inbox | raw capture / unprocessed QiBits |
| 10 | Workbench | active staging and current work |
| 20 | Timeline | chronological life ledger bucket for pure timeline-native records |
| 30 | Life | personal life, routines, household, identity |
| 40 | People | people, relationships, entities |
| 50 | Business | freelance, QiAlly, ventures |
| 60 | Finance | money, transactions, obligations, accounts |
| 70 | Legal | court, filings, evidence, housing, disputes |
| 80 | Tech | QiServer, apps, repos, tools, automation |
| 90 | Assets | media, designs, brand, reusable resources |
| 100 | Data | schemas, exports, structured datasets |
| 110 | Reference | durable knowledge, rules, templates |
| 900 | Archive | inactive/historical retained material |
| 990 | System | app config, indexes, manifests, build docs |

## Operational Views vs Structural Views

### Operational Views

These are for daily use:

```text
Today
Timeline
Inbox
Threads
Actions
Calendar
People
Money
Knowledge
Documents
Ask QiLife
```

### Structural Views

These are for organizing and filtering:

```text
00 Inbox
10 Workbench
20 Timeline
30 Life
40 People
50 Business
60 Finance
70 Legal
80 Tech
90 Assets
100 Data
110 Reference
900 Archive
990 System
```

## Timeline

Timeline is:

1. A global chronological view assembled from multiple tables.
2. A bucket for records whose primary home is the chronology itself.

Every QiBit appears on the timeline through projection, even if its primary bucket is Finance, Legal, People, Tech, or another domain.

There is no dedicated `timeline_entries` table in v1.

## Threads

Threads are ongoing cases, projects, storylines, or situations.

Examples:

- Surplus Check Recovery
- Lyft Income Sprint
- QiLife Build
- Family Hub
- QiFinance Intake
- Jeep / Vehicle
- Zai Lease
- Household Ops
- QiServer Cleanup

Threads are broader than projects. A thread can be:

- case
- project
- issue
- relationship storyline
- ongoing obligation
- recurring situation

Canonical thread statuses for v1:

```text
open
active
waiting_on
resolved
closed
archived
```

## Links

Links create exact relationships between records.

Examples:

- QiBit created Action
- Knowledge Item explains Thread
- Document supports QiBit
- Person is involved in Action
- Transaction resolves Obligation

Tags are for loose retrieval. Links are for known structure.

## Tags

Tags support flexible search and AI retrieval.

Examples:

- gas
- lyft
- surplus-check
- court
- family-ops
- qiserver
- receipt
- waiting-on

Tags should not replace links.
