# QiAccess Start Legacy Quarantine

This appendix marks the legacy doctrine that is retained for reference but is not active truth for the current QiAccess Start master blueprint.

## Active Doctrine

The active portal doctrine is:

- QiAccess Start as the cognitive front door
- seven roots only
- System as nested admin and infrastructure
- qiserver as the primary runtime host
- QiNexus and Google Drive as the storage backbone
- source-backed Knowledge, future Memory, and derived Insights

## What Is Quarantined

The following assumptions are quarantined unless explicitly revalidated:

- QiOne as the active primary portal identity
- QiPortals or QiSuite as the active portal product name
- multi-tenant client portal language as the default runtime model
- tenant-first platform requirements for current operator workflows
- CRM, client, product, and delivery documentation treated as the main active operating model
- heavy structural complexity that does not directly serve the seven-root front door

## Quarantined Areas In This Docset

These sections are retained because they may still contain useful fragments, but they must be treated as reference-only until rewritten:

- `docs/06_applications/10_web/`
- `docs/06_applications/30_admin/`
- `docs/06_applications/40_tools/`
- `docs/06_applications/50_interfaces/`
- `docs/07_operations/`
- pages that still depend on tenant-first or client-platform assumptions

## What Survives From Legacy

Legacy material may still provide:

- naming discipline
- metadata rules
- explicit ownership boundaries
- ADR discipline
- security and exposure controls
- useful implementation notes that do not conflict with the current portal

## Promotion Rule

Legacy material leaves quarantine only when one of the following happens:

1. it is rewritten to match the active QiAccess Start doctrine
2. an ADR explicitly promotes the concept back into active use
3. the implementation proves the concept is current and the blueprint is updated to match

## General Rule

- Legacy client/tenant/business-platform doctrine must stay quarantined/reference-only.

