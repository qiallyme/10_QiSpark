# Policies

Policies define how the QiAccess Start master blueprint is operated and changed.

## Merge Policy

- Prefer formal sources over informal ones.
- ADRs must exist before merging structural changes to roots, routing, schema ownership, or topology.
- Drift between doctrine and implementation must be flagged and resolved.

## Root Navigation Policy

- The active portal has seven top-level roots only.
- New user-facing concerns belong inside an existing root unless a blueprint change explicitly approves a new root.
- System subroutes remain nested under `System`.

## Placement Policy

- Placement is based on operational ownership, not technical convenience.
- A file, record, or page belongs to the layer that owns its lifecycle.
- When ownership is ambiguous, escalate to an ADR before placing.

## Lifecycle Policy

Objects and records progress through lifecycle states:

```text
active -> deprecated -> archived
```

- **Active**: in use, maintained, and part of current truth
- **Deprecated**: retained but not extended; must be marked clearly
- **Archived**: no longer active; preserved for lineage only

Documentation quarantine is an additional handling rule for legacy doctrine. Quarantined material may be retained for salvage, but it is not active doctrine.

## Bootstrap Policy

- No undocumented dependencies allowed at bootstrap.
- Every environment variable and runtime dependency should be documented before it is treated as required.
- Every service dependency should be verified before a page claims it is operational.

## Registry Policy

- Classification happens via explicit registry or documented ownership, not assumptions.
- No governed object should enter the system without a canonical identifier or clear owning reference.
- Registry issuance and naming decisions must be traceable.

## Contribution Policy

All contributors, human or AI, must:

- avoid parallel schemas or shadow structures without ADR review
- avoid creating new root structures without blueprint approval
- maintain single ownership for canonical objects
- treat exports and AI outputs as derived
- respect registry and naming rules where used
- document build and validation steps
- prioritize clarity over cleverness

## Active Runtime Policy

- The current QiAccess Start runtime is single-user and operator-centered unless a page explicitly marks another model as future-state.
- Current access control should default to owner-scoped or protected system-scoped behavior, not assumed tenant scaffolding.
- Older multi-tenant language may be retained for history, but it must be labeled as future-state or quarantined.

## Security and Data Access Policy

- **Anon Zero-Write Law**: Public unauthenticated access is read-only by default and must not write to canonical records directly.
- **System Role Isolation**: Elevated service credentials belong only to trusted backend, worker, or controlled automation paths.
- **Protected Surface Rule**: Private infrastructure such as server admin, storage internals, diagnostics, and raw runtime control stays behind explicit protection boundaries.
- **Derived Truth Rule**: Search, AI, graph, and export layers may assist but may not silently replace canonical sources.

## Legacy Quarantine Policy

- Legacy QiOS, QiOne, tenant, client, and business-delivery doctrine may be preserved for salvage.
- When such material conflicts with the active seven-root portal, it must be moved to or referenced from the quarantine appendix.
- Quarantined pages are reference-only until revalidated by blueprint update or ADR.

## Agent Governance Policy

QiAccess Start still enforces an Agent Governance Layer.

Agents must:

- validate doctrine before making structural changes
- preserve canonical versus derived boundaries
- treat external or reconciled notes as non-authoritative until checked against the active blueprint
- escalate when ownership, route, or truth status is unclear

## Phase 0 - Freeze and protect (QiNexus)

Goal: prevent accidental loss during reorganization.

**Mandatory Rules:**

- Do not delete anything.
- Do not let an AI move files directly.
- Create and use the `130_system/qinexus_cleanup/` folder.
- Generate manifests and reports before any moves.

### Cleanup System Structure

Located at `G:\My Drive\QiNexus\130_system\qinexus_cleanup\`:

- `rules/`: Governance and movement criteria
- `reports/`: Audit results and analysis
- `manifests/`: Snapshots of directory state
- `quarantine/`: Staging for disputed or risky items
- `scripts/`: Automation for audit and verification
- `approved_moves/`: Verified move instructions for human execution
