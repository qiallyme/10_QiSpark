# Front Matter Schema

# DOCTRINE:
# Front matter is supportive metadata only.
# It may assist rendering, filtering, search, and lifecycle display.
# It must not issue canonical identity, schema placement, routing truth,
# graph relationships, or cross-domain ownership.
# Meaning is determined by the `layout` field, but the field vocabulary is singular.

## Sections
```yaml
sections:
  core:
  lifecycle:
  classification:
  context:
  relations:
  system:
  layout_specific:
```

### Display behaviors

Use three display modes:

- always_show
- hide_if_empty
- always_hidden

That gives you a clean mental model.

---

## Final universal front matter shape

These are the fields I’d lock.

1. core — always first

    Humanly important. Always visible.

```yaml
    layout
    title
    slug
    summary
    status
```

2. lifecycle

Usually visible, but lean.

```yaml
created_at
updated_at
author
owner
```

### Recommended display:

```yaml
updated_at: always_show
created_at, author, owner: hide_if_empty
```

3. classification

Useful, but not always relevant.

```yaml
sensitivity
classification
realm_label
```

Display:

```yaml
all hide_if_empty
```

This matches current doctrine: sensitivity and classification are governed values, and realm_label is optional UI-layer labeling only.

4. context

Good for search and humans.

```yaml
context
aliases
tags
keywords
references
```

Display:

```yaml
all hide_if_empty
```

5. relations

Only if needed.

```yaml
target_system
target_scope
canonical_ref
```

Display:

```yaml
target_system, target_scope: hide_if_empty
canonical_ref: always_hidden
```

Why hidden: it is useful for machine linkage, but front matter must not masquerade as canonical identity.

6. system

Machine support fields. Hidden.

```yaml
uid
template_key
source_type
```

Display:

```yaml
all always_hidden
```

7. layout_specific

Only meaningful for certain document types.

```yaml
adr_id
supersedes
artifact_kind
registry_key
standard_key
```

Display:

```yaml
all hide_if_empty
except maybe adr_id can be always_show when layout=adr
```

What the profile file should become

Your current content_metadata_profile.yaml is too flat. Change it to include:

```yaml
field definitions
section membership
display behavior
canonical order
layout requirements
```

Here is the structure I’d use:

```yaml
profile: content_front_matter
version: 2.0.0
description: "Universal front matter profile for blueprint docs and related markdown assets."

doctrine:
  system_of_record: false
  notes:
    - "Front matter is supportive metadata only."
    - "Canonical identity comes from QiArchive or the owning system of record."
    - "Schema placement and routing truth do not come from front matter."
    - "Meaning is determined by layout, but the field vocabulary is singular."

sections:
  - id: core
    label: Core
    order: 10
  - id: lifecycle
    label: Lifecycle
    order: 20
  - id: classification
    label: Classification
    order: 30
  - id: context
    label: Context
    order: 40
  - id: relations
    label: Relations
    order: 50
  - id: system
    label: System
    order: 60
  - id: layout_specific
    label: Layout Specific
    order: 70

display_modes:
  - always_show
  - hide_if_empty
  - always_hidden

field_order:
  - layout
  - title
  - slug
  - summary
  - status
  - created_at
  - updated_at
  - author
  - owner
  - sensitivity
  - classification
  - realm_label
  - context
  - aliases
  - tags
  - keywords
  - references
  - target_system
  - target_scope
  - canonical_ref
  - uid
  - template_key
  - source_type
  - adr_id
  - supersedes
  - artifact_kind
  - registry_key
  - standard_key
```

fields:

```yaml
  layout:
    type: string
    required: true
    section: core
    display: always_show
  title:
    type: string
    required: true
    section: core
    display: always_show
  slug:
    type: string
    required: false
    section: core
    display: hide_if_empty
  summary:
    type: string
    required: false
    section: core
    display: hide_if_empty
  status:
    type: string
    required: true
    section: core
    display: always_show

  created_at:
    type: string
    required: false
    section: lifecycle
    display: hide_if_empty
  updated_at:
    type: string
    required: false
    section: lifecycle
    display: always_show
  author:
    type: string
    required: false
    section: lifecycle
    display: hide_if_empty
  owner:
    type: string
    required: false
    section: lifecycle
    display: hide_if_empty

  sensitivity:
    type: string
    required: false
    section: classification
    display: hide_if_empty
  classification:
    type: string
    required: false
    section: classification
    display: hide_if_empty
  realm_label:
    type: string
    required: false
    section: classification
    display: hide_if_empty

  context:
    type: string
    required: false
    section: context
    display: hide_if_empty
  aliases:
    type: array
    items: string
    required: false
    section: context
    display: hide_if_empty
  tags:
    type: array
    items: string
    required: false
    section: context
    display: hide_if_empty
  keywords:
    type: array
    items: string
    required: false
    section: context
    display: hide_if_empty
  references:
    type: array
    items: string
    required: false
    section: context
    display: hide_if_empty

  target_system:
    type: string
    required: false
    section: relations
    display: hide_if_empty
  target_scope:
    type: string
    required: false
    section: relations
    display: hide_if_empty
  canonical_ref:
    type: string
    required: false
    section: relations
    display: always_hidden

  uid:
    type: string
    required: false
    section: system
    display: always_hidden
  template_key:
    type: string
    required: false
    section: system
    display: always_hidden
  source_type:
    type: string
    required: false
    section: system
    display: always_hidden

  adr_id:
    type: string
    required: false
    section: layout_specific
    display: hide_if_empty
  supersedes:
    type: string
    required: false
    section: layout_specific
    display: hide_if_empty
  artifact_kind:
    type: string
    required: false
    section: layout_specific
    display: hide_if_empty
  registry_key:
    type: string
    required: false
    section: layout_specific
    display: hide_if_empty
  standard_key:
    type: string
    required: false
    section: layout_specific
    display: hide_if_empty

layouts:
  page:
    required: [layout, title, status]
  section:
    required: [layout, title, status]
  adr:
    required: [layout, title, status, adr_id]
  artifact:
    required: [layout, title, status, artifact_kind]
  standard:
    required: [layout, title, status, standard_key]
  registry:
    required: [layout, title, status, registry_key]
  appendix:
    required: [layout, title, status]
  template:
    required: [layout, title, status]
```

### How to enforce order

Do not rely on humans to keep YAML in order. That will fail.

Use 3 levels of enforcement
1. Formatter

Create a script like:

```yaml
scripts/normalize_front_matter.py
```

Its job:

parse front matter
reorder fields according to field_order
drop unknown fields or flag them
optionally group by sections with blank lines/comments between groups
2. Validator

Extend enforce_structure.py or add:

```yaml
scripts/validate_front_matter.py
```

Checks:

field order matches canonical order
required fields exist for that layout
forbidden retired fields are not used
enum values match registry if applicable

3. CI / pre-commit

Run formatter and validator:

pre-commit for local correction
CI for blocking merge if drift remains

That aligns with the repo’s general direction of machine-enforced standards and the rule that drift between formal architecture and implementation must be flagged and resolved.

## Best human-facing behavior

For site rendering or editor previews, use this rule:

Always show

```yaml
layout
title
summary if present
status
updated_at
```

Show only if present

```yaml
slug
author
owner
sensitivity
classification
realm_label
context
aliases
tags
keywords
references
target_system
target_scope
layout-specific fields
```

Always hide

```yaml
uid
canonical_ref
template_key
source_type
```

That gives you quick human sanity without exposing internal scaffolding.

Important retired fields

These should be blocked in validation, not just discouraged:

retired_fields:
  - qi_decimal
  - qid
  - node
  - system
  - naming_strategy
  - related
  - parents
  - children
  - siblings
  - graph_weight
  - orbit
  - entangled
  - realm
  - realm_slug

Why: the salvage pass explicitly says those older ontology/graph/identity patterns were rewritten, demoted, or stripped.

---
layout: ""                # home | section | page | adr | standard | registry | appendix | template | artifact
title: ""
slug: ""
summary: ""
status: "active"          # draft | active | superseded | archived
created_at: ""
updated_at: ""
author: ""
owner: ""
tags: []
keywords: []
aliases: []
context: ""
sensitivity: "internal"
classification: "business_internal"
realm_label: ""

uid: ""                   # doc-local stable id, not DB truth
canonical_ref: ""         # optional reference to actual canonical object/archive/entity id
source_type: "manual"     # manual | generated | imported
template_key: ""

domain: ""                # optional doc subject area, not schema issuance
subdomain: ""
target_system: ""
target_scope: ""          # optional: qione, qiarchive, qihome, etc.

artifact_kind: ""         # only meaningful when layout=artifact
adr_id: ""                # only meaningful when layout=adr
supersedes: ""            # optional for adr/page
registry_key: ""          # only meaningful when layout=registry
standard_key: ""          # only meaningful when layout=standard

sort: ""                  # optional sort order
version: ""               # optional version number
references: ""            # optional references
---