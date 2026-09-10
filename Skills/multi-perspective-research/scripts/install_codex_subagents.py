#!/usr/bin/env python3
"""Install optional Codex custom agents for the multi-perspective-research skill.

The script copies TOML templates from assets/codex-agents/ into either:
- <repo>/.codex/agents/ for project-scoped agents, or
- ~/.codex/agents/ for user-scoped agents.

It performs a light TOML/schema validation and refuses to overwrite existing files
unless --overwrite is provided.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from collections import Counter
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None  # type: ignore[assignment]

REQUIRED_STRING_KEYS = {"name", "description", "developer_instructions"}


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy multi-perspective Codex custom agent TOML templates into a Codex agents directory."
    )
    parser.add_argument(
        "--scope",
        choices=("repo", "user"),
        default="repo",
        help="Install into a repository .codex/agents directory or the current user's ~/.codex/agents directory.",
    )
    parser.add_argument(
        "--target",
        default=None,
        help="Repository path for --scope repo. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing agent files with the same filenames.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate templates and print the files that would be copied without writing anything.",
    )
    return parser.parse_args()


def destination_dir(scope: str, target: str | None) -> Path:
    if scope == "user":
        return Path.home() / ".codex" / "agents"
    repo = Path(target or os.getcwd()).expanduser().resolve()
    return repo / ".codex" / "agents"


def load_toml(path: Path) -> dict:
    if tomllib is None:
        raise RuntimeError("Python 3.11+ is required for built-in TOML validation via tomllib.")
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    if not isinstance(data, dict):
        raise ValueError("TOML root is not a table")
    return data


def validate_template(path: Path) -> str:
    data = load_toml(path)
    missing = sorted(REQUIRED_STRING_KEYS - set(data))
    if missing:
        raise ValueError(f"missing required keys: {', '.join(missing)}")
    for key in REQUIRED_STRING_KEYS:
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a non-empty string")
    name = data["name"]
    if not name.startswith("mpr_"):
        raise ValueError("agent name should start with 'mpr_' to avoid collisions")
    expected_stem = name.replace("_", "-")
    if path.stem != expected_stem:
        raise ValueError(f"filename stem should be '{expected_stem}' for agent name '{name}'")
    if data.get("sandbox_mode") != "read-only":
        raise ValueError("sandbox_mode must be 'read-only'")
    nicknames = data.get("nickname_candidates")
    if nicknames is not None:
        if not isinstance(nicknames, list) or not nicknames:
            raise ValueError("nickname_candidates must be a non-empty list when provided")
        if not all(isinstance(nickname, str) and nickname.strip() for nickname in nicknames):
            raise ValueError("nickname_candidates must contain only non-empty strings")
    return name


def main() -> int:
    args = parse_args()
    source_dir = skill_root() / "assets" / "codex-agents"
    templates = sorted(source_dir.glob("*.toml"))
    if not templates:
        print(f"No templates found in {source_dir}", file=sys.stderr)
        return 2

    errors: list[str] = []
    names: list[str] = []
    for template in templates:
        try:
            names.append(validate_template(template))
        except Exception as exc:  # noqa: BLE001 - report all validation errors cleanly
            errors.append(f"{template.name}: {exc}")

    duplicate_names = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicate_names:
        errors.append(f"duplicate agent names: {', '.join(duplicate_names)}")

    if errors:
        print("Template validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2

    dest = destination_dir(args.scope, args.target)
    print(f"Validated {len(templates)} templates: {', '.join(names)}")
    print(f"Destination: {dest}")

    planned = [(template, dest / template.name) for template in templates]
    for src, dst in planned:
        action = "overwrite" if dst.exists() and args.overwrite else "copy"
        if dst.exists() and not args.overwrite:
            action = "skip existing"
        print(f"{action}: {src.name} -> {dst}")

    if args.dry_run:
        print("Dry run complete; no files written.")
        return 0

    dest.mkdir(parents=True, exist_ok=True)
    copied = 0
    skipped = 0
    for src, dst in planned:
        if dst.exists() and not args.overwrite:
            skipped += 1
            continue
        shutil.copy2(src, dst)
        copied += 1

    print(f"Done. Copied {copied} file(s); skipped {skipped} existing file(s).")
    if skipped:
        print("Pass --overwrite to replace skipped files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
