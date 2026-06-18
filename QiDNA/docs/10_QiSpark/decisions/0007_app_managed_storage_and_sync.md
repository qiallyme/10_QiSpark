# Decision 0007: App-Managed Storage and Sync

## Context
Managing files and syncing manually across folders is brittle and error-prone.

## Decision
QiLife will act as a control center managing its own storage footprint (DB, file vault, exports). Folders will be projections of metadata rather than the source of truth.

## Consequences
- Eliminates manual folder management.
- Requires building storage management and health check features.
- Clear separation between repo (code), private data (DB/files), and exports (Drive/QiNexus).
