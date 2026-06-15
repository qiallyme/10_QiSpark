# QiLinks Admin And Visual Map Plan

Date: 2026-05-24

## Objective

Define a minimal admin/helper path for Homepage bookmark management without turning QiAccess into a custom application again.

## Config Inspected

- `qiaccess/config/bookmarks.yaml`
- `qiaccess/config/services.yaml`
- `qiaccess/config/widgets.yaml`
- `qiaccess/config/settings.yaml`

## Reload / Revalidate Findings

- Upstream local docs state that `settings.yaml` changes require static regeneration, typically via the Homepage refresh icon.
- Upstream local docs also state that adding local image assets may require a container restart.
- Local repo code confirms a revalidate endpoint exists at `/api/revalidate`.
- For QiLinks planning, bookmark edits should be treated as:
  - write
  - validate
  - trigger revalidate / refresh
  - restart only if static asset behavior requires it

## Conclusions

- Homepage remains the display/runtime layer.
- QiLinks should start as a tiny admin-only helper around `bookmarks.yaml`.
- The helper should not be public.
- The visual map should be generated from Homepage config, not maintained by hand.

## Access Model

- Preferred protection:
  - Tailscale-only
  - or Cloudflare Zero Trust protected
- No public unauthenticated bookmark editor

## Bookmark Admin Scope

Phase 1:

- add bookmark
- edit bookmark
- delete bookmark
- move bookmark between groups
- backup before write
- YAML validation before and after write

Phase 2:

- group ordering
- icon selection
- tags / access metadata sidecar
- `services.yaml` editing
- `widgets.yaml` editing

## Homepage Reload Notes

- `settings.yaml` changes require Homepage revalidation / static regeneration per upstream docs.
- local icons/images may require container restart per upstream docs.
- bookmark/service/widget edits should be treated as requiring at least a refresh or revalidate step.

## Prototype Added

- `tools/qiaccess_map_generator/generate_qiaccess_map.py`

Outputs:

- `_audit/qiaccess_map.mmd`
- `_audit/qiaccess_map.md`

Behavior:

- reads `qiaccess/config/*.yaml`
- extracts bookmarks, services, and widgets
- emits a generated Mermaid mind map and Markdown summary

Current generated artifact summary:

- bookmark groups: `3`
- bookmarks: `12`
- service groups: `7`
- services: `24`
- widgets: `3`

## What Was Not Built

- no web editor
- no server deployment
- no public admin route
- no direct write helper for YAML edits yet

## Remaining Work

- no bookmark editor has been built yet
- no backup-writing helper exists yet
- no YAML-preserving round-trip editor exists yet
- no protected admin surface exists yet

## Recommendation

Build QiLinks as a CLI-first or private helper-first tool before any UI work.
