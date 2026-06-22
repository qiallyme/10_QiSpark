# Changelog

## v0.5 - QiAccess Start Doctrine Merge
**Date**: 2026-05-10

### What Changed

- Reframed the master blueprint around the active QiAccess Start seven-root portal
- Rewrote the landing, governance, architecture, and portal overview pages to match current doctrine
- Preserved useful constitutional rules around identity, metadata, naming, ADRs, and derived truth boundaries
- Added an explicit legacy quarantine appendix for older QiOS, QiOne, tenant, and client-platform doctrine
- Marked retained application material as reference-only when it still reflects the older runtime model

### Key Decisions Made

- QiAccess Start is the active portal doctrine
- Seven roots remain the only top-level navigation contract
- System stays nested under the portal rather than expanding into new roots
- Legacy doctrine is preserved by quarantine, not by co-owning the active blueprint

### Known Remaining Work

- deeper legacy pages still need page-by-page revalidation
- some structure, identity, and operations pages still carry older platform terminology
- doc generation and nav indexes should be refreshed with the existing rebuild scripts

## v0.4 - Reconciliation and Canonicalization Release
**Date**: 2026-03-27

### What Changed

- Established `qios-master-blueprint` as standalone canonical doctrine repo
- Defined the 3-band model (Core / Platform / Domain)
- Mapped all live schemas to their bands
- Populated registry inventory and band assignments
- Added naming rules with canonical naming contract
- Added machine validation and supporting schemas
- Consolidated earlier narrative ontology while retiring overlapping concepts

### Key Decisions Made

- ADR-0001: Blueprint scope locked
- ADR-0002: Single domain rule adopted
- ADR-0003: Band model adopted
- ADR-0006: Narrative and knowledge layer consolidation adopted
