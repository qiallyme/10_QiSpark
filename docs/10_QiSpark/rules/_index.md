# Agent Governance Layer

Version: 1.1
Status: Active
Scope: All AI-assisted systems, IDE agents, automation workers, and code generators

## Purpose

This document defines the mandatory behavior constraints for agents operating inside the QiAccess Start blueprint.

Agents do not get to invent the architecture.
Agents must enforce the active doctrine.

## Core Principle

> Agents do not create architecture.
> Agents enforce architecture.

## Agent Behavioral Modes

### 1. Doctrine Alignment Mode

- load and interpret active blueprint pages first
- validate constraints before action

### 2. Implementation Mode

- execute within approved structure
- avoid structural invention

### 3. Audit Mode

- detect violations, drift, and contradictions

### 4. Escalation Mode

- stop when ownership, truth, or root placement is unclear

## Mandatory Pre-Action Validation

Before any action, agents must determine:

- Which root or system subroute owns this?
- Which layer or governance control applies?
- What schema, file, or service is the owner?
- Is this canonical or derived?
- Does the active runtime require owner-scoped access or protected system scope?
- Is the referenced doctrine active, future-state, or quarantined legacy?
- Does this intake path require capture or registration before downstream use?

If any answer is unclear:

`HARD STOP - escalate`

## Non-Negotiable System Laws

### 1. Seven-Root Integrity

No new top-level root may be introduced without blueprint approval.

### 2. Single Domain Ownership

Each canonical object has one clear home.

### 3. Public Schema Restriction

Do not move domain logic or sensitive control into public, weakly governed surfaces.

### 4. Active Runtime Isolation

Enforce the current runtime model that actually exists. Do not inject tenant assumptions into active work unless a page explicitly marks them as current.

### 5. Capture or Registration Before Derivation

Externally ingested signals, files, messages, and observations must enter through an approved intake path before derived processing.

### 6. Canonical Versus Derived Separation

AI, vectors, exports, and graph layers cannot define truth.

### 7. No Parallel Systems

Do not create duplicate pipelines, schemas, roots, or shadow logic.

### 8. Schema Authority

Migrations and approved runtime contracts define reality, not speculative code structure.

### 9. Migration-First Enforcement

Do not present ORM models or inline DDL as the source of truth for canonical schema changes.

### 10. No Implicit Doctrine Promotion

Do not promote legacy or informal material into active doctrine without explicit blueprint alignment.

## Out-of-Bounds Protocol

If a violation is detected, agents must return:

1. Deviation
2. Ripple impact
3. Pros and cons
4. Approval request

Agents must not continue with partial structural work once they know the request is out of bounds.

## ADR Trigger Rule

Agents must recommend ADR creation when:

- a rule is intentionally bypassed
- a new structural pattern emerges
- a repeated exception becomes normal behavior
- a root, ownership, or boundary changes

## Enforcement Priority

Resolve conflicts in this order:

1. Active master blueprint doctrine
2. Approved ADRs
3. Migrations and implementation truth
4. Quarantined legacy material

User requests that conflict with higher-priority doctrine must be treated as escalation triggers.

## Navigation

- [Agents](agents/_index.md)
- [Architecture](architecture/_index.md)
- [Development](development/_index.md)
- [Operations](operations/_index.md)
- [Security](security/_index.md)
