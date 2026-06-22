# QiOS and QiAccess Start: Consolidated Doctrine

## Overview & Operating Truth

QiOS is the master operating system for the Qi ecosystem. Its primary purpose is to reduce drift, preserve system memory, and keep implementation repositories aligned with a single source of doctrine. QiAccess Start inherits the strongest aspects of this constitutional model while securely locking the active portal's doctrine to actual daily use.

> **Legacy Note:** Portions of the original QiOS Core Doctrine are superseded, having been reconciled on 2026-06-12. Operating truths and promotion rules were moved to `01_QiDNA/QiEOS/_QiEOS.md`, and layer names were superseded by ADR-0017. The legacy material is retained in place purely as hierarchy-preserving archive evidence.
> 
> 

---

## Layer Definitions & System Structure

The system is organized into specific layers, each owning a dedicated domain of the ecosystem:

* **QiOS:** The entire ecosystem.


* **QiEOS:** The origin brain containing doctrine, decisions, receipts, and the system map.


* **QiOS Start / QiAccess:** The cockpit, which serves as the front door, launcher, main UI, docs surface, and access dashboard.


* **QiSystem:** The rules layer responsible for schemas, naming, metadata, database doctrine, and lifecycle rules.


* **QiServer:** The runtime and infrastructure layer.


* **QiCapture:** The ingestion and processing layer.


* **QiNexus:** The storage and workspace model.


* **QiApps:** Standalone apps, tools, and sites.


* **QiConnect:** Integrations, APIs, workers, and connector surfaces.



### Directory Progression

The physical structure mirrors these responsibilities.

* **Primary Documents:** Includes the QiOS Core Doctrine, QiAccess Start Blueprint, and Governance README.


* **Mirror Subfolders:** Structured chronologically as 10 Governance (The Soul), 20 Structure (The Body), 30 Data (The Blood), 40 Service Apps (The Function), 50 Operations (The Action), 60 Knowledge (The Memory), and 70 Assets (The Resources).


* **Compute Models:** Workflow definitions and distributed compute resources are kept in the `Workers` and `Workflows` folders.



---

## Core Constitutional Principles

These foundational rules govern the structural integrity of the entire ecosystem and remain non-negotiable:

* There must be exactly one canonical identity per object.


* There must be one clear home per concern.


* Metadata must precede automation, meaning automation relies on minimum structure first.


* Lineage must survive transformation.


* Naming must be human-readable while maintaining machine-stable identity.


* Architecture should be local-first where appropriate and cloud-backed where strategic.


* Systems must compose cleanly without collision.


* Exposure boundaries must be explicit.


* Any structural changes must earn ADR review.


* Identity cannot be redefined downstream.


* Logic must not be silently duplicated across apps, workers, and scripts.


* Important files and system records require clear ownership.



---

## QiAccess Start Operating Principles

The active portal operates under a strict subset of design and UX principles:

* **QiAccess is the Portal:** The application functions as the front door, not an abstract platform diagram.


* **Seven Roots Only:** The top-level navigation contract is strictly limited to Home, Start, Capture, Knowledge, Memory, Insights, and System.


* **Capture is First-Class:** If offloading thoughts, files, or observations is slow, the system is failing its primary job.


* **System Stays Nested:** Administration, infrastructure, storage, blueprint, and diagnostics belong under "System" and must not become parallel roots.


* **Distinct Information Domains:** Knowledge is curated source material, Memory is continuity and context, and Insights are derived interpretations.


* **AI is Never Truth:** Every summary, link, pattern, or suggestion derived from AI must point back to a source.


* **Legacy Preservation:** Legacy models and older platforms are preserved by quarantine and must be explicitly labeled before reuse.


* **No Co-owning Doctrine:** Older models do not define the active runtime or co-own doctrine unless promoted again on purpose.



---

## Promotion & Governance Flows

QiEOS is the governing doctrine for the Qi system. It holds the doctrine, keeps system layer names fixed, resolves conflicts, and explains the reasoning behind the mirror structure.

* **Documentation Rules:** The ecosystem prioritizes flat structures over nested, linked files over duplicated ones, documented information over remembered knowledge, and modular components over massive designs.


* **Runtime vs. Assumptions:** Runtime facts always beat assumptions.


* **Derived Truth:** Derived layers and systems are never treated as truth sources by themselves.


* **Overriding DNA:** Implementation repos can hold local docs, but informal notes and local documents cannot override active QiOS DNA unless a formal decision record is added.


* **Promotion Laws:** Raw imported documents are considered evidence and must be reviewed before becoming canonical law. Exports are simply snapshots.


* **Decision Flow:** Doctrine or decision questions should be directed to `01_QiDNA/QiEOS/_folder.md`, where the reasoning is then applied to the matching system-layer folder. Each system folder independently documents what it owns and how it operates.