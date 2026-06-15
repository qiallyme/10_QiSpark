---
title: "QiOS Cockpit GUI Development Prompt"
slug: "cockpit_gui_prompt"
realm: QiOS
realm_slug: "qios"
qi_decimal: "1.02.00-DOC"
qid:
type: doc
node: file
keywords: ["prompt", "cursor", "GUI", "cockpit", "dashboard", "development"]
tags: ["prompt", "cursor", "development", "ui"]
context: "Cursor project prompt for building QiOS Cockpit GUI dashboard"
created: 2025-11-25
updated: 2025-11-25
version: "0.1.0"
status: draft
system: qios
naming_strategy: slug_only
sort: 0
related: []
parents: []
children: []
siblings: []
references: []
graph_weight: 5
orbit: inner
entangled: []
summary: "Development prompt for building QiOS Cockpit GUI - a local-first status dashboard for the QiOS worker ecosystem"
sensitivity: internal
classification: system_darkmatter
---

# QiOS Cockpit GUI Development Prompt

You are building the **QiOS Cockpit GUI** (Vite + React).

Everything must align with **QiOS Genesis** and **QiRules v1.1**.

## Goal

A local-first status dashboard that visualizes the QiOS worker ecosystem in real-time.

## Requirements

### API Endpoints

Must call orchestrator endpoints:

- `GET /health` - System health status
- `GET /workflow_graph` - Worker dependency graph
- `GET /queue` - Ingestion queue status
- `GET /errors` - Recent error log
- `GET /file_history` - File processing history
- `GET /workers` - Worker status for all workers

### UI Components

#### WorkerCard Component
Render each worker as a card with:
- **State color mapping:**
  - `green` = running/healthy
  - `orange` = degraded/warning
  - `gray` = stopped/inactive
  - `red` = error/failed
- **Metadata display:**
  - Last heartbeat timestamp
  - Last run timestamp
  - Queue depth
  - Last error message (if any)
  - Worker name and ID

#### WorkflowGraph Component
- Visualize worker dependency graph using `/workflow_graph` response
- Show worker relationships and dependencies
- Color-code by state
- Interactive (hover for details)

#### ErrorsPanel Component
- Display recent errors (last 50 from `/errors`)
- Group by worker or error type
- Show timestamp, error code, message
- Filter/search capability

#### QueuePanel Component
- Show ingestion queue status from `/queue`
- Display: pending, in_progress, complete, quarantined counts
- List recent queue items
- Show processing rate

#### FileHistoryPanel Component
- Display file processing history from `/file_history`
- Show: file path, event type, timestamp, actor
- Pagination support
- Filter by event type or file path

### UX Requirements

- **Minimal friction:** One screen, auto-refresh every 5s, manual refresh button
- **Configurable API base URL:** Default to `http://localhost:8787` for local dev
- **No auth for local dev:** Skip authentication for local development
- **Responsive design:** Works on desktop and tablet
- **Dark theme:** Match QiOS dark aesthetic

## Deliverables

### Project Structure

Create `apps/cockpit/` as Vite React project:

```
apps/cockpit/
  src/
    components/
      WorkerCard.jsx
      WorkflowGraph.jsx
      ErrorsPanel.jsx
      QueuePanel.jsx
      FileHistoryPanel.jsx
    App.jsx
    main.jsx
    config.js
    index.css
  index.html
  package.json
  vite.config.js
  _readme.md
```

### Configuration

Create `src/config.js`:

```javascript
export const DEFAULT_ORCHESTRATOR_URL = 
  import.meta.env.VITE_ORCHESTRATOR_URL || 
  'http://localhost:8787'

export const REFRESH_INTERVAL = 5000 // 5 seconds
```

### README

Create `_readme.md` explaining:
- How to run cockpit + orchestrator together
- Configuration options
- Development workflow
- API endpoint documentation

## Technical Stack

- **Vite** - Build tool and dev server
- **React 18** - UI framework
- **CSS Modules or Tailwind** - Styling (prefer CSS modules for simplicity)
- **Fetch API** - HTTP requests (no axios needed)

## QiOS Compliance

- Follow QiOS naming conventions (lowercase_underscored for files)
- Include front matter in `_readme.md`
- Use semantic versioning
- Follow Layer 0-7 governance rules
- Place in `apps/` root per QiOS ontology

## Success Criteria

- ✅ Dashboard loads and displays all worker status
- ✅ Auto-refreshes every 5 seconds
- ✅ Manual refresh button works
- ✅ All API endpoints integrated
- ✅ Error handling for failed requests
- ✅ Responsive layout
- ✅ Dark theme applied
- ✅ README complete with setup instructions

