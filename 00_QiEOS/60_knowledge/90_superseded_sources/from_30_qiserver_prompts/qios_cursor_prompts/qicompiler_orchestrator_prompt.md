---
title: QiCompiler Orchestrator Integration Prompt
slug: qicompiler_orchestrator_prompt
realm: QiOS
type: rule
node: file
created: 2025-01-27T00:00:00Z
updated: 2025-01-27T00:00:00Z
version: 1.0.0
status: canonical
system: qios
keywords: [qicompiler, orchestrator, cursor, prompt, integration]
tags: [prompt, cursor, automation, tooling]
context: Cursor prompt for updating orchestrator to consume compiled constitution instead of raw registries.
sensitivity: internal
classification: system_darkmatter
---

# QiCompiler Orchestrator Integration Prompt

Update `workers/orchestrator/worker_orchestrator.ts`:

- Remove direct reads of registries.
- Load constitution via `_shared/constitution.ts`.
- Use `constitution.rules.layers` for pipeline ordering.
- Use `constitution.ignore.patterns` for scans.
- Use `constitution.realms` for enable/disable decisions.

Preserve existing durable object logic.

