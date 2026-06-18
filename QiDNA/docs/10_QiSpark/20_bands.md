# Bands

Bands are the top-level structural tiers of the QiOS ecosystem. In current doctrine they organize QiAccess Start documentation, QiNexus structures, qiserver runtime concepts, and any future relational domain work.

## Band Model

| Band | ID | Schemas |
| --- | --- | --- |
| **Core** | `b_core` | `qiarchive`, `qigraph`, `qially`, `qisys` (reference / future-conditional schemas) |
| **Platform** | `b_platform` | `qione`, `public` (legacy / future-conditional schemas) |
| **Domain** | `b_domain` | `qicase`, `qichronicle`, `qicms`, `qihome`, `qiknowledge`, `qitax`, `qivault` (reference / future-conditional schemas) |

## Band Definitions

### Core (`b_core`)

Fundamental system infrastructure. Identity backbone, archive spine, system operations, and any future derived graph or AI memory layers.

**Rule**: Other bands depend on Core. Core does not depend on other bands.

### Platform (`b_platform`)

Operational services and deferred container model. Multi-tenant features (tenancy, member roles) are retained here as legacy/future-state reference rather than current runtime doctrine.

**Rule**: Platform provides theoretical containers. Current runtime defaults to a single-account / user-owned model.

### Domain (`b_domain`)

Specific bounded operational domains. Each domain is self-contained and should not reach into other domains without explicit cross-domain contracts.

**Rule**: If a relational domain layer is activated, domain schemas should prefer `owner_user_id`-style user ownership. Multi-tenant `tenant_id` remains deferred and future/conditional.

## Structural Rules

* Any future relational schema must be declared in `registry/band_registry.yaml` before use.
* A schema may not span two bands.
* Any future shared-container access model requires a new ADR before tenant-style isolation assumptions become active doctrine.
