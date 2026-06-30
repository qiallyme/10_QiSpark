---
title: QiCompiler Add Prompt
slug: qicompiler_add_prompt
realm: QiOS
type: rule
node: file
created: 2025-01-27T00:00:00Z
updated: 2025-01-27T00:00:00Z
version: 1.0.0
status: canonical
system: qios
keywords: [qicompiler, cursor, prompt, tools]
tags: [prompt, cursor, automation, tooling]
context: Cursor prompt for adding QiCompiler to tools directory. Ensures exact file creation and test run.
sensitivity: internal
classification: system_darkmatter
---

# QiCompiler Add Prompt

Create `tools/qicompiler.py` and `tools/qicompiler_config.yaml` exactly as provided.

Do not refactor filenames or paths.

After creation, run a local compile test against existing registries and confirm output at `data/compiled/qios_constitution_v1.json`.

