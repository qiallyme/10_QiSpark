---
title: Cursor User Prompt
slug: cursor_user_prompt
realm: QiOS
realm_slug: qios_cursor_prompts
qi_decimal: 0.00.11-RUL
qid:
type: rule
node: file
keywords:
  - QiOS
  - Governance
  - Cursor
  - Instruction
  - Coding
tags:
  - Rules
  - User
  - Prompt
context: QiOS_v1
created: 2025-11-23
updated: 2025-11-24
aliases:
  - cursor_task_prompt
  - qios_cursor_user_prompt
version: 1.0.0
status: active
system: qios
naming_strategy: slug_only
sort: 11
related: "[[project_prompt.md]]"
parents:
children:
siblings:
  - "[[project_prompt.md]]"
references:
  - "[[0.00.00-qios_genesis|QiEOS: The Genesis Document]]"
graph_weight: 400
orbit: core
entangled:
summary:
sensitivity: internal
classification: system_darkmatter
---
You are working inside the QiOS_v1 repository. 
Your NUMBER ONE job is to ensure every file, schema, seed, worker, rule, and folder you touch is 100% consistent with the canonical QiOS Genesis document and the QiOS EOS protocols referenced below.

CANONICAL SOURCES (do not contradict):
- QiOS Genesis: ./0.00.00-qios_genesis.md
- EOS Protocols:
  - QID spec: ./0.00.01.15_qid.md
  - QiDecimal spec: ./0.00.01.01_qidecimal.md
  - Formatting standards: ./0.00.01.05_formatting.md
  - Atomicity rule: ./0.00.01.07_atomicity.md
  - Realms/Taxonomy: ./0.00.03.01_realms.md, ./0.00.03.00_taxonomy.md, ./0.00.03.03_tag_taxonomy.md
- Rule registries:
  - YAML rules: ./rules/qios_rules_v1_1.yaml, ./rules/realms_registry.yaml, ./rules/folder_registry.yaml
  - CSV registries: ./data/sheets/front_matter_schema_v1.csv, ./data/sheets/qios_rules_v1_1.csv, ./data/sheets/realms_registry.csv, ./data/sheets/sensitivity_classification_registry.csv
  - SQL schema + seeds: ./data/schemas/qios_brain_db_v1.sql, ./data/seeds/supabase_seed_realms.sql, ./data/seeds/supabase_seed_rules.sql

HARD CONSTRAINTS YOU MUST OBEY:
1. Filenames = slug + extension. Optional QiDecimal prefix only for ordering. Never add dates to filenames.
2. QID is opaque, global, monotonic, immutable. Never encode meaning in QID, never change an existing QID.
3. QiDecimal is semantic address. Never auto-renumber existing QiDecimals; only propose new ones.
4. Markdown formatting:
   - Exactly ONE H1 (#) per file, matching front matter title.
   - All content sections start at H2 (##) or deeper. Do not use H1 in body.
5. Atomicity: one primary concept per doc. Split instead of bloating.
6. Realms define ownership/context; Assets define format and live inside realms.
7. Rules apply by 7-layer linter order. Never design logic that bypasses Layer ordering.
8. If a requirement is unclear, infer from Genesis/registries first. If still ambiguous, choose the safer, more conservative interpretation (no destructive actions, quarantine instead of delete).

TASK: Apply QiOS Observability + Orchestrator bundle v1.1.

You must:

1) Add and run DB patch:
   - create system_event, worker_status, qid_counter (if missing), claim_qid()
   - file: data/schemas/qios_brain_db_v1_1_patch.sql

2) Add seed patch:
   - system_event vocab rows
   - baseline worker_status rows
   - file: data/seeds/supabase_seed_core_status.sql

3) Update registries:
   - append DOC.010, DOC.020, OBS.010 to data/sheets/qios_rules_v1_1.csv
   - mirror same logic into rules/qios_rules_v1_1.yaml
   - update any front_matter_schema descriptions if needed (no new props)

4) Create worker stubs:
   - workers/orchestrator/worker_orchestrator.ts
   - workers/_shared/heartbeat.ts
   Ensure naming, layering, and rule ordering align with Genesis.

5) Update Genesis doc:
   - Add H2 Observability & One-Click Runtime addendum
   - Add Orchestrator under QiWorkers ontology
   - No H1 in body, H2+ only.

OUTPUT REQUIREMENTS:
- Produce changes that are consistent with the canon above.
- If you propose a new rule/prop/table/folder, update the matching registry file(s) in the same change.
- Include a short “Canon Check” section explaining how your output aligns to Genesis + specific EOS rules.
