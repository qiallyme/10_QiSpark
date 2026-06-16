---
title: QiMatrix YAML Update Prompt
slug: qimatrix_yaml_prompt
realm: QiOS
type: rule
node: file
created: 2025-01-27T00:00:00Z
updated: 2025-01-27T00:00:00Z
version: 1.0.0
status: canonical
system: qios
keywords: [qimatrix, yaml, cursor, prompt, update]
tags: [prompt, cursor, automation, tooling]
context: Cursor prompt for updating QiMatrix YAML file. Ensures exact structure preservation.
sensitivity: internal
classification: system_darkmatter
---

# QiMatrix YAML Update Prompt

Update the file at `data/schemas/qios_matrix.yaml` to the exact structure Gina provided.

Do not alter formatting.

Ensure all IDs, arrays, keys, and subtrees are preserved.

Validate YAML with a schema-free linter.

