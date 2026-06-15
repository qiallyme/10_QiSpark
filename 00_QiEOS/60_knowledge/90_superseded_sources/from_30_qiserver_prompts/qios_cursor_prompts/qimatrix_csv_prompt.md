---
title: QiMatrix CSV Update Prompt
slug: qimatrix_csv_prompt
realm: QiOS
type: rule
node: file
created: 2025-01-27T00:00:00Z
updated: 2025-01-27T00:00:00Z
version: 1.0.0
status: canonical
system: qios
keywords: [qimatrix, csv, cursor, prompt, update]
tags: [prompt, cursor, automation, tooling]
context: Cursor prompt for updating QiMatrix CSV file. Ensures header validation and Supabase import script generation.
sensitivity: internal
classification: system_darkmatter
---

# QiMatrix CSV Update Prompt

Place `qios_matrix.csv` into `data/sheets/`.

Validate headers.

Generate matching Supabase import script for `qios_matrix`.

