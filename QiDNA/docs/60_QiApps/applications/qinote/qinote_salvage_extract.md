# QiNote Salvage Extract

## Retired Project Carry-Forward Map

### Purpose

This document preserves the durable ideas, goals, constraints, and module requirements from the retiring project that should be carried forward into **QiNote**.

The extraction rule is simple:

**Preserve principles, architecture, workflows, and long-term goals. Do not preserve obsolete scaffolding, duplicate trees, or project-specific clutter.**

---

# 1. QiNote Identity

## 1.1 Definition

**QiNote is the local-first note, knowledge, memory, and retrieval layer of the Qi ecosystem.**

It is not merely a note-taking app. It is the system that turns personal, household, legal, financial, technical, and operational information into durable, searchable, structured knowledge.

## 1.2 Platform Role

QiNote belongs inside the broader QiOne / QiAccess / QiNexus ecosystem:

- **QiAccess** = front door, interface, and launchpad
- **QiNexus** = human workspace and source library
- **QiArchive** = AI memory pipeline, ingestion, extraction, chunking, embeddings, graph, and backups
- **QiLabs** = code, execution, tooling, and experiments
- **QiNote** = local-first knowledge, note, memory, and retrieval module
- **QiGraph** = graph, relationship visualization, and intelligence layer
- **Paperless-NGX** = document intake, OCR, and document processing plant
- **Qdrant** = vector search and semantic retrieval
- **Neo4j** = relationship graph
- **Ollama / Open WebUI** = local AI interaction layer

## 1.3 Core Positioning

QiNote should become the long-term engine for:

- atomic notes
- structured objects
- source-backed recall
- personal knowledge management
- AI-readable memory
- timeline reconstruction
- document intelligence
- graph-based relationships
- local-first private retrieval
- publishable and private knowledge views

Short-term tools like Obsidian, Capacities, Wiki.js, or static sites can be used as bridges, but QiNote is the eventual owned system.

---

# 2. Non-Negotiable Doctrine

## 2.1 Source Files Remain Truth

The canonical truth must remain in durable source files, documents, or structured records.

Derived systems must never become the only copy of truth.

Derived systems include:

- vector indexes
- graph indexes
- generated summaries
- AI memory
- dashboards
- search APIs
- static published views
- Graphify outputs
- admin panels

All derived objects must point back to source.

## 2.2 Local-First, Cloud-Backed

QiNote should be private and local-first by default.

Preferred model:

- local SSD or server cache for active processing
- Google Drive / QiNexus as the cloud-backed source library
- private qiserver runtime for services
- Tailscale / Cloudflare only for controlled access
- no public exposure unless explicitly intended

## 2.3 Human-Readable Names + Stable IDs

Files and notes should have clean names humans can understand, but every important object must also have stable machine identity.

Preferred principles:

- human-readable display names
- stable canonical IDs underneath
- short visible suffixes where useful
- metadata-first indexing
- deterministic naming where possible
- IDs that survive file moves and renames

## 2.4 Metadata Before Automation

Do not automate chaos.

QiNote should prioritize clean metadata, source identity, ingestion state, and object classification before advanced AI automation.

The AI layer should enrich and retrieve. It should not invent structure where none exists.

## 2.5 One Home Per Concern

Each concern needs a clear owner.

Examples:

- Documents and source assets live in QiNexus / QiArchive paths.
- Notes and knowledge objects live in QiNote.
- OCR intake belongs to Paperless-NGX.
- AI indexing belongs to QiArchive / ingestion services.
- Relationship mapping belongs to Neo4j / QiGraph.
- Semantic retrieval belongs to Qdrant.
- Front-door navigation belongs to QiAccess.

Avoid duplicate folder trees, duplicate registries, and multiple competing “truth” locations.

## 2.6 Derived Systems Must Reference Source

Every chunk, embedding, graph node, summary, and AI answer must be traceable back to source.

Minimum lineage fields:

- `source_id`
- `source_path`
- `document_id`
- `chunk_id`
- `hash`
- `created_at`
- `ingestion_run_id`
- `extraction_method`
- `status`

## 2.7 Lightweight ADRs

Architectural decisions should be recorded as lightweight ADRs when they affect long-term structure.

Use ADRs for:

- storage doctrine
- ingestion doctrine
- naming standards
- ID strategy
- exposure and security rules
- module ownership
- canonical pipeline changes

Do not bury major decisions in random chat notes.

---

# 3. Core QiNote Goals

## 3.1 Capture Fast, Structure Later

QiNote must support low-friction capture from multiple inputs:

- quick notes
- tasks and reminders
- care observations
- legal and finance notes
- links
- voice notes
- screenshots
- PDFs
- scans
- documents
- project notes
- journal entries

Capture should go to a safe inbox first, then be processed.

## 3.2 Turn Notes Into Objects

QiNote should not be only page-based. It should understand knowledge objects.

Core object ontology:

1. Person
2. Project
3. Document
4. Note / Idea
5. Task
6. Event
7. Topic / Concept
8. Source

Future objects may include:

- Account
- Vendor
- Case
- Asset
- Location
- Timeline Item
- Decision
- Evidence Item
- Routine
- System Component

## 3.3 Make Recall Source-Backed

The goal is not generic chat. The goal is accurate recall.

QiNote should answer questions like:

- “What did I decide about this?”
- “Where is the source document?”
- “What changed since last time?”
- “What evidence supports this?”
- “What tasks came from this note?”
- “What people, projects, and documents are connected?”
- “What is the timeline?”

Every serious answer should be grounded in source references.

## 3.4 Support Timeline Reconstruction

QiNote should help reconstruct timelines from:

- notes
- documents
- emails
- calendar events
- logs
- screenshots
- receipts
- legal filings
- project updates
- journal entries

Timeline support is central, especially for legal, finance, care, and project work.

## 3.5 Enable Private AI Memory

QiNote should become the user-owned memory layer.

Not vague “AI remembers things.” Real memory means:

- source-backed notes
- structured objects
- canonical IDs
- embeddings
- graph relationships
- ingestion logs
- confidence states
- review workflows
- privacy controls

---

# 4. QiNote Architecture to Preserve

## 4.1 High-Level Architecture

Preferred spine:

Source files / notes / docs  
→ detect  
→ register canonical identity  
→ normalize filename  
→ extract text  
→ enrich metadata  
→ chunk  
→ embed locally  
→ store vectors  
→ create or update graph nodes  
→ expose searchable API  
→ show in QiAccess / QiNote UI

## 4.2 Canonical Pipeline

Canonical ingestion flow:

1. Source
2. Detect
3. Resolve domain / namespace
4. Register in QiArchive
5. Assign canonical identity
6. Assign short visible code
7. Normalize filename
8. Extract / inspect
9. Enrich metadata
10. Chunk
11. Embed locally
12. Index in vector store
13. Route / review / act

## 4.3 State Model

Every item should have a visible processing state.

Recommended states:

- `detected`
- `registered`
- `normalized`
- `extracted`
- `enriched`
- `chunked`
- `embedded`
- `indexed`
- `review_pending`
- `routed`
- `finalized`
- `failed`

Failures must be:

- visible
- stateful
- retryable
- tied to canonical IDs

No silent failure. Silent failure is trash. Burn it.

## 4.4 Ingestion Ledger

Every ingestion run should be logged.

Minimum fields:

- `ingestion_run_id`
- `source_id`
- `source_path`
- `source_hash`
- `file_size`
- `detected_type`
- `extraction_method`
- `chunk_count`
- `embedding_model`
- `vector_collection`
- `graph_update_status`
- `started_at`
- `completed_at`
- `status`
- `error_message`

## 4.5 Stable IDs

Every document and chunk needs stable identity.

Minimum identity fields:

- `source_id`
- `document_id`
- `chunk_id`
- `canonical_path`
- `original_path`
- `hash`
- `version`
- `qicode` or short code, where applicable

## 4.6 Chunking Rules

Chunking should preserve traceability.

Each chunk should include:

- `chunk_id`
- `document_id`
- `source_id`
- `chunk_index`
- text
- heading or context, if available
- page number, if available
- byte or character offsets, if available
- source path
- `created_at`
- embedding status

Chunks should never float loose without source context.

---

# 5. Paperless-NGX Role

## 5.1 Paperless Is Intake, Not the Brain

Paperless-NGX should be used as the document engine for:

- scanning
- OCR
- dedupe support
- document metadata
- document storage
- searchable archive

Paperless should not become the full AI system.

## 5.2 Downstream AI Pipeline

Paperless should feed:

1. Canonical SQL registry
2. Text extraction
3. Chunks
4. Qdrant embeddings
5. Neo4j graph
6. QiNote / QiAccess views

## 5.3 Do Not Run Heavy AI Inside Paperless

Rule:

**Paperless does Paperless. The AI pipeline does AI pipeline.**

Do not overload the Paperless container with heavy AI, graph, or embedding responsibilities.

## 5.4 Test Before Bulk Import

Before mass importing documents:

- test with 10 documents
- confirm OCR quality
- confirm metadata rules
- confirm filename format
- confirm dedupe behavior
- confirm storage paths
- confirm export and recovery strategy

Do not feed the beast a mountain of chaos and then act shocked when it burps fire.

---

# 6. QiNexus Relationship

## 6.1 QiNexus Is the Source Library

QiNexus is the human-facing source library and workspace.

QiNote should read from and write back to QiNexus-compatible structures where appropriate.

## 6.2 Preferred Root Buckets

Canonical QiNexus root order:

0. inbox
1. workbench
2. timeline
3. life
4. people
5. business
6. finance
7. legal
8. tech
9. assets
10. data
11. reference
12. archive
13. system

Numbered variant:

- `00_inbox`
- `01_workbench`
- `02_timeline`
- `03_life`
- `04_people`
- `05_business`
- `06_finance`
- `07_legal`
- `08_tech`
- `09_assets`
- `10_data`
- `11_reference`
- `12_archive`
- `13_system`

## 6.3 QiNexus Is Not QiNote

QiNexus stores and organizes the source material.

QiNote interprets, links, recalls, and works with that material.

Do not collapse them into one vague folder blob.

---

# 7. QiAccess Relationship

## 7.1 QiAccess Is the Front Door

QiAccess should expose QiNote through clean modules and links.

QiAccess root doctrine:

- Home
- Start
- Capture
- Knowledge
- Memory
- Insights
- System

Do not add extra top-level sections casually.

## 7.2 QiNote Views in QiAccess

QiAccess can provide:

- capture form
- knowledge browser
- memory search
- graph viewer
- timeline view
- ingestion status page
- recent notes
- source lookup
- admin and system diagnostics

QiAccess should not become the source of truth.

---

# 8. Capture Model to Preserve

## 8.1 Capture Modes

Known useful capture modes:

- quick note
- task / reminder
- care observation
- legal / finance note
- link save

## 8.2 Capture Targets

Recommended targets:

- QiNexus inbox
- Paperless
- Knowledge
- System storage
- Timeline
- Finance
- Legal
- Tech
- Reference

## 8.3 Capture Doctrine

Capture should be fast and forgiving.

Processing should be structured and controlled.

Flow:

Capture → Inbox → Classify → Enrich → Route → Link → Index → Review

---

# 9. Naming, IDs, and File Doctrine

## 9.1 Naming Principle

Use short, readable names with stable machine identity underneath.

## 9.2 Filename Direction

Preserve this direction:

- readable normalized base name
- domain prefix, where useful
- short visible code, where useful
- full identity in metadata / registry

## 9.3 Short Code Direction

A prior useful convention:

- short visible file suffix = `Q` + 6 uppercase hex characters

Example pattern:

- `{domain_prefix}_{normalized_base}_{short_code}.{ext}`

## 9.4 Date Handling

Dates should be embedded where they add clarity, ordering, or retrieval value.

Acceptable date formats:

- `YYYY-MM-DD` for readable files
- `YYYYMMDD` or `YYMMDD` for compact codes

For standalone Markdown files, preferred format:

- `yyyy-mm-dd_{title_name}.md`

## 9.5 Folder Numbering

All important folder systems should be numbered so order is intentional, not alphabetical.

Use decimal-style or numeric prefixes where useful.

---

# 10. Markdown and Publishing Doctrine

## 10.1 Markdown-First

QiNote should remain Markdown-first where practical.

Benefits:

- readable without app lock-in
- Git-friendly
- AI-indexable
- portable
- easy to publish
- easy to back up
- compatible with Obsidian, Wiki.js, and static site bridges

## 10.2 Publish Rules

Default privacy is private.

Only publish files with explicit approval:

`publish: true`

Never publish:

- secrets
- temp files
- unapproved drafts
- private notes
- raw evidence unless intentionally shared
- system credentials
- ingestion logs containing sensitive paths or keys

## 10.3 Static Export

QiNote should support future static export and publishing for approved content.

Possible consumers:

- QiAccess static site
- Cloudflare Pages
- public knowledge pages
- family / household docs
- client-safe documentation

---

# 11. Graph and RAG Doctrine

## 11.1 Graphify Role

Graphify or similar tools are useful as mapping and visualization layers.

They are not sources of truth.

Use them to generate:

- `graph.html`
- `graph.json`
- `GRAPH_REPORT.md`
- dependency maps
- file relationship views

Preserve Markdown, files, and registry records as truth.

## 11.2 Qdrant Role

Qdrant stores semantic embeddings for retrieval.

It should answer:

- similar notes
- related documents
- semantic search
- memory recall
- context assembly

## 11.3 Neo4j Role

Neo4j stores relationships.

It should answer:

- who is connected to what
- which projects touch which files
- which decisions came from which events
- legal, finance, and care timeline relationships
- system dependency graphs

## 11.4 RAG Rule

RAG must be source-backed.

No answer should pretend confidence without retrievable source context.

Every serious AI response should support:

- source references
- confidence / uncertainty
- date awareness
- object links
- chunk lineage

---

# 12. Structured Data Doctrine

## 12.1 SQL Registry

A canonical SQL registry should track confirmed structured data.

Use SQL / Postgres / NocoDB for things like:

- document registry
- ingestion ledger
- accounts
- vendors
- finance data
- task records
- event records
- source metadata
- object relationships where graph storage is not required

## 12.2 Do Not Put Everything in SQL

Not every Markdown file needs to be converted into database rows.

Rule:

- Source content can stay as files.
- Confirmed metadata goes into the registry.
- Relationships go into the graph.
- Embeddings go into the vector store.
- The UI reads from all layers.

---

# 13. Security and Exposure Rules

## 13.1 Private by Default

QiNote should assume private data.

Admin tools should be local or private unless explicitly exposed.

## 13.2 Service Exposure

Preferred exposure model:

- localhost-bound services
- Tailscale for personal device access
- Cloudflare only for approved public or static surfaces
- no broad public admin dashboards
- secrets stored in `.env`
- no credentials committed to repos

## 13.3 Ollama Warning

Ollama should generally be localhost-only unless intentionally opened through LAN or Tailscale with firewall controls.

Preferred:

- `OLLAMA_HOST=127.0.0.1:11434`

Avoid casual `0.0.0.0` exposure.

---

# 14. UI / UX Goals

## 14.1 QiNote Should Feel Like a Calm Control Room

QiNote should not feel like a cluttered admin panel.

Core UI needs:

- quick capture
- search
- source lookup
- recent activity
- timeline
- graph view
- object view
- ingestion status
- review queue
- publish / private controls

## 14.2 Low Cognitive Load

The interface should support ADHD-friendly workflows:

- fast capture
- minimal required fields
- progressive enrichment
- clear next action
- visible status
- no mystery queues
- no hidden failure
- filters instead of folder digging

## 14.3 Review Queue

QiNote needs a human review layer.

The review queue should show:

- unclassified captures
- failed ingestions
- low-confidence extracted metadata
- duplicate candidates
- source conflicts
- publish candidates
- orphan chunks
- graph relationship suggestions

---

# 15. QiNote Module Requirements

## 15.1 MVP Requirements

QiNote MVP should include:

1. Quick capture inbox
2. Markdown-backed notes
3. Basic object registry
4. Source / document registry
5. Local search
6. Paperless document link support
7. Ingestion ledger
8. Chunking pipeline
9. Qdrant embedding search
10. Neo4j relationship sync
11. Admin status UI
12. Review queue
13. Exportable Markdown
14. Source-backed AI answer endpoint

## 15.2 Later Requirements

Later versions can add:

- voice capture
- mobile PWA
- timeline builder
- graph explorer
- automated summaries
- calendar and email ingestion
- local LLM chat interface
- publishable knowledge pages
- family and care dashboards
- legal and evidence bundles
- finance / source reconciliation
- personal memory assistant

---

# 16. Suggested QiNote Folder / Module Shape

This is a proposed carry-forward shape, not a rigid final tree.

## 16.1 Code / App Side

- `apps/qinote/`
  - frontend UI
  - capture interface
  - note browser
  - search views
  - review queue
  - graph / timeline views

- `services/ai_ingestion/`
  - source detection
  - text extraction
  - chunking
  - embeddings
  - Qdrant sync
  - Neo4j sync
  - ingestion ledger

- `services/qinote_api/`
  - object API
  - notes API
  - search API
  - source lookup API
  - AI answer endpoint

- `docs/qinote/`
  - doctrine
  - architecture
  - object model
  - ingestion contract
  - naming contract
  - ADRs
  - runbooks

## 16.2 Knowledge Side

- `00_inbox/`
- `01_workbench/`
- `02_timeline/`
- `03_life/`
- `04_people/`
- `05_business/`
- `06_finance/`
- `07_legal/`
- `08_tech/`
- `09_assets/`
- `10_data/`
- `11_reference/`
- `12_archive/`
- `13_system/`

---

# 17. What to Archive From the Retired Project

Archive but do not actively carry forward:

- duplicate folder trees
- old business blueprint scaffolding
- vague `nexus_core` terminology
- obsolete route structures
- experimental naming that conflicts with QiNexus / QiArchive / QiNote doctrine
- anything that makes QiAccess the source of truth
- any pipeline that skips canonical IDs
- any AI memory concept without source references
- any public publishing flow without `publish: true`

Recommended archive destination:

- `docs/legacy/Legacy_QiOS_Business_Blueprint_Extracts.md`

---

# 18. What to Preserve as Active QiNote Doctrine

Preserve these as active doctrine:

1. QiNote is the local-first knowledge and memory layer.
2. Source files remain truth.
3. Derived indexes must point to source.
4. QiArchive owns the ingestion and memory pipeline.
5. QiNexus is the human source workspace.
6. QiAccess is the front door.
7. Paperless handles OCR and document intake.
8. Qdrant handles semantic retrieval.
9. Neo4j handles relationships.
10. Metadata comes before automation.
11. Stable IDs are mandatory.
12. Every ingestion run is logged.
13. Every chunk is traceable.
14. Failures must be visible and retryable.
15. Markdown remains the portable base layer.
16. Publishing is private by default and explicit only.
17. Folder order should be intentional and numbered.
18. Object-based notes matter more than page clutter.
19. Timeline reconstruction is a core use case.
20. AI recall must be grounded, not vibes in a trench coat.

---

# 19. Recommended Next Build Order

## Phase 1 — Freeze Doctrine

Create or update:

- `docs/qinote/00_readme.md`
- `docs/qinote/10_doctrine.md`
- `docs/qinote/20_architecture.md`
- `docs/qinote/30_object_model.md`
- `docs/qinote/40_ingestion_pipeline.md`
- `docs/qinote/50_security_exposure.md`
- `docs/qinote/60_roadmap.md`

## Phase 2 — Build the Ingestion Spine

Build:

- source registry
- ingestion ledger
- text extractor
- chunker
- embedding worker
- Qdrant writer
- Neo4j writer
- retryable failure states

## Phase 3 — Build the QiNote UI

Build:

- quick capture
- inbox
- note list
- document / source view
- search
- review queue
- ingestion status

## Phase 4 — Add AI Recall

Build:

- source-backed ask endpoint
- context assembler
- citation / source viewer
- confidence labels
- memory search

## Phase 5 — Add Graph + Timeline

Build:

- relationship viewer
- timeline builder
- object graph
- project / person / source maps

---

# 20. Codex Transfer Prompt

Use this when telling Codex to implement the carry-forward QiNote module:

> We are retiring an older project and preserving only the durable QiNote architecture. Build QiNote as the local-first knowledge, notes, memory, and retrieval module of the Qi ecosystem. Source files remain truth. Derived systems must point back to source. QiNexus is the human source workspace, QiArchive owns the ingestion and memory pipeline, QiAccess is the front door, Paperless-NGX handles document OCR and intake, Qdrant handles vector search, and Neo4j handles relationships. Build a simple, readable MVP with a source registry, ingestion ledger, stable IDs, chunking, local embeddings, Qdrant indexing, Neo4j graph sync, review queue, Markdown-backed notes, quick capture, and source-backed AI answer endpoint. Keep admin and private services local or Tailscale-only. Use `.env` for secrets. Prioritize a working pipeline over overengineering. Every document and chunk must have `source_id`, `document_id`, `chunk_id`, `source_path`, `hash`, `ingestion_run_id`, and `status`. Failures must be visible, stateful, retryable, and tied to canonical IDs.

---

# 21. Final North Star

QiNote should become the system where captured reality becomes structured memory.

Not another notes app.

A private, local-first, source-backed knowledge engine that can answer:

- what happened
- what matters
- where the proof is
- what connects
- what changed
- what needs action
- what should be remembered

