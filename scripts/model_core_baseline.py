"""Freeze the 29 tracked public entry points before imported appendices."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def capture(root: Path) -> dict:
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", "HEAD", "--", ".agents/skills"], cwd=root, text=True).splitlines()
    entries = []
    for path in sorted(p for p in paths if p.endswith("/SKILL.md")):
        text = subprocess.check_output(["git", "show", "HEAD:" + path], cwd=root).decode("utf-8-sig").replace("\r\n", "\n").rstrip()
        entries.append({"path": path, "characters": len(text), "sha256": hashlib.sha256(text.encode()).hexdigest()})
    if len(entries) != 29:
        raise ValueError("core-baseline-count")
    return {"schema_version": 1, "expected_count": 29, "entries": entries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    path = args.root / "docs/exports/core-baseline.json"
    output = json.dumps(capture(args.root), ensure_ascii=True, indent=2) + "\n"
    if args.write and not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
    if not path.exists() or path.read_text(encoding="utf-8") != output:
        raise SystemExit("FAIL: core-baseline-drift")
    print("PASS: 29 tracked public core entry points frozen; no source skill modified")


if __name__ == "__main__":
    main()
