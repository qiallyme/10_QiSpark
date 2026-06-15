# QiLinks Bookmark Admin Plan

## Purpose

QiAccess/Homepage remains the display layer.

QiLinks is a small admin-only helper for managing Homepage configuration, starting with `qiaccess/config/bookmarks.yaml` so bookmark changes do not require direct YAML editing for every routine update.

QiLinks is not a replacement for Homepage, not a revival of the old React QiAccess portal, and not a public-facing application.

## Access Boundary

- QiLinks should be admin-only.
- Preferred access:
  - Tailscale-only
  - or Cloudflare Zero Trust protected
- It should not be exposed as a public editor on `access.qially.com` without an explicit later decision.

## Current Config Reality

Active Homepage config lives under:

- `qiaccess/config/settings.yaml`
- `qiaccess/config/services.yaml`
- `qiaccess/config/bookmarks.yaml`
- `qiaccess/config/widgets.yaml`
- `qiaccess/config/docker.yaml`

Current bookmarks are still placeholder-oriented, which makes bookmark editing a good first scope for a helper tool.

## Initial Scope

Initial QiLinks scope should be narrow:

- add bookmark
- edit bookmark
- delete bookmark
- choose or create bookmark group
- preview normalized bookmark data before write

This first version should update only `bookmarks.yaml`.

## Later Scope

Later scope can expand carefully into:

- `services.yaml`
- `widgets.yaml`
- icon selection / icon validation
- group management and reordering
- schema validation / linting
- import/export helpers
- access tags and environment-specific filtering

## Save Behavior

QiLinks should write YAML safely:

1. Read and parse the current `bookmarks.yaml`.
2. Normalize data into an internal bookmark model.
3. Create a timestamped backup before writing.
4. Write the updated YAML atomically where practical.
5. Preserve formatting and ordering where possible.

Recommended backup pattern:

- store backups under `qiaccess/config/_backups/`
- use a timestamped filename such as:
  - `bookmarks_2026-05-24T06-15-00.yaml`

Formatting note:

- Plain `PyYAML` is acceptable for a first CLI helper, but it may not preserve comments and exact formatting.
- If formatting preservation becomes important, move to a round-trip YAML library later.

## Validation Behavior

QiLinks should validate before and after write:

- parse current YAML before any edit
- reject invalid or incomplete bookmark records before write
- write to a temp path first when possible
- parse the newly written YAML again after write
- only replace the active file if the post-write parse succeeds

Minimum validation checks:

- `group` is present
- `name/title` is present
- `href` is present
- `href` uses a safe URL or approved scheme
- `abbr` and `icon` are optional, but Homepage rules should be respected

## Restart / Reload Behavior

Homepage behavior differs by config type:

- `settings.yaml`:
  - local docs say settings changes require regenerating static HTML, typically via the refresh icon in the lower-right UI
- local icons / images:
  - local docs say adding new image files may require a container restart
- `bookmarks.yaml`, `services.yaml`, `widgets.yaml`:
  - Homepage reads these configs through its config helpers and API routes
  - in practice, changes should be treated as requiring at least a Homepage revalidate/refresh cycle

Safe operational rule for QiLinks:

1. write YAML
2. validate write
3. call Homepage revalidate if the helper is colocated with the app
4. if visual state does not update, use the built-in Homepage refresh action
5. restart the container only when image or static asset behavior requires it

QiLinks should document this honestly rather than promising live hot-edit behavior everywhere.

## Proposed Bookmark Schema

Homepage bookmark YAML is group-based and compact, but QiLinks should use a clearer internal schema:

```yaml
group: External / Mobile Functions
name: Google Drive / QiNexus
href: https://drive.google.com/
icon: null
abbr: QD
description: QiNexus workspace placeholder
tags:
  - storage
  - qinexus
visibility:
  access: external
  notes: Public web link, daily-use surface
```

Recommended fields:

- `group`
- `name/title`
- `href`
- `icon`
- `abbr`
- `description`
- `tags`
- `visibility/access notes`

Mapping notes:

- `group`, `name`, `href`, `icon`, `abbr`, and `description` map naturally into Homepage YAML
- `tags` and `visibility/access notes` do not map directly into current Homepage bookmark rendering
- for now those extra fields should live in QiLinks metadata only, or later in a sidecar file if needed

## Proposed Interface

The first implementation should be a CLI or protected admin helper, not a public web app.

Suggested command shape:

- `qilinks list`
- `qilinks add`
- `qilinks edit`
- `qilinks delete`
- `qilinks backup`
- `qilinks validate`

Suggested edit flow:

1. select group
2. select bookmark or create new
3. edit fields
4. preview resulting YAML shape
5. backup
6. write
7. validate
8. optionally trigger Homepage revalidate

## Visual Map Generator Plan

The visual map should be generated, not hand-maintained.

Inputs:

- `qiaccess/config/bookmarks.yaml`
- `qiaccess/config/services.yaml`
- `qiaccess/config/widgets.yaml`
- optionally `qiaccess/config/settings.yaml` for title and group ordering context

Outputs:

- Mermaid mind map or flow map
- Markmap-compatible markdown

Write targets:

- `_audit/qiaccess_map.mmd`
- `_audit/qiaccess_map.md`

Generation behavior:

1. read YAML inputs
2. extract groups, bookmarks, services, and widgets
3. build a simple tree rooted at `QiAccess`
4. emit Mermaid and Markdown outputs
5. regenerate whenever config changes

The map should be treated as a derived artifact, not hand-edited source.

## Recommended Rollout

Phase 1:

- keep Homepage as-is
- add QiLinks CLI helper for bookmarks only
- add generated visual map output

Phase 2:

- add safe editing for `services.yaml`
- add validation and optional sidecar metadata

Phase 3:

- add a protected admin UI only if the CLI stops being sufficient

## Non-Goals

- no Homepage replacement
- no public bookmark editor
- no old QiAccess portal revival
- no direct server deployment work in this phase
