"""
vault_publish_tagger.py
-----------------------
Scans the QiVault and sets `status: publish` on markdown files whose
filename/title do NOT appear sensitive.

Sensitivity is judged by keyword matching on the filename stem.
Safety-first: when in doubt, skip (leave untouched).

Usage:
  py vault_publish_tagger.py              # dry-run, prints what WOULD change
  py vault_publish_tagger.py --apply      # applies changes
  py vault_publish_tagger.py --verbose    # show every skip reason too
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Force UTF-8 output so emoji/unicode filenames don't crash on Windows terminals
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
VAULT_ROOT = Path(r"C:\QiLabs\40_QiVault")

# Folders to completely skip — never publish anything from these
SKIP_DIRS = {
    ".git", ".obsidian", ".trash", ".neural_memory", ".smart-env",
    ".reference-map",
    "02_directory",   # personal contacts / people directory
    "10_daily",       # personal journal / daily notes — too personal
    "01_inbox",       # unprocessed inbox — unknown content
    "20_life",        # personal life / health / identity
    "80_records",     # records (financial, medical, legal)
    "45_cases",       # legal cases
    "90_outputs",     # internal cleanup logs and AI outputs
    "Lisa_Care_Record_2026",  # care/medical records folder
    "Templates",      # template stubs, not real content
    "copilot",        # AI chat logs
    "Voice Entries",  # voice journal
    "TaskNotes",      # scratch task notes
    "Markwhen",       # timeline data
    "_qiconfig",      # config files
}

# Filename stem keywords that indicate sensitive content — SKIP these
# Even one match = skip the file
SENSITIVE_KEYWORDS = {
    # Personal/identity
    "private", "personal", "confidential", "secret", "sensitive",
    "password", "credential", "token", "api_key", "ssn", "social_security",
    "address", "phone", "contact_info", "contact",
    # Legal / case matters
    "lawsuit", "case", "court", "judgment", "felony", "owi", "bmv",
    "suspension", "arrest", "criminal", "deport", "immigration", "waiver",
    "i601", "i_601", "charges", "offense", "escape", "entry",
    # Financial records
    "debt", "foreclosure", "frozen", "financial_report", "annual_financial",
    "promissory", "mortgage", "check_fraud", "theft", "consolidate",
    "creditor", "bankruptcy", "amex", "chase", "citi", "capone",
    "consoridate",  # typo variant in the vault
    # Medical / health records
    "diagnosis", "medical", "health_crisis", "escalating_health",
    "care_record", "therapy", "mental_health", "emotional",
    "trauma", "abuse", "neglect", "prostitution",
    "physical_health", "mental_clarity", "emotional_balance", "wellbeing",
    "health_and",
    # Relationship / private matters
    "betrayal", "narcissistic", "abusive", "roommate",
    "deportation", "grief", "compounded_grief",
    "marriage", "meeting_joel", "joels", "birthday_boundaries",
    # Business disputes
    "iisitax", "unlawfully", "employee_theft", "business_collapse",
    "loss_of_assets", "housing_instability",
    # People's legal issues (named individuals)
    "luis_", "zaitullah", "joels_",
    # Location / household
    "household_meeting", "elliott_st", "unclaimed_property",
    # War/refugee (personal stories)
    "kabul", "taliban", "evacuation", "combat",
    # Misc raw / system files
    "_index", "missing_metadata", "todo", "scratch", "draft",
    "inbox", "capture", "chatnotw", "ai_chat",
    "copilot", "voice",
    # Cleanup / internal logs
    "cleanup_", "triage", "lisa_care",
}

# Folder path segments that signal sensitivity (any part of the path)
SENSITIVE_PATH_SEGMENTS = {
    "10_daily", "01_inbox", "80_records", "45_cases",
    "Luis_Care_Record", "20_life/10_me",  # personal life/identity
    "10_me",     # personal identity notes
    "20_stuff",  # personal misc
    "40_work",   # work records (could contain private info)
    "ai_chats", "copilot",
}

# Filename stems that are ALWAYS safe to publish regardless of folder
ALWAYS_PUBLISH_STEMS = {
    "readme", "_index",  # keep _index off by default but override here if needed
}

# Statuses that already count as published — don't touch
ALREADY_PUBLISHED = {"publish", "published", "public", "pub"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
STATUS_RE = re.compile(r"^status\s*:\s*(.+)$", re.MULTILINE)
PRIVACY_RE = re.compile(r"^privacy\s*:\s*(.+)$", re.MULTILINE)
VISIBILITY_RE = re.compile(r"^visibility\s*:\s*(.+)$", re.MULTILINE)
SENSITIVITY_RE = re.compile(r"^sensitivity\s*:\s*(.+)$", re.MULTILINE)
PRIVATE_FLAG_RE = re.compile(r"^(private|confidential|sensitive)\s*:\s*(true|yes|1)$", re.MULTILINE | re.IGNORECASE)


def get_frontmatter_block(text: str) -> str | None:
    m = FRONTMATTER_RE.match(text)
    return m.group(1) if m else None


def get_fm_value(fm: str, pattern: re.Pattern) -> str:
    m = pattern.search(fm)
    return m.group(1).strip().strip('"\'').lower() if m else ""


def is_sensitive_by_name(stem: str) -> tuple[bool, str]:
    """Check filename stem for sensitive keywords."""
    stem_lower = stem.lower()
    for kw in SENSITIVE_KEYWORDS:
        if kw in stem_lower:
            return True, f"keyword '{kw}' in filename"
    return False, ""


def is_sensitive_by_path(rel_path: Path) -> tuple[bool, str]:
    """Check any part of the relative path for sensitive segments."""
    parts_lower = {p.lower() for p in rel_path.parts}
    for seg in SENSITIVE_PATH_SEGMENTS:
        seg_lower = seg.lower()
        for part in parts_lower:
            if seg_lower in part:
                return True, f"path segment '{seg}'"
    return False, ""


def is_sensitive_by_frontmatter(fm: str) -> tuple[bool, str]:
    """Check frontmatter fields for privacy/sensitivity markers."""
    privacy = get_fm_value(fm, PRIVACY_RE)
    visibility = get_fm_value(fm, VISIBILITY_RE)
    sensitivity = get_fm_value(fm, SENSITIVITY_RE)

    if privacy in ("private", "internal"):
        return True, f"privacy: {privacy}"
    if visibility in ("private", "internal"):
        return True, f"visibility: {visibility}"
    if sensitivity in ("private", "sensitive", "confidential"):
        return True, f"sensitivity: {sensitivity}"
    if PRIVATE_FLAG_RE.search(fm):
        return True, "explicit private/confidential flag in frontmatter"

    return False, ""


def set_status_publish(text: str, fm_block: str) -> str:
    """Replace the status field in frontmatter with 'publish'."""
    old_status_match = STATUS_RE.search(fm_block)
    if old_status_match:
        old_line = old_status_match.group(0)
        # Build new status line preserving indentation style
        new_line = re.sub(r"(status\s*:\s*).*", r"\1publish", old_line)
        new_fm = fm_block.replace(old_line, new_line, 1)
    else:
        new_fm = fm_block.rstrip() + "\nstatus: publish"

    # Replace the frontmatter block using plain string ops (avoid regex on user content)
    old_block = f"---\n{fm_block}\n---"
    new_block = f"---\n{new_fm}\n---"
    # Only replace the first occurrence (the frontmatter at the top)
    return text.replace(old_block, new_block, 1)


# ---------------------------------------------------------------------------
# Main scan
# ---------------------------------------------------------------------------
def scan_vault(apply: bool, verbose: bool) -> None:
    stats = {
        "scanned": 0,
        "already_published": 0,
        "marked_publish": 0,
        "skipped_no_frontmatter": 0,
        "skipped_sensitive_path": 0,
        "skipped_sensitive_name": 0,
        "skipped_sensitive_frontmatter": 0,
        "skipped_skip_dir": 0,
        "errors": 0,
    }
    changed_files: list[str] = []
    skipped_files: list[tuple[str, str]] = []

    for md_file in sorted(VAULT_ROOT.rglob("*.md")):
        rel = md_file.relative_to(VAULT_ROOT)
        stats["scanned"] += 1

        # 1. Skip entire folder trees
        skip_dir_hit = None
        for part in rel.parts[:-1]:  # exclude the filename itself
            if part in SKIP_DIRS:
                skip_dir_hit = part
                break
        if skip_dir_hit:
            stats["skipped_skip_dir"] += 1
            if verbose:
                print(f"  SKIP-DIR    {rel}  (in skip dir: {skip_dir_hit})")
            continue

        # 2. Read file
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR reading {rel}: {e}")
            continue

        # 3. Must have frontmatter
        fm_block = get_frontmatter_block(text)
        if fm_block is None:
            stats["skipped_no_frontmatter"] += 1
            if verbose:
                print(f"  SKIP-FM     {rel}  (no frontmatter)")
            continue

        # 4. Already published?
        current_status = get_fm_value(fm_block, STATUS_RE)
        if current_status in ALREADY_PUBLISHED:
            stats["already_published"] += 1
            if verbose:
                print(f"  ALREADY     {rel}  (status: {current_status})")
            continue

        # 5. Sensitive path check
        sensitive, reason = is_sensitive_by_path(rel)
        if sensitive:
            stats["skipped_sensitive_path"] += 1
            skipped_files.append((str(rel), f"path: {reason}"))
            if verbose:
                print(f"  SKIP-PATH   {rel}  ({reason})")
            continue

        # 6. Sensitive filename check
        sensitive, reason = is_sensitive_by_name(md_file.stem)
        if sensitive:
            stats["skipped_sensitive_name"] += 1
            skipped_files.append((str(rel), f"name: {reason}"))
            if verbose:
                print(f"  SKIP-NAME   {rel}  ({reason})")
            continue

        # 7. Sensitive frontmatter check
        sensitive, reason = is_sensitive_by_frontmatter(fm_block)
        if sensitive:
            stats["skipped_sensitive_frontmatter"] += 1
            skipped_files.append((str(rel), f"fm: {reason}"))
            if verbose:
                print(f"  SKIP-FM     {rel}  ({reason})")
            continue

        # 8. Safe to publish
        stats["marked_publish"] += 1
        changed_files.append(str(rel))
        print(f"  {'PUBLISH' if apply else 'WOULD PUBLISH'}  {rel}  (was: '{current_status}')")

        if apply:
            new_text = set_status_publish(text, fm_block)
            md_file.write_text(new_text, encoding="utf-8")

    # Summary
    print()
    print("=" * 72)
    print(f"{'APPLIED' if apply else 'DRY RUN'} — Vault Publish Tagger")
    print("=" * 72)
    print(f"  Scanned:              {stats['scanned']}")
    print(f"  Already published:    {stats['already_published']}")
    print(f"  Marked publish:       {stats['marked_publish']}  {'(WRITTEN)' if apply else '(preview only)'}")
    print(f"  Skip (skip-dir):      {stats['skipped_skip_dir']}")
    print(f"  Skip (no frontmatter):{stats['skipped_no_frontmatter']}")
    print(f"  Skip (path):          {stats['skipped_sensitive_path']}")
    print(f"  Skip (name):          {stats['skipped_sensitive_name']}")
    print(f"  Skip (frontmatter):   {stats['skipped_sensitive_frontmatter']}")
    print(f"  Errors:               {stats['errors']}")
    print()
    if not apply:
        print("Run with --apply to write changes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tag non-sensitive vault files as status: publish")
    parser.add_argument("--apply", action="store_true", help="Write changes (default is dry-run)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all skip reasons too")
    args = parser.parse_args()
    scan_vault(apply=args.apply, verbose=args.verbose)
