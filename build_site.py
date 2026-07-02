from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any

import markdown


# ---------------------------------------------------------------------------
# Default paths
# ---------------------------------------------------------------------------
DEFAULT_QILABS_ROOT = Path(r"C:\QiLabs")
DEFAULT_SOURCE = Path(r"C:\QiLabs\40_QiVault")
DEFAULT_DIST = Path(r"C:\QiLabs\10_QiSpark\dist")
BOOKMARKS_CSV = Path(
    r"C:\QiLabs\00_QiLabs.workspace\toolbox\tools\access\qiaccess_bookmarks\bookmarks.csv"
)

# Controlled tag vocabulary configuration
VALID_STATUSES = {"publish", "published", "public"}
EXCLUDE_SENSITIVITY = {"private", "sensitive", "confidential"}
EXCLUDE_CLASSIFICATION = {"private", "sensitive", "confidential"}
EXCLUDE_FLAGS = ["private", "sensitive", "confidential", "private_theory_flag"]

# Tree safety defaults.
# This still gives you a usable QiLabs map without dumping junk folders,
# virtual environments, dependency caches, or obvious secret files into a public site.
TREE_SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".obsidian",
    ".trash",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".next",
    ".nuxt",
    ".svelte-kit",
    "dist",
    "build",
    ".wrangler",
    ".vercel",
    ".netlify",
    "30_QiDrive",
}
TREE_SKIP_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    ".env.test",
    "id_rsa",
    "id_dsa",
    "id_ed25519",
}
TREE_SKIP_EXTENSIONS = {
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".sqlite",
    ".sqlite3",
    ".db",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def normalize_path(path: Path) -> Path:
    return path.expanduser().resolve()


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def ensure_safe_build_paths(source_dir: Path, dist_dir: Path) -> None:
    """
    Guardrail: this builder treats source content as read-only.

    It only deletes/writes inside dist_dir. It refuses to run if dist is the
    source folder or nested inside the source folder, because that could delete
    or publish the source vault by accident.
    """
    source_dir = normalize_path(source_dir)
    dist_dir = normalize_path(dist_dir)

    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")

    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_dir}")

    if dist_dir == source_dir:
        raise ValueError("Refusing to build: --dist cannot be the same as --source.")

    if is_relative_to(dist_dir, source_dir):
        raise ValueError(
            "Refusing to build: --dist is inside --source. "
            "That risks deleting or publishing source content."
        )


def safe_clean_dist(dist_dir: Path) -> None:
    """
    Overwrite old dist cleanly, with a sanity check so a bad arg does not nuke a root.
    """
    dist_dir = normalize_path(dist_dir)

    if dist_dir.exists():
        if dist_dir.name.lower() != "dist":
            raise ValueError(
                f"Refusing to delete output folder because it is not named 'dist': {dist_dir}"
            )
        shutil.rmtree(dist_dir)

    dist_dir.mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"['\"`]", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untitled"


def text_to_title(value: str) -> str:
    value = Path(value).stem
    value = value.replace("_", " ").replace("-", " ")
    return value.title()


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text

    match = re.search(r"\n---\s*\n", text)
    if not match:
        return {}, text

    raw = text[4 : match.start()]
    body = text[match.end() :]
    data: dict[str, Any] = {}
    current_key: str | None = None

    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        list_item = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if list_item and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(list_item.group(1).strip("'\" "))
            continue

        key_match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if not key_match:
            continue

        key, value = key_match.group(1), key_match.group(2).strip("'\" ")
        current_key = key

        if value == "":
            data[key] = [] if key in {"tags", "aliases", "keywords", "references"} else ""
        elif value == "[]":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            data[key] = [v.strip("'\" ") for v in value.strip("[]").split(",") if v.strip()]
        else:
            if key in {"tags", "aliases", "keywords", "references"}:
                data[key] = [value]
            else:
                data[key] = value

    return data, body


def should_include(fm: dict[str, Any], allow_active: bool) -> tuple[bool, str]:
    status = str(fm.get("status") or "").lower().strip()
    visibility = str(fm.get("visibility") or "").lower().strip()
    publish_target = str(fm.get("publish_target") or "").lower().strip()
    sensitivity = str(fm.get("sensitivity") or "").lower().strip()
    classification = str(fm.get("classification") or "").lower().strip()

    # 1. Safety exclusions
    if visibility in ("private",):
        return False, f"Visibility is '{visibility}'"

    if sensitivity in EXCLUDE_SENSITIVITY:
        return False, f"Sensitivity '{sensitivity}' is restricted"

    if classification in EXCLUDE_CLASSIFICATION:
        return False, f"Classification '{classification}' is restricted"

    # Explicit boolean flags
    for flag in EXCLUDE_FLAGS:
        val = fm.get(flag)
        if isinstance(val, bool) and val:
            return False, f"Explicit flag '{flag}' is true"
        if str(val).lower() in ("yes", "true", "1"):
            return False, f"Explicit flag '{flag}' is enabled"

    # 2. Strict / Backwards Compatible Publish matching
    is_backward_publish = status in ("published", "public")
    is_strict_publish = (
        status == "publish" and 
        visibility == "public" and 
        publish_target == "qispark"
    )
    is_active_allowed = (
        allow_active and 
        status == "active"
    )

    if not (is_backward_publish or is_strict_publish or is_active_allowed):
        return (
            False,
            f"Status '{status}', visibility '{visibility}', publish_target '{publish_target}' not eligible for build"
        )

    return True, ""


def read_bookmarks(csv_path: Path) -> list[dict[str, str]]:
    bookmarks: list[dict[str, str]] = []
    if not csv_path.exists():
        print(f"Warning: Bookmarks CSV not found at {csv_path}")
        return []

    try:
        with csv_path.open(mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if str(row.get("enabled", "")).lower() == "true":
                    bookmarks.append({k: (v or "") for k, v in row.items()})
    except Exception as e:
        print(f"Error reading bookmarks: {e}")

    return bookmarks


def hex_to_rgb(hex_str: str) -> str:
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return f"{r}, {g}, {b}"


# ---------------------------------------------------------------------------
# Shared HTML shell
# ---------------------------------------------------------------------------
HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {{
            --bg-color: #08090d;
            --card-bg: rgba(255, 255, 255, 0.035);
            --card-border: rgba(255, 255, 255, 0.08);
            --card-hover-border: rgba(99, 102, 241, 0.34);
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.16);
            --text-color: #e2e8f0;
            --text-muted: #94a3b8;
            --sidebar-width: 320px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            overflow-x: hidden;
        }}

        .bg-glow-1 {{
            position: fixed;
            top: -10%;
            left: -10%;
            width: 50vw;
            height: 50vw;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, rgba(99, 102, 241, 0) 70%);
            filter: blur(100px);
            z-index: -1;
            pointer-events: none;
        }}

        .bg-glow-2 {{
            position: fixed;
            bottom: -10%;
            right: -10%;
            width: 45vw;
            height: 45vw;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.08) 0%, rgba(168, 85, 247, 0) 70%);
            filter: blur(100px);
            z-index: -1;
            pointer-events: none;
        }}

        header {{
            border-bottom: 1px solid var(--card-border);
            background: rgba(8, 9, 13, 0.78);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .nav-container {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            padding: 1rem 1.5rem;
        }}

        .logo-section {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: white;
            font-weight: 650;
            font-size: 1.3rem;
            letter-spacing: -0.5px;
            white-space: nowrap;
        }}

        .logo-icon {{
            color: var(--primary);
        }}

        .nav-links {{
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: 0.35rem;
        }}

        .nav-link {{
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.92rem;
            font-weight: 500;
            transition: color 0.2s, background 0.2s;
            display: flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.45rem 0.65rem;
            border-radius: 999px;
        }}

        .nav-link:hover, .nav-link.active {{
            color: white;
            background: rgba(255, 255, 255, 0.05);
        }}

        .nav-link i, .logo-section i {{
            width: 18px;
            height: 18px;
        }}

        .glass-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 18px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
        }}

        .glass-card:hover {{
            border-color: var(--card-hover-border);
            box-shadow: 0 12px 30px -10px var(--primary-glow);
            transform: translateY(-2px);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
        }}

        @media (max-width: 820px) {{
            .nav-container {{
                align-items: flex-start;
                flex-direction: column;
            }}

            .nav-links {{
                justify-content: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="bg-glow-1"></div>
    <div class="bg-glow-2"></div>
    <header>
        <div class="nav-container">
            <a href="{home_path}" class="logo-section">
                <i data-lucide="zap" class="logo-icon"></i>
                <span>QiAccess Cockpit</span>
            </a>
            <div class="nav-links">
                <a href="{home_path}" class="nav-link"><i data-lucide="layout-dashboard"></i> Dashboard</a>
                <a href="{docs_path}" class="nav-link"><i data-lucide="book-open"></i> Documentation</a>
                <a href="{tree_path}" class="nav-link"><i data-lucide="folder-tree"></i> QiLabs Tree</a>
            </div>
        </div>
    </header>
"""


HTML_FOOTER = """
    <script>
        lucide.createIcons();
    </script>
</body>
</html>
"""


def make_header(title: str, home_path: str, docs_path: str, tree_path: str, site_title: str = "QiSpark Cockpit") -> str:
    return (
        HTML_HEADER
        .replace("{title}", html.escape(title))
        .replace("{home_path}", home_path)
        .replace("{docs_path}", docs_path)
        .replace("{tree_path}", tree_path)
        .replace("<span>QiAccess Cockpit</span>", f"<span>{html.escape(site_title)}</span>")
    )


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
def render_dashboard(bookmarks: list[dict[str, str]], services: list[dict[str, Any]], docs_root_rel: str, tree_rel: str) -> str:
    bookmark_groups: dict[str, list[dict[str, str]]] = {}
    for bm in bookmarks:
        group = bm.get("group", "Other Bookmarks") or "Other Bookmarks"
        bookmark_groups.setdefault(group, []).append(bm)

    # Group services by category
    service_groups: dict[str, list[dict[str, Any]]] = {}
    for svc in services:
        category = svc.get("category", "Other Services") or "Other Services"
        service_groups.setdefault(category, []).append(svc)

    services_sections_html = ""
    for category, svcs in service_groups.items():
        cards_html = ""
        for svc in svcs:
            url = svc.get("url", "")
            if url == "docs/index.html":
                url = f"{docs_root_rel}/index.html"
            elif url == "tree.html":
                url = tree_rel

            cards_html += f"""
            <a href="{html.escape(url, quote=True)}" class="glass-card service-card" style="--accent: {svc.get('color', '#6366f1')}; text-decoration: none;">
                <div class="service-icon" style="background: rgba({hex_to_rgb(svc.get('color', '#6366f1'))}, 0.12); color: {svc.get('color', '#6366f1')}"><i data-lucide="{svc.get('icon', 'zap')}"></i></div>
                <div class="service-details">
                    <h3>{html.escape(svc.get('title', 'Untitled'))}</h3>
                    <p>{html.escape(svc.get('description', ''))}</p>
                </div>
                <div class="service-arrow"><i data-lucide="chevron-right"></i></div>
            </a>
            """

        services_sections_html += f"""
        <h2 class="section-subtitle"><i data-lucide="layers" style="color: var(--primary); width: 18px; height: 18px;"></i> {html.escape(category)}</h2>
        <div class="dashboard-grid">
            {cards_html}
        </div>
        """

    bookmarks_html = ""
    for group_name, items in sorted(bookmark_groups.items()):
        group_items_html = ""
        for item in items:
            tags_html = ""
            for tag in [t.strip() for t in item.get("tags", "").split(",") if t.strip()]:
                tags_html += f'<span class="bm-tag">#{html.escape(tag)}</span>'

            group_items_html += f"""
            <div class="bookmark-item">
                <div class="bm-content">
                    <a href="{html.escape(item.get('url', '#'), quote=True)}" target="_blank" rel="noopener noreferrer" class="bm-title-link">
                        {html.escape(item.get('title', 'Untitled'))} <i data-lucide="external-link" class="link-icon"></i>
                    </a>
                    <p class="bm-desc">{html.escape(item.get('description', ''))}</p>
                    <div class="bm-tags">{tags_html}</div>
                </div>
            </div>
            """

        bookmarks_html += f"""
        <div class="glass-card bookmark-group-card">
            <h2><i data-lucide="folder" style="color: var(--primary)"></i> {html.escape(group_name)}</h2>
            <div class="bookmark-list">
                {group_items_html}
            </div>
        </div>
        """

    if not bookmarks_html.strip():
        bookmarks_html = """
        <div class="glass-card bookmark-group-card">
            <h2><i data-lucide="info" style="color: var(--primary)"></i> No bookmarks loaded</h2>
            <p class="bm-desc">The bookmarks CSV was not found or did not contain enabled rows.</p>
        </div>
        """

    return f"""
    <style>
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
            gap: 1.1rem;
            margin-top: 1.5rem;
            margin-bottom: 2.5rem;
        }}

        .service-card {{
            padding: 1.2rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}

        .service-card::after {{
            content: '';
            position: absolute;
            top: 0; left: 0; width: 4px; height: 100%;
            background: var(--accent);
            opacity: 0.85;
        }}

        .service-icon {{
            width: 44px;
            height: 44px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .service-icon i {{
            width: 22px;
            height: 22px;
        }}

        .service-details h3 {{
            color: white;
            font-size: 1.08rem;
            font-weight: 650;
            margin-bottom: 0.2rem;
        }}

        .service-details p {{
            color: var(--text-muted);
            font-size: 0.84rem;
            line-height: 1.35;
        }}

        .service-arrow {{
            margin-left: auto;
            color: var(--text-muted);
            transition: transform 0.2s;
        }}

        .service-card:hover .service-arrow {{
            transform: translateX(4px);
            color: white;
        }}

        .section-title {{
            font-size: clamp(1.75rem, 4vw, 2.4rem);
            font-weight: 760;
            letter-spacing: -0.7px;
            margin-bottom: 0.45rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .section-subtitle {{
            font-size: 1.25rem;
            font-weight: 650;
            margin-top: 2rem;
            margin-bottom: 0.95rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: white;
        }}

        .section-desc {{
            color: var(--text-muted);
            margin-bottom: 2rem;
            font-size: 1rem;
        }}

        .bookmarks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
            gap: 1.25rem;
        }}

        .bookmark-group-card {{
            padding: 1.35rem;
        }}

        .bookmark-group-card h2 {{
            font-size: 1.16rem;
            font-weight: 650;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: white;
        }}

        .bookmark-list {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .bookmark-item {{
            border-left: 2px solid rgba(255, 255, 255, 0.1);
            padding-left: 0.9rem;
            transition: border-color 0.2s;
        }}

        .bookmark-item:hover {{
            border-left-color: var(--primary);
        }}

        .bm-title-link {{
            color: #f1f5f9;
            font-weight: 520;
            font-size: 0.98rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            transition: color 0.2s;
        }}

        .bm-title-link:hover {{
            color: white;
            text-decoration: underline;
        }}

        .link-icon {{
            width: 14px;
            height: 14px;
            opacity: 0.65;
        }}

        .bm-desc {{
            color: var(--text-muted);
            font-size: 0.84rem;
            margin-top: 0.25rem;
        }}

        .bm-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            margin-top: 0.5rem;
        }}

        .bm-tag {{
            font-size: 0.74rem;
            color: var(--primary);
            background: rgba(99, 102, 241, 0.08);
            padding: 0.1rem 0.4rem;
            border-radius: 999px;
        }}
    </style>

    <main class="container">
        <h1 class="section-title"><i data-lucide="layout-grid" style="color: var(--primary)"></i> Main Cockpit</h1>
        <p class="section-desc">Quick launch pads for operational systems, docs, and generated workspace navigation.</p>

        {services_sections_html}

        <h1 class="section-title"><i data-lucide="bookmarks" style="color: var(--primary)"></i> Bookmarks Registry</h1>
        <p class="section-desc">Static references imported from the local toolbox cockpit.</p>

        <div class="bookmarks-grid">
            {bookmarks_html}
        </div>
    </main>
    """


# ---------------------------------------------------------------------------
# Docs pages
# ---------------------------------------------------------------------------
def render_docs_layout(sidebar_html: str, content_html: str, fm: dict[str, Any]) -> str:
    metadata_html = ""
    if fm:
        meta_items = [
            ("Status", fm.get("status"), "tag"),
            ("Sensitivity", fm.get("sensitivity"), "shield"),
            ("Classification", fm.get("classification"), "file-text"),
            ("Updated At", fm.get("updated_at"), "calendar"),
            ("Author", fm.get("author"), "user"),
            ("Source Type", fm.get("source_type"), "database"),
        ]

        meta_blocks = ""
        for label, val, icon in meta_items:
            if val:
                meta_blocks += f"""
                <div class="meta-block">
                    <span class="meta-label"><i data-lucide="{icon}"></i> {html.escape(label)}</span>
                    <span class="meta-value">{html.escape(str(val))}</span>
                </div>
                """

        if meta_blocks:
            metadata_html = f'<div class="doc-metadata">{meta_blocks}</div>'

    return f"""
    <style>
        .docs-layout {{
            display: flex;
            min-height: calc(100vh - 69px);
        }}

        .sidebar {{
            width: var(--sidebar-width);
            border-right: 1px solid var(--card-border);
            background: rgba(8, 9, 13, 0.46);
            flex-shrink: 0;
            padding: 1.5rem 1rem;
            overflow-y: auto;
            position: sticky;
            top: 69px;
            height: calc(100vh - 69px);
        }}

        .sidebar-title {{
            font-size: 0.78rem;
            font-weight: 760;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .doc-tree {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}

        .tree-folder {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .folder-header {{
            font-weight: 650;
            font-size: 0.92rem;
            color: white;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.35rem;
            margin-bottom: 0.2rem;
        }}

        .tree-item {{
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.88rem;
            padding: 0.28rem 0.55rem;
            border-left: 1px solid rgba(255, 255, 255, 0.07);
            margin-left: 0.45rem;
            border-radius: 0 8px 8px 0;
            transition: all 0.2s;
            display: block;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .tree-item:hover, .tree-item.active {{
            color: white;
            border-left-color: var(--primary);
            padding-left: 0.75rem;
            background: rgba(255, 255, 255, 0.045);
        }}

        .content-area {{
            flex-grow: 1;
            padding: 2.5rem clamp(1.25rem, 5vw, 4rem);
            max-width: 980px;
            overflow-y: auto;
        }}

        .doc-metadata {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 2rem;
            padding-bottom: 1.25rem;
            border-bottom: 1px solid var(--card-border);
        }}

        .meta-block {{
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }}

        .meta-label {{
            font-size: 0.72rem;
            font-weight: 650;
            text-transform: uppercase;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .meta-label i {{
            width: 12px;
            height: 12px;
        }}

        .meta-value {{
            font-size: 0.9rem;
            color: white;
            font-weight: 520;
        }}

        .markdown-body {{
            font-size: 1rem;
        }}

        .markdown-body h1 {{
            font-size: clamp(2rem, 5vw, 2.65rem);
            font-weight: 820;
            letter-spacing: -1px;
            margin-bottom: 1.35rem;
            color: white;
            line-height: 1.1;
        }}

        .markdown-body h2 {{
            font-size: 1.55rem;
            font-weight: 740;
            letter-spacing: -0.4px;
            margin-top: 2rem;
            margin-bottom: 0.85rem;
            color: white;
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
            padding-bottom: 0.45rem;
        }}

        .markdown-body h3 {{
            font-size: 1.2rem;
            font-weight: 650;
            margin-top: 1.35rem;
            margin-bottom: 0.65rem;
            color: white;
        }}

        .markdown-body p {{
            margin-bottom: 1.15rem;
            color: #cbd5e1;
        }}

        .markdown-body ul, .markdown-body ol {{
            margin-bottom: 1.15rem;
            padding-left: 1.5rem;
            color: #cbd5e1;
        }}

        .markdown-body li {{
            margin-bottom: 0.35rem;
        }}

        .markdown-body code {{
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            background: rgba(255, 255, 255, 0.06);
            padding: 0.15rem 0.35rem;
            border-radius: 6px;
            font-size: 0.9em;
            color: #fb7185;
        }}

        .markdown-body pre {{
            background: #0f1115;
            border: 1px solid var(--card-border);
            padding: 1.1rem;
            border-radius: 14px;
            overflow-x: auto;
            margin-bottom: 1.35rem;
        }}

        .markdown-body pre code {{
            background: none;
            padding: 0;
            color: #e2e8f0;
            font-size: 0.9rem;
        }}

        .markdown-body a {{
            color: #a5b4fc;
            text-decoration: none;
            border-bottom: 1px solid transparent;
        }}

        .markdown-body a:hover {{
            border-bottom-color: #a5b4fc;
        }}

        .markdown-body blockquote {{
            border-left: 4px solid var(--primary);
            padding-left: 1.1rem;
            color: var(--text-muted);
            font-style: italic;
            margin-bottom: 1.35rem;
        }}

        .markdown-body table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.25rem 0;
            overflow: hidden;
            border-radius: 12px;
        }}

        .markdown-body th, .markdown-body td {{
            border: 1px solid var(--card-border);
            padding: 0.65rem 0.75rem;
            vertical-align: top;
        }}

        .markdown-body th {{
            color: white;
            background: rgba(255, 255, 255, 0.045);
            text-align: left;
        }}

        @media (max-width: 900px) {{
            .docs-layout {{
                display: block;
            }}

            .sidebar {{
                width: 100%;
                height: auto;
                position: static;
                border-right: none;
                border-bottom: 1px solid var(--card-border);
            }}
        }}
    </style>
    <main class="docs-layout">
        <aside class="sidebar">
            <div class="sidebar-title"><i data-lucide="book-open" style="width: 16px; height: 16px;"></i> Document Tree</div>
            <nav class="doc-tree">
                {sidebar_html}
            </nav>
        </aside>
        <section class="content-area">
            {metadata_html}
            <div class="markdown-body">
                {content_html}
            </div>
        </section>
    </main>
    """


def build_sidebar(docs_list: list[dict[str, Any]], current_rel_path: str | None = None) -> str:
    # Filter out nav_hidden: True files
    visible_docs = [doc for doc in docs_list if not doc.get("nav_hidden", False)]

    # Group by nav_group
    hierarchy: dict[str, list[dict[str, Any]]] = {}
    for doc in visible_docs:
        group = doc.get("nav_group") or "Root"
        hierarchy.setdefault(group, []).append(doc)

    output = ""
    # Sort folders/groups by name
    for folder, items in sorted(hierarchy.items()):
        # Sort items inside each folder by nav_order, then nav_title
        sorted_items = sorted(
            items,
            key=lambda x: (x.get("nav_order", 999), str(x.get("nav_title") or "").lower())
        )

        folder_items_html = ""
        for item in sorted_items:
            is_active = current_rel_path == item["rel_html"]
            active_class = " active" if is_active else ""

            link_prefix = ""
            if current_rel_path:
                depth = len(current_rel_path.split("/")) - 1
                link_prefix = "../" * depth

            folder_items_html += f"""
            <a href="{link_prefix}{html.escape(item['rel_html'], quote=True)}" class="tree-item{active_class}" title="{html.escape(item['nav_title'], quote=True)}">
                {html.escape(item['nav_title'])}
            </a>
            """

        output += f"""
        <div class="tree-folder">
            <div class="folder-header"><i data-lucide="folder" style="width: 14px; height: 14px; color: var(--text-muted)"></i> {html.escape(folder)}</div>
            {folder_items_html}
        </div>
        """

    return output


def convert_md_files(source_dir: Path, dist_dir: Path, allow_active: bool) -> tuple[list[dict[str, Any]], dict[str, int]]:
    docs_list: list[dict[str, Any]] = []
    docs_dir = dist_dir / "docs"

    stats = {
        "scanned": 0,
        "compiled": 0,
        "skipped": 0,
        "status_not_publishable": 0,
        "visibility_restricted": 0,
        "sensitivity_restricted": 0,
        "classification_restricted": 0,
        "explicit_flags_restricted": 0,
        "read_errors": 0
    }

    for root_dir, dirnames, files in os.walk(source_dir):
        root_path = Path(root_dir)

        # Mutate dirnames in-place so os.walk does not recurse into skipped folders.
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d != "_qiconfig" and d not in TREE_SKIP_DIRS
        ]

        parts = root_path.relative_to(source_dir).parts
        if any(p.startswith(".") for p in parts) or "_qiconfig" in parts:
            continue

        for file_name in files:
            if not file_name.lower().endswith(".md"):
                continue

            full_path = root_path / file_name
            rel_path = full_path.relative_to(source_dir)
            stats["scanned"] += 1

            try:
                content = full_path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"Error reading {full_path}: {e}")
                stats["read_errors"] += 1
                stats["skipped"] += 1
                continue

            fm, body_text = parse_frontmatter(content)

            ok, reason = should_include(fm, allow_active)
            if not ok:
                stats["skipped"] += 1
                if "Status" in reason:
                    stats["status_not_publishable"] += 1
                elif "Visibility" in reason:
                    stats["visibility_restricted"] += 1
                elif "Sensitivity" in reason:
                    stats["sensitivity_restricted"] += 1
                elif "Classification" in reason:
                    stats["classification_restricted"] += 1
                elif "Explicit flag" in reason:
                    stats["explicit_flags_restricted"] += 1
                else:
                    stats["status_not_publishable"] += 1
                continue

            html_body = markdown.markdown(
                body_text,
                extensions=["fenced_code", "tables", "nl2br", "toc"],
                output_format="html5",
            )

            title = str(fm.get("title") or text_to_title(rel_path.name))
            slug = str(fm.get("slug") or slugify(title))

            rel_html_path = rel_path.with_suffix(".html")
            out_html_path = docs_dir / rel_html_path

            folder_name = rel_path.parts[0] if len(rel_path.parts) > 1 else ""
            if folder_name.isdigit() or (len(folder_name) > 2 and folder_name[:2].isdigit()):
                folder_name = re.sub(r"^\d+_", "", folder_name).replace("_", " ").title()
            elif folder_name:
                folder_name = folder_name.replace("_", " ").title()
            else:
                folder_name = "Root"

            # Parse navigation fields
            nav_title = fm.get("nav_title") or title
            nav_group = fm.get("nav_group") or folder_name

            try:
                nav_order = int(fm.get("nav_order", 999))
            except (ValueError, TypeError):
                nav_order = 999

            nav_hidden_val = fm.get("nav_hidden")
            if isinstance(nav_hidden_val, bool):
                nav_hidden = nav_hidden_val
            elif str(nav_hidden_val).lower() in ("yes", "true", "1"):
                nav_hidden = True
            else:
                nav_hidden = False

            is_index_val = fm.get("is_index")
            if is_index_val is not None:
                if isinstance(is_index_val, bool):
                    is_index = is_index_val
                else:
                    is_index = str(is_index_val).lower() in ("yes", "true", "1")
            else:
                is_index = rel_path.name.lower() in ("_index.md", "index.md")

            parent_ref = str(fm.get("parent_ref") or "")

            docs_list.append(
                {
                    "title": title,
                    "slug": slug,
                    "source_path": full_path,
                    "source_rel": rel_path.as_posix(),
                    "rel_html": "docs/" + rel_html_path.as_posix(),
                    "out_path": out_html_path,
                    "html_body": html_body,
                    "frontmatter": fm,
                    "folder": folder_name,
                    "nav_title": nav_title,
                    "nav_group": nav_group,
                    "nav_order": nav_order,
                    "nav_hidden": nav_hidden,
                    "is_index": is_index,
                    "parent_ref": parent_ref,
                }
            )
            stats["compiled"] += 1

    return docs_list, stats


# ---------------------------------------------------------------------------
# QiLabs tree page
# ---------------------------------------------------------------------------
def should_skip_tree_path(path: Path, root: Path, include_hidden: bool) -> bool:
    name = path.name

    if not include_hidden and name.startswith("."):
        return True

    if path.is_dir():
        return name in TREE_SKIP_DIRS

    lowered = name.lower()
    if lowered in TREE_SKIP_FILE_NAMES:
        return True

    if path.suffix.lower() in TREE_SKIP_EXTENSIONS:
        return True

    return False


def build_doc_source_link_map(docs: list[dict[str, Any]], tree_root: Path) -> dict[str, str]:
    """
    Map source markdown files to generated doc links.
    Values are hrefs from dist/tree.html.
    """
    mapping: dict[str, str] = {}
    tree_root = normalize_path(tree_root)

    for doc in docs:
        source_path = normalize_path(Path(doc["source_path"]))
        try:
            key = source_path.relative_to(tree_root).as_posix()
        except ValueError:
            continue
        mapping[key] = doc["rel_html"]

    return mapping


def render_tree_node(
    path: Path,
    root: Path,
    doc_link_map: dict[str, str],
    include_hidden: bool,
    max_depth: int | None,
    current_depth: int = 0,
) -> str:
    if should_skip_tree_path(path, root, include_hidden):
        return ""

    try:
        rel_key = path.relative_to(root).as_posix()
    except ValueError:
        rel_key = path.as_posix()

    display_name = path.name if path != root else path.name or str(path)
    safe_name = html.escape(display_name)

    if max_depth is not None and current_depth > max_depth:
        return ""

    if path.is_dir():
        children_html = ""
        try:
            children = sorted(
                path.iterdir(),
                key=lambda p: (not p.is_dir(), p.name.lower()),
            )
        except PermissionError:
            return f"""
            <li class="tree-dir blocked">
                <span class="tree-row"><i data-lucide="lock"></i>{safe_name}</span>
            </li>
            """
        except OSError:
            return ""

        for child in children:
            children_html += render_tree_node(
                child,
                root,
                doc_link_map,
                include_hidden,
                max_depth,
                current_depth + 1,
            )

        count = children_html.count("<li")
        open_attr = " open" if current_depth <= 1 else ""

        return f"""
        <li class="tree-dir">
            <details{open_attr}>
                <summary class="tree-row">
                    <i data-lucide="folder"></i>
                    <span class="node-name">{safe_name}</span>
                    <span class="node-count">{count}</span>
                </summary>
                <ul>{children_html}</ul>
            </details>
        </li>
        """

    icon = "file-text" if path.suffix.lower() == ".md" else "file"
    file_link = doc_link_map.get(rel_key)

    if file_link:
        return f"""
        <li class="tree-file linked">
            <a class="tree-row" href="{html.escape(file_link, quote=True)}">
                <i data-lucide="{icon}"></i>
                <span class="node-name">{safe_name}</span>
                <span class="node-badge">published</span>
            </a>
        </li>
        """

    return f"""
    <li class="tree-file">
        <span class="tree-row">
            <i data-lucide="{icon}"></i>
            <span class="node-name">{safe_name}</span>
        </span>
    </li>
    """


def render_tree_page(
    tree_root: Path,
    docs: list[dict[str, Any]],
    include_hidden: bool,
    max_depth: int | None,
) -> str:
    tree_root = normalize_path(tree_root)
    doc_link_map = build_doc_source_link_map(docs, tree_root)
    tree_html = render_tree_node(
        tree_root,
        tree_root,
        doc_link_map,
        include_hidden=include_hidden,
        max_depth=max_depth,
    )

    skipped = ", ".join(sorted(TREE_SKIP_DIRS))
    depth_text = "full depth" if max_depth is None else f"max depth {max_depth}"

    return f"""
    <style>
        .tree-page {{
            max-width: 1200px;
        }}

        .tree-hero {{
            padding: 1.4rem;
            margin-bottom: 1.25rem;
        }}

        .tree-hero h1 {{
            font-size: clamp(2rem, 5vw, 2.75rem);
            line-height: 1.05;
            letter-spacing: -1px;
            margin-bottom: 0.65rem;
            color: white;
        }}

        .tree-hero p {{
            color: var(--text-muted);
            margin-bottom: 0.75rem;
        }}

        .tree-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
        }}

        .tree-pill {{
            border: 1px solid var(--card-border);
            background: rgba(255, 255, 255, 0.04);
            color: #cbd5e1;
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            font-size: 0.82rem;
        }}

        .tree-panel {{
            padding: 1rem;
            overflow-x: auto;
        }}

        .qilabs-tree,
        .qilabs-tree ul {{
            list-style: none;
        }}

        .qilabs-tree ul {{
            margin-left: 1.25rem;
            padding-left: 0.75rem;
            border-left: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .qilabs-tree li {{
            margin: 0.18rem 0;
        }}

        .tree-row {{
            color: #cbd5e1;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            min-height: 1.75rem;
            padding: 0.2rem 0.45rem;
            border-radius: 9px;
            transition: background 0.15s, color 0.15s;
        }}

        .tree-row:hover {{
            color: white;
            background: rgba(255, 255, 255, 0.045);
        }}

        .tree-row i {{
            width: 16px;
            height: 16px;
            color: var(--text-muted);
        }}

        .tree-dir > details > summary {{
            cursor: pointer;
            user-select: none;
            color: white;
            font-weight: 550;
        }}

        .tree-dir > details > summary::-webkit-details-marker {{
            display: none;
        }}

        .tree-dir > details > summary::before {{
            content: "▸";
            color: var(--text-muted);
            display: inline-block;
            width: 0.8rem;
            transition: transform 0.15s;
        }}

        .tree-dir > details[open] > summary::before {{
            transform: rotate(90deg);
        }}

        .tree-file .tree-row {{
            font-size: 0.92rem;
        }}

        .tree-file.linked .tree-row {{
            color: #a5b4fc;
        }}

        .node-name {{
            white-space: nowrap;
        }}

        .node-count,
        .node-badge {{
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.055);
            padding: 0.05rem 0.38rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 520;
        }}

        .node-badge {{
            color: #c4b5fd;
        }}

        .tree-note {{
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 1rem;
        }}
    </style>

    <main class="container tree-page">
        <section class="glass-card tree-hero">
            <h1>QiLabs Tree</h1>
            <p>Generated from the local workspace tree during the static-site build. Markdown files that passed publish filters are linked to their generated docs pages.</p>
            <div class="tree-meta">
                <span class="tree-pill">Root: {html.escape(str(tree_root))}</span>
                <span class="tree-pill">Generated: {html.escape(now_iso())}</span>
                <span class="tree-pill">{html.escape(depth_text)}</span>
                <span class="tree-pill">Hidden included: {str(include_hidden).lower()}</span>
            </div>
        </section>

        <section class="glass-card tree-panel">
            <ul class="qilabs-tree">
                {tree_html}
            </ul>
            <p class="tree-note">Skipped noisy or risky folders/files by default: {html.escape(skipped)}. Secret-like files and database/key extensions are also hidden.</p>
        </section>
    </main>
    """


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------
def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(description="Static HTML documentation site builder for QiSpark.")
    parser.add_argument("--source", type=str, default=None, help="Read-only source markdown directory")
    parser.add_argument("--dist", type=str, default=None, help="Output static site directory")
    parser.add_argument("--tree-root", type=str, default=None, help="Root folder to render into dist/tree.html")
    parser.add_argument("--allow-active", action="store_true", help="Include active status files in documentation build")
    parser.add_argument("--no-tree", action="store_true", help="Skip generating dist/tree.html")
    parser.add_argument("--include-hidden-tree", action="store_true", help="Include hidden dot folders/files in the tree page")
    parser.add_argument(
        "--tree-max-depth",
        type=int,
        default=None,
        help="Maximum tree depth. Default is full depth, while still skipping noisy/risky folders.",
    )
    parser.add_argument("--config", type=str, default=None, help="Site config JSON path")
    parser.add_argument("--bookmarks-csv", type=str, default=None, help="Bookmarks CSV file path (overrides config)")
    parser.add_argument("--services-json", type=str, default=None, help="Services registry JSON path (overrides config)")
    parser.add_argument("--site-title", type=str, default=None, help="Overrides site title")
    args = parser.parse_args()

    # Load site configuration
    site_title = "QiSpark Cockpit"
    source_path = DEFAULT_SOURCE
    dist_path = DEFAULT_DIST
    tree_root_path = DEFAULT_QILABS_ROOT

    config_file = Path(args.config) if args.config else Path("00_config/site.config.json")
    if config_file.exists():
        try:
            with config_file.open("r", encoding="utf-8") as f:
                site_conf = json.load(f)
                site_title = site_conf.get("site_title", site_title)
                source_path = Path(site_conf.get("default_source", str(source_path)))
                dist_path = Path(site_conf.get("default_dist", str(dist_path)))
                tree_root_path = Path(site_conf.get("default_tree_root", str(tree_root_path)))
        except Exception as e:
            print(f"Error loading site config JSON: {e}")

    # CLI overrides
    if args.site_title:
        site_title = args.site_title
    if args.source:
        source_path = Path(args.source)
    if args.dist:
        dist_path = Path(args.dist)
    if args.tree_root:
        tree_root_path = Path(args.tree_root)

    source_dir = normalize_path(source_path)
    dist_dir = normalize_path(dist_path)
    tree_root = normalize_path(tree_root_path)
    allow_active = args.allow_active

    print(f"Building Static Site inside: {dist_dir}")
    print(f"Markdown Source, read-only: {source_dir}")
    print(f"QiLabs Tree Root: {tree_root}")
    print(f"Allow active status files: {allow_active}")
    print(f"Site Title: {site_title}")
    print("-" * 72)

    # Load publish filters JSON
    filters_file = Path("00_config/publish.filters.json")
    if filters_file.exists():
        try:
            with filters_file.open("r", encoding="utf-8") as f:
                pub_filters = json.load(f)
                global VALID_STATUSES, EXCLUDE_SENSITIVITY, EXCLUDE_CLASSIFICATION, EXCLUDE_FLAGS
                if "allowed_statuses" in pub_filters:
                    VALID_STATUSES = set(pub_filters["allowed_statuses"])
                if "exclude_sensitivity" in pub_filters:
                    EXCLUDE_SENSITIVITY = set(pub_filters["exclude_sensitivity"])
                if "exclude_classification" in pub_filters:
                    EXCLUDE_CLASSIFICATION = set(pub_filters["exclude_classification"])
                if "exclude_flags" in pub_filters:
                    EXCLUDE_FLAGS = list(pub_filters["exclude_flags"])
        except Exception as e:
            print(f"Error loading publish filters JSON: {e}")

    # Load bookmarks config to resolve path
    bookmarks_csv_path = BOOKMARKS_CSV
    bookmarks_conf_file = Path("00_config/bookmarks.config.json")
    if bookmarks_conf_file.exists():
        try:
            with bookmarks_conf_file.open("r", encoding="utf-8") as f:
                bm_conf = json.load(f)
                canonical_p = Path(bm_conf.get("canonical_csv", ""))
                source_p = Path(bm_conf.get("source_csv", ""))
                if canonical_p.exists():
                    bookmarks_csv_path = canonical_p
                elif source_p.exists():
                    bookmarks_csv_path = source_p
        except Exception as e:
            print(f"Error loading bookmarks config: {e}")

    if args.bookmarks_csv:
        bookmarks_csv_path = Path(args.bookmarks_csv)

    # Load services registry JSON
    services = []
    services_file = Path(args.services_json) if args.services_json else Path("00_config/services.registry.json")
    if services_file.exists():
        try:
            with services_file.open("r", encoding="utf-8") as f:
                services = json.load(f)
        except Exception as e:
            print(f"Error loading services registry JSON: {e}")

    if not services:
        services = [
            {"title": "QiServer Cockpit", "description": "Control plane and Private server cluster management.", "url": "https://server.qially.com", "icon": "server", "color": "#a855f7", "category": "Primary"},
            {"title": "QiLife", "description": "Personal life organizer and task manager.", "url": "https://life.qially.com", "icon": "heart", "color": "#ec4899", "category": "Primary"},
            {"title": "QiFinance", "description": "QiFinance dashboard and analytics.", "url": "https://fi.qially.com", "icon": "wallet", "color": "#eab308", "category": "Primary"},
            {"title": "QiSpark Docs", "description": "Static documentation and blueprints.", "url": "docs/index.html", "icon": "book-open", "color": "#38bdf8", "category": "Primary"},
            {"title": "QiLabs Tree", "description": "Current generated map of the local QiLabs workspace.", "url": "tree.html", "icon": "folder-tree", "color": "#f59e0b", "category": "Primary"},
            {"title": "QiSaysIt", "description": "Public writing, posts and publishing surface.", "url": "https://qsaysit.com", "icon": "pencil-line", "color": "#10b981", "category": "Publishing"},
            {"title": "QiAlly", "description": "Primary QiAlly public/domain hub.", "url": "https://qially.com", "icon": "globe", "color": "#3b82f6", "category": "Publishing"}
        ]

    # 1. Path guardrails + clean output
    ensure_safe_build_paths(source_dir, dist_dir)
    safe_clean_dist(dist_dir)

    # 2. Basic static build markers
    write_text(dist_dir / ".nojekyll", "")
    write_text(
        dist_dir / "build_manifest.json",
        json.dumps(
            {
                "generated_at": now_iso(),
                "source": str(source_dir),
                "dist": str(dist_dir),
                "tree_root": str(tree_root),
                "source_read_only_mode": True,
                "allow_active": allow_active,
                "site_title": site_title
            },
            indent=2,
        ),
    )

    # 3. Read bookmarks
    bookmarks = read_bookmarks(bookmarks_csv_path)
    print(f"Loaded {len(bookmarks)} bookmarks from CSV.")

    # 4. Process Markdown documents
    docs, stats = convert_md_files(source_dir, dist_dir, allow_active)
    print(f"Markdown files scanned: {stats['scanned']}")
    print(f"Published docs compiled: {stats['compiled']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"- status not publishable: {stats['status_not_publishable']}")
    print(f"- visibility private/internal: {stats['visibility_restricted']}")
    print(f"- sensitivity restricted: {stats['sensitivity_restricted']}")
    print(f"- classification restricted: {stats['classification_restricted']}")
    print(f"- explicit flags restricted: {stats['explicit_flags_restricted']}")
    print(f"- read errors: {stats['read_errors']}")

    # 5. Generate individual docs pages
    for doc in docs:
        doc_sidebar = build_sidebar(docs, doc["rel_html"])
        depth = len(doc["rel_html"].split("/")) - 1
        home_path = "../" * depth + "index.html"
        docs_path = "../" * depth + "docs/index.html"
        tree_path = "../" * depth + "tree.html"

        page_html = make_header(doc["title"], home_path, docs_path, tree_path, site_title=site_title)
        page_html += render_docs_layout(doc_sidebar, doc["html_body"], doc["frontmatter"])
        page_html += HTML_FOOTER

        write_text(doc["out_path"], page_html)

    # 6. Generate docs index page
    if docs:
        docs_idx_path = dist_dir / "docs" / "index.html"
        docs_idx_sidebar = build_sidebar(docs, "docs/index.html")
        welcome_html = """
        <h1>Welcome to QiSpark Documentation</h1>
        <p>Select a document from the left sidebar to begin reading.</p>
        """
        docs_index = make_header("QiSpark Documentation Index", "../index.html", "index.html", "../tree.html", site_title=site_title)
        docs_index += render_docs_layout(docs_idx_sidebar, welcome_html, {})
        docs_index += HTML_FOOTER
        write_text(docs_idx_path, docs_index)

    # 7. Generate QiLabs tree page
    if not args.no_tree:
        if tree_root.exists() and tree_root.is_dir():
            tree_page = make_header("QiLabs Tree", "index.html", "docs/index.html" if docs else "#", "tree.html", site_title=site_title)
            tree_page += render_tree_page(
                tree_root=tree_root,
                docs=docs,
                include_hidden=args.include_hidden_tree,
                max_depth=args.tree_max_depth,
            )
            tree_page += HTML_FOOTER
            write_text(dist_dir / "tree.html", tree_page)
            print(f"Generated QiLabs tree: {dist_dir / 'tree.html'}")
        else:
            print(f"Warning: Tree root not found or not a directory: {tree_root}")

    # 8. Generate homepage
    docs_path = "docs/index.html" if docs else "#"
    dashboard_html = make_header(site_title, "index.html", docs_path, "tree.html", site_title=site_title)
    dashboard_html += render_dashboard(bookmarks, services, "docs" if docs else "#", "tree.html")
    dashboard_html += HTML_FOOTER
    write_text(dist_dir / "index.html", dashboard_html)

    print()
    print("=" * 72)
    print("Static Site Build Complete!")
    print(f"Homepage: {dist_dir / 'index.html'}")
    print(f"Tree:     {dist_dir / 'tree.html'}")
    if docs:
        print(f"Docs:     {dist_dir / 'docs' / 'index.html'}")
    print("=" * 72)


if __name__ == "__main__":
    main()
