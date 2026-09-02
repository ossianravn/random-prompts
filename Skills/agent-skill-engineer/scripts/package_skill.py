#!/usr/bin/env python3
"""Create a deterministic one-top-level-folder zip for an Agent Skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True

from validate_skill import validate_skill

EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules"}
EXCLUDED_FILES = {".DS_Store"}
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def include_file(root: Path, path: Path, output: Path) -> bool:
    relative = path.relative_to(root)
    if path.is_symlink():
        return False
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if path.name in EXCLUDED_FILES:
        return False
    try:
        if path.resolve() == output.resolve():
            return False
    except FileNotFoundError:
        pass
    return path.is_file()


def write_deterministic(zf: zipfile.ZipFile, source: Path, archive_name: str) -> None:
    data = source.read_bytes()
    info = zipfile.ZipInfo(archive_name, date_time=FIXED_TIMESTAMP)
    mode = source.stat().st_mode
    permissions = stat.S_IMODE(mode) or 0o644
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | permissions) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, data)


def package_skill(skill_path: Path, output: Path, force: bool = False) -> dict[str, object]:
    root = skill_path.expanduser().resolve()
    report = validate_skill(root)
    if not report.ok:
        details = "; ".join(item.message for item in report.errors)
        raise ValueError(f"Skill validation failed: {details}")

    output = output.expanduser().resolve()
    if root == output or root in output.parents:
        raise ValueError("Output archive must be outside the skill directory.")
    if output.exists() and not force:
        raise FileExistsError(f"Output already exists: {output}. Use --force to replace it.")
    output.parent.mkdir(parents=True, exist_ok=True)

    files = sorted(path for path in root.rglob("*") if include_file(root, path, output))
    if not files:
        raise ValueError("No files were found to package.")

    temporary = output.with_suffix(output.suffix + ".tmp")
    if temporary.exists():
        temporary.unlink()
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for path in files:
                relative = path.relative_to(root).as_posix()
                write_deterministic(zf, path, f"{root.name}/{relative}")
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return {
        "archive": str(output),
        "skill_name": root.name,
        "files": len(files),
        "bytes": output.stat().st_size,
        "sha256": digest,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Package an Agent Skill as a deterministic zip archive.")
    parser.add_argument("skill_path", type=Path, help="Path to the validated skill directory.")
    parser.add_argument("--output", type=Path, help="Output zip path. Defaults beside the skill directory.")
    parser.add_argument("--force", action="store_true", help="Replace an existing output archive.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit package metadata as JSON.")
    args = parser.parse_args(argv)

    root = args.skill_path.expanduser().resolve()
    output = args.output or root.parent / f"{root.name}.zip"
    try:
        result = package_skill(root, output, force=args.force)
    except (ValueError, FileExistsError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Created {result['archive']}")
        print(f"Files: {result['files']}")
        print(f"Bytes: {result['bytes']}")
        print(f"SHA-256: {result['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
