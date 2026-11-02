import json

from test_validate_model import ModelCase


class MatrixTests(ModelCase):
    def matrix_rules(self):
        self.write_matrix()
        return self.rules(".codex/skill-routing.json")

    def test_complete_schema(self):
        self.assertEqual(self.matrix_rules(), set())

    def test_missing_matrix(self):
        (self.root / ".codex/skill-routing.json").unlink()
        self.assertIn("matrix-missing", self.rules())

    def test_json_syntax_invalid_top_level_and_duplicate_keys(self):
        for text in ("{", "[]", '{"schema_version":1,"schema_version":1}'):
            with self.subTest(kind="json"):
                self.write(".codex/skill-routing.json", text)
                self.assertTrue({"matrix-json", "matrix-schema"} & self.rules())

    def test_version_exact_integer_not_boolean(self):
        for value in (True, "1", 2):
            with self.subTest(value=value):
                self.matrix["schema_version"] = value
                self.assertIn("matrix-schema", self.matrix_rules())

    def test_declarative_and_path_base_contract(self):
        self.matrix["recommendation_only"] = False
        self.matrix["path_base"] = "current-directory"
        self.assertIn("matrix-schema", self.matrix_rules())

    def test_unknown_schema_fields_fail_closed(self):
        self.matrix["unexpected"] = {}
        self.assertIn("matrix-schema", self.matrix_rules())

    def test_skill_reference_in_agent_resolves(self):
        self.matrix["agents"]["worker"]["skills"] = ["haos-absent"]
        self.assertIn("matrix-skill-reference", self.matrix_rules())

    def test_route_targets_and_skills_resolve(self):
        self.matrix["routes"][0]["agents"] = ["absent"]
        self.matrix["routes"][0]["skills"] = ["haos-absent"]
        self.assertTrue({"matrix-agent-reference", "matrix-skill-reference"} <= self.matrix_rules())

    def test_duplicate_route_id(self):
        self.matrix["routes"].append(dict(self.matrix["routes"][0]))
        self.assertIn("matrix-duplicate-route-id", self.matrix_rules())

    def test_duplicate_reference(self):
        self.matrix["routes"][0]["agents"] = ["worker", "worker"]
        self.assertIn("matrix-duplicate-reference", self.matrix_rules())

    def test_unsafe_and_mismatched_catalog_paths(self):
        for path in (
            "../outside.toml", "/outside.toml", "C:" + "/repo/worker.toml",
            ".codex\\agents\\worker.toml", ".codex/agents/../worker.toml",
            ".codex//agents/worker.toml", ".codex/agents/./worker.toml",
        ):
            with self.subTest(kind="unsafe-path"):
                self.matrix["agents"]["worker"]["path"] = path
                self.assertIn("matrix-path-unsafe", self.matrix_rules())

    def test_path_requires_own_registered_file_not_arbitrary_existing_file(self):
        self.matrix["agents"]["worker"]["path"] = ".codex/skill-routing.json"
        self.assertIn("matrix-path-mismatch", self.matrix_rules())

    def test_missing_file_in_catalog(self):
        (self.root / ".codex/agents/worker.toml").unlink()
        self.assertIn("local-path-missing", self.matrix_rules())

    def test_unregistered_file_cannot_be_silently_ignored(self):
        self.write(".codex/agents/other.toml", 'developer_instructions = "Other."\n')
        self.assertIn("matrix-agents-coverage", self.matrix_rules())

    def test_unregistered_skill_cannot_be_silently_ignored(self):
        self.write(".agents/skills/haos-extra/SKILL.md", "---\nname: haos-extra\ndescription: Extra.\n---\n")
        self.assertIn("matrix-skills-coverage", self.matrix_rules())

    def test_council_references_resolve(self):
        self.matrix["council"]["agents"] = ["absent"]
        self.matrix["council"]["financial_agent"] = "absent"
        self.assertIn("matrix-agent-reference", self.matrix_rules())

    def test_entrypoint_key_and_skill_must_match_real_skill(self):
        self.matrix["entrypoints"]["haos-test"]["skill"] = "haos-absent"
        self.assertIn("matrix-entrypoint-reference", self.matrix_rules())

    def test_malformed_types_never_crash(self):
        malformed = [None, [], {}, 3, True, "text"]
        original = json.dumps(self.matrix)
        for field in ("defaults", "skills", "agents", "routes", "council", "entrypoints", "capabilities"):
            for value in malformed:
                with self.subTest(field=field, value=value):
                    self.matrix = json.loads(original)
                    self.matrix[field] = value
                    self.assertIn("matrix-schema", self.matrix_rules())

    def test_malformed_route_and_agent_field_types_never_crash(self):
        original = json.dumps(self.matrix)
        for field in ("id", "agents", "skills", "mode", "triggers", "external_approval_required"):
            for value in (None, [], {}, True, 42):
                if field in {"agents", "skills"} and value == []:
                    continue
                if field == "external_approval_required" and type(value) is bool:
                    continue
                with self.subTest(field=field, value=value):
                    self.matrix = json.loads(original)
                    self.matrix["routes"][0][field] = value
                    self.assertTrue(self.matrix_rules())

    def test_parallel_and_correction_limits(self):
        for value in (True, 0, 4, "3", []):
            with self.subTest(value=value):
                self.matrix["defaults"]["max_parallel_agents"] = value
                self.assertIn("matrix-schema", self.matrix_rules())
