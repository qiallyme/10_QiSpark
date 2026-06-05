Perfect. Now we’re locked in.

Here’s your final Codex prompt with your actual repo already inserted, ready to paste and run:

⸻

You are working inside the QiDNA repository.

Repository:
https://github.com/qiallyme/_QiOS_DNA.git

You already have access via Git integration.

PRIMARY OBJECTIVE

Completely clean, normalize, and rebuild the QiDNA repository into a single, coherent, structured source of truth that mirrors the actual system architecture.

CRITICAL BEHAVIOR RULES

1. Do not leave old and new content side-by-side
2. Do not create duplicate structures
3. Do not keep old versions in place
4. Do not scatter cleaned content across existing folders

Instead:

All existing content must be moved into a single folder:

/legacy_intake/

This is a temporary holding zone.

STEP 1 — LEGACY ISOLATION

Move all existing folders and documents into:

/legacy_intake/

Except:

* config files (docs.json, mintlify config, etc.)
* root README (optional)

Do not delete anything yet.

STEP 2 — REBUILD STRUCTURE FROM SCRATCH

Create a clean structure that mirrors the real system exactly.

Top-level folders must match system layers:

01_QiDNA
10_QiAccess
20_QiSystem
30_QiServer
40_QiCapture
50_QiNexus
60_QiApp_QiLife
70_QiConnect

STRUCTURE RULE

QiDNA must mirror the system.

If something exists in a system layer, its documentation must exist in the matching folder.

Do not place core documentation in abstract-only folders like Architecture or Modules.

Navigation must follow location-based logic, not conceptual lookup.

STEP 3 — INTERNAL STRUCTURE PER FOLDER

Inside each system folder, create:

overview.md
responsibilities.md
flows.md
structure.md
notes.md (optional)

Each file should be clear, minimal, and specific to that layer.

STEP 4 — QIEOS DOCTRINE

Create:

01_QiDNA/QiEOS/

Move all doctrine, philosophy, decisions, and system reasoning into this folder.

This is the only location for system-level reasoning and “why”.

STEP 5 — CONSOLIDATION

From /legacy_intake/:

* extract useful content
* merge duplicates
* eliminate overlap
* resolve contradictions
* rewrite for clarity

Move cleaned content into the new mirrored structure.

CONSOLIDATION RULE

If two documents overlap:

* merge into one
* remove redundancy

There must be one clear source of truth per concept.

STEP 6 — SYSTEM MODEL

Document clearly:

QiAccess → QiLife → (QiSystem + QiNexus + QiCapture + QiConnect)

This must be visible and consistent across documentation.

STEP 7 — DOCS NAVIGATION

Update docs.json or equivalent so the documentation site reflects:

* mirrored system structure
* clean hierarchy
* no legacy clutter

STEP 8 — SELF-AUDIT (CRITICAL)

Before finalizing:

Audit this entire operation, including these instructions.

Check for:

* incorrect or inconsistent folder names
* missing system layers
* mismatches between repo structure and documentation
* anything that violates the mirror principle

If something in this prompt is wrong, incomplete, or inconsistent with the system:

* correct it
* proceed with the corrected version

Do not blindly follow incorrect instructions.

FINAL STATE REQUIREMENTS

* no duplicate documents
* no conflicting definitions
* no legacy structure outside /legacy_intake/
* mirrored folder hierarchy
* one clear document per concept
* documentation matches real system layout

CRITICAL RULE

If something is unclear:

* align it to the system model
* simplify it
* do not invent new architecture

END GOAL

QiDNA becomes a system where any question can be answered by navigating to the exact matching folder and reading one clear document.

DO NOT

* redesign the system
* rename system layers
* introduce new abstractions
* leave legacy clutter in active folders

Proceed step-by-step and restructure the repository accordingly.

⸻

🔥 What you do next

1. Paste this into Codex
2. Let it run
3. Don’t interrupt it halfway
4. Review output ONLY after it finishes

⸻

🔴 What I want you to look for after

When it’s done, check:

* Does it feel like “kitchen → pot → spoon”?
* Can you navigate without thinking?
* Did it accidentally rename anything?
* Did it leave junk outside legacy_intake?

⸻

When you get the result, bring it back.

That’s where we do the final tightening pass and make it bulletproof.