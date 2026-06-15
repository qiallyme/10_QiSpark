# Chronicle QiDNA

Chronicle QiDNA is the portable, status-labeled master manual for the QiOS ecosystem. It preserves current doctrine, architecture, schemas, decisions, evidence, and reconciliation work needed to understand or rebuild the system.

## Canonical Structure

- **QiOS**: the overall ecosystem.
- **QiDNA**: governance and documentation.
- **QiEOS**: doctrine inside `00_QiEOS`.
- **QiAccess**: cockpit, launcher, front door, and documentation surface.
- **QiSystem**: rules, schemas, naming, database doctrine, and lifecycle rules.
- **QiServer**: infrastructure, runtime, networking, monitoring, and backups.
- **QiCapture**: ingestion, OCR, parsing, embeddings, and pipelines.
- **QiNexus**: file, export, reference, and archive storage.
- **QiApp QiLife**: private life operating app and structured-data spine.
- **QiConnect**: external integrations, APIs, workers, and connectors.

```text
C:\QiLabs\
  .github\
  .qios\
  .vscode\
  00_QiEOS\
  10_QiOS_Start\
  20_QiSystem\
  30_QiServer\
  40_QiCapture\
  50_QiNexus\
    My Drive\
  60_QiConnect\
  1000_QiApps\
  1100_QiLife\
  packages\
  scripts\
  toolbox\
```

Older roots such as `00_QiEOS`, `10_QiOS_Start`, and `60_QiApps` are retained as Legacy or Evidence. They cannot override Active documentation.

## Data Authority

- Supabase Postgres is the canonical QiLife structured-data authority.
- QiNexus stores files, exports, references, archives, and backups.
- SQLite is deprecated and limited to legacy, local, or transitional use.
- The canonical schema reference is `20_QiSystem/schemas/QiLife_Data_Spine.mdx`.

## Repository Rule

This repository mirrors the system's ownership boundaries for governance and documentation. It is not the runtime file-storage root and does not duplicate the full QiNexus bucket tree.

Documents are explicitly classified as Active, Legacy, Proposed, Generated, or Evidence. Historical material is preserved, while current authority is kept singular and visible.

## Truth Rule

```text
Runtime facts beat planning notes.
Active canonical docs govern.
Legacy and evidence explain history.
Generated exports are snapshots.
```
