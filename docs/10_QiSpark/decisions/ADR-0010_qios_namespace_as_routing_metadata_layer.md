---
title: ADR-0010 — QiOS Namespace as Routing Metadata Layer
status: Accepted
date: 2026-05-18
owner: Cody
related:
  - docs/10_core/30_data/50_namespace_registry.md
  - docs/10_core/10_governance/60_registry/band_registry.yaml
  - docs/10_core/30_data/70_object_model.md
  - docs/10_core/30_data/110_front_matter.md
---

# ADR-0010 — QiOS Namespace as Routing Metadata Layer

## Status

Accepted.

## Context

QiOS previously used namespace-style bands and route codes as part of a broader system blueprint. The current active system has evolved into separate layers:

- QiAccess Start as the operational front door
- QiNexus as the visible storage/workspace model
- Repo docs as engineering/source-of-truth doctrine
- Wiki.js as the readable operating library
- Paperless-ngx, RAG, graph indexing, and manifests as derived/indexed systems

The namespace model remains useful, but it must not compete with QiNexus or recreate the folder tree.

## Decision

The QiOS namespace is adopted as a routing and metadata layer.

It does not define the visible folder tree.

QiNexus defines storage placement. Namespace routes define machine-readable routing, classification, grouping, rollup logic, and automation targets.

Relational IDs and namespace routes are separate:

- relational IDs answer: “what is this?”
- namespace routes answer: “where does this work belong?”

## Consequences

- Namespace bands may be used in front matter, manifests, Paperless tags, Wiki.js metadata, graph/RAG records, and automation rules.
- Namespace bands must not be casually converted into Drive root folders.
- New top-level namespace bands require blueprint update or ADR approval.
- Entities such as people, contacts, clients, vendors, organizations, and users should exist as relational records first.
- Namespace allocations are only used for governed containers, matters, projects, archive blocks, durable routing groups, or approved operational partitions.
- The canonical namespace registry lives at `docs/10_core/30_data/50_namespace_registry.md`.
- The machine-readable band registry lives at `docs/10_core/10_governance/60_registry/band_registry.yaml`.

## Operating Rule

QiNexus keeps the visible system navigable.

The namespace keeps the machine-readable system coherent.

Relational identity keeps real-world entities accurate.
