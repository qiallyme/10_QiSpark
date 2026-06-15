# Codex Reconciliation Brief: QiOS DNA

## Purpose

This document is the merged instruction brief for Codex to reconcile the `_QiOS_DNA` repository without destroying raw imports, losing context, or inventing a new folder doctrine.

Codex should use this as the controlling task document.

---

## 1. Locked System Model

The locked local root structure is:

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
  60_QiApps\
  70_QiConnect\
  packages\
  scripts\
  toolbox\
```

This repo, `_QiOS_DNA`, is the portable GitHub documentation/doctrine version of the QiLabs system brain. It should mirror the locked QiLabs root logic, not a generic documentation hierarchy.

---

## 2. Layer Definitions

Use these definitions as canon:

```text
QiOS        = whole ecosystem / operating system
QiEOS       = origin brain / doctrine / decisions / receipts / system map
QiOS_Start  = cockpit / launcher / front door / docs surface
QiSystem    = rules / schemas / naming / database doctrine / lifecycle rules
QiServer    = infrastructure / Docker / Cloudflare / deploy / monitoring / backups
QiCapture   = ingestion / OCR / parsing / embeddings / pipelines
QiNexus     = storage backbone / workspace model
QiApps      = standalone apps, sites, tools
QiConnect   = integrations / APIs / workers
packages    = shared code, types, utilities, db helpers
scripts     = thin wrappers only
toolbox     = local tools and power utilities
```

Important correction: QiOS is not only the interface. The interface is QiOS_Start. QiOS is the whole operating system/ecosystem.

---

## 3. Current Doctrine Relationships

Use these module relationships:

```text
QiOS
├── 00_QiEOS        master doctrine / DNA / decisions / receipts / map
├── 10_QiOS_Start  front door / cockpit / access dashboard / docs surface
├── 20_QiSystem    rules / naming / schemas / lifecycle / database doctrine
├── 30_QiServer    runtime / infrastructure / deploy / monitoring
├── 40_QiCapture   ingestion / OCR / parsing / embedding / pipelines
├── 50_QiNexus     storage model / My Drive bucket doctrine
├── 60_QiApps      apps including QiLife and QiJourney
├── 70_QiConnect   connectors / integrations / APIs / workers
├── packages       reusable shared code
├── scripts        thin wrappers only
└── toolbox        local utilities and power tools
```

### Active modules

```text
QiAccess Start = lives under 10_QiOS_Start/QiAccess_Start
QiLife         = lives under 60_QiApps/QiLife and is the living data spine
QiJourney      = lives under 60_QiApps/QiJourney and is the interpretation / narrative branch
QiNexus        = storage model lives under 50_QiNexus, actual files live in My Drive elsewhere
QiServer       = runtime layer under 30_QiServer
QiCapture      = ingestion layer under 40_QiCapture
QiConnect      = integration layer under 70_QiConnect
```

---

## 4. Hard Truth Rules

```text
Raw imports are evidence.
Canonical docs are law.
Exports are snapshots.
```

Do not promote raw imported docs to canon without review.

Do not delete raw imported docs.

Do not silently merge conflicting docs.

Do not duplicate the full QiNexus `My Drive` storage bucket tree inside this repo.

Do not invent a new folder hierarchy.

Do not treat old app-specific docs as master doctrine unless the content is promoted into `00_QiEOS` or `20_QiSystem` with review.

---

## 5. QiNexus Bucket Doctrine

QiNexus is the storage/workspace backbone. The actual file buckets are:

```text
50_QiNexus/My Drive/
  00_inbox
  01_workbench
  02_timeline
  03_life
  04_people
  05_business
  06_finance
  07_legal
  08_tech
  09_assets
  10_data
  11_reference
  12_archive
  13_system
```

Do not create duplicate roots inside `My Drive` such as:

```text
20_qinexus
30_qiarchive
40_qisystem
70_qiconnect
```

Those are wrong inside QiNexus storage. They belong to the QiLabs root model, not inside the My Drive bucket tree.

---

## 6. Current Repo Condition

The repo now contains a new locked-structure spine, but it also appears to contain older imported/mirrored folders such as:

```text
01_QiDNA/
60_qiapps/
70_qiconnect/
site/
```

These older folders should be reviewed before moving, renaming, or deleting.

Codex should not bulldoze them.

---

## 7. Target Canonical Repo Structure

The intended canonical roots are:

```text
_QiOS_DNA/
├── README.md
├── docs.json
├── index.mdx
├── 00_QiEOS/
│   ├── doctrine/
│   ├── decisions/
│   ├── receipts/
│   │   └── raw_imports/
│   ├── system_map/
│   ├── reconciliation/
│   └── exports/
├── 10_QiOS_Start/
│   └── QiAccess_Start/
├── 20_QiSystem/
│   ├── rules/
│   ├── schemas/
│   ├── naming/
│   ├── metadata/
│   ├── database_doctrine/
│   ├── lifecycle/
│   └── manifests/
├── 30_QiServer/
├── 40_QiCapture/
├── 50_QiNexus/
│   └── My_Drive_Model/
├── 60_QiApps/
│   ├── QiLife/
│   └── QiJourney/
├── 70_QiConnect/
├── packages/
├── scripts/
├── toolbox/
└── 09_tools/
```

Note: `09_tools/` is acceptable in the repo as a helper/scripts location for repo-maintenance tools, even though local QiLabs has `toolbox` and `scripts`. If desired later, it can be reconciled into `toolbox` or `scripts`, but do not move it now unless the repo convention is explicitly changed.

---

## 8. Source Material to Reconcile

Primary sources already present or expected in repo:

```text
README.md
docs.json
index.mdx
00_QiEOS/**
10_QiOS_Start/**
20_QiSystem/**
30_QiServer/**
40_QiCapture/**
50_QiNexus/**
60_QiApps/**
70_QiConnect/**
01_QiDNA/**
60_qiapps/**
70_qiconnect/**
site/**
```

Source repos that informed this reconciliation:

```text
qiallyme/_QiAccess_Start
qiallyme/qilife
qiallyme/_QiOS_DNA
```

Expected raw import location:

```text
00_QiEOS/receipts/raw_imports/2026-06-09/
```

If raw import folders are elsewhere, do not delete them. Report where they are and recommend a move.

---

## 9. File Classification Rules

Classify each document into one of these groups:

```text
PROMOTE_CANON
KEEP_AS_MODULE_DOC
KEEP_AS_RECEIPT
ARCHIVE_LEGACY
DUPLICATE_CONFLICT
NEEDS_REVIEW
GENERATED_EXPORT
TOOLING
```

### Promote to canon

Promote only when a document clearly defines the whole system, naming, rules, schema, source of truth, or root structure.

Targets:

```text
00_QiEOS/doctrine/
00_QiEOS/decisions/
00_QiEOS/system_map/
20_QiSystem/rules/
20_QiSystem/schemas/
20_QiSystem/naming/
20_QiSystem/metadata/
20_QiSystem/database_doctrine/
20_QiSystem/lifecycle/
20_QiSystem/manifests/
```

### Keep as module doc

If the doc explains one module/app, place or summarize it under:

```text
10_QiOS_Start/QiAccess_Start/
30_QiServer/
40_QiCapture/
50_QiNexus/My_Drive_Model/
60_QiApps/QiLife/
60_QiApps/QiJourney/
70_QiConnect/
```

### Keep as receipt

If it is a raw import, old source snapshot, prior draft, chat-derived doc, or evidence of previous decisions, keep it under:

```text
00_QiEOS/receipts/
```

### Archive legacy

If it is superseded but historically useful, recommend archive location but do not delete.

### Duplicate/conflict

If two docs disagree, do not merge automatically. Flag both and explain the conflict.

---

## 10. Specific Reconciliation Corrections

### QiAccess Start

QiAccess Start is the front door/cockpit/access dashboard/docs surface.

It is not the whole operating system.

If any QiAccess doc says it replaces all QiOS doctrine, rewrite or flag that as outdated. Correct doctrine:

```text
QiAccess Start replaces older dashboard/front-door framing, not QiOS itself.
QiOS DNA / QiEOS remains the master doctrine layer.
```

### QiLife

QiLife is the living operational data spine and AI LifeDesk.

QiLife owns or models:

```text
qibits
buckets
threads
actions
action_steps
people
transactions
obligations
knowledge_items
documents
events
links
activity_log
ai_outputs
daily_summaries
```

Timeline is a projection over timestamped records, not its own truth table.

### QiJourney

QiJourney is interpretation, reflection, narrative, creative synthesis, and meaning-making.

QiJourney outputs are derived unless linked back to canonical records.

### QiNexus

QiNexus storage buckets are not to be duplicated inside the repo as if they are root doctrine folders.

This repo may document the model under:

```text
50_QiNexus/My_Drive_Model/
```

---

## 11. Codex Tasks

### Task A: Generate full file inventory

Run or use:

```bash
python 09_tools/build_qios_chronicle.py
```

This should generate or update:

```text
20_QiSystem/manifests/QiOS_DNA_File_Manifest.md
00_QiEOS/exports/QiOS_DNA_Chronicle.md
```

If the script outputs `.md` while Mintlify expects `.mdx`, do not break the docs site. Either keep `.md` for generated exports or add matching nav entries only when needed.

### Task B: Create reconciliation matrix

Create:

```text
00_QiEOS/reconciliation/2026-06-09_reconciliation_matrix.md
```

For every meaningful doc, include:

```text
path
classification
recommended target
status
notes/conflicts
```

### Task C: Identify outdated folder roots

Create:

```text
00_QiEOS/reconciliation/2026-06-09_folder_drift_report.md
```

Include old/lowercase/non-locked folders and recommended action:

```text
keep
move later
merge later
archive later
delete only after review
```

Do not delete anything in this pass.

### Task D: Promote obvious canonical summaries only

Only promote documents when obvious. If uncertain, leave them in receipts and mark `NEEDS_REVIEW`.

### Task E: Validate Mintlify docs

Check `docs.json` references. Ensure each referenced page exists or create a safe placeholder.

Do not point Mintlify to huge generated raw imports unless intentionally publishing them.

---

## 12. Required Deliverables

Codex should produce or update these files:

```text
20_QiSystem/manifests/QiOS_DNA_File_Manifest.md
00_QiEOS/exports/QiOS_DNA_Chronicle.md
00_QiEOS/reconciliation/2026-06-09_reconciliation_matrix.md
00_QiEOS/reconciliation/2026-06-09_folder_drift_report.md
00_QiEOS/reconciliation/2026-06-09_codex_summary.md
```

Optional if useful:

```text
00_QiEOS/reconciliation/2026-06-09_conflict_log.md
00_QiEOS/reconciliation/2026-06-09_promotion_plan.md
```

---

## 13. Acceptance Criteria

Reconciliation is complete for this pass when:

1. Every readable doc/config file is listed in the manifest.
2. The Chronicle export can be generated without scanning junk folders.
3. Folder drift is reported, not silently changed.
4. Mintlify navigation points only to files that exist.
5. Raw imports remain preserved.
6. Obvious canonical docs are placed in the locked QiLabs structure.
7. Unclear docs are marked `NEEDS_REVIEW` instead of guessed.
8. No full QiNexus `My Drive` bucket tree is duplicated inside `_QiOS_DNA`.
9. QiAccess Start is correctly treated as front door/cockpit, not master doctrine.
10. QiLife is correctly treated as data spine, not the whole OS.
11. QiJourney is correctly treated as derived interpretation/creative layer.

---

## 14. Commit Guidance

Use small commits:

```text
Generate QiOS DNA manifest and chronicle
Add QiOS DNA reconciliation matrix
Add folder drift report
Fix Mintlify navigation references
Promote obvious canonical QiOS docs
```

Avoid one giant mystery commit.

---

## 15. Non-Negotiables

```text
Do not delete raw imports.
Do not delete older folders.
Do not flatten the repo.
Do not invent new root naming.
Do not mix QiNexus storage buckets with QiLabs system roots.
Do not treat generated exports as canonical.
Do not hide conflicts.
```

The job is not to make the repo look clean by force.

The job is to make the repo understandable, auditable, and safe to reconcile.
