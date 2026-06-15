---
layout: adr ... ...
title: "ADR-0007: Unified Front Matter and Progressive Documentation Topology"
slug: adr-0007-unified-front-matter-and-progressive-doc-topology ... ...
summary: Adopts one universal front matter schema with layout-based meaning, canonical field ordering, and a second-layer documentation topology so blueprint sections read progressively instead of as flat page buckets. ... ...
status: proposed
created_at: 2026-04-01
updated_at: 2026-04-01
author: Cody / AI ... ...
owner: Cody ... ...
sensitivity: internal ... ...
classification: business_internal ... ...
realm_label: ""
context: The blueprint has grown large enough that flat section folders are creating navigation friction. Prior front matter attempts also produced overlapping taxonomies, retired ontology fields, and drift between human-readable metadata and canonical system truth. ... ...
aliases: []
tags:
  - governance
  - front-matter
  - documentation
  - templates
  - topology
keywords:
  - front matter
  - layout
  - templates
  - doc structure
  - blueprint topology
references: []
target_system: QiOS Master Blueprint
target_scope: docs, templates, standards, scripts, mkdocs navigation ... ...
canonical_ref: ""
uid: ""
template_key:
  - adr-template
source_type: manual ... ...
adr_id: ADR-0007 ... ...
supersedes: ""
artifact_kind: ""
registry_key: ""
standard_key: ""
---

# ADR-0007: Unified Front Matter and Progressive Documentation Topology

## Status

Proposed

## Context

The blueprint documentation has expanded beyond a comfortable flat structure. Several sections now contain enough material that readers must hop between sibling pages without a clear progressive path.

At the same time, earlier front matter systems introduced overlapping and now-retired concepts such as `qid`, `qi_decimal`, graph-poetry attributes, and realm-driven structural meaning. The current blueprint doctrine already establishes that front matter is supportive metadata only, not the system of record, and that canonical truth comes from governed system layers rather than file headers. :contentReference[oaicite:1]{index=1} :contentReference[oaicite:2]{index=2}

A unified, lean, enforceable front matter profile is required, along with a documentation topology that preserves reading order and reduces cognitive load.

## Decision

QiOS adopts the following documentation and metadata rules:

1. **Universal Front Matter Vocabulary**
   - All markdown documentation within the blueprint uses one shared front matter vocabulary.
   - The `layout` field determines document intent and conditional requirements.
   - Required fields may vary by `layout`, but the field vocabulary remains singular.

2. **Front Matter Is Supportive Metadata Only**
   - Front matter does not issue canonical identity.
   - Front matter does not define schema placement, routing truth, or graph truth.
   - Legacy fields tied to retired identity/ontology models are removed from active doctrine.

3. **Canonical Field Order**
   - Front matter fields must appear in a governed order.
   - Fields are grouped into human-readable sections.
   - A formatter/linter will normalize order and validate layout-specific requirements.

4. **Progressive Documentation Topology**
   - Each major blueprint section may contain ordered subfolders.
   - Subfolders must support a progressive reading path from overview to model to rules to reference.
   - Documentation should read linearly within a section rather than as a flat bucket of peer pages.

5. **Canonical Source Separation**
   - `docs/` remains the rendered doctrine layer.
   - `standards/`, `registry/`, `adr/`, and `schemas/` remain canonical source layers outside `docs/`.
   - The documentation site may render or summarize those sources through pages in `docs/`, but they do not move into `docs/` merely for visibility.

## Consequences

### Positive

- Reduces front matter drift and overlapping taxonomies.
- Makes documentation easier to read in sequence.
- Preserves separation between rendered doctrine and machine-readable source-of-truth files.
- Creates a stable template and validation model for future growth.

### Negative

- Existing docs will need normalization and partial folder moves.
- MkDocs navigation must be updated to reflect second-layer section structure.
- Some legacy front matter fields and earlier taxonomy experiments will be formally retired.

## Affected Documents

- `standards/content_metadata_profile.yaml`
- `standards/metadata_rules.yaml`
- `templates/page_template.md`
- `templates/adr_template.md`
- `templates/artifact_template.md`
- `scripts/normalize_front_matter.py`
- `mkdocs.yml`
- `docs/01_governance/*`
- `docs/02_architecture/*`
- `docs/03_structure/*`
- `docs/04_data/*`
- `docs/05_compute/*`
- `docs/06_applications/*`
- `docs/07_operations/*`