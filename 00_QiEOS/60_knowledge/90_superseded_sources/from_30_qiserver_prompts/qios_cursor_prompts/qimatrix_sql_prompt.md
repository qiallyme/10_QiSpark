---
title: QiMatrix SQL Update Prompt
slug: qimatrix_sql_prompt
realm: QiOS
type: rule
node: file
created: 2025-01-27T00:00:00Z
updated: 2025-01-27T00:00:00Z
version: 1.0.0
status: canonical
system: qios
keywords: [qimatrix, sql, cursor, prompt, update]
tags: [prompt, cursor, automation, tooling]
context: Cursor prompt for updating QiMatrix SQL schema file. Ensures proper SQL formatting and table creation.
sensitivity: internal
classification: system_darkmatter
---

# QiMatrix SQL Update Prompt

Place `qios_matrix.sql` into `data/schemas/` exactly as provided.

Run through SQL formatter but do not reorder columns.

Ensure table exists in Supabase.

