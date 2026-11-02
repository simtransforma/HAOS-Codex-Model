"""All sensitive-looking fixtures are synthetic and created outside the checkout."""

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.model_safety import sensitive_rules
from scripts.validate_model import Validator, frontmatter, main


def fake_email():
    return "operator" + "@" + "private-company.tld"


def fake_secret():
    return "gh" + "p_" + "aB7z" * 9


def matrix_fixture():
    return {
        "schema_version": 1,
        "description": "Synthetic declarative fixture.",
        "recommendation_only": True,
        "path_base": "repository-root",
        "defaults": {"effort": "high", "max_parallel_agents": 3, "max_correction_cycles": 3},
        "skills": {"haos-test": {"path": ".agents/skills/haos-test/SKILL.md", "description": "Test method."}},
        "agents": {"worker": {"path": ".codex/agents/worker.toml", "description": "Worker.", "skills": ["haos-test"], "function": "implementation"}},
        "routes": [{"id": "engineering", "description": "Engineering route.", "triggers": ["implementation"], "agents": ["worker"], "skills": ["haos-test"], "mode": "DELEGATE", "external_approval_required": False}],
        "council": {"agents": ["worker"], "financial_agent": "worker", "financial_when": "Financial decision."},
        "entrypoints": {"haos-test": {"skill": "haos-test", "description": "Test entrypoint."}},
        "capabilities": {"included": ["engineering"], "adapted": [], "optional_dependencies": [], "excluded": ["external runtime"]},
    }


class ModelCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="haos-model-fixture-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write(".codex/agents/worker.toml", 'developer_instructions = "Do scoped work."\n')
        self.write(".agents/skills/haos-test/SKILL.md", "---\nname: haos-test\ndescription: Test method.\n---\n")
        self.matrix = matrix_fixture()
        self.write_matrix()

    def write_matrix(self):
        self.write(".codex/skill-routing.json", json.dumps(self.matrix))

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return path

    def findings(self):
        return Validator(self.root).run()

    def rules(self, path=None):
        return {finding.rule for finding in self.findings() if path is None or finding.path == path}

    def link(self, source, target, directory=False):
        try:
            (self.root / source).symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError):
            self.skipTest("Creating symlinks is unavailable on this host")


class StructureTests(ModelCase):
    def test_valid_complete_model(self):
        self.assertEqual(self.findings(), [])

    def test_real_toml_parser_rejects_malformed_toml(self):
        self.write(".codex/agents/worker.toml", 'developer_instructions = "unterminated\n')
        self.assertIn("agent-toml", self.rules())

    def test_toml_errors_never_expose_parser_content(self):
        self.write(".codex/agents/worker.toml", fake_secret() + " = [broken")
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["--root", str(self.root)]), 1)
        self.assertNotIn(fake_secret(), output.getvalue())
        self.assertNotIn(str(self.root), output.getvalue())

    def test_agent_instruction_and_effort_types(self):
        self.write(".codex/agents/worker.toml", 'developer_instructions = []\nmodel_reasoning_effort = 42\n')
        self.assertTrue({"agent-instructions", "agent-effort"} <= self.rules())

    def test_agent_id_matches_filename_when_declared(self):
        self.write(".codex/agents/worker.toml", 'id = "other"\ndeveloper_instructions = "Work."\n')
        self.assertIn("agent-id-mismatch", self.rules())

    def test_duplicate_agent_ids_in_nested_folders(self):
        self.write(".codex/agents/nested/worker.toml", 'developer_instructions = "Work."\n')
        self.assertIn("duplicate-agent-id", self.rules())

    def test_duplicate_skill_ids_and_folder_mismatch(self):
        self.write(".agents/skills/other/SKILL.md", "---\nname: haos-test\ndescription: Other.\n---\n")
        self.assertTrue({"duplicate-skill-id", "skill-folder-name"} <= self.rules())

    def test_frontmatter_required(self):
        self.write(".agents/skills/haos-test/SKILL.md", "# No metadata\n")
        self.assertIn("skill-frontmatter", self.rules())

    def test_skill_directory_requires_skill_file(self):
        self.write(".agents/skills/incomplete/README.md", "# Incomplete\n")
        self.assertIn("skill-file-missing", self.rules())

    def test_missing_model_not_accepted(self):
        empty = self.root / "empty"
        empty.mkdir()
        self.assertEqual({finding.rule for finding in Validator(empty).run()}, {"model-empty"})

    def test_missing_root_is_failure(self):
        self.assertIn("root-unreadable", {finding.rule for finding in Validator(self.root / "absent").run()})

    def test_invalid_encoding_rejected_for_structured_text(self):
        self.write(".codex/agents/worker.toml", b"\xff\x80")
        self.assertIn("text-encoding", self.rules())


class FrontmatterTests(unittest.TestCase):
    def test_plain_quoted_and_block_descriptions(self):
        descriptions = ['A plain description.', '"A quoted description."', "'A quoted description.'", ">-\n  A folded\n  description.", "|\n  A literal\n  description."]
        for description in descriptions:
            with self.subTest(description=description):
                result = frontmatter("---\nname: haos-test\ndescription: " + description + "\n---\n")
                self.assertEqual(result["name"], "haos-test")
                self.assertTrue(result["description"])

    def test_only_required_fields_are_interpreted(self):
        result = frontmatter("---\nname: haos-test\ndescription: Method.\nmetadata:\n  anything: [not, parsed]\n---\n")
        self.assertEqual(set(result), {"name", "description"})

    def test_invalid_or_ambiguous_required_fields_rejected(self):
        for body in (
            "name: haos-test", "name: haos-test\ndescription: []",
            "name: haos-test\nname: duplicate\ndescription: Method.",
            'name: haos-test\ndescription: "unterminated',
            "name: haos-test\ndescription: &anchor value", "name: haos-test\ndescription: >",
        ):
            with self.subTest(body=body), self.assertRaises(ValueError):
                frontmatter("---\n" + body + "\n---\n")

    def test_unclosed_frontmatter_rejected(self):
        with self.assertRaises(ValueError):
            frontmatter("---\nname: haos-test\ndescription: Method.\n")


class SafetyTests(ModelCase):
    def test_private_paths_both_separator_styles(self):
        for value in (
            "C:" + "/Users/" + "operator/work", "C:" + "\\Users\\" + "operator\\work",
            "H:" + "/internal/repo", "h:" + "\\internal\\repo",
        ):
            with self.subTest(kind="path"):
                self.assertIn("private-environment-path", sensitive_rules(value))

    def test_generic_examples_do_not_trigger(self):
        text = "\n".join((
            "reader@example.com", "user@docs.example.org", "person@service.invalid",
            "person@service.test", "phone: <PHONE>", "api_key = YOUR_API_KEY",
            "token = ${TOKEN}", "account_id = <ACCOUNT_ID>", "version 3.11.14",
            "password = PASSWORD_HERE", "secret = not-a-real-secret", "api_key = SUA_CHAVE_AQUI",
            "2026-11-02", "12345678901234567890", "a" * 40,
            "C:" + "/Users/<USER>/project", "H:" + "/<WORKSPACE>/project",
            "GT" + "M-" + "X" * 8, "act" + "_" + "0" * 12,
            "gh" + "p_" + "X" * 36, "-----BEGIN " + "PRIVATE KEY-----",
        ))
        self.assertEqual(sensitive_rules(text), set())

    def test_personal_email(self):
        self.assertEqual(sensitive_rules(fake_email()), {"personal-email"})

    def test_phones(self):
        for value in ("+" + "55 31 98765-4321", "(" + "31) 98765-4321", "phone: " + "5531987654321"):
            with self.subTest(kind="phone"):
                self.assertIn("phone-number", sensitive_rules(value))

    def test_contextual_production_identifiers(self):
        for value in (
            "act" + "_" + "24681357902468", "GT" + "M-" + "AB12CD34",
            "campaign_id = " + "24681357902468", "project_id = " + "abcd1234-5678-abcd",
            "24681357902468" + "@" + "g.us",
        ):
            with self.subTest(kind="identifier"):
                self.assertIn("production-id", sensitive_rules(value))

    def test_secret_patterns_and_assignments(self):
        for value in (
            fake_secret(), "sk" + "-proj-" + "aB7z" * 12,
            "AK" + "IA" + "AB12" * 4,
            "-----BEGIN " + "PRIVATE KEY-----\n" + "aB7z" * 12,
            'api_key = "' + "q7Za9B2c8D4e6F1g" + '"',
            "postgres://operator:" + "p4ssword" + "@localhost/db",
        ):
            with self.subTest(kind="secret"):
                self.assertTrue({"secret-pattern", "secret-assignment"} & sensitive_rules(value))

    def test_untracked_ignored_and_extensionless_candidates_are_scanned(self):
        self.write(".gitignore", "new-private/\n")
        self.write("new-private/payload", fake_email())
        self.assertIn("personal-email", self.rules("new-private/payload"))

    def test_binary_and_utf16_are_scanned(self):
        self.write("payload.bin", b"\x00\xff" + fake_secret().encode() + b"\x00")
        self.write("wide.bin", fake_email().encode("utf-16"))
        self.assertIn("secret-pattern", self.rules("payload.bin"))
        self.assertIn("personal-email", self.rules("wide.bin"))

    def test_only_named_metadata_and_dependency_caches_excluded(self):
        for directory in (".git", "node_modules", ".venv", "__pycache__", ".pytest_cache"):
            self.write(directory + "/secret.txt", fake_secret())
        self.write("build/payload.txt", fake_secret())
        self.write("docs/payload.txt", fake_secret())
        hits = {finding.path for finding in self.findings() if finding.rule == "secret-pattern"}
        self.assertEqual(hits, {"build/payload.txt", "docs/payload.txt"})

    def test_worktree_git_file_is_excluded(self):
        self.write(".git", "gitdir: " + "H:" + "/private/worktree")
        self.assertNotIn("private-environment-path", self.rules(".git"))

    def test_output_contains_file_and_rule_not_secret_or_email(self):
        self.write("payload.txt", fake_secret() + "\n" + fake_email())
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["--root", str(self.root)]), 1)
        self.assertNotIn(fake_secret(), output.getvalue())
        self.assertNotIn(fake_email(), output.getvalue())
        rows = [json.loads(line) for line in output.getvalue().splitlines() if line.startswith("{")]
        self.assertTrue(rows)
        self.assertTrue(all(set(row) == {"file", "rule"} for row in rows))

    def test_file_read_errors_do_not_dump_exception_content(self):
        original = Path.read_bytes

        def read(path):
            if path.name == "payload.txt":
                raise PermissionError(fake_secret())
            return original(path)

        self.write("payload.txt", "plain")
        with patch.object(Path, "read_bytes", read):
            self.assertIn("file-unreadable", self.rules("payload.txt"))


class LocalLinkTests(ModelCase):
    def test_valid_relative_and_encoded_local_links(self):
        self.write("docs/a file.md", "# Target\n")
        self.write("docs/guide.md", "[target](a%20file.md#target)\n[other](../README.md)\n")
        self.write("README.md", "[guide](docs/guide.md)\n![asset](<docs/a file.md>)\n")
        self.assertFalse(any(f.rule.startswith("local-path") for f in self.findings()))

    def test_parentheses_and_escaped_spaces_in_targets(self):
        self.write("docs/a(b).md", "# Target\n")
        self.write("docs/a file.md", "# Target\n")
        self.write("README.md", '[one](docs/a(b).md "title")\n[two](docs/a\\ file.md)\n')
        self.assertFalse(any(f.rule.startswith("local-path") for f in self.findings()))

    def test_reference_labels_case_and_space_normalization(self):
        self.write("target.md", "# Target\n")
        self.write("README.md", "[go][Some Label]\n[some   label]: target.md\n")
        self.assertNotIn("markdown-reference-missing", self.rules("README.md"))

    def test_inline_markdown_syntax_example_ignored(self):
        self.write("README.md", "Use `[label](placeholder.md)` as a generic example.\n")
        self.assertNotIn("local-path-missing", self.rules("README.md"))

    def test_missing_inline_and_reference_links(self):
        self.write("README.md", "[inline](missing.md)\n[reference][target]\n[target]: absent.md\n[undefined][nope]\n")
        self.assertTrue({"local-path-missing", "markdown-reference-missing"} <= self.rules("README.md"))

    def test_explicit_inline_repo_path_checked(self):
        self.write("README.md", "`docs/missing.md`\n")
        self.assertIn("local-path-missing", self.rules("README.md"))

    def test_generic_code_examples_and_remote_urls_not_required_locally(self):
        self.write("README.md", "\n".join((
            "[remote](https://example.com/absent.md)", "[anchor](#part)",
            "```md", "[example](missing.md)", "`docs/placeholder.md`", "```",
            "`config.toml` `.agents/skills/<name>/SKILL.md` `scripts/**`",
        )))
        self.assertFalse(any(f.rule.startswith("local-path") for f in self.findings()))

    def test_escaping_paths_and_unsafe_schemes_rejected(self):
        for target in ("../escape.md", "%2e%2e/escape.md", "/absolute.md", "file:///outside.md", "javascript:alert"):
            with self.subTest(target=target):
                self.write("README.md", "[bad](" + target + ")")
                self.assertTrue({"local-path-escape", "local-path-unsafe"} & self.rules("README.md"))

    def test_file_symlink_and_dangling_symlink_rejected(self):
        self.write("target.txt", "plain")
        self.link("alias.txt", self.root / "target.txt")
        self.link("dangling.txt", self.root / "absent.txt")
        self.assertIn("symlink", self.rules("alias.txt"))
        self.assertIn("symlink", self.rules("dangling.txt"))

    def test_directory_symlink_not_followed_even_with_excluded_name(self):
        self.write("target/payload.txt", fake_secret())
        self.link("node_modules", self.root / "target", directory=True)
        self.assertIn("symlink", self.rules("node_modules"))
        self.assertFalse(any(f.path.startswith("node_modules/") for f in self.findings()))

    def test_link_to_symlink_is_rejected(self):
        self.write("target.txt", "plain")
        self.link("alias.txt", self.root / "target.txt")
        self.write("README.md", "[alias](alias.txt)\n")
        self.assertIn("local-path-symlink", self.rules("README.md"))


class CLITests(ModelCase):
    def test_sensitive_filenames_redacted_for_every_rule_without_changing_matches(self):
        values = {
            "token": fake_secret(),
            "email": fake_email(),
            "phone": "+" + "55 31 98765-4321",
        }
        content = "[missing](absent.md)\n" + "\n".join(values.values())
        paths = {kind: "fixtures/" + value + ".md" for kind, value in values.items()}
        for path in paths.values():
            self.write(path, content)
        self.write("ordinary.md", content)
        expected = self.findings()
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["--root", str(self.root)]), 1)
        console = output.getvalue()
        for value in values.values():
            self.assertTrue(value not in console, "Sensitive filename or content appeared in CLI output")
        rows = [json.loads(line) for line in console.splitlines() if line.startswith("{")]
        redacted = [row for row in rows if row["file"].startswith("<redacted-path:")]
        self.assertEqual(len(rows), len(expected))
        self.assertEqual(len({row["file"] for row in redacted}), len(paths))
        self.assertEqual(
            sorted(row["rule"] for row in redacted),
            sorted(finding.rule for finding in expected if finding.path in paths.values()),
        )
        for path in {row["file"] for row in redacted}:
            self.assertRegex(path, r"^<redacted-path:[a-f0-9]{64}>$")
            self.assertIn("local-path-missing", {row["rule"] for row in redacted if row["file"] == path})
        self.assertTrue(any(row["file"] == "ordinary.md" for row in rows))

    def test_sensitive_parent_directory_redacted_even_on_read_error(self):
        name = "fixtures/" + fake_email() + "/payload.txt"
        self.write(name, "plain")
        original = Path.read_bytes

        def read(path):
            if path.name == "payload.txt":
                raise PermissionError("fixture read error")
            return original(path)

        output = io.StringIO()
        with patch.object(Path, "read_bytes", read), redirect_stdout(output):
            self.assertEqual(main(["--root", str(self.root)]), 1)
        console = output.getvalue()
        self.assertTrue(fake_email() not in console, "Sensitive directory appeared in CLI output")
        rows = [json.loads(line) for line in console.splitlines() if line.startswith("{")]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["rule"], "file-unreadable")
        self.assertRegex(rows[0]["file"], r"^<redacted-path:[a-f0-9]{64}>$")

    def test_sensitive_path_ids_not_enumerable_across_invocations(self):
        self.write(fake_secret() + ".txt", "plain")
        identifiers = []
        for _ in range(2):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["--root", str(self.root)]), 1)
            self.assertTrue(fake_secret() not in output.getvalue(), "Sensitive name appeared in CLI output")
            row = json.loads(output.getvalue().splitlines()[0])
            identifiers.append(row["file"])
        self.assertNotEqual(identifiers[0], identifiers[1])

    def test_cli_failure_exit_code_and_no_traceback(self):
        self.write("payload.txt", fake_secret())
        script = Path(__file__).resolve().parents[1] / "scripts" / "validate_model.py"
        result = subprocess.run(
            [sys.executable, "-B", str(script), "--root", str(self.root)],
            cwd=self.temporary.name, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertIn("FAIL:", result.stdout)

    def test_cli_success_exit_code_and_no_traceback(self):
        script = Path(__file__).resolve().parents[1] / "scripts" / "validate_model.py"
        result = subprocess.run(
            [sys.executable, "-B", str(script), "--root", str(self.root)],
            cwd=self.temporary.name, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stderr, "")
        self.assertIn("PASS:", result.stdout)


if __name__ == "__main__":
    unittest.main()
