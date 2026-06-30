# Legacy Constitution Salvage Pass

This appendix preserves the earlier salvage reasoning from the older QiOS master blueprint.

It remains useful for understanding what governance DNA was intentionally kept, but it is no longer the final word on active doctrine.

For the current quarantine status of legacy material, use:

- `qiaccess_start_legacy_quarantine.md`

## Context

During the earlier `v0.4` transition, parts of the old QiOne constitution were audited for salvage.

The goal was to keep useful organizational instincts without reintroducing obsolete ontology, duplicate identity systems, or overbuilt structure.

## What Was Kept and Integrated

| Concept | Action Taken | Location | Why It Still Matters |
|---|---|---|---|
| Front matter profile | Reframed | `standards/content_metadata_profile.yaml` | Useful for note hygiene, but subordinate to canonical source ownership |
| Sensitivity and classification | Normalized | `registry/sensitivity_classification.yaml` | Still useful for operational security and handling |
| Realms | Demoted | `registry/workspace_realms.yaml` | Still useful as a UX filtering label, not as ontology |
| Ignore patterns | Absorbed | runtime conventions | Useful for keeping ingest and workspace boundaries clean |
| Taxonomy instinct | Acknowledged | naming and registry controls | Useful only when simplified into clear ownership and naming rules |

## What Was Rewritten

- Front matter is not identity.
- UI realms are not domain ontology.
- Narrative or graph concepts do not govern canonical structure.

## What Was Excluded

- legacy QID worker logic as active identity authority
- matrix governance systems that overcomplicate the current portal
- poetic graph canon as structural truth
- folder-law systems that conflict with the current QiLabs and QiNexus model
