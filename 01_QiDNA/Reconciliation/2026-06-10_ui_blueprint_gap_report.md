# UI Blueprint Gap Report

## Accepted Direction

QiAccess and QiLife are separate layers:

- QiAccess is the shell, front door, cockpit, launcher, and documentation surface.
- QiLife is the private life operating app and structured data spine.

V1 is manual-first. AI assistance remains a reviewable draft.

## V1 Workflow Scope

```text
Capture
  -> Inbox/Triage
  -> QiBit Review
  -> Approve or Edit
  -> Action, Document Link, Person Link, or Other Structured Record
  -> Timeline Projection
  -> Daily Summary
```

## Existing Evidence

Current module documents describe QiBits, Inbox, Timeline, Actions indirectly, Documents, People, and AI review behavior. QiAccess has a seven-root navigation concept, and QiLife has a Personal LifeDesk model.

## Blueprint Gaps

### Application Boundaries

- exact handoff from QiAccess to QiLife
- authentication and session ownership
- deep-link behavior
- offline and unavailable-service behavior

### Routes and Screens

No approved route catalog exists for:

- capture
- inbox
- QiBit detail and review
- timeline
- actions and action detail
- documents and evidence linking
- people and entity detail
- daily summary
- settings and system status

### Interaction Contracts

Missing approved behavior includes:

- create, edit, approve, reject, archive, restore, and delete
- validation and conflict handling
- loading, empty, error, retry, and offline states
- unsaved changes and optimistic updates
- keyboard and mobile behavior
- accessibility requirements
- confirmation requirements for high-impact actions

### Data Mapping

Every screen still needs:

- entities and fields read
- mutations performed
- API or repository method
- permission and visibility rule
- timeline and activity-log effect
- acceptance criteria

## Recommended V1 Screen Order

1. Global capture entry.
2. Inbox list.
3. QiBit review workspace.
4. Actions list and detail.
5. Timeline.
6. Documents and evidence linker.
7. People and entity detail.
8. Daily summary.

## Exit Criteria

UI implementation may continue only after the route catalog, screen inventory, workflow state machines, entity mappings, and acceptance criteria are approved.
