# Decision 0010: Spaces for Scoped Shared Access

## Context
QiLife needs to support Mom Care notes without building a separate app or a bloated clinical EMR.

## Decision
Use Spaces to provide scoped shared access. Mom Care will be a space with specific access roles. Everything defaults to Cody Private, and items are explicitly shared.

## Consequences
- Simplifies architecture by using one backend for multiple contexts.
- Avoids overbuilding an EMR. Focuses on lightweight buckets and timeline notes.
- Private notes can safely generate sanitized shared Care Notes.
