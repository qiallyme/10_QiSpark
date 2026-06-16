# QiLabs Content Templates

This directory contains the canonical templates for generating Markdown content across the QiLabs ecosystem. These templates enforce consistent metadata and structural rules to prevent drift and ensure machine-readability by ingestion pipelines (QiArchive).

## Available Templates

| Template | Purpose | When to use |
|----------|---------|-------------|
| **`note_template.md`** | Generic knowledge, thoughts, meeting notes | Creating a new note in Obsidian or the knowledge base. |
| **`artifact_template.md`** | System outputs, plans, walkthroughs, generated code logs | When an AI agent or automated script generates a durable record of a task or plan. |
| **`adr_template.md`** | Architecture Decision Records | When formalizing a new system rule, schema change, or structural mandate. |

## Metadata Standard (Frontmatter)

All templates use YAML frontmatter that aligns with the QiOS Master Blueprint metadata rules:

- **`id`**: A unique UUID or ULID.
- **`short_code`**: A human-friendly identifier (e.g., `QXXXXXX`).
- **`domain_prefix`**: The system domain this file belongs to (e.g., `bbr4821` for the main tenant, `qiarchive` for ingestion, `qicase` for legal/cases).
- **`document_type`**: Enforces strict categorization (note, artifact, adr).
- **`status`**: The lifecycle stage of the document (draft, active, archived).
- **`tags`**: Used by the embedding system for semantic clustering.

By strictly adhering to these YAML fields, local workers (like `qiarchive`) can parse, categorize, and index the entire repository without guessing.
