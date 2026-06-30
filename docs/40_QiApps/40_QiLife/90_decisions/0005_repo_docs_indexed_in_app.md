# ADR 0005: Repo Docs Indexed in App

## Status
Accepted

---

## Context
During the design and build phases, repository markdown documentation (located in `docs/`) is the canonical source of truth for developer agents (like Codex or Antigravity) to understand system specifications. However, when Cody operates the live **QiLife** app in production, he needs access to these design docs, user flows, and guidelines. Manually copying markdown files into database editors is highly inefficient and creates sync issues.

---

## Decision
We will treat the markdown files in the repository's `docs/` folder as the canonical authoring source for system-level knowledge. The application will include an automated importer/syncer script that:
*   Crawls `docs/` at startup or via admin command.
*   Parses the frontmatter and markdown body of each file.
*   Compares the MD5 hash of the file with the database record (`sync_hash`).
*   Inserts or updates the content into the `knowledge_items` table with `source_type = 'repo_doc'`.

---

## Consequences
*   **Single Source of Truth**: System design, schemas, and ADRs are authored in git as code, but made instantly readable inside the app.
*   **RAG Coverage**: The indexed repository documents are fully searchable via the **Ask QiLife** semantic engine, allowing Cody to query system operations directly (e.g. *"What is the database schema for obligations?"*).
*   **Read-Only App View**: Imported repository documents are marked as read-only within the browser UI to prevent writes in the app from contradicting the files in git.
