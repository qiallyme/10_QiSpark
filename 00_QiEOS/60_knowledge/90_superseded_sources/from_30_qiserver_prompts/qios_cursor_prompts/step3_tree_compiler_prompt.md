---
title: Step 3 Directory Tree Compiler Prompt
slug: step3_tree_compiler_prompt
realm: QiOS
realm_slug: qios_cursor_prompts
qi_decimal: 0.00.11-RUL
qid:
type: rule
node: file
keywords: [tree, compiler, directory, structure, registry, readme]
tags: [prompt, cursor, automation, tooling]
context: Cursor prompt for implementing QiOS Directory Tree Compiler (Step 3). Local-first Python script that reads registries and generates canonical folder tree.
aliases: [tree_compiler_prompt, step3_compiler]
version: 1.0.0
status: canonical
system: qios
naming_strategy: slug_only
sort: 11
related: []
parents: []
children: []
siblings: []
references: []
graph_weight: 1
orbit: mid
entangled: []
summary: Cursor prompt for building the Directory Tree Compiler that generates QiOS_v1 folder structure from registries.
sensitivity: internal
classification: system_darkmatter
created: 2025-01-27T00:00:00Z
updated: 2025-01-27T00:00:00Z
---

# Step 3 Directory Tree Compiler Prompt

You are updating QiOS_v1. Build a local-first Directory Tree Compiler for Step 3.

## Hard Requirements

- Everything must align with `0.00.00-qios_genesis.md` and `qios_rules_v1_1.yaml/csv`.
- Input registries:
  - `data/sheets/realms_registry.csv`
  - `rules/folder_registry.yaml`
  - `data/sheets/qios_rules_v1_1.csv`
- Output:
  1) Create the canonical QiOS_v1 folder tree as stub directories.
  2) For each folder, generate README.md placeholder using the README template rules.
  3) For each realm, mirror the OS tree but omit folders marked `client_excluded=true`.
- Enforce naming strategy rules (`qidecimal_slug` or `slug_only`) on generated stubs.
- Do NOT invent new realms or folders. Only use registry sources.
- Provide:
  - `/tools/tree_compiler.py`
  - `/tools/tree_compiler_config.yaml`
  - short run instructions in `/tools/README.md`

## Script Behavior

- **Idempotent**: running twice does not create duplicates.
- Logs actions to `data/outputs/tree_compile_log.json`.
- **Dry-run mode supported**: `--dry-run` prints planned changes only.

## Implementation Notes

- Use Python 3.7+ with PyYAML.
- Follow existing `workers/linter/readme_generator.py` pattern for README rendering.
- Respect Layer 0 (Root Integrity) and Layer 2 (Realm Schema) rules.
- Generate READMEs with proper front matter per `data/sheets/front_matter_schema_v1.csv`.

Now implement.

