#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path

def get_md_title(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        # Check frontmatter
        fm_match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL | re.MULTILINE)
        if fm_match:
            fm = fm_match.group(1)
            title_match = re.search(r"^title:\s*[\"']?(.*?)[\"']?\s*$", fm, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip()
        # Check H1
        h1_match = re.search(r"^#\s+(.*?)\s*$", content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
    except Exception:
        pass
    # fallback to cleaning up the filename stem
    stem = path.stem
    if stem.startswith("_"):
        stem = stem[1:]
    return stem.replace("_", " ").title()

def generate_hierarchy(current_dir: Path, base_dir: Path, depth: int = 0) -> list[str]:
    lines = []
    indent = "  " * depth
    
    # List immediate files and subdirectories
    try:
        items = sorted(list(current_dir.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
    except OSError:
        return []
    
    for item in items:
        if item.is_file():
            if item.suffix in [".md", ".mdx"] and item.name not in ["_index.md", "index.md"]:
                title = get_md_title(item)
                rel_path = item.relative_to(base_dir).as_posix()
                lines.append(f"{indent}- [{title}]({rel_path})")
        elif item.is_dir():
            # Skip special directories
            if item.name.startswith(".") or item.name in ["node_modules", "assets"]:
                continue
            
            # Check if directory contains any markdown files recursively
            has_md = any(f.suffix in [".md", ".mdx"] for f in item.rglob("*") if f.is_file())
            if has_md:
                folder_title = item.name.replace("_", " ").title()
                index_file = item / "_index.md"
                if index_file.exists():
                    folder_title = get_md_title(index_file)
                
                rel_path = (item / "_index.md").relative_to(base_dir).as_posix()
                lines.append(f"{indent}- [{folder_title}]({rel_path})")
                # Recurse
                lines.extend(generate_hierarchy(item, base_dir, depth + 1))
    return lines

def write_index_for_dir(dir_path: Path):
    title = dir_path.name.replace("_", " ").title()
    if dir_path.name == "docs":
        title = "Documentation Root"
        
    description = ""
    index_file = dir_path / "_index.md"
    
    if index_file.exists():
        try:
            content = index_file.read_text(encoding="utf-8", errors="ignore")
            # Parse H1
            h1_match = re.search(r"^#\s+(.*?)\s*$", content, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1).strip()
            # Find everything before '## Navigation' or '## Directory Index' to preserve description
            nav_pos = re.search(r"^##\s+(Navigation|Directory Index|Folder Index)", content, re.MULTILINE | re.IGNORECASE)
            if nav_pos:
                description = content[:nav_pos.start()].strip()
            else:
                lines = content.splitlines()
                desc_lines = []
                for line in lines:
                    if line.strip().startswith("# "):
                        continue
                    desc_lines.append(line)
                description = "\n".join(desc_lines).strip()
        except Exception:
            pass

    # Build document
    header = f"# {title}"
    if description:
        if not description.startswith("#"):
            body = f"{header}\n\n{description}"
        else:
            body = description
    else:
        body = f"{header}\n\nFolder index for {title}."

    hierarchy_lines = generate_hierarchy(dir_path, dir_path, depth=0)
    
    if hierarchy_lines:
        body += "\n\n## Navigation\n\n" + "\n".join(hierarchy_lines)
    else:
        body += "\n\n(No sub-items found)"

    index_file.write_text(body + "\n", encoding="utf-8")
    print(f"Generated index: {index_file}")

def main():
    docs_root = Path("docs").resolve()
    if not docs_root.exists() or not docs_root.is_dir():
        print(f"Error: 'docs' folder not found under {os.getcwd()}")
        return

    # Gather all subdirectories recursively, starting with the root docs/ folder
    all_dirs = [docs_root]
    for root, dirs, _ in os.walk(docs_root):
        for d in dirs:
            path = Path(root) / d
            if not path.name.startswith(".") and path.name not in ["node_modules", "assets"]:
                all_dirs.append(path)

    print(f"Found {len(all_dirs)} directories to check/index.")
    for d in all_dirs:
        # Check if the folder itself contains any markdown files at all recursively
        # (if it doesn't contain any, we skip indexing it to keep the structure clean)
        has_any_md = any(f.suffix in [".md", ".mdx"] for f in d.rglob("*") if f.is_file())
        if has_any_md:
            write_index_for_dir(d)

if __name__ == "__main__":
    main()
