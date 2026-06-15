# ADR-0001: Blueprint Scope

**Date**: 2026-03-27
**Status**: Accepted

## Context

The QiOS doctrine was previously scattered across README files, working notes, and ad-hoc markdown documents inside the main monorepo. This created ambiguity about what was governing truth vs working notes.

## Decision

The `qios-master-blueprint` repo (this repo) is the **sole canonical home** for QiOS constitutional doctrine. It is:

- Constitutional doctrine
- Structure law
- Architecture law
- Schema/data/object law
- Operational map
- Decision history

It is **not**:

- App code
- Runtime code
- Experimental notes
- A random ADR graveyard

## Consequences

- All future governance decisions must be captured here, not in app repos
- The README is the entry point only — doctrine lives in `docs/`
- Machine-readable constraints go in `standards/` and `registry/`
- Decision history goes in `adr/`
