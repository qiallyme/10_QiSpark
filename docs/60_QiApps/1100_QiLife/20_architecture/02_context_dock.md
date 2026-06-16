# Context Dock and Knowledge Model

## Core Doctrine

QiLife does not separate doing from knowing.

Every major tool view should have a **Context Dock** showing the knowledge, note/reflection-type QiBits, documents, history, related QiBits, people, money, and AI interpretation relevant to the current item.

## Why Not a Separate Wiki

QiLife should embed knowledge next to the work instead of depending on a separate wiki engine.

## Context Dock Contents

```text
Context Dock
  - AI Summary
  - Relevant Knowledge
  - Related QiBits
  - Related Actions
  - Related People / Entities
  - Related Documents
  - Related Transactions / Obligations
  - Related Note / Reflection QiBits
  - Prior Resolutions
  - Reflection Prompts
  - Retrieval Tags / Links
```

## Work Modes

- Work Mode: dock collapsed or minimal
- Context Mode: tool and knowledge side by side
- Deep Knowledge Mode: expanded reading/editing mode

## Knowledge Source Doctrine

Repo docs are canonical during build.

In-app knowledge mirrors and indexes repo docs. Imported repo docs are read-only in the app.

Doctrine:

**Write once in Markdown, index everywhere.**

## Knowledge Types

```text
rule
procedure
reference
decision
note
summary
explanation
template
runbook
doctrine
```

## Retrieval Order

1. Direct links
2. Same thread
3. Same bucket
4. Same person/entity
5. Shared tags
6. Semantic similarity later
