---
title: UI Data Contracts v1
slug: ui_contracts_v1
realm: QiVault
type: doc
node: concept
created: 2025-01-27T00:00:00Z
updated: 2025-01-27T00:00:00Z
version: 1.0.0
status: canonical
system: qios
keywords: [ui, api, contracts, json, health, queue, errors, status]
tags: [architecture, ui, api, observability]
context: JSON response shapes for QiNote/QiCockpit UI rendering. Mock-friendly for static JSON development.
sensitivity: internal
classification: system_darkmatter
---

# UI Data Contracts v1

JSON response shapes for QiOS Launcher UI. Build UI with fake JSON first, swap to real endpoints later.

## /health

Overall system health and layer status.

```json
{
  "runtime": "active",
  "last_tick": "2025-01-27T22:13:00Z",
  "layers": {
    "ROT": {
      "state": "green",
      "last": "2025-01-27T22:13:00Z",
      "msg": "ok"
    },
    "DM": {
      "state": "green",
      "last": "2025-01-27T22:13:00Z",
      "msg": "ok"
    },
    "RLM": {
      "state": "orange",
      "last": "2025-01-27T22:13:00Z",
      "msg": "2 realm fixes"
    },
    "FID": {
      "state": "green",
      "last": "2025-01-27T22:13:00Z",
      "msg": "ok"
    },
    "NAM": {
      "state": "green",
      "last": "2025-01-27T22:13:00Z",
      "msg": "ok"
    },
    "MTA": {
      "state": "green",
      "last": "2025-01-27T22:13:00Z",
      "msg": "ok"
    },
    "SEM": {
      "state": "gray",
      "last": null,
      "msg": "idle"
    },
    "HEL": {
      "state": "gray",
      "last": null,
      "msg": "idle"
    }
  }
}
```

**State values**: `green` (healthy), `orange` (degraded/warnings), `red` (blocked/errors), `gray` (idle/not running)

## /queue

Ingestion queue status and counts.

```json
{
  "pending": 142,
  "in_progress": 3,
  "complete": 1234,
  "quarantined": 5,
  "last_ingested": "realms/qivault/kb/foo.md",
  "last_ingested_at": "2025-01-27T22:13:00Z"
}
```

## /errors

Recent errors and warnings by layer.

```json
[
  {
    "ts": "2025-01-27T22:13:00Z",
    "layer": "FID",
    "rule": "FID.020",
    "code": "BAD_EXT",
    "msg": "exe in KB",
    "file": "realms/qivault/kb/suspicious.exe",
    "severity": "warn"
  },
  {
    "ts": "2025-01-27T22:12:45Z",
    "layer": "RLM",
    "rule": "RLM.010",
    "code": "MISSING_SUBTREE",
    "msg": "Missing kb/ folder",
    "file": "realms/qiclients/test/",
    "severity": "block"
  }
]
```

**Severity values**: `info`, `warn`, `block`, `quarantine`

## /workers

Worker health and status.

```json
{
  "orchestrator": {
    "status": "healthy",
    "last_heartbeat": "2025-01-27T22:13:00Z",
    "uptime_seconds": 86400
  },
  "scanner": {
    "status": "healthy",
    "last_heartbeat": "2025-01-27T22:10:00Z",
    "last_scan": "2025-01-27T22:00:00Z",
    "files_scanned": 1234
  },
  "ingestion": {
    "status": "healthy",
    "last_heartbeat": "2025-01-27T22:13:00Z",
    "queue_depth": 142,
    "processing_rate": 5.2
  },
  "embedder": {
    "status": "idle",
    "last_heartbeat": null,
    "pending_chunks": 0
  },
  "router": {
    "status": "idle",
    "last_heartbeat": null,
    "pending_routes": 0
  },
  "linter": {
    "status": "healthy",
    "last_heartbeat": "2025-01-27T22:13:00Z",
    "last_run": "2025-01-27T22:13:00Z",
    "violations": 0
  },
  "healer": {
    "status": "idle",
    "last_heartbeat": null,
    "pending_dedupes": 0
  }
}
```

**Status values**: `healthy`, `degraded`, `down`, `idle`

## /file_history

Recent file lifecycle events.

```json
{
  "events": [
    {
      "id": "uuid-here",
      "file_path": "realms/qivault/kb/foo.md",
      "content_hash": "sha256-hash",
      "event_type": "seen",
      "actor": "scanner",
      "meta": {
        "scan_id": "scan-123"
      },
      "created_at": "2025-01-27T22:13:00Z"
    },
    {
      "id": "uuid-here",
      "file_path": "realms/qivault/kb/foo.md",
      "content_hash": "sha256-hash",
      "event_type": "embedded",
      "actor": "embedder",
      "meta": {
        "chunks": 5,
        "confidence": 0.95
      },
      "created_at": "2025-01-27T22:12:00Z"
    }
  ],
  "total": 1234,
  "page": 1,
  "per_page": 50
}
```

**Event types**: `seen`, `embedded`, `routed`, `renamed`, `moved`, `deduped`, `quarantined`

## /workflow_graph

Live workflow execution graph (for visual rendering).

```json
{
  "nodes": [
    {
      "id": "trigger_scan",
      "type": "trigger",
      "label": "Daily Scan",
      "status": "complete",
      "timestamp": "2025-01-27T22:00:00Z"
    },
    {
      "id": "queue_insert",
      "type": "queue",
      "label": "Ingestion Queue",
      "status": "active",
      "count": 142
    },
    {
      "id": "layer0",
      "type": "layer",
      "label": "ROT: Root Integrity",
      "status": "complete",
      "timestamp": "2025-01-27T22:00:05Z"
    }
  ],
  "edges": [
    {
      "from": "trigger_scan",
      "to": "queue_insert",
      "type": "enqueue"
    },
    {
      "from": "queue_insert",
      "to": "layer0",
      "type": "process"
    }
  ]
}
```

## Notes

- All timestamps are ISO 8601 UTC (`YYYY-MM-DDTHH:mm:ssZ`)
- All file paths are QiOS-relative (e.g., `realms/qivault/kb/foo.md`)
- Mock data can be stored as static JSON files for UI development
- Real endpoints will follow these exact shapes

