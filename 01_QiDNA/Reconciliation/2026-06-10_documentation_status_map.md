# Documentation Status Map

## Purpose

This map applies a status to every Markdown and MDX document without moving or deleting legacy evidence. The generated site uses the same deterministic rules and displays the status beside every document.

## Status Definitions

| Status | Meaning | Authority |
|---|---|---|
| Active | Accepted current doctrine, domain documentation, or architecture decision | Governs current work |
| Legacy | Superseded location or vocabulary retained for review | Cannot override Active docs |
| Proposed | Design material not yet approved as implementation contract | Input to review only |
| Generated | Build output, manifest, report, or derived rendering | Never canonical by itself |
| Evidence | Historical decision, receipt, reconciliation record, or planning evidence | Supports decisions but does not govern by itself |

## Canonical Active Roots

```text
01_QiDNA/
10_QiAccess/
20_QiSystem/
30_QiServer/
40_QiCapture/
50_QiNexus/
60_QiApp_QiLife/
70_QiConnect/
```

Documents under these roots default to Active except generated reports, manifests, and reconciliation evidence.

## Legacy Rules

Documents under these roots are Legacy unless promoted through review:

```text
00_QiEOS/
10_QiOS_Start/
20_qinexus/
30_qiarchive/
50_qiserver/
60_QiApps/
60_qiapps/
70_qiconnect/
```

Within `00_QiEOS`, exports are Generated and reconciliation records are Evidence.

## Proposed Rules

The current design collections below are Proposed because they have not yet been reconciled into approved implementation contracts:

```text
50_modules/
60_ai_layer/
70_deployment/
80_prompts/
```

## Generated Rules

- `20_QiSystem/50_Generated_Reports/`
- `20_QiSystem/manifests/`
- `00_QiEOS/exports/`
- `site/_site.md`
- `site/index.html` is generated output and is not a source document.

## Evidence Rules

- Dated reports in `01_QiDNA/Reconciliation/`
- `90_decisions/` until promoted or superseded by canonical ADRs
- `99_project_receipts/`
- root historical plans and receipts, including `ADR-0011_homepage_powered_qiaccess.md`, `README 2.md`, `codex.md`, and `qilinks_bookmark_admin_plan.md`

## Verified Coverage

The 2026-06-10 build classified 126 source documents:

- Active: 27
- Legacy: 16
- Proposed: 55
- Generated: 4
- Evidence: 24

## Enforcement

`build.js` is the executable status map. The site defaults to Active documents and provides explicit filters for all other statuses. Classification changes require review because they change which documents are presented as governing authority.
