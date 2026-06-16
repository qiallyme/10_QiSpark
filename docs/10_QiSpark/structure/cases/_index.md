## Case Domain Overview

Cases are the core operational unit in `qicase`. A case represents a bounded legal or operational matter with a defined lifecycle.

## Case Lifecycle

```
open → active → review → resolved → closed → archived
```

## Case Structure

| Object | Description |
|---|---|
| `cases` | The top-level case record |
| `phases` | Sequential or parallel phases within a case |
| `issues` | Discrete issues or items within a phase |
| `deadlines` | Time-bound milestones linked to phases or events |
| `case_documents` | Archive-linked documents associated with a case |
| `document_issues` | Issues linked to specific documents |

## Case Object (Key Fields)

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | Canonical ID |
| `tenant_id` | uuid | FK to `qione.tenants` |
| `case_number` | text | Human-readable case identifier |
| `client_id` | uuid | FK to client record |
| `status` | text | Case lifecycle state |
| `case_type` | text | civil, administrative, etc. |
| `opened_at` | timestamptz | When case was opened |

## Case Rules

* Cases must always belong to a tenant and a client
* Case documents must always reference an `archive_id` from `qiarchive`
* Deadlines linked to `qichronicle` events must have a valid `chronicle_event_id`
* Case phases must be sequential within a case or explicitly marked as parallel
* No case may have documents without a registered archive record

(No sub-items found)
