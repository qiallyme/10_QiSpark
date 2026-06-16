# QiLife Module Map

## Module List

```text
QiLife Modules
├── App Shell
├── Quick Capture
├── QiBits
├── Timeline
├── Inbox
├── Buckets
├── Threads
├── Actions
├── Calendar
├── People
├── Money
├── Knowledge
├── Documents
├── Context Dock
├── Ask QiLife
├── Settings/About
└── Import/Export
```

## App Shell

Responsibilities:

- global layout
- left navigation
- top search/capture
- center workspace
- Context Dock
- responsive behavior

## Quick Capture

Responsibilities:

- "What happened?" input
- create raw QiBit
- capture source
- optional voice/file placeholders
- send to AI triage placeholder

## QiBits

Responsibilities:

- central life item/ticket model
- detail page
- lifecycle status
- triage fields
- links to all related records

## Timeline

Responsibilities:

- chronological feed
- daily log
- filters
- timeline detail drawer
- "what happened today" view

## Inbox

Responsibilities:

- unprocessed QiBits
- bulk triage
- AI suggestions placeholder
- route to bucket/thread/action/knowledge

## Buckets

Responsibilities:

- top-level structure
- filter by domain
- match QiNexus hierarchy
- support bucket-specific knowledge

## Threads

Responsibilities:

- ongoing cases/projects/storylines
- group related QiBits/actions/money/docs
- thread status and summary
- Context Dock

## Actions

Responsibilities:

- task ledger
- action detail
- steps/subtasks
- status, priority, due/scheduled fields
- views by today, waiting, scheduled, done, bucket, thread, person

## Calendar

Responsibilities:

- scheduled actions
- events
- day/week/month views
- future slotting
- timetables/routines later

## People

Responsibilities:

- lightweight person/entity records
- relationship context
- linked QiBits/actions/threads/money/docs
- no CRM pipeline

## Money

Responsibilities:

- transactions
- obligations
- who owes me
- who I owe
- budget buckets later
- recurring items later

## Knowledge

Responsibilities:

- central navigable knowledge base
- Markdown display/edit
- bucket/module/entity links
- repo docs importer later
- Context Dock source

## Documents

Responsibilities:

- document metadata
- file path/source tracking
- link docs to QiBits/threads/actions/people/money
- no full OCR in v1

## Context Dock

Responsibilities:

- show side-by-side knowledge/context
- related QiBits
- related actions
- people
- docs
- money
- AI summary
- reflection prompts

## Ask QiLife

Responsibilities:

- AI chat/query interface
- retrieval over app data
- suggested actions
- save AI response as record

## Settings/About

Responsibilities:

- app metadata
- source/inspiration notes
- import/export settings
- local data location
- future AI settings

About text should include:

QiLife is Cody's personal local-first LifeOps / Personal LifeDesk system. It is inspired by helpdesk workflows and the visual planning feel of Will Be Done. Will Be Done source: https://github.com/will-be-done/will-be-done
