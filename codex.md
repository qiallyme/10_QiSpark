# CODEX SYSTEM CONTROL FILE

---

## 🔴 SECTION 0 — ACTIVE INSTRUCTIONS

- Always reconcile existing systems before creating new ones
- Prefer reuse over new implementation
- Identify contradictions explicitly
- Separate facts vs assumptions
- Do NOT implement unless explicitly instructed
- Always read this file fully before acting

---

## 🟡 SECTION 0.5 — LEAN EXECUTION / BUDGET DISCIPLINE

Codex usage is limited. Work lean, but do not work sloppy.

**Primary rule:**

Spend budget on understanding decisions, making correct edits, and verifying results.
Do not spend budget wandering, repeatedly searching, or trying random commands.

### 1. Start with a short plan

Before editing, state:

1. Goal
2. Files likely involved
3. Commands you plan to run
4. Risks / unknowns
5. Stop conditions

Do not begin broad repo work without a plan.

### 2. Use targeted searches first

Prefer:

```bash
git status --short --branch
git log --oneline -8
find . -maxdepth 3 -type f
rg "exact phrase"
rg "keyword" path/to/relevant/folder
```

Avoid repeated broad searches.

If three targeted searches do not find the answer, stop and ask the user or record the missing information.

### 3. Ask instead of wandering

If a fact depends on the user's environment, server, credentials, SSH setup, private path, deployment target, or account configuration, do not guess endlessly.

Ask a direct question.

Example:

> I need the server path or repo location. Should I check `/home/qiadmin/qi_workspace`, `/srv/qios`, or another path?

### 4. Do not rediscover accepted QiDNA doctrine

Treat these as current unless a newer ADR contradicts them:

- QiDNA is the governance and documentation layer.
- QiEOS is doctrine inside QiDNA.
- Active root structure:
  - `01_QiDNA`
  - `10_QiAccess`
  - `20_QiSystem`
  - `30_QiServer`
  - `40_QiCapture`
  - `50_QiNexus`
  - `60_QiApp_QiLife`
  - `70_QiConnect`
- QiAccess is the front door / cockpit / docs surface.
- QiLife is the private life operating app and data spine.
- Supabase Postgres is the current QiLife structured-data authority under ADR-0018.
- QiNexus is file/export/reference/archive storage.
- SQLite is deprecated and allowed only for legacy, local, or transitional use.

Do not reopen these decisions unless the task explicitly asks for architecture review.

### 5. Read known reconciliation files before scanning the whole repo

Before broad repo searches, read:

- `codex.md`
- `README.md`
- `docs.json`
- `01_QiDNA/_01_QiDNA.md`
- `01_QiDNA/Reconciliation/2026-06-10_blueprint_readiness_and_decision_gate.md`
- `01_QiDNA/Architecture/Decisions/ADR-0012_data_strategy.md`
- `60_QiApp_QiLife/_60_QiApp_QiLife.md`

If those files answer the question, stop searching.

### 6. Limit reconnaissance

For most tasks:

- Max 5 minutes: inspect repo status and known docs.
- Max 10 minutes: search for missing files.
- After that, summarize what is missing and ask or proceed with a bounded assumption.

Do not spend the whole session investigating.

### 7. Avoid junk folders

Do not search or process:

- `.git`
- `node_modules`
- `dist`
- `build`
- `.next`
- `.venv`
- `venv`
- `__pycache__`
- `.cache`
- `.wrangler`
- `.pytest_cache`
- `*.log`
- `*.tsbuildinfo`

### 8. Edit discipline

Prefer small, reviewable edits.

Before editing, state:

- Files to edit
- Why each file matters
- What will not be touched

Do not perform mass renames, deletes, or folder moves unless explicitly instructed.

For QiDNA:

- Do not delete legacy/evidence docs.
- Do not silently merge conflicting docs.
- Do not flatten the repo.
- Do not duplicate the QiNexus My Drive bucket tree.
- Label uncertain docs as Active / Legacy / Proposed / Generated / Evidence instead of guessing.

### 9. Verify with the smallest useful check

After edits, run only the smallest relevant verification first.

Examples:

- Docs: check `docs.json` and referenced files.
- Scripts: run the script directly.
- Frontend: run lint/typecheck only if relevant.
- Database: inspect schema/migrations before editing.

Do not run full builds repeatedly unless necessary.

### 10. Stop conditions

Stop and ask or summarize when:

- You cannot locate the source after 3 targeted searches.
- Credentials/server access is required.
- The task depends on a user decision.
- Multiple docs contradict each other.
- A command fails twice for the same reason.
- The next step would be destructive.
- You are about to run a long install/build/test without clear need.

### 11. End every task with a short report

End with:

1. What changed
2. Files changed
3. Commands run
4. What was verified
5. What remains uncertain
6. Recommended next step

Keep it short unless asked for detail.

---

## 🟡 SECTION 1 — ACTIVE AUDIT QUEUE (NEWEST FIRST)

---

### [AQ-001] Relationship Intelligence / Trust Tracking  
**Status:** Pending  
**Created:** 2026-06-09  

**Context:**  
Need system to track individuals, interactions, and derive trust/reliability.

**Ask Codex:**  
- What exists in DNA/docs for:
  - entity tracking  
  - interaction/event logs  
  - trust/reliability evaluation  
- Where is it located?  
- Is it complete, partial, or conceptual?  
- Are there contradictions?  
- What’s missing?

**Constraints:**  
Audit only. No building.

---

## 🟢 SECTION 2 — RESOLVED / ARCHIVE

(None yet)


---

## 🔵 SECTION 3 — CURRENT STATUS AND NEXT ACTIONS

### [STATUS-2026-06-14] Supabase Authority and QiDNA Reconciliation

**Verified status:**

- Canonical mirrored hierarchy remains unchanged.
- ADR-0018 supersedes prior SQLite authority decisions.
- Supabase Postgres is the canonical QiLife structured-data authority.
- SQLite and the 15-table SQLModel implementation are legacy/local/transitional evidence.
- Canonical baseline: Entity, Entity Relationship, and QiBit.
- Local migration created at `supabase/migrations/20260614162319_establish_qilife_entity_qibit_spine.sql`.
- Migration contains exactly two schemas and three tables.
- Migration was syntax-applied successfully in disposable PostgreSQL 16; the validation container was removed.
- RLS is enabled; no client grants or policies are defined.
- No deployment or SQLite data conversion was run.
- QiDNA tree navigation and mind map usability repairs are built into the generated site.
- Referral side quest found no matching source in QiDNA, `/home/qiadmin/qi_workspace`, or `/srv/qios/repos`.

### Next Actions - In Order

1. Approve identity ownership, custom-schema exposure, RLS policies, and grants.
2. Define SQLite-to-Supabase mapping, backup, rollback, and cutover.
3. Continue document-by-document QiLife reconciliation.
4. Complete the route, screen, workflow, permission, and entity-to-view UI blueprint.

### Questions for Cody

- What Supabase user/tenant ownership column should protect each Entity and QiBit?
- Should the custom schemas be exposed through the Supabase Data API, or accessed only by trusted backend code?
- Where is the referral/bonus page repository if it is outside the three searched roots?
