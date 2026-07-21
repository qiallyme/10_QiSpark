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
    r"C:\QiLabs\00_QiLabs.workspace\_qiconfig\_bookmarks\bookmarks.csv"
)

# Controlled tag vocabulary configuration
VALID_STATUSES = {"publish", "published", "public", "pub"}
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
    """Return (True, "") if a file should be included in the build.

    Fail-closed publish safety rule:
      A document MUST satisfy ALL of the following to be included in QiSpark Public:
      1. status in VALID_STATUSES (publish, published, public, pub) OR (allow_active is True and status == 'active')
      2. visibility == 'public'
      3. publish_target contains 'qispark'
      4. sensitivity == 'public'
      5. classification == 'public'

      If any required tag is missing or non-public, the document is excluded.
    """
    status = str(fm.get("status") or "").lower().strip()
    visibility = str(fm.get("visibility") or "").lower().strip()
    sensitivity = str(fm.get("sensitivity") or "").lower().strip()
    classification = str(fm.get("classification") or "").lower().strip()

    pt_val = fm.get("publish_target") or ""
    if isinstance(pt_val, list):
        targets = [str(t).lower().strip() for t in pt_val]
    else:
        targets = [t.strip() for t in str(pt_val).lower().replace(";", ",").split(",") if t.strip()]

    # Explicit exclusions check first
    if visibility in ("private", "internal", "business_internal"):
        return False, f"Visibility is '{visibility}'"
    if sensitivity in EXCLUDE_SENSITIVITY or sensitivity != "public":
        return False, f"Sensitivity '{sensitivity}' is not 'public'"
    if classification in EXCLUDE_CLASSIFICATION or classification != "public":
        return False, f"Classification '{classification}' is not 'public'"
    for flag in EXCLUDE_FLAGS:
        val = fm.get(flag)
        if isinstance(val, bool) and val or str(val).lower() in ("yes", "true", "1"):
            return False, f"Explicit flag '{flag}' is enabled"

    # Require visibility to be public
    if visibility != "public":
        return False, f"Visibility '{visibility}' is not 'public'"

    # Require publish_target to include qispark
    if "qispark" not in targets:
        return False, f"Publish target '{pt_val}' does not include 'qispark'"

    # Require status to be valid publish status (or active if allow_active=True)
    if status in VALID_STATUSES:
        return True, ""
    if allow_active and status == "active":
        return True, ""

    return False, f"Status '{status}' is not a publish status (expected one of: {', '.join(sorted(VALID_STATUSES))})"


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
        :root {
            --bg-color: #05060b;
            --card-bg: rgba(255, 255, 255, 0.028);
            --card-border: rgba(255, 255, 255, 0.065);
            --card-hover-border: rgba(99, 102, 241, 0.45);
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.22);
            --accent-purple: #a855f7;
            --text-color: #e2e8f0;
            --text-muted: #94a3b8;
            --text-subtle: #64748b;
            --sidebar-width: 340px;
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
            line-height: 1.65;
            overflow-x: hidden;
        }

        .bg-glow-1 {
            position: fixed;
            top: -10%;
            left: -10%;
            width: 50vw;
            height: 50vw;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.14) 0%, rgba(99, 102, 241, 0) 70%);
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
            background: radial-gradient(circle, rgba(168, 85, 247, 0.09) 0%, rgba(168, 85, 247, 0) 70%);
            filter: blur(100px);
            z-index: -1;
            pointer-events: none;
        }

        header {
            border-bottom: 1px solid var(--card-border);
            background: rgba(5, 6, 11, 0.92);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 1px 0 rgba(255,255,255,0.03);
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            padding: 1rem 1.5rem;
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: white;
            font-weight: 650;
            font-size: 1.32rem;
            letter-spacing: -0.5px;
            white-space: nowrap;
        }

        .nav-links {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: 0.4rem;
        }

        .nav-link {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.93rem;
            font-weight: 500;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.48rem 0.75rem;
            border-radius: 9999px;
            position: relative;
        }

        .nav-link:hover, .nav-link.active {
            color: white;
            background: rgba(255, 255, 255, 0.06);
        }

        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 50%;
            transform: translateX(-50%);
            width: 5px;
            height: 5px;
            background: var(--primary);
            border-radius: 50%;
        }

        .glass-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 18px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
        }

        .glass-card:hover {
            border-color: var(--card-hover-border);
            box-shadow: 0 14px 32px -12px var(--primary-glow);
            transform: translateY(-3px);
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2.75rem 1.5rem;
        }

        @media (max-width: 820px) {
            .nav-container {
                align-items: flex-start;
                flex-direction: column;
                gap: 1rem;
            }
            .nav-links {
                justify-content: flex-start;
            }
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
                <span>{site_title}</span>
            </a>
            <div class="nav-links">
                <a href="{home_path}" class="nav-link"><i data-lucide="home"></i> Home</a>
                <a href="{docs_path}" class="nav-link"><i data-lucide="book-open"></i> Documentation</a>
                <a href="{tree_path}" class="nav-link"><i data-lucide="folder-tree"></i> QiLabs Tree</a>
            </div>
        </div>
    </header>
"""


HTML_FOOTER = """
    <script>
        lucide.createIcons();

        function setActiveNav() {
            const currentPath = window.location.pathname;
            document.querySelectorAll('.nav-link').forEach(link => {
                const href = link.getAttribute('href');
                if (!href) return;
                // Match if the current path ends with the href, or if the href
                // points to the same resolved URL.
                try {
                    const resolved = new URL(href, window.location.href).pathname;
                    if (resolved === currentPath || currentPath === resolved + 'index.html') {
                        link.classList.add('active');
                        return;
                    }
                } catch(e) {}
                if (currentPath.endsWith(href) || (href.includes('index.html') && (currentPath === '/' || currentPath.endsWith('/')))) {
                    link.classList.add('active');
                }
            });
        }

        function toggleAllDetails(open) {
            document.querySelectorAll('.doc-tree details').forEach(el => el.open = open);
        }

        window.addEventListener('load', setActiveNav);
    </script>
</body>
</html>
"""


def make_header(title: str, home_path: str, docs_path: str, tree_path: str, site_title: str = "QiSpark") -> str:
    return (
        HTML_HEADER
        .replace("{title}", html.escape(title))
        .replace("{home_path}", home_path)
        .replace("{docs_path}", docs_path)
        .replace("{tree_path}", tree_path)
        .replace("{site_title}", html.escape(site_title))
    )


# ---------------------------------------------------------------------------
# Landing Page
# ---------------------------------------------------------------------------
def render_landing(services: list[dict[str, Any]], docs_root_rel: str, tree_rel: str) -> str:
    # Filter services by surface == public
    public_services = [svc for svc in services if "public" in svc.get("surface", ["public"])]

    # Group services by category
    service_groups = {}
    for svc in public_services:
        category = svc.get("category", "Other Services") or "Other Services"
        service_groups.setdefault(category, []).append(svc)

    services_sections_html = ""
    for category, svcs in service_groups.items():
        cards_html = ""
        for svc in svcs:
            url = svc.get("url")
            status = str(svc.get("status", "active")).lower().strip()
            is_dev = status == "development" or not url or url == "#"

            if url == "docs/index.html":
                url = f"{docs_root_rel}/index.html" if not docs_root_rel.endswith("docs") else f"{docs_root_rel}/index.html"
                if docs_root_rel == "#":
                    url = "docs/index.html"
            elif url == "tree.html":
                url = tree_rel

            color = svc.get('color', '#6366f1')
            rgb = hex_to_rgb(color)
            title = html.escape(svc.get('title', 'Untitled'))
            desc = html.escape(svc.get('description', ''))
            icon = svc.get('icon', 'zap')

            if is_dev:
                cards_html += f'''
                <div class="glass-card service-card service-card-disabled" style="--accent: {color}; cursor: default; opacity: 0.85;">
                    <div class="service-icon" style="background: rgba({rgb}, 0.12); color: {color}"><i data-lucide="{icon}"></i></div>
                    <div class="service-details">
                        <h3>{title} <span class="status-badge dev-badge">In Development</span></h3>
                        <p>{desc}</p>
                    </div>
                </div>
                '''
            else:
                cards_html += f'''
                <a href="{html.escape(url, quote=True)}" class="glass-card service-card" style="--accent: {color}; text-decoration: none;">
                    <div class="service-icon" style="background: rgba({rgb}, 0.12); color: {color}"><i data-lucide="{icon}"></i></div>
                    <div class="service-details">
                        <h3>{title}</h3>
                        <p>{desc}</p>
                    </div>
                    <div class="service-arrow"><i data-lucide="chevron-right"></i></div>
                </a>
                '''

        services_sections_html += f'''
        <h2 class="section-subtitle"><i data-lucide="layers" style="color: var(--primary); width: 18px; height: 18px;"></i> {html.escape(category)}</h2>
        <div class="dashboard-grid">
            {cards_html}
        </div>
        '''

    return f'''
    <style>
        .hero-section {{
            text-align: center;
            padding: 4rem 1rem;
            margin-bottom: 2rem;
        }}
        .hero-section h1 {{
            font-size: clamp(2.5rem, 6vw, 4rem);
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 1rem;
            background: linear-gradient(to right, #fff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-section p {{
            font-size: 1.25rem;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto 2.5rem auto;
        }}
        .enter-qilife-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            background: var(--primary);
            color: white;
            padding: 0.85rem 2rem;
            border-radius: 9999px;
            font-size: 1.1rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s;
            box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39);
        }}
        .enter-qilife-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.23);
            background: #4f46e5;
        }}
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
        
        .status-badge {{
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.15rem 0.45rem;
            border-radius: 999px;
            margin-left: 0.35rem;
            vertical-align: middle;
            display: inline-block;
        }}

        .dev-badge {{
            background: rgba(236, 72, 153, 0.15);
            color: #f472b6;
            border: 1px solid rgba(236, 72, 153, 0.3);
        }}

        .service-card-disabled:hover {{
            transform: none !important;
            border-color: var(--card-border) !important;
            box-shadow: none !important;
        }}
    </style>

    <main class="container">
        <div class="hero-section">
            <h1>Welcome to QiSpark</h1>
            <p>The centralized public gateway for the QiLabs ecosystem.</p>
            <a href="https://qilife.local" class="enter-qilife-btn">
                Enter QiLife <i data-lucide="arrow-right"></i>
            </a>
        </div>
        
        {services_sections_html}
    </main>
    '''


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

        .tree-folder details {{
            width: 100%;
        }}

        .tree-folder summary {{
            list-style: none;
            cursor: pointer;
            outline: none;
            user-select: none;
        }}

        .tree-folder summary::-webkit-details-marker {{
            display: none;
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

        .folder-content {{
            padding-left: 0.55rem;
            border-left: 1px dashed rgba(255, 255, 255, 0.08);
            margin-left: 0.45rem;
            margin-top: 0.2rem;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .sidebar-controls {{
            display: flex;
            gap: 0.5rem;
            padding: 0.5rem 0.25rem;
            border-bottom: 1px solid var(--card-border);
            margin-bottom: 0.75rem;
        }}

        .sidebar-controls button {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}

        .sidebar-controls button:hover {{
            background: rgba(99, 102, 241, 0.15);
            border-color: var(--card-hover-border);
            color: white;
        }}

        .sidebar-controls button i {{
            width: 12px;
            height: 12px;
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
            <div class="sidebar-controls">
                <button onclick="toggleAllDetails(true)"><i data-lucide="folder-open"></i> Expand All</button>
                <button onclick="toggleAllDetails(false)"><i data-lucide="folder-closed"></i> Collapse All</button>
            </div>
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


def build_sidebar(docs_list: list[dict[str, Any]], current_rel_path: str | None = None, base_path: str = "/") -> str:
    # Filter out nav_hidden: True files
    visible_docs = [doc for doc in docs_list if not doc.get("nav_hidden", False)]

    # Use absolute base_path prefix for all sidebar links
    link_prefix = base_path

    # Build a nested tree structure
    root_node = {"files": [], "dirs": {}}

    for doc in visible_docs:
        rel_html = doc["rel_html"]  # e.g., "docs/30_empowerqnow713/manifesto.html"
        
        # Strip "docs/" prefix if present to find nested folder structure
        path_str = rel_html
        if path_str.startswith("docs/"):
            path_str = path_str[5:]
        elif path_str.startswith("docs\\"):
            path_str = path_str[5:]
            
        parts = path_str.replace("\\", "/").split("/")
        dir_parts = parts[:-1]
        
        current_node = root_node
        for part in dir_parts:
            if not part:
                continue
            current_node = current_node["dirs"].setdefault(part, {"files": [], "dirs": {}})
            
        current_node["files"].append(doc)

    def render_node(node: dict[str, Any], current_path: str | None, prefix: str) -> str:
        html_out = ""
        
        # Render directories first
        for dir_key in sorted(node["dirs"].keys()):
            child = node["dirs"][dir_key]
            
            display_name = dir_key
            if display_name.isdigit() or (len(display_name) > 2 and display_name[:2].isdigit()):
                display_name = re.sub(r"^\d+_", "", display_name)
            display_name = display_name.replace("_", " ").title()
            
            child_html = render_node(child, current_path, prefix)
            if not child_html.strip():
                continue
                
            is_open = False
            if current_path:
                norm_path = current_path.replace("\\", "/")
                path_parts = norm_path.split("/")[:-1]
                if dir_key in path_parts:
                    is_open = True
                    
            open_attr = " open" if is_open else ""
            
            html_out += f"""
            <div class="tree-folder">
                <details{open_attr}>
                    <summary class="folder-header">
                        <i data-lucide="folder" style="width: 14px; height: 14px; color: var(--text-muted)"></i>
                        {html.escape(display_name)}
                    </summary>
                    <div class="folder-content">
                        {child_html}
                    </div>
                </details>
            </div>
            """
            
        # Render files
        sorted_files = sorted(
            node["files"],
            key=lambda x: (x.get("nav_order", 999), str(x.get("nav_title") or "").lower())
        )
        for f in sorted_files:
            is_active = current_path == f["rel_html"]
            active_class = " active" if is_active else ""
            html_out += f"""
            <a href="{html.escape(prefix + f['rel_html'], quote=True)}" class="tree-item{active_class}" title="{html.escape(f['nav_title'], quote=True)}">
                {html.escape(f['nav_title'])}
            </a>
            """
            
        return html_out

    return render_node(root_node, current_rel_path, link_prefix)


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


def render_manifest_node(node: dict[str, Any], docs: list[dict[str, Any]], base_path: str = "/") -> str:
    name = html.escape(node.get("name", "Untitled"))
    node_type = node.get("type", "file")

    if node_type == "directory":
        children = node.get("children", [])
        children_html = "".join(render_manifest_node(child, docs, base_path) for child in children)
        count = len(children)
        return f"""
        <li class="tree-dir">
            <details open>
                <summary class="tree-row">
                    <i data-lucide="folder"></i>
                    <span class="node-name">{name}</span>
                    <span class="node-count">{count}</span>
                </summary>
                <ul>{children_html}</ul>
            </details>
        </li>
        """
    elif node_type == "docs_root":
        doc_items_html = ""
        for doc in sorted(docs, key=lambda d: str(d.get("title")).lower()):
            doc_title = html.escape(doc.get("title", "Untitled"))
            doc_url = html.escape(base_path + doc.get("rel_html", ""), quote=True)
            doc_items_html += f"""
            <li class="tree-file linked">
                <a class="tree-row" href="{doc_url}">
                    <i data-lucide="file-text"></i>
                    <span class="node-name">{doc_title}</span>
                    <span class="node-badge">published</span>
                </a>
            </li>
            """
        if not doc_items_html.strip():
            doc_items_html = '<li class="tree-file"><span class="tree-row"><i data-lucide="info"></i><span class="node-name">No published documents</span></span></li>'

        return f"""
        <li class="tree-dir">
            <details open>
                <summary class="tree-row">
                    <i data-lucide="book-open"></i>
                    <span class="node-name">{name}</span>
                    <span class="node-count">{len(docs)}</span>
                </summary>
                <ul>{doc_items_html}</ul>
            </details>
        </li>
        """
    else:
        url = node.get("url")
        if url:
            if not (url.startswith("http://") or url.startswith("https://") or url.startswith("/")):
                url = base_path + url
            return f"""
            <li class="tree-file linked">
                <a class="tree-row" href="{html.escape(url, quote=True)}">
                    <i data-lucide="globe"></i>
                    <span class="node-name">{name}</span>
                </a>
            </li>
            """
        return f"""
        <li class="tree-file">
            <span class="tree-row">
                <i data-lucide="file"></i>
                <span class="node-name">{name}</span>
            </span>
        </li>
        """


def render_tree_page(
    manifest_path: Path,
    docs: list[dict[str, Any]],
    base_path: str = "/",
) -> str:
    manifest_data: dict[str, Any] = {}
    if manifest_path.exists() and manifest_path.is_file():
        try:
            with manifest_path.open("r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except Exception as e:
            print(f"Error loading tree manifest JSON: {e}")

    nodes = manifest_data.get("nodes", [])
    root_title = manifest_data.get("root_name", "QiLabs Public Surface")

    tree_html = "".join(render_manifest_node(node, docs, base_path) for node in nodes)

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
            border-radius: 999px;
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
            <p>Sanitized public manifest map of QiLabs systems and published documentation pages.</p>
            <div class="tree-meta">
                <span class="tree-pill">Surface: {html.escape(root_title)}</span>
                <span class="tree-pill">Generated: {html.escape(now_iso())}</span>
                <span class="tree-pill">Published Docs: {len(docs)}</span>
            </div>
        </section>

        <section class="glass-card tree-panel">
            <ul class="qilabs-tree">
                {tree_html}
            </ul>
            <p class="tree-note">Built strictly from explicit public architecture manifests. Unpublished filesystem directories are omitted.</p>
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

    SCRIPT_DIR = Path(__file__).resolve().parent

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
        help="Maximum tree depth.",
    )
    parser.add_argument("--config", type=str, default=None, help="Site config JSON path")
    parser.add_argument("--bookmarks-csv", type=str, default=None, help="Bookmarks CSV file path (overrides config)")
    parser.add_argument("--services-json", type=str, default=None, help="Services registry JSON path (overrides config)")
    parser.add_argument("--site-title", type=str, default=None, help="Overrides site title")
    parser.add_argument(
        "--base-path",
        type=str,
        default=None,
        help="URL base path for deployment (e.g. '/' for domain root). "
             "All internal links become absolute from this root.",
    )
    args = parser.parse_args()

    # Load site configuration
    site_title = "QiSpark"
    source_path = DEFAULT_SOURCE
    dist_path = DEFAULT_DIST
    tree_root_path = DEFAULT_QILABS_ROOT
    base_path = "/"  # default: site served from domain root

    config_file = Path(args.config) if args.config else (SCRIPT_DIR / "00_config/site.config.json")
    if config_file.exists() and config_file.is_file():
        try:
            with config_file.open("r", encoding="utf-8") as f:
                site_conf = json.load(f)
                site_title = site_conf.get("site_title", site_title)
                source_path = Path(site_conf.get("default_source", str(source_path)))
                dist_path = Path(site_conf.get("default_dist", str(dist_path)))
                tree_root_path = Path(site_conf.get("default_tree_root", str(tree_root_path)))
                base_path = site_conf.get("base_path", base_path)
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
    if args.base_path is not None:
        base_path = args.base_path

    # Normalize base_path: must start and end with '/'
    base_path = base_path.strip()
    if not base_path.startswith("/"):
        base_path = "/" + base_path
    if not base_path.endswith("/"):
        base_path = base_path + "/"

    source_dir = normalize_path(source_path)
    dist_dir = normalize_path(dist_path)
    tree_root = normalize_path(tree_root_path)
    allow_active = args.allow_active

    print(f"Building Static Site inside: {dist_dir}")
    print(f"Markdown Source, read-only: {source_dir}")
    print(f"QiLabs Tree Root: {tree_root}")
    print(f"Base Path: {base_path}")
    print(f"Allow active status files: {allow_active}")
    print(f"Site Title: {site_title}")
    print("-" * 72)

    # Load publish filters JSON
    filters_file = SCRIPT_DIR / "00_config/publish.filters.json"
    if filters_file.exists() and filters_file.is_file():
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

    # Load services registry JSON
    services = []
    services_file = Path(args.services_json) if args.services_json else (SCRIPT_DIR / "00_config/services.registry.json")
    if services_file.exists() and services_file.is_file():
        try:
            with services_file.open("r", encoding="utf-8") as f:
                services = json.load(f)
        except Exception as e:
            print(f"Error loading services registry JSON: {e}")

    if not services:
        services = [
            {"id": "qispark_docs", "title": "QiSpark Docs", "description": "Static documentation and blueprints.", "url": "docs/index.html", "icon": "book-open", "color": "#38bdf8", "category": "Primary", "surface": ["public"], "status": "active"},
            {"id": "qilabs_tree", "title": "QiLabs Tree", "description": "Sanitized map of public workspace systems and documentation.", "url": "tree.html", "icon": "folder-tree", "color": "#14b8a6", "category": "Primary", "surface": ["public"], "status": "active"},
            {"id": "qisaysit", "title": "QiSaysIt", "description": "Public writing, posts and publishing surface.", "url": "https://qsaysit.com", "icon": "pencil-line", "color": "#10b981", "category": "Publishing", "surface": ["public"], "status": "active"},
            {"id": "qially", "title": "QiAlly", "description": "Primary QiAlly public domain hub.", "url": "https://qially.com", "icon": "globe", "color": "#3b82f6", "category": "Publishing", "surface": ["public"], "status": "active"}
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
        doc_sidebar = build_sidebar(docs, doc["rel_html"], base_path=base_path)
        home_path = base_path + "index.html"
        docs_path = base_path + "docs/index.html"
        tree_path = base_path + "tree.html"

        page_html = make_header(doc["title"], home_path, docs_path, tree_path, site_title=site_title)
        page_html += render_docs_layout(doc_sidebar, doc["html_body"], doc["frontmatter"])
        page_html += HTML_FOOTER

        write_text(doc["out_path"], page_html)

    # 6. Generate docs index page
    if docs:
        docs_idx_path = dist_dir / "docs" / "index.html"
        docs_idx_sidebar = build_sidebar(docs, "docs/index.html", base_path=base_path)
        welcome_html = """
        <h1>Welcome to QiSpark Documentation</h1>
        <p>Select a document from the left sidebar to begin reading.</p>
        """
        docs_index = make_header("QiSpark Documentation Index", base_path + "index.html", base_path + "docs/index.html", base_path + "tree.html", site_title=site_title)
        docs_index += render_docs_layout(docs_idx_sidebar, welcome_html, {})
        docs_index += HTML_FOOTER
        write_text(docs_idx_path, docs_index)

    # 7. Generate QiLabs tree page
    if not args.no_tree:
        tree_manifest_file = SCRIPT_DIR / "00_config/tree.manifest.json"
        tree_page = make_header("QiLabs Tree", base_path + "index.html", base_path + "docs/index.html" if docs else "#", base_path + "tree.html", site_title=site_title)
        tree_page += render_tree_page(
            manifest_path=tree_manifest_file,
            docs=docs,
            base_path=base_path,
        )
        tree_page += HTML_FOOTER
        write_text(dist_dir / "tree.html", tree_page)
        print(f"Generated QiLabs tree: {dist_dir / 'tree.html'}")

    # 8. Generate homepage
    docs_path_hp = base_path + "docs/index.html" if docs else "#"
    dashboard_html = make_header(site_title, base_path + "index.html", docs_path_hp, base_path + "tree.html", site_title=site_title)
    dashboard_html += render_landing(services, base_path + "docs" if docs else "#", base_path + "tree.html")
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
