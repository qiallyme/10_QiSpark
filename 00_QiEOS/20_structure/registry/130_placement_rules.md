# Placement Rules

Placement rules define where every type of object belongs. When placement is ambiguous, escalate to an ADR.

Current active doctrine is document-first and runtime-first: QiAccess Start documentation lives in Markdown/YAML, qiserver owns local runtime execution, QiNexus remains the storage backbone, and Supabase-specific placement remains legacy/reference-only or future/conditional unless a specific job requires it.

## The Primary Rule

> Every object has exactly one canonical domain.

If you cannot answer "which domain or governed container owns this object's lifecycle?" - the object is not ready to be placed.

## Placement Decision Tree

```text
Is it a file or ingested record?          -> qiarchive
Is it a legal/operational case?           -> qicase
Is it a calendar event or time record?    -> qichronicle
Is it published content or a post?        -> qicms
Is it a household expense or chore?       -> qihome
Is it a note or local knowledge record?   -> qiknowledge
Is it a tax return or related document?   -> qitax
Is it a secure document or contract?      -> qivault
Is it an AI session or memory record?     -> qially (future/conditional)
Is it a system job or worker event?       -> qisys
Is it a graph node or derived edge?       -> qigraph (future/conditional)
Is it a modular config or module registry record? -> qione (reference only)
Is it a tenant, member, or RBAC record?   -> qione (Platform-Future only)
Is it an email account integration param? -> qione (reference only)
Is it an ingested email message/thread?   -> qiarchive
Is it an email sync event or cursor?      -> qisys
Is it a global auth record?               -> future auth layer if one is explicitly activated
```

## Rules for New Objects

| Rule | Requirement |
| --- | --- |
| Every object must have | A canonical ID |
| Every domain-scoped object must have | A `owner_user_id` FK |
| Every file-derived object or email attachment must have | An `archive_id` FK |
| Every object must have | A status field |
| Every mutable object must have | `created_at` + `updated_at` timestamps |

## Domain-Specific Guardrails

* **Email**: Do not create a top-level `qiemail` schema unless a future ADR explicitly approves it. Email should be modeled as an integration path into the canonical Spine, relying on `qione` for configuration only if that relational layer is reactivated, `qiarchive` for content, `qisys` for sync state, and `qially` for semantic memory only if that future layer is activated. Durable, secure email attachments may be promoted to `qivault`.

## What Belongs in `public`

Only:

* `profiles` — user profile data tied to `auth.users`
* Legacy tables retained for compatibility (`todos`, `nods_page`)

**No new tables should be created in `public` schema.**

## Object Naming Contract

```text
{domain}_{name}_{QXXXXXX}.ext
```

* `domain` = lowercase domain prefix (e.g. `bbr4821`)
* `name` = normalized, human-readable base
* `QXXXXXX` = Q + 6 uppercase hex short code assigned by QiArchive
* `.ext` = lowercase file extension
