import os
import json
from pathlib import Path

def get_markdown_files(paths):
    files = []
    for p in paths:
        path_obj = Path(p)
        if not path_obj.exists():
            continue
        if path_obj.is_file():
            if path_obj.suffix in ['.md', '.mdx']:
                files.append(path_obj.stem)
        else:
            for root, _, filenames in os.walk(p):
                # Skip archive
                if '90_archive' in root:
                    continue
                for f in filenames:
                    if f.endswith('.md') or f.endswith('.mdx'):
                        full_path = os.path.join(root, f)
                        # Store posix path relative to current dir, without extension
                        rel = Path(full_path).as_posix()
                        rel = rel.rsplit('.', 1)[0]
                        files.append(rel)
    return sorted(files)

nav = [
    {
        "group": "QiLabs Workspace",
        "pages": ["00_start_here/index"] + get_markdown_files(["README.md", "codex.md", "docs/00_QiLabs.workspace"])
    },
    {
        "group": "QiSpark",
        "pages": get_markdown_files(["docs/10_QiSpark", "decisions", "registries", "standards"])
    },
    {
        "group": "QiServer",
        "pages": get_markdown_files(["docs/20_QiServer"])
    },
    {
        "group": "QiMemory",
        "pages": get_markdown_files(["docs/30_QiMemory"])
    },
    {
        "group": "QiVault",
        "pages": get_markdown_files(["docs/40_QiVault"])
    },
    {
        "group": "QiConnect",
        "pages": get_markdown_files(["docs/50_QiConnect"])
    },
    {
        "group": "QiApps",
        "pages": get_markdown_files(["docs/60_QiApps"])
    }
]

# Filter out empty groups just in case, though they should be fine
nav = [g for g in nav if len(g["pages"]) > 0]

docs = {
  "name": "QiOS DNA Knowledge Base",
  "logo": {
    "dark": "/logo/dark.svg",
    "light": "/logo/light.svg"
  },
  "favicon": "/favicon.svg",
  "colors": {
    "primary": "#2D3748",
    "light": "#4A5568",
    "dark": "#1A202C"
  },
  "topbarLinks": [
    {
      "name": "GitHub",
      "url": "https://github.com"
    }
  ],
  "navigation": nav
}

with open("docs.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, indent=2)

# Also write to docs/docs.json for Mintlify subdirectory support
docs_dir = Path("docs")
if docs_dir.exists() and docs_dir.is_dir():
    with open(docs_dir / "docs.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)

print("docs.json successfully regenerated in root and docs/ subfolder.")
