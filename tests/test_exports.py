"""Synthetic export manifests and adversarial content; no imported code runs."""

import hashlib
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import time
import unittest

from scripts.model_exports import build_catalog, body_text, canonical_dependencies, digest, manifest_hash_matches, numeric_integrity, portable_sha256, safe_file, validate_exports
from scripts.model_frontmatter import document
from scripts.model_safety import sensitive_rules
from test_validate_model import ModelCase


class ImportedSyntaxTests(ModelCase):
    def test_neighbor_dependency_is_canonicalized_but_escape_is_rejected(self):
        target = ".agents/skills/worker"
        contract = {"reference": "../haos-test/SKILL.md", "status": "public-present", "contract": "Existing neighboring skill."}
        converted = canonical_dependencies(self.root, target, [contract])
        self.assertEqual(converted[0]["reference"], ".agents/skills/haos-test/SKILL.md")
        self.assertEqual(converted[0]["original_reference"], contract["reference"])
        with self.assertRaisesRegex(ValueError, "export-path-unsafe"):
            canonical_dependencies(self.root, target, [{**contract, "reference": "../../../../outside.py"}])

    def test_nested_metadata_quoted_keys_lists_and_scalars(self):
        value, body = document('---\n"name": haos-test\ndescription: "Method: precise"\nmetadata:\n  tools: [python, "shell"]\n  enabled: true\n---\nBody')
        self.assertEqual(value["metadata"]["tools"], ["python", "shell"])
        self.assertEqual(body, "Body")

    def test_duplicate_quoted_or_nested_key_is_ambiguous(self):
        for extra in ('"name": other\n', 'metadata:\n  tools: []\n  "tools": []\n'):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                document("---\nname: haos-test\ndescription: Method\n" + extra + "---\n")

    def test_arbitrary_yaml_constructor_is_rejected(self):
        with self.assertRaises(ValueError):
            document("---\nname: haos-test\ndescription: Method\nmetadata: !!python/object/apply:os.system []\n---\n")

    def test_invalid_imported_python_is_not_excused_by_contract(self):
        self.write(".agents/skills/haos-test/scripts/helper.py", "resource = ${RESOURCE_ID}\n")
        self.write(".agents/skills/haos-test/PORTABILITY.md", "Helper requires setup; not executed.\n")
        self.assertIn("python-syntax", self.rules())

    def test_duplicate_json_key_and_nonfinite_values_fail(self):
        for text in ('{"a": 1, "a": 2}', '{"a": NaN}', '{broken'):
            self.write(".agents/skills/haos-test/settings.json", text)
            self.assertIn("json-syntax", self.rules())

    def test_static_parser_does_not_execute_code(self):
        self.write(".agents/skills/haos-test/scripts/helper.py", 'raise RuntimeError("MUST NOT RUN")\n')
        self.assertNotIn("python-syntax", self.rules())


class ExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        builder = cls(methodName="runTest")
        builder.make_fixture()
        cls.addClassCleanup(builder.doCleanups)
        cls.fixture_root = builder.root
        cls.fixture_source = builder.source
        cls.fixture_groups = json.dumps(builder.groups)
        cls.fixture_catalog = json.dumps(builder.catalog)
        cls.fixture_body = (builder.root / builder.groups[0]["target_path"] / "SKILL.md").read_text(encoding="utf-8")
        cls.fixture_texts = {p.relative_to(builder.root).as_posix(): p.read_text(encoding="utf-8") for p in builder.root.rglob("*") if p.is_file()}
        cls.fixture_hashes = {name: hashlib.sha256(text.encode()).hexdigest() for name, text in cls.fixture_texts.items()}

    def setUp(self):
        self.root = self.fixture_root
        self.source = self.fixture_source
        self.groups = json.loads(self.fixture_groups)
        self.catalog = json.loads(self.fixture_catalog)
        (self.root / self.groups[0]["target_path"] / "SKILL.md").write_text(self.fixture_body, encoding="utf-8")
        self.write_groups()
        self.save()

    def make_fixture(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "public"
        self.source = Path(self.tmp.name) / "source"
        self.root.mkdir()
        entries = []
        for i in range(193):
            folder = f"method-{i}"
            text = f"---\nname: {folder}\ndescription: Synthetic method.\nmetadata:\n  tags: [test]\n---\n" + "Verify source interfaces, preserve attribution, compare evidence, test failures and report unresolved dependencies. " * 3
            for base in (self.source, self.root / ".agents/skills"):
                target = base / folder / "SKILL.md"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")
            relative = f".agents/skills/{folder}/SKILL.md"
            entries.append({"source_folder": folder, "target_path": f".agents/skills/{folder}",
                            "status": "ported_full", "reason": "Source transported.",
                            "sha256original": digest(self.source / folder / "SKILL.md"),
                            "files": [relative] if i < 97 else [{"path": relative, "sha256": portable_sha256((self.root / relative).read_bytes())}],
                            "dependencies": [], "license": {"status": "unknown", "relicensed": False}})
        (self.root / "docs/exports").mkdir(parents=True)
        self.groups = entries
        self.write_groups()
        cores = []
        for entry in entries[:29]:
            path = entry["target_path"] + "/SKILL.md"
            text = (self.root / path).read_text(encoding="utf-8").rstrip()
            cores.append({"path": path, "characters": len(text), "sha256": hashlib.sha256(text.encode()).hexdigest()})
        (self.root / "docs/exports/core-baseline.json").write_text(json.dumps({"schema_version": 1, "expected_count": 29, "entries": cores}), encoding="utf-8")
        self.catalog = build_catalog(self.root, self.source)
        self.save()

    def write_groups(self):
        for group, entries in (("a", self.groups[:97]), ("b", self.groups[97:])):
            (self.root / f"docs/exports/group-{group}.json").write_text(json.dumps(entries), encoding="utf-8")

    def save(self):
        (self.root / "docs/exports/catalog.json").write_text(json.dumps(self.catalog), encoding="utf-8")

    def rules(self):
        result = []
        texts = dict(self.fixture_texts)
        hashes = dict(self.fixture_hashes)
        changed = ["docs/exports/catalog.json", "docs/exports/group-a.json", "docs/exports/group-b.json", self.groups[0]["target_path"] + "/SKILL.md"]
        for name in changed:
            path = self.root / name
            if path.exists():
                texts[name] = path.read_text(encoding="utf-8")
                hashes[name] = portable_sha256(path.read_bytes())
            else:
                texts.pop(name, None)
                hashes.pop(name, None)
        validate_exports(self.root, lambda path, rule: result.append(rule), hashes=hashes, texts=texts)
        return set(result)

    def test_two_manifest_formats_cover_all_origins(self):
        self.assertEqual(len(self.catalog["entries"]), 193)
        self.assertEqual(self.rules(), set())

    def test_missing_catalog_cannot_silently_skip_coverage(self):
        (self.root / "docs/exports/catalog.json").unlink()
        self.assertEqual(self.rules(), {"export-catalog-missing"})

    def test_original_public_core_cannot_be_silently_rewritten(self):
        path = self.root / self.groups[0]["target_path"] / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("Synthetic method.", "Changed method."), encoding="utf-8")
        self.assertIn("export-core-modified", self.rules())

    def test_missing_and_duplicate_origin_fail(self):
        self.catalog["entries"][-1] = self.catalog["entries"][0]
        self.save()
        self.assertIn("export-source-coverage", self.rules())

    def test_worker_manifest_drift_fails_coverage(self):
        self.groups.pop()
        self.write_groups()
        self.assertIn("export-source-coverage", self.rules())

    def test_body_stub_and_hash_tampering_are_rejected(self):
        item = self.catalog["entries"][0]
        (self.root / item["body"]["path"]).write_text("# Procedure\nSee external tool.\n", encoding="utf-8")
        self.assertTrue({"export-file-hash", "export-body-hash", "export-body-stub"} <= self.rules())

    def test_missing_support_helper_is_not_available(self):
        self.catalog["entries"][0]["files"].append({"path": ".agents/skills/method-0/scripts/helper.py", "sha256": "0" * 64})
        self.save()
        self.assertIn("export-support-file-missing", self.rules())

    def test_external_dependency_claimed_bundled_fails(self):
        self.catalog["entries"][0]["dependencies"] = [{"name": "../outside.py", "status": "bundled", "contract": "Available."}]
        self.save()
        self.assertIn("export-path-unsafe", self.rules())

    def test_missing_bundled_dependency_fails(self):
        self.catalog["entries"][0]["dependencies"] = [{"name": "scripts/absent.py", "status": "bundled", "contract": "Available."}]
        self.save()
        self.assertIn("export-bundled-dependency-missing", self.rules())

    def test_nonbundled_dependency_needs_explicit_contract(self):
        self.catalog["entries"][0]["dependencies"] = [{"name": "external.py", "status": "user-supplied-not-runtime-verified"}]
        self.save()
        self.assertIn("export-dependency-contract", self.rules())

    def test_source_sha_is_checked_against_real_source(self):
        self.groups[0]["sha256original"] = "0" * 64
        self.write_groups()
        with self.assertRaisesRegex(ValueError, "export-source-hash"):
            build_catalog(self.root, self.source)

    def test_unknown_license_does_not_exclude_import(self):
        self.assertEqual(self.rules(), set())

    def test_root_mit_cannot_relicense_import(self):
        self.catalog["entries"][0]["license"]["relicensed"] = True
        self.save()
        self.assertIn("export-license-contract", self.rules())


class SafetyPerformanceTests(unittest.TestCase):
    def test_long_base64_and_alphabetic_tokens_stay_bounded(self):
        start = time.perf_counter()
        for text in ("a" * 200_000, "Ab3+/=" * 30_000):
            self.assertEqual(sensitive_rules(text), set())
            self.assertIn("secret-pattern", sensitive_rules(text + "\n" + "gh" + "p_" + "aB7z" * 9))
        self.assertLess(time.perf_counter() - start, 5.0)

    def test_two_megabyte_token_and_secret_across_size_boundary(self):
        code = (
            "from scripts.model_safety import sensitive_rules; "
            "s='a'*2000000; assert not sensitive_rules(s); "
            "prefix='a'*(65536-3)+'\\n'; secret='gh'+'p_'+'aB7z'*9; "
            "assert 'secret-pattern' in sensitive_rules(prefix+secret+'\\n'+s)"
        )
        completed = subprocess.run([sys.executable, "-B", "-c", code],
                                   cwd=Path(__file__).resolve().parent.parent,
                                   capture_output=True, timeout=15)
        self.assertEqual(completed.returncode, 0, "Bounded child safety scan failed")

    def test_email_maximum_lengths_still_detected(self):
        address = "a" * 64 + "@" + ".".join(["b" * 63, "c" * 63, "d" * 63, "e" * 61])
        self.assertIn("personal-email", sensitive_rules(address))

    def test_uri_credentials_after_long_token_are_still_detected(self):
        self.assertIn("secret-pattern", sensitive_rules("a" * 30_000 + "\nhttps://" + "reader:" + "synthetic-password" + "@service.invalid"))


class SemanticIntegrityTests(unittest.TestCase):
    def test_lf_crlf_target_hash_and_body_are_portable(self):
        lf = b"---\nname: test\ndescription: Test.\n---\nBody\n"
        crlf = lf.replace(b"\n", b"\r\n")
        self.assertEqual(portable_sha256(lf), portable_sha256(crlf))
        self.assertEqual(body_text(lf.decode()), body_text(crlf.decode()))
        self.assertTrue(manifest_hash_matches(lf, hashlib.sha256(crlf).hexdigest()))
        self.assertTrue(manifest_hash_matches(crlf, hashlib.sha256(lf).hexdigest()))
        self.assertFalse(manifest_hash_matches(lf + b"changed", hashlib.sha256(lf).hexdigest()))

    def test_binary_hash_is_not_newline_normalized(self):
        data = b"\xff\x80\r\n"
        self.assertEqual(portable_sha256(data), hashlib.sha256(data).hexdigest())
    def test_large_nonprivate_numeric_setting_cannot_be_zeroed(self):
        self.assertFalse(numeric_integrity('{"max_payload_bytes":10485760}', '{"max_payload_bytes":0}'))

    def test_identifier_redaction_does_not_excuse_numeric_setting_changes(self):
        self.assertTrue(numeric_integrity('{"resource_id":12345678,"limit":50}', '{"resource_id":0,"limit":50}'))
        self.assertFalse(numeric_integrity('{"resource_id":12345678,"limit":50}', '{"resource_id":0,"limit":0}'))

    def test_missing_numeric_key_is_not_preservation(self):
        self.assertFalse(numeric_integrity('{"nested":{"limit":100}}', '{"nested":{}}'))
