## Overview

GINA Desktop is a lightweight standalone desktop assistant for the QiOS ecosystem.

Primary goals:

* Always-on-top floating assistant
* Voice or text input
* Coherent retrieval from Supabase
* Read/write/update structured records
* ADHD-friendly low-friction UX
* Fast local-feeling interaction
* Minimal dependencies on full QiOS infrastructure

This is intentionally a **thin client MVP**, not the full orchestration stack.

---


## MVP Requirements

GINA Desktop must:

* Float above other windows
* Accept typed or spoken input
* Retrieve relevant context from Supabase
* Generate coherent responses using LLM context injection
* Save/update notes and memory objects
* Operate independently of the full QiOS backend

---


## MVP Architecture

```text
┌────────────────────┐
│   GINA Desktop     │
│  (Tauri + React)   │
└─────────┬──────────┘
          │
          ├── Supabase-js
          │      ├── semantic_profile
          │      ├── gina_journal
          │      └── future tables
          │
          └── OpenAI API
                 └── Chat Completion
```

---


| Layer         | Technology               |
| ------------- | ------------------------ |
| Desktop Shell | Tauri                    |
| Frontend      | React + TypeScript       |
| Build Tool    | Vite                     |
| Database      | Supabase                 |
| AI            | OpenAI                   |
| STT           | Web Speech API (initial) |
| Styling       | TailwindCSS              |
| State         | React state initially    |
| Packaging     | Tauri Build              |

---


## Recommended Location

```text
QiLabs/
└── apps/
    └── gina_desktop/
```

---

## Folder Structure

```text
gina_desktop/
├── package.json
├── vite.config.ts
├── tauri.conf.json
├── .env.local
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── styles/
│   ├── lib/
│   │   ├── supabaseClient.ts
│   │   ├── openaiClient.ts
│   │   ├── askGina.ts
│   │   ├── speech.ts
│   │   └── ginaPrompt.ts
│   ├── components/
│   │   ├── FloatingShell.tsx
│   │   ├── MicButton.tsx
│   │   ├── MessageList.tsx
│   │   ├── InputBar.tsx
│   │   └── SettingsPanel.tsx
│   └── types/
│       └── index.ts
└── src-tauri/
```

---


## `.env.local`

```env
VITE_SUPABASE_URL=
VITE_SUPABASE_SERVICE_KEY=
VITE_OPENAI_API_KEY=
```

---


## Required Tables

### semantic_profile

Used for contextual retrieval.

Minimum recommended columns:

```sql
id uuid primary key
title text
chunk_index integer
content text
summary text
tags text[]
created_at timestamptz
updated_at timestamptz
```

---

### gina_journal

Used for assistant-created notes.

```sql
create table if not exists gina_journal (
    id uuid primary key default gen_random_uuid(),
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    author text,
    title text,
    body text,
    tags text[]
);
```

---


## Flow

```text
User Input
    ↓
Speech-to-Text
    ↓
Query Supabase
    ↓
Inject Context into Prompt
    ↓
OpenAI Completion
    ↓
Display Response
    ↓
Optional Save to Supabase
```

---


## Initial Retrieval Strategy

MVP uses text similarity:

```ts
.ilike('content', `%${query}%`)
```

This is temporary.

---

## Future Upgrade

Replace with:

* pgvector
* embeddings
* semantic ranking
* graph retrieval
* hybrid search

---


## Structure

```text
SYSTEM:
GINA personality + operational rules

CONTEXT:
Relevant semantic_profile rows

USER:
Actual user message
```

---

## Context Injection Rules

* Limit to ~10 chunks
* Truncate oversized context
* Preserve source attribution
* Prefer recent records
* Avoid duplicate chunks

---


## Allowed Operations (MVP)

| Operation             | Allowed |
| --------------------- | ------- |
| Read semantic_profile | YES     |
| Create journal notes  | YES     |
| Update journal notes  | YES     |
| Delete journal notes  | YES     |
| Arbitrary SQL         | NO      |
| Schema modification   | NO      |

---


## IMPORTANT

This is currently a trusted local desktop application.

The MVP may temporarily use:

```env
VITE_SUPABASE_SERVICE_KEY
```

This is acceptable ONLY if:

* app is local-only
* not publicly distributed
* not browser-hosted

---

## Future Security Upgrade

Later versions should:

* proxy through local_core
* use signed auth
* use RLS
* use scoped service accounts
* remove browser-visible keys

---


## UX Priorities

### MUST HAVE

* Extremely low friction
* Minimal clicks
* Floating utility feel
* Fast perceived response
* Keyboard-first
* ADHD-friendly
* Persistent availability

---

## Avoid

* Modal overload
* Settings clutter
* Complex navigation
* Multi-window workflows
* Excessive animations

---


## Required

| Behavior      | Status   |
| ------------- | -------- |
| Always-on-top | REQUIRED |
| Frameless     | REQUIRED |
| Resizable     | YES      |
| Transparent   | OPTIONAL |
| Global hotkey | FUTURE   |
| Tray icon     | FUTURE   |

---


## MVP Choice

Use browser-native speech recognition:

```ts
window.SpeechRecognition
window.webkitSpeechRecognition
```

Advantages:

* fast
* free
* easy

Limitations:

* browser dependent
* inconsistent quality
* internet-dependent

---

## Future Upgrade Path

Possible replacements:

| Engine          | Notes               |
| --------------- | ------------------- |
| Whisper.cpp     | Strong local option |
| faster-whisper  | Excellent           |
| Deepgram        | Cloud               |
| OpenAI realtime | Future possibility  |

---


## Phase 1 — Current MVP

```text
Desktop → Supabase/OpenAI directly
```

---

## Phase 2 — Local Core Gateway

```text
Desktop → local_core → Supabase/OpenAI
```

Benefits:

* central auth
* unified orchestration
* tool routing
* memory control
* logging
* caching

---

## Phase 3 — Full QiOS Agent

```text
Desktop
    ↓
Orchestrator
    ↓
Workers
    ↓
RAG + Graph + Memory
```

---


## MVP Logging

Create:

```text
logs/
```

Store:

* prompt logs
* errors
* retrieval failures
* response latency
* Supabase errors

---


## Build Order

### Phase 1

* Floating window
* Text input
* Supabase retrieval
* OpenAI responses

### Phase 2

* Speech input
* Save notes
* Journal browsing

### Phase 3

* Semantic retrieval
* Embeddings
* Graph memory

### Phase 4

* Tool calling
* Scheduling
* Calendar
* Automation

---


## Development

```bash
npm install
npm run tauri dev
```

---

## Build

```bash
npm run tauri build
```

---


## Expected Limitations

| Limitation               | Reason                 |
| ------------------------ | ---------------------- |
| Weak retrieval           | No embeddings yet      |
| Context overflow         | Simple chunk injection |
| No memory hierarchy      | MVP only               |
| No agent tools           | Deferred               |
| No auth isolation        | Trusted local app      |
| STT quality inconsistent | Browser API            |

---


GINA Desktop MVP succeeds if:

* Cody can click and ask questions quickly
* GINA can retrieve coherent Supabase context
* GINA can save/update notes reliably
* Interaction feels immediate and low-friction
* Daily usage replaces scattered note-taking

Not success:

* Full AGI orchestration
* Perfect memory graph
* Multi-agent ecosystem
* Enterprise security
* Autonomous workflows

Those come later.

---


This app is not the final architecture.

This is a stabilization layer.

The real purpose is:

> give immediate operational relief and restore cognitive continuity.

That matters more right now than perfect architecture.

(No sub-items found)

(No sub-items found)
