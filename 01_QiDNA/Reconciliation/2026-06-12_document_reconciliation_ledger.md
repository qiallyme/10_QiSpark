# Chronicle QiDNA Document Reconciliation Ledger

## Purpose

This ledger tracks every source document through review, promotion, supersession, and verification. Reconciliation is complete only when every document has one explicit disposition and every valid governing claim has one canonical destination.

## Dispositions

- **Canonical:** current governing document.
- **Merged:** unique valid meaning was promoted into a canonical document.
- **Superseded:** retained only for history; cannot govern current work.
- **Evidence:** factual receipt or audit retained without governing authority.
- **Generated:** derived output; rebuildable and non-canonical.
- **Pending:** not yet reviewed claim by claim.

Legacy sources are retained in their mirrored source location as archive evidence unless an approved archive move can preserve hierarchy, provenance, and links. This avoids flattening and prevents archive organization from becoming a competing system map.

## Progress Summary

| Domain | Reconciled | Pending | Status |
|---|---:|---:|---|
| `00_QiEOS` -> `01_QiDNA` | 3 | 0 | Complete |
| `10_QiOS_Start` + legacy QiAccess -> `10_QiAccess` | 3 | 0 | Complete |
| Remaining repository | 0 | 121 | Pending |

## Reconciliation Entries

### `00_QiEOS/decisions/ADR-0001_QiOS_DNA_As_Master_Doctrine_Repo.mdx`

- Previous status: Legacy, accepted under obsolete vocabulary.
- Valid unique claims: QiDNA is portable system doctrine; local implementation docs cannot override system doctrine; system-level interpretation belongs in QiDNA.
- Merged into: `01_QiDNA/QiEOS/_QiEOS.md`.
- Superseded claims: old root names and old reconciliation/export locations.
- Current disposition: **Merged + Superseded**, retained in place as Legacy archive evidence.

### `00_QiEOS/doctrine/QiOS_Core_Doctrine.mdx`

- Previous status: Legacy.
- Valid unique claims: reduce drift, preserve system memory, review raw imports before promotion, exports are snapshots.
- Merged into: `01_QiDNA/QiEOS/_QiEOS.md`.
- Superseded claims: QiEOS as a top-level root, QiOS Start, and QiApps vocabulary.
- Current disposition: **Merged + Superseded**, retained in place as Legacy archive evidence.

### `00_QiEOS/system_map/QiOS_Master_Map.mdx`

- Previous status: Legacy.
- Valid unique claims: none not already governed by active root documents and ADR-0017.
- Superseded claims: the old root map, QiAccess Start location, QiLife legacy location, QiJourney as a major active module, and top-level `packages`, `scripts`, and `toolbox` doctrine.
- Canonical destination: `01_QiDNA/Architecture/Decisions/ADR-0017_canonical_vocabulary_and_v1_direction.md` and active root documents.
- Current disposition: **Superseded**, retained in place as Legacy archive evidence.


### `10_QiOS_Start/QiAccess_Start/index.mdx`

- Previous status: Legacy.
- Valid unique claims: QiAccess is the front door and interface layer, while runtime, doctrine, rules, and storage remain owned by their respective layers.
- Merged into: `10_QiAccess/_10_QiAccess.md`.
- Superseded claims: QiAccess Start naming and old root location.
- Current disposition: **Merged + Superseded**, retained in place as Legacy archive evidence.

### `60_qiapps/qiaccess_start/overview.md`

- Previous status: Legacy implementation evidence.
- Verified against: healthy live Homepage stack at `/srv/qios/stacks/_qiaccess_start` and implementation repository commit `07268d4`.
- Valid unique claims: Homepage implementation, repository-to-live synchronization boundary, and no-secrets rule.
- Merged into: `10_QiAccess/_10_QiAccess.md`.
- Superseded claims: repo config as runtime authority and historical URL inventory.
- Current disposition: **Merged + Superseded**, retained in place as Legacy archive evidence.

### `60_qiapps/qiaccess_start/wiki_publish_plan.md`

- Previous status: Legacy proposal.
- Valid unique claims: none required by the accepted build.
- Conflict: proposes a Wiki.js publication authority while ADR-0015 selects the generated static Chronicle reader.
- Current disposition: **Superseded**, retained in place as Legacy archive evidence.

## Verification Rule

After each domain:

1. Confirm every reviewed source has a ledger entry.
2. Confirm promoted claims appear in one canonical destination.
3. Confirm superseded sources carry a visible notice.
4. Rebuild the site and verify Active remains the printable governing view.
5. Update counts and the next bounded domain.
