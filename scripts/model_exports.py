"""Normalize A/B manifests and verify source-backed, non-stub public exports."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat

try:
    from .model_frontmatter import document
except ImportError:
    from model_frontmatter import document


SHA = re.compile(r"[0-9a-f]{64}\Z")
PRIVATE_KEY = re.compile(r"(?:^|[_-])(?:id|key|secret|token|phone|password|account|pixel|tenant|waba|campaign|business)(?:$|[_-])", re.I)


def numeric_settings(value, prefix="") -> dict:
    """Preserve numeric settings, not private identifiers or credential fields."""
    result = {}
    if isinstance(value, dict):
        for key, child in value.items():
            if not PRIVATE_KEY.search(str(key)):
                result.update(numeric_settings(child, prefix + "/" + str(key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            result.update(numeric_settings(child, prefix + "/" + str(index)))
    elif type(value) in {int, float, bool} or value is None:
        result[prefix] = value
    return result


def numeric_integrity(original: str, transported: str) -> bool:
    source = numeric_settings(json.loads(original))
    target = numeric_settings(json.loads(transported))
    return source == target


def dependency_available(root: Path, target: str, name: str) -> bool:
    for relative in (name, target + "/" + name):
        try:
            if safe_file(root, relative).is_file():
                return True
        except ValueError:
            continue
    return False


def canonical_dependencies(root: Path, target: str, dependencies: list[dict]) -> list[dict]:
    result = []
    for dependency in dependencies:
        item = dict(dependency)
        field = "name" if "name" in item else "reference"
        name = item.get(field)
        if isinstance(name, str) and name.startswith("../") and item.get("status") in {"bundled", "included", "ported", "available", "public-present"}:
            normalized = os.path.normpath(target + "/" + name).replace("\\", "/")
            path = safe_file(root, normalized)
            if not path.is_file():
                raise ValueError("export-bundled-dependency-missing")
            item["original_reference"] = name
            item[field] = normalized
        result.append(item)
    return result


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def portable_sha256(data: bytes) -> str:
    try:
        data.decode("utf-8")
    except UnicodeError:
        return hashlib.sha256(data).hexdigest()
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def manifest_hash_matches(data: bytes, expected: str) -> bool:
    candidates = {hashlib.sha256(data).hexdigest(), portable_sha256(data)}
    try:
        data.decode("utf-8")
    except UnicodeError:
        return expected in candidates
    lf = data.replace(b"\r\n", b"\n")
    candidates.add(hashlib.sha256(lf.replace(b"\n", b"\r\n")).hexdigest())
    return expected in candidates


def safe_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        raise ValueError("export-path-unsafe")
    parts = relative.split("/")
    if relative.startswith("/") or any(p in {"", "..", "."} for p in parts):
        raise ValueError("export-path-unsafe")
    root = Path(os.path.abspath(root))
    path = root / relative
    current = root
    for part in (None, *parts):
        if part is not None:
            current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("export-path-symlink")
    return path


def load_groups(root: Path, texts=None) -> list[dict]:
    entries = []
    for group in ("a", "b"):
        path = root / f"docs/exports/group-{group}.json"
        data = json.loads(texts[f"docs/exports/group-{group}.json"] if texts is not None else path.read_text(encoding="utf-8-sig"))
        if not isinstance(data, list) or any(not isinstance(e, dict) for e in data):
            raise ValueError("export-manifest-schema")
        entries.extend(data)
    return entries


def body_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    try:
        return document(text)[1]
    except ValueError:
        return text


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z][a-zA-Z_-]{3,}", text.lower()))


def build_catalog(root: Path, source: Path) -> dict:
    folders = sorted(p for p in source.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    if len(folders) != 193:
        raise ValueError("export-source-count")
    source_index = {p.name: p for p in folders}
    entries = load_groups(root)
    if Counter(e.get("source_folder") for e in entries) != Counter(source_index.keys()):
        raise ValueError("export-source-coverage")
    normalized = []
    for entry in entries:
        folder = entry["source_folder"]
        original = source_index[folder] / "SKILL.md"
        if digest(original) != entry.get("sha256original"):
            raise ValueError("export-source-hash")
        target = entry["target_path"]
        if target != f".agents/skills/{folder}":
            raise ValueError("export-target-mismatch")
        files = []
        integrity = []
        for item in entry.get("files", []):
            relative = item if isinstance(item, str) else item["path"]
            path = safe_file(root, relative)
            if not relative.startswith(target + "/") or not path.is_file():
                raise ValueError("export-support-file-missing")
            data = path.read_bytes()
            sha = portable_sha256(data)
            if isinstance(item, dict) and not manifest_hash_matches(data, item.get("sha256")):
                raise ValueError("export-file-hash: " + relative)
            file_record = {"path": relative, "sha256": sha}
            source_relative = item.get("source_rel") if isinstance(item, dict) else relative[len(target) + 1:]
            source_file = safe_file(source_index[folder], source_relative) if source_relative else None
            if source_file and source_file.is_file():
                file_record["source_sha256"] = digest(source_file)
                if path.suffix.lower() == ".json":
                    try:
                        if not numeric_integrity(source_file.read_text(encoding="utf-8-sig"), path.read_text(encoding="utf-8-sig")):
                            integrity.append({"path": relative, "rule": "export-json-settings-changed"})
                    except (ValueError, UnicodeError):
                        integrity.append({"path": relative, "rule": "export-json-settings-unverified"})
                if re.match(r"^(?:licen[cs]e|copying|notice|copyright)(?:[._-]|$)", path.name, re.I):
                    original_notice = source_file.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()
                    public_notice = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()
                    if original_notice != public_notice:
                        integrity.append({"path": relative, "rule": "export-license-modified"})
            files.append(file_record)
        source_files = [p for p in source_index[folder].rglob("*") if p.is_file() and not p.is_symlink()]
        original_body = body_text(original.read_text(encoding="utf-8-sig"))
        original_tokens = tokens(original_body)
        candidates = []
        for item in files:
            path = root / item["path"]
            if path.suffix.lower() == ".md" and path.name not in {"PORTABILITY.md", "EXPORT_DEPENDENCIES.md"}:
                body = body_text(path.read_text(encoding="utf-8-sig"))
                overlap = len(tokens(body) & original_tokens) / max(1, len(original_tokens))
                candidates.append((overlap, len(body), item["path"], hashlib.sha256(body.encode()).hexdigest()))
        if not candidates:
            raise ValueError("export-body-missing")
        overlap, length, body_path, body_sha = max(candidates)
        if length < min(120, len(original_body)) or overlap < 0.25:
            raise ValueError("export-body-stub")
        normalized.append({
            "source_folder": folder, "target_path": target, "status": entry.get("status"),
            "reason": entry.get("reason"), "source_sha256": digest(original),
            "source_file_count": len(source_files), "files": sorted(files, key=lambda f: f["path"]),
            "dependencies": canonical_dependencies(root, target, entry.get("dependencies", [])), "license": entry.get("license", {}),
            "omitted_artifacts": entry.get("omitted_artifacts", entry.get("excluded_files", [])),
            "integrity_findings": integrity,
            "body": {"path": body_path, "sha256": body_sha, "characters": length,
                     "source_characters": len(original_body), "source_token_coverage": round(overlap, 6)},
        })
    return {"schema_version": 1, "expected_source_count": 193,
            "source_folders": sorted(source_index), "entries": sorted(normalized, key=lambda e: e["source_folder"])}


def validate_exports(root: Path, report, *, hashes=None, texts=None) -> None:
    def available(relative):
        return relative in hashes if hashes is not None else (root / relative).is_file()

    def read(relative):
        return texts[relative] if texts is not None else (root / relative).read_text(encoding="utf-8-sig")

    def checked(relative):
        if hashes is None:
            return safe_file(root, relative)
        if not isinstance(relative, str) or not relative or relative.startswith("/") or ":" in relative or "\\" in relative or any(p in {"", ".", ".."} for p in relative.split("/")):
            raise ValueError("export-path-unsafe")
        # collect() already refuses symlinks/reparse points; only bytes from
        # that complete privacy scan are eligible for this read-once cache.
        return root / relative
    relative = "docs/exports/catalog.json"
    catalog_path = root / relative
    groups_present = any(available(f"docs/exports/group-{g}.json") for g in ("a", "b"))
    if not available(relative):
        if groups_present:
            report(relative, "export-catalog-missing")
        return
    try:
        baseline_path = root / "docs/exports/core-baseline.json"
        if not available("docs/exports/core-baseline.json"):
            report(relative, "export-core-baseline-missing")
        else:
            baseline = json.loads(read("docs/exports/core-baseline.json"))
            if baseline.get("schema_version") != 1 or baseline.get("expected_count") != 29 or len(baseline.get("entries", [])) != 29:
                raise ValueError("export-core-baseline-schema")
            for core in baseline["entries"]:
                path = checked(core["path"])
                if not available(core["path"]):
                    report(core["path"], "export-core-missing")
                else:
                    text = read(core["path"]).replace("\r\n", "\n")[:core["characters"]]
                    if hashlib.sha256(text.encode()).hexdigest() != core["sha256"]:
                        report(core["path"], "export-core-modified")
        catalog = json.loads(read(relative))
        entries = catalog["entries"]
        expected = catalog["source_folders"]
        groups = load_groups(root, texts)
        if catalog.get("schema_version") != 1 or catalog.get("expected_source_count") != 193:
            raise ValueError("export-catalog-schema")
        if len(expected) != 193 or len(set(expected)) != 193 or Counter(e["source_folder"] for e in entries) != Counter(expected) or Counter(e["source_folder"] for e in groups) != Counter(expected):
            raise ValueError("export-source-coverage")
        for entry in entries:
            if entry["target_path"] != ".agents/skills/" + entry["source_folder"]:
                raise ValueError("export-target-mismatch")
            if entry["status"] not in {"ported_full", "adapted_private_config"}:
                report(relative, "export-not-ported")
            if not SHA.fullmatch(entry["source_sha256"]) or type(entry["source_file_count"]) is not int or entry["source_file_count"] < 1:
                raise ValueError("export-source-provenance")
            if not entry["reason"] or not isinstance(entry["license"], dict) or not entry["license"] or entry["license"].get("relicensed") is True:
                raise ValueError("export-license-contract")
            paths = set()
            for item in entry["files"]:
                path = checked(item["path"])
                if not item["path"].startswith(entry["target_path"] + "/") or not available(item["path"]):
                    report(item["path"], "export-support-file-missing")
                elif (hashes[item["path"]] if hashes is not None else portable_sha256(path.read_bytes())) != item["sha256"]:
                    report(item["path"], "export-file-hash")
                if item["path"] in paths:
                    raise ValueError("export-file-duplicate")
                paths.add(item["path"])
            for dependency in entry["dependencies"]:
                name = dependency.get("name", dependency.get("reference"))
                if not isinstance(name, str) or not name or not dependency.get("contract") or not dependency.get("status"):
                    raise ValueError("export-dependency-contract")
                if dependency["status"] in {"bundled", "included", "ported", "available", "public-present", "available-in-source", "available-in-target", "available_in_source", "available_in_target"}:
                    if not any(available(candidate) for candidate in (name, entry["target_path"] + "/" + name)):
                        report(relative, "export-bundled-dependency-missing")
                    # Absolute/escaping names cannot be called bundled even if
                    # they coincidentally resolve after prefixing the skill path.
                    checked(name)
            for omitted in entry["omitted_artifacts"]:
                if not omitted.get("reason"):
                    raise ValueError("export-omission-reason")
            body = entry["body"]
            for issue in entry.get("integrity_findings", []):
                report(issue["path"], issue["rule"])
            body_path = checked(body["path"])
            if body["path"] not in paths or not available(body["path"]):
                report(relative, "export-body-missing")
            else:
                actual = body_text(read(body["path"]))
                if hashlib.sha256(actual.encode()).hexdigest() != body["sha256"] or len(actual) != body["characters"]:
                    report(body["path"], "export-body-hash")
                if len(actual) < min(120, body["source_characters"]) or body["source_token_coverage"] < 0.25:
                    report(body["path"], "export-body-stub")
    except (OSError, KeyError, TypeError, ValueError) as error:
        rule = str(error) if isinstance(error, ValueError) and str(error).startswith("export-") else "export-catalog-schema"
        report(relative, rule)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    catalog = build_catalog(args.root, args.source)
    output = json.dumps(catalog, ensure_ascii=True, indent=2) + "\n"
    if args.write:
        (args.root / "docs/exports/catalog.json").write_text(output, encoding="utf-8")
    else:
        previous = (args.root / "docs/exports/catalog.json").read_text(encoding="utf-8")
        if previous != output:
            raise SystemExit("FAIL: export-catalog-stale")
    print("PASS: source coverage 193/193; source hashes, bodies and supporting files checked")


if __name__ == "__main__":
    main()
