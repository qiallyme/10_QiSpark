# ADR-0003: Band Model

**Date**: 2026-03-27
**Status**: Accepted

## Context

As the number of schemas grew, it became unclear which components depended on which. There was no formal structural tier model to describe the dependency hierarchy between system infrastructure, platform services, and business domains.

## Decision

QiOS adopts a **3-band structural model**:

| Band | ID | Schemas |
|---|---|---|
| Core | `b_core` | `qiarchive`, `qigraph`, `qially`, `qisys` |
| Platform | `b_platform` | `qione`, `public` |
| Domain | `b_domain` | `qicase`, `qichronicle`, `qicms`, `qihome`, `qiknowledge`, `qitax`, `qivault` |

Dependency direction:
```
Domain → Platform → Core
```

No band may create a dependency in the reverse direction.

## Consequences

- Every new schema must be assigned a band in `registry/band_registry.yaml`
- Core schemas must not reference Domain schemas
- The `enforce_structure.py` script validates band assignments on every PR
