Understood. You want “Gina” as a local, persistent builder/operator living in your filesystem: you give a command, Gina plans, edits files, runs builds/tests, and leaves you artifacts and logs—without you babysitting.

Here’s the clean way to do that.

## What “Gina in my filesystem” actually is

A **local CLI + daemon** with:

* a **workspace** (where projects live)
* a **brain** (local LLM via Ollama/LM Studio, or hybrid)
* **hands** (file editor + command runner)
* **eyes** (verifier: build/test/lint/smoke)
* a **memory** (project notes, conventions, run history)

If you skip any of those, you get a toy.

---

## Architecture (practical, minimal, durable)

### 1) Install location

Put Gina here (Windows):

* `C:\QiOS_Local_Only\Gina\`

Recommended layout:

```
C:\QiOS_Local_Only\Gina\
  gina.exe / gina.ps1 (launcher)
  agent\
    gina.py
    config.yaml
    prompts\
    tools.py
    planner.py
    executor.py
    verifier.py
    memory.py
  runs\              # per-run logs + artifacts
  templates\         # your scaffolds (QiNote module viewer, Vite, etc.)
  policies\          # command allow/deny lists
  notes\             # “Gina memory” per project (markdown)
```

### 2) Invocation style (what you actually type)

Examples:

* `gina build "vite app: qially client portal shell"`
* `gina fix` (re-run verification and patch)
* `gina scaffold module 04_PRIMARY/10_datasets/10_banking/10_CashApp`
* `gina status` (shows last run + what’s broken)
* `gina doctor` (checks node/python/git/ollama)

### 3) Safety boundary (non-negotiable)

Gina should ONLY touch:

* allowed roots you define (e.g., `C:\QiOS_Local_Only\`)

And she should:

* refuse destructive commands by default (`rm`, `rmdir /s`, formatting disks, etc.)
* require a `--danger` flag for anything high-risk
* log every command and diff every file change

---

## The “Gina loop” (how she works every time)

1. **Plan**

* Produce a structured task list: files to create/edit, commands to run, checks to pass.

2. **Execute**

* Apply patches deterministically (no “rewrite the whole file” unless necessary)
* Scaffold using templates (your QiNote module viewer, repo skeletons, etc.)

3. **Verify**

* Run builds/tests (`npm run build`, `pytest`, etc.)
* Smoke-run if applicable

4. **Fix**

* If verify fails, parse the error and patch again
* Repeat until pass or iteration cap hit

5. **Ship**

* Leave you:

  * `runs/2026-01-07_.../log.txt`
  * `runs/.../diff.patch`
  * `runs/.../artifact.zip` (optional)

That’s “Gina in the filesystem.”

---

## Model options (local brain)

### Fastest: Ollama

* Runs local models and exposes `http://localhost:11434`
* Good for: planning + code edits + error fixing

Typical model picks (pragmatic):

* “bigger” for planning/code: 14B-ish class
* “smaller” for quick edits: 7B-ish

### Hybrid (optional)

Local by default, but can call cloud when you explicitly allow it for hard problems. This keeps you moving without forcing dependence.

---

## Gina’s “memory” (so she stays consistent)

You want consistency across repos/modules—so store rules per project:

* `notes/projects/<project_slug>.md`
* your conventions: folder structure, naming, preferred stack, “don’t touch X,” etc.

Also store global rules:

* your QiRepo top folders
* module templates
* preferred scripts
* your “QiDecimal / QID” conventions

This is how “Gina” stops acting like an amnesiac.

---

## What you should NOT do

* Don’t try to make her fully autonomous across your entire drive.
* Don’t start with “build anything.”
* Don’t skip verification/logging. That’s how you get silent broken junk.

---

## Concrete MVP you can implement first (1–2 days of real work)

**Gina v0.1**:

* CLI: `gina <command>`
* tools: file read/write/patch, run_cmd, git status
* local LLM call (Ollama)
* one template: **QiNote module lite viewer scaffold**
* verifier: node installed? run viewer build? link check?

Once that works, add:

* “Vite app scaffold”
* “repo organizer”
* “bulk rename / QID stamping”

---

## Your fastest next step (pick one)

I’m going to force clarity:

### Option A — “Gina the Builder” (best match for you)

She scaffolds modules/repos, updates templates, runs builds, fixes errors.

### Option B — “Gina the Sysadmin”

She organizes, inventories, audits, generates scripts, but doesn’t build apps much.

If you answer nothing, you clearly mean **Option A**.

---

## I can produce the actual starter repo now

Say:

* your OS (Windows yes)
* where the workspace root is (I’ll assume `C:\QiOS_Local_Only\`)
* local model runtime: **Ollama** or **LM Studio** (I’ll default to Ollama)

And I’ll give you:

* the folder tree
* the Python code for `gina.py` (planner/executor/verifier)
* a safe command runner
* logging + artifacts
* a first “module viewer scaffold” command

If you want this to feel like “Gina,” not “random script,” this is the path.
