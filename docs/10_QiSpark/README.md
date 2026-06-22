# QiAccess Start Master Blueprint

This repository is the active master blueprint for QiAccess Start.

QiAccess Start is Cody's cognitive front door:

1. Home
2. Start
3. Capture
4. Knowledge
5. Memory
6. Insights
7. System

The old QiOS material is not discarded, but it is no longer allowed to compete with the active doctrine. Useful governance, standards, registry discipline, and architecture policies remain in force. Legacy multi-tenant and client-platform assumptions are retained only as quarantined reference material until they are explicitly revalidated.

## Active Doctrine

- QiAccess is the portal.
- The map is the interface.
- The knowledge base is the memory behind each node.
- Capture must stay fast or the system fails.
- System is nested administration, not a top-level junk drawer.
- Memory and Insights stay honest when they are placeholders.

## Current Phase

Phase 1 remains stabilization and prototype flow validation:

1. keep the SPA working
2. align the app to the seven roots
3. preserve working launcher and link behavior
4. freeze legacy surfaces in place
5. validate Capture as the first real operating path

## What Stays Authoritative

- `docs/01_governance/`: principles, policies, registry, and ADR discipline
- `docs/02_architecture/`: active QiAccess Start system model and runtime framing
- `docs/06_applications/`: the seven-root portal doctrine
- `docs/08_appendices/20_legacy/`: quarantined legacy material and salvage notes
- `standards/` and `registry/`: retained structural controls that still serve the active system

## Build Loop

The blueprint can still be maintained through the existing documentation toolchain:

1. update doctrine or registry files
2. run `rebuild.bat`
3. inspect validation output
4. preview with `mkdocs serve` when needed

## Legacy Handling

Use the quarantine appendix before promoting older QiOS, QiOne, tenant, client, or product-delivery doctrine back into the active blueprint:

- `docs/08_appendices/20_legacy/legacy_salvage.md`
- `docs/08_appendices/20_legacy/qiaccess_start_legacy_quarantine.md`
