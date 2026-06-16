# Obsidian & QiDocs Configuration

This document outlines the doctrine and configuration rules for using Obsidian as the primary local Markdown editing and navigation tool for QiDocs.

## Vault Root

*   **The Vault Root**: The root of the Obsidian vault is the `/docs` directory.
*   **No Nested Vaults**: Do not use or initialize nested `.obsidian` folders under `/docs/10_blueprint` or any other subdirectories. The vault boundary exists exclusively at the `/docs` level.

## Configuration Folder

*   **Intended Config**: The intended Obsidian configuration folder is `.obsidian-qidocs`.
*   **Version Control**: Stable configuration (such as core settings, themes, and stable plugin lists) may be versioned in Git.
*   **Gitignored Churn**: Highly volatile files that create commit churn—such as `workspace.json`, `workspace-mobile.json`, cache directories, and plugin state data—must be strictly `.gitignore`d.

## Role in the System

*   **Obsidian**: Used strictly for local editing, writing, and Markdown file navigation.
*   **Wiki.js**: Acts as the readable, accessible knowledge base for the system.
*   **Source of Truth**: Raw Markdown and YAML files remain the definitive source of truth at all times.
*   **MarkMind / Visuals**: MarkMind (and similar tools) provide a generated visual layer for convenience. They are *not* the source of truth.
