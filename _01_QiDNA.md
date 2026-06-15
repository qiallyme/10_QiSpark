# QiDNA

## Overview

QiDNA is the governance and documentation layer for the Qi system. It defines the mirror rule: documentation must live in the same layer as the thing it describes.

The active system model is:

```text
QiAccess -> QiLife -> (QiSystem + QiNexus + QiCapture + QiConnect)
```

QiDNA names system layers, keeps their boundaries clear, and holds system-level doctrine in `00_QiEOS/`.

## Responsibilities

- Maintain the mirrored documentation structure.
- Keep system-layer names stable.
- Hold doctrine, philosophy, decisions, and system reasoning in `00_QiEOS/`.
- Prevent duplicate or conflicting source-of-truth documents.
- Record the active system model clearly and consistently.

## Flows

```text
Question
  -> identify the system layer
  -> open the matching folder
  -> read the local index or placement file
```

Runtime facts beat planning notes. Active mirrored docs beat legacy documents. QiEOS explains why, but each layer owns its operating details.

## Structure

```text
_QiOS_DNA/
|-- _01_QiDNA.md
|-- 00_QiEOS/
|   |-- 10_governance/
|   |-- 20_structure/
|   |-- 30_data/
|   |-- 40_service_apps/
|   |-- 50_operations/
|   |-- 60_knowledge/
|   `-- 70_assets/
|-- 05_Decisions/
|-- 10_QiAccess/
|-- 20_QiSystem/
|-- 30_QiServer/
|-- 40_QiCapture/
|-- 50_QiNexus/
|-- 60_QiConnect/
|-- 1000_QiApps/
|-- 1100_QiLife/
|-- Reconciliation/
`-- Schema/
```
