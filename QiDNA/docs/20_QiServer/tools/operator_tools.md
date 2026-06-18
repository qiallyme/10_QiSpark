# Tools

Internal tools are developer and operator utilities. They are not user-facing. They automate, validate, or inspect system state.

## Current Tools

| Tool | Location | Purpose |
|---|---|---|
| enforce_structure.py | scripts/ | Validates repo structure and YAML schemas |

## QiLabs Toolbox Module Convention

- Standalone/proven tools must use folder-name-is-tool-name structure.
- Required files are `README.md`, `__init__.py`, `<tool_name>.py`, and `manifest.yaml`.
- Standalone/proven tools should live under the QiLabs toolbox or QiAccess local toolbox pattern rather than as loose standalone scripts.
- Final toolbox destination is generally `C:\QiLabs\toolbox\tools\<tool_name>\` unless the tool is intentionally repo-specific.
- Prototype scripts may begin temporarily under repo `tools\` only when they are explicitly marked as prototypes.
- Once a tool is promoted/proven, it must graduate into the toolbox module structure and should not remain as a loose standalone utility script directly under `tools\`.
- The tool manifest is required so agents and launchers can identify and use the tool.
- The README is required so humans and agents understand usage, safety, inputs, and outputs.
- Python tool files must include a commented intro near the top, immediately after the shebang if present, identifying filename, purpose/context, usage, inputs, outputs, safety, and owner.

## Aider Usage Rules

- Aider is installed under /srv/qios/tools/aider.
- Aider should be used inside cloned repos under /srv/qios/repos, not directly inside live runtime stack folders.
- qwen2.5-coder:3b is the preferred interactive Aider model.
- qwen2.5-coder:7b exists but is too heavy/slow for interactive CPU-only use.

## Ollama Usage Rules

- Ollama is installed on qiserver and locked to 127.0.0.1:11434.

## Legacy Tools (Quarantined)

*Note: mkdocs serve and pnpm db:migrate are now quarantined. MkDocs is superseded. Supabase is not active unless it has a specific job.*
