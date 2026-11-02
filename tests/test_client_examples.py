import importlib
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parent.parent


class ClientExamplesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(ROOT / 'scripts'))
        cls.model = importlib.import_module('model_client_examples')
        sys.path.pop(0)

    def test_geographic_dictionary_preserves_both_state_aliases(self):
        text = (ROOT / '.agents/skills/clint-api/scripts/clint_client.py.example').read_text(encoding='utf-8')
        _, values = self.model.state_map_literal(text)
        self.assertEqual(values['sao paulo'], 'sp')
        self.assertEqual(values['são paulo'], 'sp')
        self.assertNotIn('sao usuario-do-sandbox', values)

    def test_synthetic_payloads_do_not_redact_geography(self):
        text = '# Example\n\n```json\n{"cidade": "São Paulo", "estado": "SP", "slug": "sao-paulo"}\n```\n'
        clean = self.model.sanitize_document('clint-api/references/schema.md', text)
        self.assertIn('"cidade": "São Paulo"', clean)
        self.assertIn('"estado": "SP"', clean)
        self.assertIn('"slug": "sao-paulo"', clean)

    def test_complete_ten_file_scope_has_no_private_factual_markers(self):
        count, findings = self.model.audit_client_scope(ROOT)
        self.assertEqual(count, 10)
        self.assertEqual(findings, [])
        for relative in self.model.CLIENT_FILES:
            if relative.endswith('.md'):
                text = (ROOT / '.agents/skills' / relative).read_text(encoding='utf-8')
                self.assertIn('<!-- synthetic-client-examples -->', text)

    def test_document_models_are_idempotent(self):
        for relative in self.model.CLIENT_FILES:
            if relative.endswith('.md'):
                with self.subTest(file=relative):
                    text = (ROOT / '.agents/skills' / relative).read_bytes().decode('utf-8-sig')
                    self.assertEqual(self.model.sanitize_document(relative, text), text)

    def test_indented_payload_fences_preserve_layout_and_replace_actual_count(self):
        text = '# Example\n\n  ```json\n    {"totalCount": 123456, "name": "Sample Person"}\n  ```\n'
        clean = self.model.synthetic_payloads(text)
        self.assertIn('  ```json\n    {"totalCount": 2,', clean)
        self.assertTrue(clean.endswith('  ```\n'))
        self.assertNotIn('123456', clean)

    def test_legacy_production_assertions_are_replaced_not_ignored(self):
        examples = {
            'clint-api/references/endpoints.md': '# Example\n\nContrato validado em producao em 01/01/2000.\n',
            'clint-api/scripts/clint_client.py.example': '"""Example\nCodigo validado em producao em 01/01/2000.\n"""\n',
        }
        for relative, text in examples.items():
            with self.subTest(file=relative):
                clean = self.model.sanitize_document(relative, text)
                self.assertNotRegex(clean, r'validado em producao|01/01/2000')
                self.assertIn('Contrato de exemplo a verificar', clean)
