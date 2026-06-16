from pathlib import Path
import shutil
import hashlib
import os

ROOT = Path(r"C:\QiLabs\10_QiSpark")
QISERVER_SUPABASE_DEST = Path(r"C:\QiLabs\20_QiServer\data\supabase\qisupabase")

ACTIONS = []


def log(msg: str):
    print(msg)
    ACTIONS.append(msg)


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    i = 2
    while True:
        candidate = parent / f"{stem}__dup{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def remove_if_empty(path: Path):
    try:
        if path.exists() and path.is_dir() and not any(path.iterdir()):
            path.rmdir()
            log(f"REMOVED EMPTY DIR: {path}")
    except Exception as e:
        log(f"SKIPPED EMPTY DIR REMOVE: {path} :: {e}")


def move_path(src: Path, dest: Path):
    src = Path(src)
    dest = Path(dest)

    if not src.exists():
        return

    ensure_dir(dest.parent)

    if src.is_dir():
        ensure_dir(dest)

        for child in list(src.iterdir()):
            move_path(child, dest / child.name)

        remove_if_empty(src)
        return

    if dest.exists():
        if dest.is_file():
            try:
                if file_hash(src) == file_hash(dest):
                    src.unlink()
                    log(f"DELETED DUPLICATE FILE: {src}")
                    return
            except Exception:
                pass

        dest = unique_path(dest)

    shutil.move(str(src), str(dest))
    log(f"MOVED: {src} -> {dest}")


def move_contents(src_dir: Path, dest_dir: Path):
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)

    if not src_dir.exists() or not src_dir.is_dir():
        return

    ensure_dir(dest_dir)

    for child in list(src_dir.iterdir()):
        move_path(child, dest_dir / child.name)

    remove_if_empty(src_dir)


def rename_file(src: Path, dest: Path):
    move_path(src, dest)


def delete_aider():
    for path in sorted(ROOT.rglob("*"), key=lambda p: len(str(p)), reverse=True):
        if "aider" in path.name.lower():
            if path.is_dir():
                shutil.rmtree(path)
                log(f"DELETED AIDER DIR: {path}")
            elif path.is_file():
                path.unlink()
                log(f"DELETED AIDER FILE: {path}")


def remove_empty_dirs():
    for path in sorted(ROOT.rglob("*"), key=lambda p: len(str(p)), reverse=True):
        if path.is_dir():
            remove_if_empty(path)


def main():
    if not ROOT.exists():
        raise SystemExit(f"ROOT NOT FOUND: {ROOT}")

    docs = ROOT / "docs"

    # ---------------------------------------------------------------------
    # Required root folders
    # ---------------------------------------------------------------------
    for folder in [
        ".agents",
        ".obsidian",
        "00_start_here",
        "assets",
        "docs",
        "site",
        "tools",
    ]:
        ensure_dir(ROOT / folder)

    for folder in [
        "00_QiLabs.workspace",
        "10_QiSpark",
        "20_QiServer",
        "30_QiMemory",
        "40_QiVault",
        "50_QiConnect",
        "60_QiApps",
        "decisions",
        "standards",
        "registries",
        "schemas",
    ]:
        ensure_dir(docs / folder)

    # ---------------------------------------------------------------------
    # Root files that Mintlify / QiSpark expects at root
    # ---------------------------------------------------------------------
    move_path(docs / "assistant.md", ROOT / "assistant.md")
    move_path(docs / "docs.json", ROOT / "docs.json")
    move_path(docs / "codex.md", ROOT / "codex.md")

    # ---------------------------------------------------------------------
    # Start Here should be static HTML
    # ---------------------------------------------------------------------
    start_here = ROOT / "00_start_here"
    if (start_here / "index.mdx").exists() and not (start_here / "index.html").exists():
        move_path(start_here / "index.mdx", start_here / "index.html")

    # ---------------------------------------------------------------------
    # Root docs buckets belong inside docs/
    # ---------------------------------------------------------------------
    move_path(docs / "decisions", docs / "decisions")
    move_path(docs / "standards", docs / "standards")
    move_path(docs / "registries", docs / "registries")

    # schema -> schemas
    move_contents(docs / "schema", docs / "schemas")
    remove_if_empty(docs / "schema")

    # loose rules folder belongs under standards
    move_contents(docs / "rules", docs / "standards" / "rules")
    remove_if_empty(docs / "rules")

    # operations are QiSpark docs operations, not a top-level docs root
    move_contents(docs / "operations", docs / "10_QiSpark" / "operations")
    remove_if_empty(docs / "operations")

    # ---------------------------------------------------------------------
    # Clean docs/10_QiSpark/_qieos into current folders
    # ---------------------------------------------------------------------
    qieos = docs / "10_QiSpark" / "_qieos"

    if qieos.exists():
        move_contents(qieos / "decisions", docs / "decisions")
        move_contents(qieos / "governance", docs / "10_QiSpark" / "governance")
        move_contents(qieos / "principals", docs / "10_QiSpark" / "principles")
        move_contents(qieos / "principles", docs / "10_QiSpark" / "principles")
        move_contents(qieos / "registry", docs / "registries")
        move_contents(qieos / "rules", docs / "standards" / "rules")
        move_contents(qieos / "standards", docs / "standards")
        move_contents(qieos / "structure", docs / "10_QiSpark" / "structure")

        # qieos/data contains docs and registries. Split the obvious registry/schema parts.
        data = qieos / "data"
        if data.exists():
            move_contents(data / "35_registry", docs / "registries")
            move_contents(data / "50_namespace_registry", docs / "registries" / "namespace_registry")
            move_contents(data / "schemas", docs / "schemas")
            move_contents(data, docs / "10_QiSpark" / "data")

        # qieos/services splits by actual new root purpose.
        services = qieos / "services"
        if services.exists():
            move_contents(services / "100_integrations", docs / "50_QiConnect" / "integrations")
            move_contents(services / "10_infrastructure", docs / "20_QiServer" / "infrastructure")
            move_contents(services / "110_qiserver", docs / "20_QiServer")
            move_contents(services / "120_applications", docs / "60_QiApps" / "applications")
            move_contents(services / "130_GINA", docs / "60_QiApps" / "GINA")
            move_contents(services / "20_ai_compute", docs / "20_QiServer" / "ai_compute")
            move_contents(services / "30_capture", docs / "30_QiMemory" / "tools")
            move_contents(services / "40_productivity", docs / "60_QiApps" / "productivity")
            move_contents(services / "50_apis", docs / "50_QiConnect" / "apis")
            move_contents(services / "60_workers", docs / "20_QiServer" / "workers")
            move_contents(services / "workers", docs / "20_QiServer" / "workers")
            move_contents(services / "70_pipelines", docs / "30_QiMemory" / "pipelines")
            move_contents(services / "80_tools", docs / "20_QiServer" / "tools")
            move_contents(services / "90_interfaces", docs / "60_QiApps" / "interfaces")

            move_path(services / "40_service_apps.md", docs / "10_QiSpark" / "service_apps.md")
            move_path(services / "_index.md", docs / "10_QiSpark" / "services_index.md")
            remove_if_empty(services)

        # qieos loose files
        move_path(qieos / "README.md", docs / "10_QiSpark" / "README.md")
        move_path(qieos / "_QiEOS.md", docs / "10_QiSpark" / "core_overview.md")
        move_path(qieos / "codex.md", ROOT / "codex.md")
        move_path(qieos / "file-index.json", ROOT / "assets" / "exports" / "file-index.json")

        remove_if_empty(qieos)

    # ---------------------------------------------------------------------
    # Server docs: remove old QiSystem wrapper and move app material out
    # ---------------------------------------------------------------------
    server = docs / "20_QiServer"
    qiserver_app_stuff = docs / "60_QiApps" / "QiLife"

    move_contents(server / "50_modules", qiserver_app_stuff / "50_modules")
    move_contents(server / "60_ai_layer", qiserver_app_stuff / "60_ai_layer")
    move_contents(server / "70_deployment", qiserver_app_stuff / "70_deployment")
    move_contents(server / "80_prompts", qiserver_app_stuff / "80_prompts")

    # Flatten old QiSystem wrapper into server docs if anything exists.
    move_contents(server / "20_QiSystem", server)
    remove_if_empty(server / "20_QiSystem")

    # Rename marker files.
    rename_file(server / "_30_QiServer.md", server / "_20_QiServer.md")
    rename_file(server / "_20_QiSystem.md", server / "server_data_source.md")

    # Rename old DNA manifest if present.
    rename_file(
        server / "manifests" / "QiOS_DNA_File_Manifest.mdx",
        server / "manifests" / "QiSpark_File_Manifest.mdx",
    )

    # ---------------------------------------------------------------------
    # QiMemory docs
    # ---------------------------------------------------------------------
    memory = docs / "30_QiMemory"

    rename_file(memory / "_40_QiCapture.md", memory / "_30_QiMemory.md")

    # Keep old tooling notes, but put them in one place.
    ensure_dir(memory / "legacy_tools")
    move_path(memory / "nocodb.md", memory / "legacy_tools" / "nocodb.md")
    move_path(memory / "wikijs.md", memory / "legacy_tools" / "wikijs.md")
    move_path(memory / "obsidian_qidocs.md", memory / "legacy_tools" / "obsidian_qidocs.md")

    # ---------------------------------------------------------------------
    # QiVault docs
    # ---------------------------------------------------------------------
    vault = docs / "40_QiVault"
    rename_file(vault / "_50_QiNexus.md", vault / "_40_QiVault.md")

    # ---------------------------------------------------------------------
    # QiConnect docs
    # ---------------------------------------------------------------------
    connect = docs / "50_QiConnect"
    move_contents(connect / "06_workflows", connect / "workflows")
    remove_if_empty(connect / "06_workflows")
    rename_file(connect / "_60_QiConnect.md", connect / "_50_QiConnect.md")

    # ---------------------------------------------------------------------
    # QiApps docs: flatten old 1000/1100 wrappers
    # ---------------------------------------------------------------------
    apps = docs / "60_QiApps"

    move_contents(apps / "1100_QiLife", apps / "QiLife")

    old_apps = apps / "1000_QiApps"
    if old_apps.exists():
        move_contents(old_apps / "QiJourney", apps / "QiJourney")
        move_contents(old_apps / "QiLife", apps / "QiLife")
        move_contents(old_apps / "qiaccess_start", apps / "QiAccess")
        move_contents(old_apps / "site", apps / "Sites" / "legacy_static_site")
        move_path(old_apps / "_1000_QiApps.md", apps / "_60_QiApps.md")
        remove_if_empty(old_apps)

    rename_file(apps / "QiLife" / "_1100_QiLife.md", apps / "QiLife" / "_QiLife.md")

    # ---------------------------------------------------------------------
    # Move descriptive schema docs into docs/schemas
    # ---------------------------------------------------------------------
    move_path(ROOT / "Schema" / "_Schema.md", docs / "schemas" / "_Schema.md")
    remove_if_empty(ROOT / "Schema")

    # ---------------------------------------------------------------------
    # Move Supabase out of QiSpark. QiSpark should not own DB runtime files.
    # ---------------------------------------------------------------------
    if (ROOT / "supabase").exists():
        move_contents(ROOT / "supabase", QISERVER_SUPABASE_DEST)
        remove_if_empty(ROOT / "supabase")

    # ---------------------------------------------------------------------
    # Root helper files into tools/assets
    # ---------------------------------------------------------------------
    move_path(ROOT / "build_docs_json.py", ROOT / "tools" / "build_docs_json.py")
    move_path(ROOT / "code_extractor.py", ROOT / "tools" / "code_extractor.py")
    move_path(ROOT / "update_nav.js", ROOT / "tools" / "update_nav.js")
    move_path(ROOT / "vizvibe.mmd", ROOT / "assets" / "diagrams" / "vizvibe.mmd")

    # ---------------------------------------------------------------------
    # Move loose old root docs into docs/10_QiSpark
    # ---------------------------------------------------------------------
    move_path(ROOT / "_01_QiDNA.md", docs / "10_QiSpark" / "old_qidna_notes.md")
    move_path(ROOT / "_Architecture.md", docs / "10_QiSpark" / "architecture.md")

    # Delete junk loose file if present.
    junk = ROOT / ".md"
    if junk.exists() and junk.is_file():
        junk.unlink()
        log(f"DELETED JUNK FILE: {junk}")

    junk = ROOT / "occurrences.txt"
    if junk.exists() and junk.is_file():
        junk.unlink()
        log(f"DELETED JUNK FILE: {junk}")

    # ---------------------------------------------------------------------
    # Aider can go.
    # ---------------------------------------------------------------------
    delete_aider()

    # ---------------------------------------------------------------------
    # Remove empty directories after all moves.
    # ---------------------------------------------------------------------
    remove_empty_dirs()

    # ---------------------------------------------------------------------
    # Final scan for old names in active paths.
    # ---------------------------------------------------------------------
    old_terms = [
        "00_QiEOS",
        "_qieos",
        "QiDNA",
        "QiSystem",
        "QiCapture",
        "QiNexus",
        "1000_QiApps",
        "1100_QiLife",
        "aider",
    ]

    hits = []
    for path in ROOT.rglob("*"):
        rel = str(path.relative_to(ROOT))
        lowered = rel.lower()
        for term in old_terms:
            if term.lower() in lowered:
                hits.append(rel)
                break

    print("\n" + "=" * 72)
    print("QiSpark cleanup complete.")
    print("=" * 72)

    print("\nFinal expected root folders:")
    for name in [
        ".agents",
        ".obsidian",
        "00_start_here",
        "assets",
        "docs",
        "site",
        "tools",
    ]:
        print(f" - {name}")

    print("\nFinal expected docs folders:")
    for name in [
        "00_QiLabs.workspace",
        "10_QiSpark",
        "20_QiServer",
        "30_QiMemory",
        "40_QiVault",
        "50_QiConnect",
        "60_QiApps",
        "decisions",
        "standards",
        "registries",
        "schemas",
    ]:
        print(f" - docs\\{name}")

    if hits:
        print("\nOld-name paths still found:")
        for h in hits[:200]:
            print(f" - {h}")
        if len(hits) > 200:
            print(f" ... plus {len(hits) - 200} more")
    else:
        print("\nNo old-name paths found.")

    print("\nActions performed:", len(ACTIONS))


if __name__ == "__main__":
    main()