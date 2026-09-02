#!/usr/bin/env python3
"""Validate the portable structure of an Agent Skill bundle.

This is a dependency-light fallback for environments where the official
`skills-ref validate` command is unavailable. When PyYAML is installed it
parses complete YAML frontmatter; otherwise it performs a conservative check
of the required scalar fields.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from urllib.parse import unquote

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - exercised only without PyYAML
    yaml = None

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SENSITIVE_NAMES = {
    ".env",
    "credentials.json",
    "secrets.json",
    "id_rsa",
    "id_ed25519",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
RESIDUE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", "node_modules", ".git"}
RESIDUE_FILES = {".DS_Store"}
PORTABLE_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


@dataclass
class Finding:
    level: str
    code: str
    message: str
    path: str | None = None


@dataclass
class Report:
    skill_path: str
    errors: list[Finding]
    warnings: list[Finding]
    info: dict[str, Any]

    @property
    def ok(self) -> bool:
        return not self.errors


def add(findings: list[Finding], level: str, code: str, message: str, path: Path | None = None) -> None:
    findings.append(Finding(level, code, message, str(path) if path else None))


def split_frontmatter(text: str) -> tuple[str, str]:
    normalized = text.lstrip("\ufeff")
    lines = normalized.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with a YAML frontmatter delimiter (---).")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    raise ValueError("SKILL.md is missing the closing YAML frontmatter delimiter (---).")


def minimal_scalar(frontmatter: str, key: str) -> str | None:
    """Read a simple or folded top-level scalar without a YAML dependency."""
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        match = re.match(rf"^{re.escape(key)}:\s*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip()
        if value in {">", ">-", "|", "|-", ">+", "|+"}:
            block: list[str] = []
            for following in lines[index + 1 :]:
                if following and not following[0].isspace():
                    break
                block.append(following.strip())
            return " ".join(part for part in block if part).strip()
        return value.strip('"\'')
    return None


def parse_frontmatter(frontmatter: str, warnings: list[Finding], skill_file: Path) -> dict[str, Any]:
    if yaml is not None:
        try:
            data = yaml.safe_load(frontmatter)
        except Exception as exc:  # PyYAML exposes several exception subclasses
            raise ValueError(f"YAML frontmatter could not be parsed: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError("YAML frontmatter must be a mapping.")
        return data

    add(
        warnings,
        "warning",
        "yaml-parser-unavailable",
        "PyYAML is not installed; only required scalar fields were checked. Use skills-ref for full validation.",
        skill_file,
    )
    return {
        "name": minimal_scalar(frontmatter, "name"),
        "description": minimal_scalar(frontmatter, "description"),
        "compatibility": minimal_scalar(frontmatter, "compatibility"),
    }


def markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(" ", 1)[0]
    return unquote(target.split("#", 1)[0])


def within_root(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def validate_trigger_evals(
    data: Any,
    path: Path,
    errors: list[Finding],
    warnings: list[Finding],
    info: dict[str, Any],
) -> None:
    if not isinstance(data, list):
        add(errors, "error", "trigger-evals-format", "trigger-evals.json must contain a JSON array.", path)
        return
    positive = 0
    negative = 0
    for index, item in enumerate(data):
        label = f"trigger-evals.json item {index}"
        if not isinstance(item, dict):
            add(errors, "error", "trigger-eval-item", f"{label} must be an object.", path)
            continue
        if not isinstance(item.get("query"), str) or not item["query"].strip():
            add(errors, "error", "trigger-eval-query", f"{label} requires a non-empty query string.", path)
        if not isinstance(item.get("should_trigger"), bool):
            add(errors, "error", "trigger-eval-label", f"{label} requires a boolean should_trigger value.", path)
        elif item["should_trigger"]:
            positive += 1
        else:
            negative += 1
    info["trigger_evals_positive"] = positive
    info["trigger_evals_negative"] = negative
    if data and (positive == 0 or negative == 0):
        add(warnings, "warning", "trigger-evals-balance", "Trigger evals should normally include both positive and negative cases.", path)


def validate_behavior_evals(
    data: Any,
    root: Path,
    path: Path,
    errors: list[Finding],
    info: dict[str, Any],
) -> None:
    if not isinstance(data, dict):
        add(errors, "error", "behavior-evals-format", "evals.json must contain a JSON object.", path)
        return
    skill_name = data.get("skill_name")
    if not isinstance(skill_name, str) or not skill_name.strip():
        add(errors, "error", "behavior-evals-skill", "evals.json requires a non-empty skill_name string.", path)
    elif skill_name != root.name:
        add(errors, "error", "behavior-evals-name", f"evals.json skill_name '{skill_name}' does not match '{root.name}'.", path)
    evals = data.get("evals")
    if not isinstance(evals, list):
        add(errors, "error", "behavior-evals-list", "evals.json requires an evals array.", path)
        return
    seen_ids: set[str] = set()
    for index, item in enumerate(evals):
        label = f"evals.json item {index}"
        if not isinstance(item, dict):
            add(errors, "error", "behavior-eval-item", f"{label} must be an object.", path)
            continue
        eval_id = item.get("id")
        if eval_id is None:
            add(errors, "error", "behavior-eval-id", f"{label} requires an id.", path)
        else:
            key = str(eval_id)
            if key in seen_ids:
                add(errors, "error", "behavior-eval-duplicate-id", f"Duplicate eval id: {key}.", path)
            seen_ids.add(key)
        for field in ("prompt", "expected_output"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                add(errors, "error", f"behavior-eval-{field}", f"{label} requires a non-empty {field} string.", path)
        files = item.get("files", [])
        if not isinstance(files, list) or any(not isinstance(value, str) or not value for value in files):
            add(errors, "error", "behavior-eval-files", f"{label} files must be an array of non-empty strings.", path)
            continue
        for value in files:
            candidate = root / value
            if not within_root(root, candidate):
                add(errors, "error", "behavior-eval-path-traversal", f"{label} file leaves the skill root: {value}", path)
            elif not candidate.is_file():
                add(errors, "error", "behavior-eval-file-missing", f"{label} file does not exist: {value}", candidate)
    info["behavior_evals"] = len(evals)


def validate_skill(skill_path: Path) -> Report:
    errors: list[Finding] = []
    warnings: list[Finding] = []
    info: dict[str, Any] = {}

    root = skill_path.expanduser().resolve()
    if not root.exists():
        add(errors, "error", "missing-skill", "Skill path does not exist.", root)
        return Report(str(root), errors, warnings, info)
    if not root.is_dir():
        add(errors, "error", "not-directory", "Skill path must be a directory.", root)
        return Report(str(root), errors, warnings, info)

    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        add(errors, "error", "missing-skill-md", "Required SKILL.md was not found.", skill_file)
        return Report(str(root), errors, warnings, info)

    try:
        text = skill_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        add(errors, "error", "invalid-utf8", f"SKILL.md must be UTF-8: {exc}", skill_file)
        return Report(str(root), errors, warnings, info)

    info["skill_md_lines"] = len(text.splitlines())
    if info["skill_md_lines"] > 500:
        add(
            warnings,
            "warning",
            "long-skill-md",
            f"SKILL.md has {info['skill_md_lines']} lines; progressive disclosure is recommended above 500 lines.",
            skill_file,
        )

    try:
        frontmatter_text, body = split_frontmatter(text)
        data = parse_frontmatter(frontmatter_text, warnings, skill_file)
    except ValueError as exc:
        add(errors, "error", "frontmatter", str(exc), skill_file)
        return Report(str(root), errors, warnings, info)

    name = data.get("name")
    description = data.get("description")
    compatibility = data.get("compatibility")

    if not isinstance(name, str) or not name.strip():
        add(errors, "error", "name-required", "Frontmatter name must be a non-empty string.", skill_file)
    else:
        name = name.strip()
        info["name"] = name
        if len(name) > 64:
            add(errors, "error", "name-length", "Frontmatter name exceeds 64 characters.", skill_file)
        if not NAME_RE.fullmatch(name):
            add(
                errors,
                "error",
                "name-format",
                "Name must contain only lowercase ASCII letters, digits, and single hyphens, with no leading or trailing hyphen.",
                skill_file,
            )
        if root.name != name:
            add(
                errors,
                "error",
                "folder-name-mismatch",
                f"Folder name '{root.name}' does not match frontmatter name '{name}'.",
                root,
            )

    if not isinstance(description, str) or not description.strip():
        add(errors, "error", "description-required", "Frontmatter description must be a non-empty string.", skill_file)
    else:
        description = description.strip()
        info["description_chars"] = len(description)
        if len(description) > 1024:
            add(errors, "error", "description-length", "Description exceeds 1024 characters.", skill_file)

    if compatibility is not None:
        if not isinstance(compatibility, str) or not compatibility.strip():
            add(errors, "error", "compatibility-format", "Compatibility must be a non-empty string when present.", skill_file)
        elif len(compatibility.strip()) > 500:
            add(errors, "error", "compatibility-length", "Compatibility exceeds 500 characters.", skill_file)

    if yaml is not None:
        metadata = data.get("metadata")
        if metadata is not None:
            if not isinstance(metadata, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items()):
                add(errors, "error", "metadata-format", "Metadata must be a mapping from strings to strings.", skill_file)
        if data.get("allowed-tools") is not None and not isinstance(data.get("allowed-tools"), str):
            add(errors, "error", "allowed-tools-format", "allowed-tools must be a space-separated string.", skill_file)
        if data.get("license") is not None and not isinstance(data.get("license"), str):
            add(errors, "error", "license-format", "license must be a string.", skill_file)
        unknown = sorted(set(data) - PORTABLE_FIELDS)
        for field in unknown:
            add(
                warnings,
                "warning",
                "nonportable-frontmatter-field",
                f"Frontmatter field '{field}' is outside the portable core; confirm target support.",
                skill_file,
            )

    if not body.strip():
        add(errors, "error", "empty-body", "SKILL.md must contain execution instructions after frontmatter.", skill_file)

    for match in MARKDOWN_LINK_RE.finditer(body):
        target = markdown_target(match.group(1))
        if not target or target.startswith(("http://", "https://", "mailto:", "/", "#")):
            continue
        candidate = root / target
        if not within_root(root, candidate):
            add(errors, "error", "link-path-traversal", f"Relative link leaves the skill root: {target}", skill_file)
        elif not candidate.exists():
            add(errors, "error", "missing-relative-link", f"Relative link target does not exist: {target}", candidate)

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        parts = set(relative.parts)
        if path.is_symlink():
            add(errors, "error", "symlink-entry", f"Symlinks inside a portable skill bundle are not packaged safely: {relative}", path)
            continue
        if path.is_dir() and path.name in RESIDUE_DIRS:
            add(warnings, "warning", "residue-directory", f"Generated or repository residue should not be packaged: {relative}", path)
            continue
        if path.is_file():
            if path.name in RESIDUE_FILES:
                add(warnings, "warning", "residue-file", f"Generated residue should not be packaged: {relative}", path)
            if path.name in SENSITIVE_NAMES or path.suffix.lower() in SENSITIVE_SUFFIXES or path.name.startswith(".env."):
                add(errors, "error", "sensitive-file", f"Potential credential or secret file must not be bundled: {relative}", path)
            if "evals" in parts and path.suffix.lower() == ".json":
                try:
                    parsed_json = json.loads(path.read_text(encoding="utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    add(errors, "error", "invalid-json", f"JSON resource is invalid: {exc}", path)
                else:
                    relative_name = relative.as_posix()
                    if relative_name == "evals/trigger-evals.json":
                        validate_trigger_evals(parsed_json, path, errors, warnings, info)
                    elif relative_name == "evals/evals.json":
                        validate_behavior_evals(parsed_json, root, path, errors, info)

    openai_yaml = root / "agents" / "openai.yaml"
    if openai_yaml.exists():
        if yaml is None:
            add(warnings, "warning", "openai-yaml-unchecked", "agents/openai.yaml could not be parsed without PyYAML.", openai_yaml)
        else:
            try:
                openai_data = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
            except Exception as exc:
                add(errors, "error", "openai-yaml-invalid", f"agents/openai.yaml is invalid YAML: {exc}", openai_yaml)
            else:
                if not isinstance(openai_data, dict):
                    add(errors, "error", "openai-yaml-format", "agents/openai.yaml must contain a mapping.", openai_yaml)
                else:
                    policy = openai_data.get("policy")
                    if policy is not None and not isinstance(policy, dict):
                        add(errors, "error", "openai-policy-format", "openai.yaml policy must be a mapping.", openai_yaml)
                    elif isinstance(policy, dict) and "allow_implicit_invocation" in policy and not isinstance(policy["allow_implicit_invocation"], bool):
                        add(errors, "error", "openai-policy-boolean", "policy.allow_implicit_invocation must be boolean.", openai_yaml)

    if (root / "README.md").exists():
        add(
            warnings,
            "warning",
            "readme-present",
            "README.md is not part of the portable core; retain it only when the selected distribution target needs it.",
            root / "README.md",
        )

    info["files"] = sum(1 for path in root.rglob("*") if path.is_file())
    return Report(str(root), errors, warnings, info)


def print_text(report: Report) -> None:
    status = "PASS" if report.ok else "FAIL"
    print(f"{status}: {report.skill_path}")
    for finding in [*report.errors, *report.warnings]:
        location = f" [{finding.path}]" if finding.path else ""
        print(f"{finding.level.upper()} {finding.code}: {finding.message}{location}")
    print(f"Summary: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    if report.info:
        print("Info:")
        for key, value in sorted(report.info.items()):
            print(f"  {key}: {value}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the portable structure of an Agent Skill bundle.")
    parser.add_argument("skill_path", type=Path, help="Path to the skill directory.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit a machine-readable JSON report.")
    args = parser.parse_args(argv)

    report = validate_skill(args.skill_path)
    if args.as_json:
        payload = {
            "ok": report.ok,
            "skill_path": report.skill_path,
            "errors": [asdict(item) for item in report.errors],
            "warnings": [asdict(item) for item in report.warnings],
            "info": report.info,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_text(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
