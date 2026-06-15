# QiOS DNA

QiOS DNA is the portable master manual for the QiOS ecosystem.

It preserves the origin doctrine, system map, rules, schemas, decisions, receipts, and reconciliation work needed to understand or rebuild the system.

## Core doctrine

- **QiOS** = the overall ecosystem / operating system.
- **QiEOS** = the origin brain / DNA / doctrine layer.
- **QiOS Start** = the cockpit / launcher / front door / docs surface.
- **QiSystem** = rules, schemas, naming, database doctrine, and lifecycle rules.
- **QiServer** = infrastructure, runtime, Docker, Cloudflare, monitoring, and backups.
- **QiCapture** = ingestion, OCR, parsing, embeddings, and pipelines.
- **QiNexus** = storage backbone and file system model.
- **QiApps** = standalone apps, sites, and tools.
- **QiConnect** = external integrations, APIs, workers, and connector surfaces.

## Locked QiLabs structure

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

## Repo rule

This repo mirrors the QiLabs root logic for doctrine and documentation. It is not the actual file-storage root and does not duplicate the full QiNexus `My Drive` bucket system.

Raw imported docs stay under:

```text
00_QiEOS/receipts/raw_imports/
```

Canonical doctrine is promoted only after review.

## Truth rule

```text
Raw imports are evidence.
Canonical docs are law.
Exports are snapshots.
```
