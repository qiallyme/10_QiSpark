from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
import markdown


# Default paths
DEFAULT_SOURCE = Path(r"C:\QiLabs\40_QiVault")
DEFAULT_DIST = Path(r"C:\QiLabs\10_QiSpark\dist")
BOOKMARKS_CSV = Path(r"C:\QiLabs\00_QiLabs.workspace\toolbox\tools\access\qiaccess_bookmarks\bookmarks.csv")

# Controlled tag vocabulary configuration
VALID_STATUSES = {"publish", "published", "public"}
EXCLUDE_SENSITIVITY = {"private", "sensitive", "confidential"}


def rel(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"['\"`]", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untitled"


def parse_frontmatter(text: str) -> tuple[dict[str, any], str]:
    if not text.startswith("---\n"):
        return {}, text
    match = re.search(r"\n---\s*\n", text)
    if not match:
        return {}, text
    raw = text[4 : match.start()]
    body = text[match.end() :]
    data = {}
    current_key = None
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


def should_include(fm: dict[str, any], allow_active: bool) -> tuple[bool, str]:
    # 1. Check status
    status = str(fm.get("status") or "").lower().strip()
    if allow_active and status == "active":
        pass
    elif status not in VALID_STATUSES:
        return False, f"Status '{status}' not in {list(VALID_STATUSES)} (use --allow-active to include 'active')"

    # 2. Check sensitivity / classification
    sensitivity = str(fm.get("sensitivity") or "").lower().strip()
    if sensitivity in EXCLUDE_SENSITIVITY:
        return False, f"Sensitivity '{sensitivity}' is restricted"

    classification = str(fm.get("classification") or "").lower().strip()
    if classification in EXCLUDE_SENSITIVITY:
        return False, f"Classification '{classification}' is restricted"

    # 3. Check explicit boolean flags
    for flag in ["private", "sensitive", "confidential", "private_theory_flag"]:
        val = fm.get(flag)
        if isinstance(val, bool) and val:
            return False, f"Explicit flag '{flag}' is true"
        if str(val).lower() in ("yes", "true", "1"):
            return False, f"Explicit flag '{flag}' is enabled"

    return True, ""


def read_bookmarks() -> list[dict]:
    bookmarks = []
    if not BOOKMARKS_CSV.exists():
        print(f"Warning: Bookmarks CSV not found at {BOOKMARKS_CSV}")
        return []
    try:
        with open(BOOKMARKS_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("enabled", "").lower() == "true":
                    bookmarks.append(row)
    except Exception as e:
        print(f"Error reading bookmarks: {e}")
    return bookmarks


# Modern glassmorphism layout templates
HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --bg-color: #08090d;
            --card-bg: rgba(255, 255, 255, 0.02);
            --card-border: rgba(255, 255, 255, 0.06);
            --card-hover-border: rgba(99, 102, 241, 0.3);
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.15);
            --text-color: #e2e8f0;
            --text-muted: #94a3b8;
            --sidebar-width: 320px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            overflow-x: hidden;
        }

        .bg-glow-1 {
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
        }

        .bg-glow-2 {
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
        }

        header {
            border-bottom: 1px solid var(--card-border);
            background: rgba(8, 9, 13, 0.7);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 2rem;
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: white;
            font-weight: 600;
            font-size: 1.4rem;
            letter-spacing: -0.5px;
        }

        .logo-icon {
            color: var(--primary);
        }

        .nav-links {
            display: flex;
            gap: 1.5rem;
        }

        .nav-link {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 500;
            transition: color 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .nav-link:hover, .nav-link.active {
            color: white;
        }

        /* Glass Cards */
        .glass-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 18px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .glass-card:hover {
            border-color: var(--card-hover-border);
            box-shadow: 0 12px 30px -10px var(--primary-glow);
            transform: translateY(-4px);
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2.5rem 2rem;
        }
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
            </div>
        </div>
    </header>
"""


def render_dashboard(bookmarks: list[dict], docs_root_rel: str) -> str:
    # Compile groups from bookmarks
    bookmark_groups = {}
    for bm in bookmarks:
        group = bm.get("group", "Other Bookmarks")
        bookmark_groups.setdefault(group, []).append(bm)

    services_html = ""
    # Branded Cockpit Buttons
    services = [
        {"title": "QiAccess", "desc": "Access/cockpit entry point for workflows.", "url": "https://access.qially.com", "icon": "layout-dashboard", "color": "#6366f1"},
        {"title": "QiSaysIt", "desc": "Public writing, posts and publishing surface.", "url": "https://qsaysit.com", "icon": "pencil-line", "color": "#10b981"},
        {"title": "QiAlly", "desc": "Primary QiAlly public/domain hub.", "url": "https://qially.com", "icon": "globe", "color": "#3b82f6"},
        {"title": "QiFinance", "desc": "QiFinance dashboard and analytics.", "url": "https://fi.qially.com", "icon": "wallet", "color": "#eab308"},
        {"title": "QiLife", "desc": "Personal life organizer and task manager.", "url": "https://life.qially.com", "icon": "heart", "color": "#ec4899"},
        {"title": "QiServer", "desc": "Local private server cluster control plane.", "url": "https://server.qially.com", "icon": "server", "color": "#a855f7"},
        {"title": "QiVault", "desc": "Secure document storage and credentials.", "url": "https://vault.qially.com", "icon": "shield-check", "color": "#f97316"},
        {"title": "QiConnect", "desc": "API integrations and event scheduler.", "url": "https://connect.qially.com", "icon": "git-branch", "color": "#14b8a6"},
        {"title": "QiSpark Docs", "desc": "Static documentation and blue prints.", "url": f"{docs_root_rel}/index.html", "icon": "book-open", "color": "#38bdf8"},
    ]

    for svc in services:
        services_html += f"""
        <a href="{svc['url']}" class="glass-card service-card" style="--accent: {svc['color']}; text-decoration: none;">
            <div class="service-icon" style="background: rgba({hex_to_rgb(svc['color'])}, 0.1); color: {svc['color']}"><i data-lucide="{svc['icon']}"></i></div>
            <div class="service-details">
                <h3>{svc['title']}</h3>
                <p>{svc['desc']}</p>
            </div>
            <div class="service-arrow"><i data-lucide="chevron-right"></i></div>
        </a>
        """

    bookmarks_html = ""
    for group_name, items in bookmark_groups.items():
        group_items_html = ""
        for item in items:
            tags_html = ""
            for tag in [t.strip() for t in item.get("tags", "").split(",") if t.strip()]:
                tags_html += f'<span class="bm-tag">#{tag}</span>'
            
            group_items_html += f"""
            <div class="bookmark-item">
                <div class="bm-content">
                    <a href="{item['url']}" target="_blank" class="bm-title-link">
                        {item['title']} <i data-lucide="external-link" class="link-icon"></i>
                    </a>
                    <p class="bm-desc">{item['description']}</p>
                    <div class="bm-tags">{tags_html}</div>
                </div>
            </div>
            """
        
        bookmarks_html += f"""
        <div class="glass-card bookmark-group-card">
            <h2><i data-lucide="folder" style="color: var(--primary)"></i> {group_name}</h2>
            <div class="bookmark-list">
                {group_items_html}
            </div>
        </div>
        """

    html = f"""
    <style>
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
            margin-bottom: 3.5rem;
        }}

        .service-card {{
            padding: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1.25rem;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}

        .service-card::after {{
            content: '';
            position: absolute;
            top: 0; left: 0; width: 4px; height: 100%;
            background: var(--accent);
            opacity: 0.8;
        }}

        .service-icon {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .service-details h3 {{
            color: white;
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}

        .service-details p {{
            color: var(--text-muted);
            font-size: 0.85rem;
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
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .section-desc {{
            color: var(--text-muted);
            margin-bottom: 2rem;
            font-size: 1rem;
        }}

        /* Bookmarks Section */
        .bookmarks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 2rem;
        }}

        .bookmark-group-card {{
            padding: 1.75rem;
        }}

        .bookmark-group-card h2 {{
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: white;
        }}

        .bookmark-list {{
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}

        .bookmark-item {{
            border-left: 2px solid rgba(255, 255, 255, 0.1);
            padding-left: 1rem;
            transition: border-color 0.2s;
        }}

        .bookmark-item:hover {{
            border-left-color: var(--primary);
        }}

        .bm-title-link {{
            color: #f1f5f9;
            font-weight: 500;
            font-size: 1rem;
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
            opacity: 0.6;
        }}

        .bm-desc {{
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 0.25rem;
        }}

        .bm-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            margin-top: 0.5rem;
        }}

        .bm-tag {{
            font-size: 0.75rem;
            color: var(--primary);
            background: rgba(99, 102, 241, 0.08);
            padding: 0.1rem 0.4rem;
            border-radius: 4px;
        }}
    </style>

    <main class="container">
        <h1 class="section-title"><i data-lucide="layout-grid" style="color: var(--primary)"></i> Main Cockpit</h1>
        <p class="section-desc">Quick launch pads for your operational systems and websites.</p>
        
        <div class="dashboard-grid">
            {services_html}
        </div>

        <h1 class="section-title"><i data-lucide="bookmarks" style="color: var(--primary)"></i> Bookmarks Registry</h1>
        <p class="section-desc">Static references imported from your local toolbox cockpit.</p>

        <div class="bookmarks-grid">
            {bookmarks_html}
        </div>
    </main>
    """
    return html


def hex_to_rgb(hex_str: str) -> str:
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return f"{r}, {g}, {b}"


def render_docs_layout(sidebar_html: str, content_html: str, fm: dict[str, any]) -> str:
    metadata_html = ""
    if fm:
        meta_items = [
            ("Status", fm.get("status"), "tag"),
            ("Sensitivity", fm.get("sensitivity"), "shield"),
            ("Classification", fm.get("classification"), "file-text"),
            ("Updated At", fm.get("updated_at"), "calendar"),
            ("Author", fm.get("author"), "user"),
            ("Source Type", fm.get("source_type"), "database")
        ]
        
        meta_blocks = ""
        for label, val, icon in meta_items:
            if val:
                meta_blocks += f"""
                <div class="meta-block">
                    <span class="meta-label"><i data-lucide="{icon}"></i> {label}</span>
                    <span class="meta-value">{val}</span>
                </div>
                """
        if meta_blocks:
            metadata_html = f'<div class="doc-metadata">{meta_blocks}</div>'

    html = f"""
    <style>
        .docs-layout {{
            display: flex;
            min-height: calc(100vh - 73px);
        }}

        /* Sidebar */
        .sidebar {{
            width: var(--sidebar-width);
            border-right: 1px solid var(--card-border);
            background: rgba(8, 9, 13, 0.4);
            flex-shrink: 0;
            padding: 2rem 1.5rem;
            overflow-y: auto;
            position: sticky;
            top: 73px;
            height: calc(100vh - 73px);
        }}

        .sidebar-title {{
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .doc-tree {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .tree-folder {{
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }}

        .folder-header {{
            font-weight: 600;
            font-size: 0.95rem;
            color: white;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.5rem;
            margin-bottom: 0.25rem;
        }}

        .tree-item {{
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            padding: 0.25rem 0.5rem;
            border-left: 1px solid rgba(255, 255, 255, 0.05);
            margin-left: 0.5rem;
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
            background: rgba(255, 255, 255, 0.01);
        }}

        /* Main Content */
        .content-area {{
            flex-grow: 1;
            padding: 3rem 4rem;
            max-width: 960px;
            overflow-y: auto;
        }}

        /* Document Metadata */
        .doc-metadata {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.25rem;
            margin-bottom: 2.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--card-border);
        }}

        .meta-block {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .meta-label {{
            font-size: 0.75rem;
            font-weight: 600;
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
            font-weight: 500;
        }}

        /* Markdown Styles */
        .markdown-body h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 1.5rem;
            color: white;
        }}

        .markdown-body h2 {{
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: white;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.5rem;
        }}

        .markdown-body h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            color: white;
        }}

        .markdown-body p {{
            margin-bottom: 1.25rem;
            color: #cbd5e1;
        }}

        .markdown-body ul, .markdown-body ol {{
            margin-bottom: 1.25rem;
            padding-left: 1.5rem;
            color: #cbd5e1;
        }}

        .markdown-body li {{
            margin-bottom: 0.35rem;
        }}

        .markdown-body code {{
            font-family: monospace;
            background: rgba(255, 255, 255, 0.05);
            padding: 0.15rem 0.35rem;
            border-radius: 4px;
            font-size: 0.9em;
            color: #f43f5e;
        }}

        .markdown-body pre {{
            background: #0f1115;
            border: 1px solid var(--card-border);
            padding: 1.25rem;
            border-radius: 12px;
            overflow-x: auto;
            margin-bottom: 1.5rem;
        }}

        .markdown-body pre code {{
            background: none;
            padding: 0;
            color: #e2e8f0;
            font-size: 0.9rem;
        }}

        .markdown-body a {{
            color: var(--primary);
            text-decoration: none;
            transition: border-bottom 0.15s;
            border-bottom: 1px solid transparent;
        }}

        .markdown-body a:hover {{
            border-bottom-color: var(--primary);
        }}

        .markdown-body blockquote {{
            border-left: 4px solid var(--primary);
            padding-left: 1.25rem;
            color: var(--text-muted);
            font-style: italic;
            margin-bottom: 1.5rem;
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
    return html


HTML_FOOTER = """
    <script>
        // Initialize Lucide Icons
        lucide.createIcons();
    </script>
</body>
</html>
"""


def build_sidebar(docs_list: list[dict], current_rel_path: str = None) -> str:
    # Group files by top-level parent folder
    hierarchy = {}
    for doc in docs_list:
        folder = doc["folder"] or "Root"
        hierarchy.setdefault(folder, []).append(doc)

    html = ""
    # Render folders and files
    for folder, items in sorted(hierarchy.items()):
        folder_items_html = ""
        for item in sorted(items, key=lambda x: x["title"]):
            is_active = current_rel_path == item["rel_html"]
            active_class = " active" if is_active else ""
            
            # Make sure links resolve correctly depending on depth
            link_prefix = ""
            if current_rel_path:
                depth = len(current_rel_path.split("/")) - 1
                link_prefix = "../" * depth
            
            folder_items_html += f"""
            <a href="{link_prefix}{item['rel_html']}" class="tree-item{active_class}" title="{item['title']}">
                {item['title']}
            </a>
            """
        
        html += f"""
        <div class="tree-folder">
            <div class="folder-header"><i data-lucide="folder" style="width: 14px; height: 14px; color: var(--text-muted)"></i> {folder}</div>
            {folder_items_html}
        </div>
        """
    return html


def convert_md_files(source_dir: Path, dist_dir: Path, allow_active: bool) -> list[dict]:
    docs_list = []
    docs_dir = dist_dir / "docs"
    
    # Process all Markdown files
    for root_dir, _, files in os.walk(source_dir):
        # Ignore git, obsidian, etc.
        parts = Path(root_dir).relative_to(source_dir).parts
        if any(p.startswith(".") for p in parts) or "_qiconfig" in parts:
            continue
        
        for file in files:
            if not file.lower().endswith(".md"):
                continue
            
            full_path = Path(root_dir) / file
            rel_path = full_path.relative_to(source_dir)
            
            # Read and parse front matter
            try:
                content = full_path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"Error reading {full_path}: {e}")
                continue
                
            fm, body_text = parse_frontmatter(content)
            
            # Check inclusion criteria
            ok, reason = should_include(fm, allow_active)
            if not ok:
                # Log why it was skipped
                print(f"Skipped {rel_path} - {reason}")
                continue
                
            # Render Markdown body to HTML
            html_body = markdown.markdown(body_text, extensions=['fenced_code', 'tables', 'nl2br'])
            
            title = fm.get("title") or fm.get("title") or rel_path.stem.replace("_", " ").replace("-", " ").title()
            slug = fm.get("slug") or slugify(title)
            
            # Calculate output path
            rel_html_path = rel_path.with_suffix(".html")
            out_html_path = docs_dir / rel_html_path
            
            # Top-level folder naming for grouping
            folder_name = rel_path.parts[0] if len(rel_path.parts) > 1 else ""
            if folder_name.isdigit() or (len(folder_name) > 2 and folder_name[:2].isdigit()):
                # strip number prefixes e.g. "04_projects" -> "projects"
                folder_name = re.sub(r"^\d+_", "", folder_name).replace("_", " ").title()
            elif folder_name:
                folder_name = folder_name.replace("_", " ").title()
            else:
                folder_name = "Root"

            docs_list.append({
                "title": title,
                "slug": slug,
                "rel_html": "docs/" + rel_html_path.as_posix(),
                "out_path": out_html_path,
                "html_body": html_body,
                "frontmatter": fm,
                "folder": folder_name
            })
            
    return docs_list


def main() -> None:
    parser = argparse.ArgumentParser(description="Static HTML documentation site builder for QiSpark.")
    parser.add_argument("--source", type=str, default=str(DEFAULT_SOURCE), help="Source markdown directory")
    parser.add_argument("--dist", type=str, default=str(DEFAULT_DIST), help="Output static site directory")
    parser.add_argument("--allow-active", action="store_true", help="Include active status files in documentation build")
    args = parser.parse_args()

    source_dir = Path(args.source)
    dist_dir = Path(args.dist)
    allow_active = args.allow_active

    print(f"Building Static Site inside: {dist_dir}")
    print(f"Markdown Source: {source_dir}")
    print(f"Allow active status files: {allow_active}")
    print("-" * 60)

    # 1. Clean and recreate output dirs
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Read bookmarks
    bookmarks = read_bookmarks()
    print(f"Loaded {len(bookmarks)} bookmarks from CSV.")

    # 3. Process and convert all Markdown documents
    docs = convert_md_files(source_dir, dist_dir, allow_active)
    print(f"Compiled {len(docs)} documents.")

    # 4. Generate individual docs pages
    sidebar_html = build_sidebar(docs)
    for doc in docs:
        doc_sidebar = build_sidebar(docs, doc["rel_html"])
        depth = len(doc["rel_html"].split("/")) - 1
        home_path = "../" * depth + "index.html"
        docs_path = "../" * depth + "docs/index.html" if len(docs) > 0 else "#"
        
        # Wrap inside general layout
        page_html = HTML_HEADER.replace("{title}", doc["title"]).replace("{home_path}", home_path).replace("{docs_path}", docs_path)
        page_html += render_docs_layout(doc_sidebar, doc["html_body"], doc["frontmatter"])
        page_html += HTML_FOOTER
        
        doc["out_path"].parent.mkdir(parents=True, exist_ok=True)
        doc["out_path"].write_text(page_html, encoding="utf-8")

    # 5. Generate docs index page
    if docs:
        docs_idx_path = dist_dir / "docs" / "index.html"
        docs_idx_sidebar = build_sidebar(docs, "docs/index.html")
        welcome_html = "<h1>Welcome to QiSpark Documentation</h1><p>Select a document from the left sidebar to begin reading.</p>"
        
        docs_index = HTML_HEADER.replace("{title}", "QiSpark Documentation Index").replace("{home_path}", "../index.html").replace("{docs_path}", "index.html")
        docs_index += render_docs_layout(docs_idx_sidebar, welcome_html, {})
        docs_index += HTML_FOOTER
        
        docs_idx_path.parent.mkdir(parents=True, exist_ok=True)
        docs_idx_path.write_text(docs_index, encoding="utf-8")

    # 6. Generate the Cockpit / Homepage (index.html)
    home_path = "index.html"
    docs_path = "docs/index.html" if docs else "#"
    
    dashboard_html = HTML_HEADER.replace("{title}", "QiAccess Cockpit").replace("{home_path}", home_path).replace("{docs_path}", docs_path)
    dashboard_html += render_dashboard(bookmarks, "docs" if docs else "#")
    dashboard_html += HTML_FOOTER
    
    (dist_dir / "index.html").write_text(dashboard_html, encoding="utf-8")

    print()
    print("=" * 72)
    print("Static Site Build Complete!")
    print(f"Homepage: {dist_dir / 'index.html'}")
    if docs:
        print(f"Docs Index: {dist_dir / 'docs' / 'index.html'}")
    print("=" * 72)


if __name__ == "__main__":
    main()
