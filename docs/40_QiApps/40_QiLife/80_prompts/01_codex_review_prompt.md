# Codex Prompt: Documentation Consistency Review

You are an expert software architect and systems analyst specializing in local-first personal productivity systems. Your task is to perform a comprehensive validation check on the entire documentation suite for **QiLife**.

---

## Instructions

1.  **Read and Analyze** the files in the following directory:
    - `docs/` (Overview, Product, Architecture, Data Model, UI Flows, Modules, AI Layer, Deployment, and Decisions)

2.  **Verify Naming Rules**:
    Ensure the following concepts are used with exact case-sensitivity and terminology across all files. Flags any deviation (e.g., "qibit" or "lifedesk" lowercase, "project" instead of "Thread" when referring to ongoing cases, or "wiki" instead of "Context Dock"):
    - **QiLife** (The product)
    - **QiBit** (The atomic data unit)
    - **Personal LifeDesk** (The operating model)
    - **Timeline** (The spinal ledger)
    - **Bucket** (The top-level categorization domain)
    - **Thread** (The case/ongoing project)
    - **Action** (The task ledger item)
    - **Step** (The subtask list item)
    - **Context Dock** (The contextual sidebar widget)
    - **Ask QiLife** (The retrieval layer)

3.  **Check Structural Integrity**:
    - Do the database schema fields in `docs/30_data_model/` match the definitions and descriptions in the `docs/50_modules/` overview files?
    - Are the AI service functions defined in `docs/60_ai_layer/` consistent with how AI behaviors are referenced in `docs/50_modules/` module files?
    - Are the bucket code definitions consistent across information architecture, data models, and module specifications?

4.  **Detect Gaps & Risks**:
    - Identify any missing details in the database schemas or relationship maps.
    - Identify potential bottlenecks in the "Human-in-the-loop" AI review workflow.
    - Highlight any over-engineered components that violate the "Spine-first / No bank sync / No calendar sync" constraint of V1.

---

## Expected Output Format

Provide your evaluation as a Markdown report containing:
*   **Executive Summary**: Overall readiness score for the V1 build.
*   **Terminology Deviations**: Table showing file name, line number, incorrect term, and expected term.
*   **Structural Discrepancies**: Description of any misaligned tables, schemas, or service definitions.
*   **Gaps & Recommendations**: Bullet points outlining critical missing specs or logical loops.
*   **Build Readiness Status**: `[READY TO BUILD]` or `[REVISION REQUIRED]`.
