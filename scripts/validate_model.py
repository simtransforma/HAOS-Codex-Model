"""Validate the public model offline, using only Python 3.11+ stdlib.

The scan includes untracked and ignored files except named metadata/dependency
caches. This is a conservative publication gate, not a complete secret detector.
Markdown checks cover local inline/reference links and explicit repository paths
in inline code, outside fenced examples; remote URLs and anchors are not fetched.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hmac
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from urllib.parse import unquote, urlsplit

if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11+ required")

import tomllib

try:
    from .model_safety import sensitive_rules
    from .model_matrix import validate_matrix
    from .model_links import local_targets, prose
except ImportError:
    from model_safety import sensitive_rules
    from model_matrix import validate_matrix
    from model_links import local_targets, prose


EXCLUDED_DIRS = frozenset({
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".cache", ".tox", ".nox", ".venv", "venv", "node_modules", "site-packages",
    ".eggs",
})
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REPO_PREFIX = re.compile(r"^(?:\.agents|\.codex|docs|scripts|tests|playbooks|hooks|memory)/")


@dataclass(frozen=True, order=True)
class Finding:
    path: str
    rule: str


def is_link(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & 0x400
    )  # Windows junctions and other reparse points must not be followed either.


def frontmatter(text: str) -> dict[str, str]:
    """Read only name/description scalars, not a general YAML implementation."""
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("frontmatter")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError("frontmatter") from None
    result: dict[str, str] = {}
    i = 1
    while i < end:
        match = re.fullmatch(r"(name|description):\s*(.*)", lines[i])
        i += 1
        if not match:
            continue
        key, value = match.groups()
        if key in result:
            raise ValueError("frontmatter")
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            block = []
            while i < end and (not lines[i].strip() or lines[i][0].isspace()):
                block.append(lines[i].strip())
                i += 1
            value = ("\n" if value.startswith("|") else " ").join(block).strip()
        elif value.startswith('"'):
            try:
                value = json.loads(value)
            except (ValueError, TypeError):
                raise ValueError("frontmatter") from None
        elif value.startswith("'"):
            if not value.endswith("'") or len(value) < 2:
                raise ValueError("frontmatter")
            value = value[1:-1].replace("''", "'")
        elif value.startswith(("[", "{", "!", "&", "*", "|", ">")):
            raise ValueError("frontmatter")
        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
        if not isinstance(value, str) or not value.strip():
            raise ValueError("frontmatter")
        result[key] = value
    if set(result) != {"name", "description"}:
        raise ValueError("frontmatter")
    return result


class Validator:
    def __init__(self, root: Path):
        self.root = Path(os.path.abspath(root))
        self.findings: set[Finding] = set()
        self.files: dict[str, str] = {}
        self.agents: set[str] = set()
        self.skills: set[str] = set()

    def report(self, path: str, rule: str) -> None:
        self.findings.add(Finding(path, rule))

    def collect(self) -> None:
        try:
            if is_link(self.root):
                self.report(".", "symlink")
                return
            if not self.root.is_dir():
                self.report(".", "root-not-directory")
                return
        except OSError:
            self.report(".", "root-unreadable")
            return
        pending = [self.root]
        while pending:
            directory = pending.pop()
            relative = directory.relative_to(self.root).as_posix()
            try:
                entries = sorted(directory.iterdir(), key=lambda item: item.name)
            except OSError:
                self.report(relative, "directory-unreadable")
                continue
            for path in entries:
                name = path.relative_to(self.root).as_posix()
                try:
                    if is_link(path):
                        self.report(name, "symlink")
                        continue
                    if path.is_dir():
                        if path.name not in EXCLUDED_DIRS:
                            if path.parent == self.root / ".agents/skills" and not (path / "SKILL.md").is_file():
                                self.report(name, "skill-file-missing")
                            pending.append(path)
                        continue
                    if path.name == ".git":
                        continue  # A worktree's .git file is metadata too.
                    if not stat.S_ISREG(path.lstat().st_mode):
                        self.report(name, "nonregular-file")
                        continue
                    data = path.read_bytes()
                except OSError:
                    self.report(name, "file-unreadable")
                    continue
                for rule in sensitive_rules(name):
                    self.report(name, rule)
                # Do not use an extension allowlist or skip binary payloads.
                views = [data.decode("utf-8", errors="replace")]
                if data.startswith((b"\xff\xfe", b"\xfe\xff")):
                    views.append(data.decode("utf-16", errors="replace"))
                for view in views:
                    for rule in sensitive_rules(view):
                        self.report(name, rule)
                try:
                    self.files[name] = data.decode("utf-8-sig")
                except UnicodeError:
                    if path.suffix.lower() in {".md", ".toml", ".json", ".py", ".yml", ".yaml"}:
                        self.report(name, "text-encoding")

    def structures(self) -> None:
        agent_ids: set[str] = set()
        skill_ids: set[str] = set()
        for name, text in sorted(self.files.items()):
            path = PurePosixPath(name)
            if name.startswith(".codex/agents/") and path.suffix == ".toml":
                identifier = path.stem
                if not ID.fullmatch(identifier):
                    self.report(name, "agent-id")
                if identifier.casefold() in agent_ids:
                    self.report(name, "duplicate-agent-id")
                agent_ids.add(identifier.casefold())
                self.agents.add(identifier)
                try:
                    agent = tomllib.loads(text)
                except tomllib.TOMLDecodeError:
                    self.report(name, "agent-toml")
                    continue
                instructions = agent.get("developer_instructions")
                if not isinstance(instructions, str) or not instructions.strip():
                    self.report(name, "agent-instructions")
                for field in ("name", "id"):
                    if field in agent and agent[field] != identifier:
                        self.report(name, "agent-id-mismatch")
                effort = agent.get("model_reasoning_effort")
                if effort is not None and effort not in (
                    "none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra"
                ):
                    self.report(name, "agent-effort")
            if name.startswith(".agents/skills/") and path.name == "SKILL.md":
                try:
                    metadata = frontmatter(text)
                except ValueError:
                    self.report(name, "skill-frontmatter")
                    continue
                identifier = metadata["name"]
                if not ID.fullmatch(identifier):
                    self.report(name, "skill-id")
                if identifier.casefold() in skill_ids:
                    self.report(name, "duplicate-skill-id")
                skill_ids.add(identifier.casefold())
                if identifier != path.parent.name:
                    self.report(name, "skill-folder-name")
                self.skills.add(identifier)
        if not self.agents:
            self.report(".codex/agents", "agents-missing")
        if not self.skills:
            self.report(".agents/skills", "skills-missing")

    def local_path(self, source: str, target: str, *, repository: bool = False) -> bool:
        target = unquote(target).replace("\\", "/")
        if "\x00" in target or re.match(r"^(?:[a-zA-Z]:|/|~)", target):
            self.report(source, "local-path-unsafe")
            return False
        base = self.root if repository else (self.root / source).parent
        candidate = base / target
        normalized = Path(os.path.abspath(candidate))
        if not normalized.is_relative_to(self.root):
            self.report(source, "local-path-escape")
            return False
        current = self.root
        try:
            for part in candidate.relative_to(self.root).parts:
                if part == "..":
                    current = current.parent
                    continue
                current = current / part
                if current.exists() or current.is_symlink():
                    if is_link(current):
                        self.report(source, "local-path-symlink")
                        return False
            if not normalized.exists():
                self.report(source, "local-path-missing")
                return False
        except (OSError, ValueError):
            self.report(source, "local-path-unreadable")
            return False
        return True

    def links(self) -> None:
        for name, text in self.files.items():
            if not name.lower().endswith(".md"):
                continue
            text = prose(text)
            targets, missing_reference = local_targets(text)
            if missing_reference:
                self.report(name, "markdown-reference-missing")
            for target in targets:
                try:
                    parsed = urlsplit(target)
                except ValueError:
                    self.report(name, "local-path-unsafe")
                    continue
                if parsed.scheme in {"http", "https", "mailto", "tel"}:
                    continue
                if parsed.scheme or parsed.netloc:
                    self.report(name, "local-path-unsafe")
                    continue
                if parsed.path:
                    self.local_path(name, parsed.path)
            for target in re.findall(r"(?<!`)`([^`\n]+)`(?!`)", text):
                if REPO_PREFIX.match(target) and not any(c in target for c in "*<> {}\n"):
                    target = re.sub(r":\d+$", "", target.split("#", 1)[0])
                    self.local_path(name, target, repository=True)

    def matrix(self) -> None:
        name = ".codex/skill-routing.json"
        if name not in self.files:
            self.report(name, "matrix-missing")
            return
        def unique_object(pairs: list[tuple[str, object]]) -> dict:
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("duplicate-key")
                result[key] = value
            return result

        try:
            data = json.loads(self.files[name], object_pairs_hook=unique_object)
        except (ValueError, TypeError):
            self.report(name, "matrix-json")
            return
        # The matrix contract is checked separately from JSON syntax. Never
        # silently accept a different schema or infer unresolved references.
        if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
            self.report(name, "matrix-schema")
            return
        rules = validate_matrix(
            data, self.agents, self.skills,
            lambda target: self.local_path(name, target, repository=True),
        )
        for rule in rules:
            self.report(name, rule)

    def run(self) -> list[Finding]:
        self.collect()
        if self.files:
            self.structures()
            self.matrix()
            self.links()
        elif not self.findings:
            self.report(".", "model-empty")
        return sorted(self.findings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args(argv)
    validator = Validator(args.root)
    findings = validator.run()
    # An ephemeral key prevents enumeration of low-entropy names (e.g. phones).
    # Reuse the same safe identifier for every rule concerning a given path.
    redaction_key = os.urandom(32)
    display_paths: dict[str, str] = {}
    for finding in findings:
        path = finding.path
        if path not in display_paths:
            if sensitive_rules(path):
                identifier = hmac.digest(
                    redaction_key, path.encode("utf-8", errors="surrogatepass"), "sha256"
                ).hex()
                display_paths[path] = f"<redacted-path:{identifier}>"
            else:
                display_paths[path] = path
        print(json.dumps({"file": display_paths[path], "rule": finding.rule}, ensure_ascii=True))
    if findings:
        print(f"FAIL: {len(findings)} finding(s); {len(validator.files)} text file(s) checked")
        return 1
    print(f"PASS: {len(validator.files)} text file(s); {len(validator.agents)} agent(s); {len(validator.skills)} skill(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
