---
record_type: dev_session
schema_version: 1.0
session_id: DEV-20260516-directory-markmind-mapper
date: 2026-05-16
project: QiOne Toolbox / QiAccess Start
repo: c:\QiLabs\toolbox
branch:
feature_area: sys_directory_markmind_mapper
tooling:
  - Python
  - Tkinter
  - QiOne Desktop Tools
  - BaseTool
  - Markmind
  - Markmap
status: planned
owner: QiLabs
created_by: ChatGPT
source: chat_session
tags:
  - toolbox
  - sys
  - qione
  - directory-map
  - markmind
  - documentation
related_files:
  - tools/sys/directory_markmind_mapper/directory_markmind_mapper.py
  - tools/sys/directory_markmind_mapper/README.md
  - tools/sys/directory_markmind_mapper/tool_manifest.yaml
related_tables:
  - dev_history
related_tools:
  - QiOne Desktop Tools
---

# Dev Session: Directory Markmind Mapper Toolbox Tool

## 01. Session Identity

| Field | Value |
|---|---|
| Date | 2026-05-16 |
| Project | QiOne Toolbox / QiAccess Start |
| Repo | `c:\QiLabs\toolbox` |
| Branch | TBD |
| Feature Area | `sys_directory_markmind_mapper` |
| Status | Planned |
| Owner | QiLabs |
| Session Type | Toolbox utility build |

## 02. Purpose

Build a QiOne Desktop Tools utility that walks a selected root directory and generates a Markmind/Markmap-friendly Markdown file showing the directory tree.

The tool is intended to make repo/app/folder structure review faster, cleaner, and repeatable.

## 03. Context

The user wants a local toolbox tool, not a loose script.

The tool must follow the established QiOne toolbox pattern:

- module class inherits from `BaseTool`
- loaded by the toolbox build system
- launched from `main_ui.py`
- receives `target_path`, `is_live`, `log`, and `prog` through `execute()`
- supports dry-run and live execution
- provides its own UI through `build_ui()`

The user provided `rule_tester.py` as the pattern reference.

## 04. Decisions Made

| Decision | Reason | Status |
|---|---|---|
| Build as QiOne toolbox module | Matches existing toolbox architecture | Accepted |
| Place in `tools/sys/directory_markmind_mapper/` | This is a system/file-structure documentation tool, not a dev-only tester | Accepted |
| Use `DirectoryMarkmindMapperTool(BaseTool)` | Keeps module discoverable by the toolbox UI | Accepted |
| Generate Markdown with YAML front matter | Supports Markmind/Markmap review and future indexing | Accepted |
| Skip build artifacts by default | Prevents `node_modules`, `dist`, `.next`, etc. from polluting maps | Accepted |
| Write only generated Markdown output | Keeps tool safe and read-only against source directories | Accepted |
| Add manifest YAML | Enables future agent/toolbox discovery | Accepted |

## 05. Files / Folders Affected

| Path | Action | Notes |
|---|---|---|
| `tools/sys/directory_markmind_mapper/` | create | New toolbox tool folder |
| `tools/sys/directory_markmind_mapper/directory_markmind_mapper.py` | create | Main tool module |
| `tools/sys/directory_markmind_mapper/README.md` | create | Usage and safety documentation |
| `tools/sys/directory_markmind_mapper/tool_manifest.yaml` | create | Toolbox metadata manifest |

## 06. Database / Schema Notes

No application database changes are required for the mapper tool itself.

However, the session revealed a need for a durable development history system inside Supabase.

Recommended future table:

`public.dev_history`

Purpose:

- store development decisions
- record prompts
- track files affected
- preserve implementation history
- connect markdown dev session docs to structured searchable records

## 07. Implementation Plan

### Step 1

Create the tool folder:

`tools/sys/directory_markmind_mapper/`

### Step 2

Create `directory_markmind_mapper.py` using the `BaseTool` pattern.

Required methods:

- `__init__`
- `get_name`
- `build_ui`
- `execute`

### Step 3

Add UI options:

- include files
- include build/dependency artifacts
- include YAML metadata
- max depth
- output folder
- output filename
- extra excluded folders
- extra excluded files
- extra excluded extensions

### Step 4

Implement scanning behavior:

- walk selected `target_path`
- skip junk folders by default
- skip junk files by default
- respect max depth
- respect cancellation
- log progress

### Step 5

Generate Markdown output:

- YAML front matter
- title
- generated timestamp
- root path
- nested directory tree

### Step 6

Create `README.md` and `tool_manifest.yaml`.

### Step 7

Run through QiOne Desktop Tools UI.

Validate:

- dry run writes nothing
- live run writes Markdown
- build artifacts are skipped
- files can be included/excluded
- output opens cleanly in Markmind/Markmap-compatible viewers

## 08. Code / Prompt Artifacts

### Codex Prompt

Create a new QiOne toolbox tool module using the existing BaseTool pattern.

Create this folder:

`tools/sys/directory_markmind_mapper/`

Create these files:

- `directory_markmind_mapper.py`
- `README.md`
- `tool_manifest.yaml`

The Python module must follow this structure:

- Header comments:
  - `# file`
  - `# purpose`
  - `# usage`
  - `# inputs`
  - `# outputs`
  - `# safety`
  - `# owner`
- Import `BaseTool` from `core.base_tool`
- Define class `DirectoryMarkmindMapperTool(BaseTool)`
- Implement:
  - `__init__`
  - `get_name`
  - `build_ui`
  - `execute`

Goal:

The tool should walk the user-selected target directory from the QiOne Desktop Tools UI and generate a Markmind/Markmap-friendly Markdown directory tree.

Behavior:

1. The toolbox shell provides `target_path` to `execute(target_path, is_live, log, prog)`.
2. In dry run mode, show selected config but do not write output.
3. In live mode, generate the Markdown output file.
4. Default output filename: `YYYY-MM-DD_directory_map_{root_slug}.md`
5. Default output folder: selected target root, unless user chooses another output folder.
6. Include YAML front matter unless user disables it.
7. Include files by default, but allow folders-only mode.
8. Skip build/dependency junk folders by default:
   `.git`, `node_modules`, `dist`, `build`, `.next`, `coverage`, `__pycache__`, `.venv`, `.cache`, `logs`, `tmp`
9. Skip junk files:
   `.DS_Store`, `Thumbs.db`, `desktop.ini`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`
10. Allow extra excluded folders, files, and extensions through UI text areas.
11. Allow max depth through UI.
12. Support `cancel_requested` during scanning.
13. Use only Python standard library.
14. Do not delete, move, rename, or modify source files.
15. Write only the generated Markdown output file.

Keep the implementation surgical and consistent with the existing `rule_tester.py` style.

## 09. Risks / Watch Items

| Risk | Why It Matters | Mitigation |
|---|---|---|
| Tool gets built as loose CLI script | Would not fit QiOne toolbox UI | Must inherit `BaseTool` |
| Scans huge build folders | Output becomes useless and slow | Skip build artifacts by default |
| Output gets written somewhere confusing | User may lose generated file | Default output to selected root and log full path |
| Too much UI clutter | Tool becomes annoying to use | Keep options simple |
| Cancelling does not stop scan | Bad UX on large folders | Check `cancel_requested` during recursion |

## 10. Validation Checklist

- [ ] Tool appears in QiOne Desktop Tools
- [ ] Tool name displays as `🗺️ Directory Markmind Mapper`
- [ ] Dry run does not write a file
- [ ] Live run writes a Markdown file
- [ ] Output filename defaults correctly
- [ ] Output folder override works
- [ ] `node_modules` is skipped by default
- [ ] `.git` is skipped by default
- [ ] Files can be excluded
- [ ] Folders-only mode works
- [ ] Max depth works
- [ ] Markdown opens cleanly in Markmind/Markmap-compatible viewer
- [ ] No source files are modified

## 11. Final Outcome

Planned tool architecture and implementation prompt completed.

The tool should be created as:

`tools/sys/directory_markmind_mapper/`

with:

- `directory_markmind_mapper.py`
- `README.md`
- `tool_manifest.yaml`

## 12. Next Actions

| Priority | Action | Owner | Notes |
|---|---|---|---|
| P1 | Have Codex create the toolbox module | Cody / Codex | Use the prompt above |
| P1 | Run tool against `c:\QiLabs\_QiAccess_Start\src` | Cody | Validate output |
| P2 | Save generated map to QiAccess docs | Cody | Use as structure review artifact |
| P2 | Add Supabase `dev_history` table | Cody / Codex | Store future session records |
| P3 | Add export/import between Markdown dev docs and Supabase | Future | Useful but not needed today |

## 13. Restart Prompt

Use this to resume later:

> We were building a QiOne toolbox tool called Directory Markmind Mapper. It belongs at `tools/sys/directory_markmind_mapper/`, inherits from `BaseTool`, and generates a Markmind/Markmap-friendly Markdown file from a selected directory tree. The next step is to have Codex create the module files and test it against `c:\QiLabs\_QiAccess_Start\src`.
