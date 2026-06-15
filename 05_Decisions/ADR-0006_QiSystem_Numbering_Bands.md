# ADR-0006 — QiSystem Numbering Bands

Status: Accepted

## Decision

QiSystem uses numeric bands to separate core system modules from app/product modules.

Core modules live below `80` unless deliberately expanded.

`80–999` is reserved for future core/system expansion.

Apps begin at `1000`.

## Canonical Bands

| Band     | Meaning                                               |
| -------- | ----------------------------------------------------- |
| `00–79`  | Active core/system modules                            |
| `80–999` | Reserved future core/system space                     |
| `1000+`  | Apps, products, experiments, and app-specific systems |

## Current Canonical Placements

| Number | Name        | Role                                        |
| -----: | ----------- | ------------------------------------------- |
|   `50` | `QiNexus`   | Storage / file backbone                     |
|   `60` | `QiConnect` | Integrations, connections, external systems |
| `1000` | `QiApps`    | Application namespace root                  |
| `1100` | `QiLife`    | Primary life cockpit app                    |

## Rationale

QiConnect belongs directly after QiNexus because storage and connection/integration layers are adjacent infrastructure concerns.

Apps should not compete with core infrastructure numbering.

Starting apps at `1000` leaves room for future core modules while allowing application spaces to expand indefinitely.

## Rules

* Do not create new core modules casually inside `80–999`.
* Do not place app/product folders below `1000`.
* Do not rename working folders without checking references.
* Update documentation first, then rename folders only after safety review.

Apps may expand freely in the `1000+` namespace without affecting core system numbering.
