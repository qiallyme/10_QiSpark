# QiLife App Flow and Screens

## Main System Flow

```text
REAL LIFE
  ↓
What Happened?
  ↓
QiBit Capture
  ↓
Triage / Interpret
  ↓
Bucket + Thread + People + Meaning
  ↓
Action Required?
  ├── No → Save as Knowledge / Log / Reference
  └── Yes → Create Action → Add Steps → Slot in Time
  ↓
Work / Waiting / Done
  ↓
Resolution
  ↓
Reflection
  ↓
Retrieval through Timeline / Search / AI
```

## App Shell

```text
┌────────────────────────────────────────────────────────────────────┐
│ Top Bar: Search | Quick Capture | Ask QiLife | Notifications      │
├───────────────┬───────────────────────────────────┬────────────────┤
│ Left Nav      │ Center Workspace                  │ Right Panel    │
│               │                                   │ Context Dock   │
│ - Today       │ Selected View                     │ - Knowledge    │
│ - Timeline    │                                   │ - Related bits │
│ - Inbox       │                                   │ - People       │
│ - Threads     │                                   │ - Docs         │
│ - Actions     │                                   │ - Money        │
│ - Calendar    │                                   │ - AI summary   │
│ - People      │                                   │ - Reflection   │
│ - Money       │                                   │                │
│ - Knowledge   │                                   │                │
│ - Documents   │                                   │                │
│ - Ask QiLife  │                                   │                │
└───────────────┴───────────────────────────────────┴────────────────┘
```

## Today

Purpose: command center.

Sections:

```text
Today
├── Quick Capture
├── AI Focus Summary
├── Due / Scheduled Actions
├── Open Loops
├── Waiting On
├── Today's QiBits
├── Money Today
├── People Touched Today
├── Thread Updates
└── Reflection Prompt
```

Question answered:

**What matters right now?**

## Timeline

Purpose: chronological truth.

Sections:

```text
Timeline
├── Filter Bar
│   ├── Date
│   ├── Bucket
│   ├── Thread
│   ├── Person
│   ├── Type
│   └── Status
├── Timeline Feed
│   ├── QiBit cards
│   ├── Actions
│   ├── Transactions
│   ├── Notes
│   ├── Documents
│   └── Resolutions
└── Timeline Detail Drawer
```

Question answered:

**What happened?**

## Inbox

Purpose: chaos catcher.

Sections:

```text
Inbox
├── Quick capture input
├── Voice / text / file import placeholder
├── Unprocessed QiBits
├── AI Triage Suggestions placeholder
└── Bulk Process / Review
```

Question answered:

**What have I not processed yet?**

## Threads

Purpose: ongoing cases/projects/storylines.

Sections:

```text
Threads
├── Thread List
├── Thread Status
├── Related QiBits
├── Related Actions
├── Related People
├── Related Money
├── Related Documents
├── AI Summary
└── Context Dock
```

Question answered:

**What is going on with this whole situation?**

## Actions

Purpose: execution/task ledger.

Sections:

```text
Actions
├── Today
├── Next
├── Waiting
├── Scheduled
├── Done
├── By Bucket
├── By Thread
├── By Person
└── By Context
```

Question answered:

**What do I need to do?**

## Calendar

Purpose: time placement.

Sections:

```text
Calendar
├── Day view
├── Week view
├── Month view
├── Scheduled actions
├── Events
├── Time blocks / timetables
└── Map-linked errands placeholder
```

Question answered:

**When does this happen?**

## People

Purpose: lightweight context for humans/entities.

Sections:

```text
People
├── Person list
└── Person detail
    ├── Notes
    ├── Related QiBits
    ├── Threads
    ├── Actions
    ├── Money
    ├── Documents
    └── Activity log
```

Question answered:

**Who is involved and what is the history?**

## Money

Purpose: transactions and obligations.

Sections:

```text
Money
├── Transactions
├── Obligations
├── Who owes me
├── Who I owe
├── Budget buckets
├── Recurring items
└── Money-related threads
```

Question answered:

**What moved, what is owed, and what is unresolved?**

## Knowledge

Purpose: contextual knowledge, not separate wiki-land.

Sections:

```text
Knowledge
├── Global knowledge items
├── Bucket knowledge
├── Thread knowledge
├── Rules / procedures / notes
├── Search
└── Linked contextual usage
```

Question answered:

**What do I know that matters here?**

## Ask QiLife

Purpose: AI-connected retrieval and guidance.

Sections:

```text
Ask QiLife
├── Ask anything box
├── Suggested prompts
├── AI answer
├── Supporting records
├── Suggested next actions
└── Save answer as note / knowledge / action
```

Question answered:

**Help me cut through the noise.**
