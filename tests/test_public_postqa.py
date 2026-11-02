import importlib
from pathlib import Path
import shutil
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent.parent


class PublicPostQATests(unittest.TestCase):
    def test_private_integration_history_is_conditional(self):
        text = (ROOT / '.agents/skills/clint-api/SKILL.md').read_text(encoding='utf-8')
        self.assertNotRegex(text, r'Integra[cç][oõ]es j[aá] existentes|\d[\d.,]*\s+leads? importados')
        self.assertIn('## Modelos condicionais de integracao', text)
        for procedure in ('paginacao', 'pooler', 'polling/diff', 'Webhooks', 'Broker'):
            self.assertIn(procedure, text)

    def test_personal_sandbox_heading_is_conditional(self):
        text = (ROOT / '.agents/skills/haos-replicacao-runtimes/references/runbook-por-destino.md').read_text(encoding='utf-8')
        self.assertIsNone(re.search(r'^##\s+Destino\s+\d+[.:\u2014\u2013\s-]+.+?\s*\(sandbox\)\s*$', text, re.M | re.I))
        self.assertIn('sandbox privado (modelo condicional)', text)
        for procedure in ('scp', 'registry', 'SOUL'):
            self.assertIn(procedure, text)

    def test_vercel_offline_regressions(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('Node.js unavailable; offline Vercel regression not tested')
        result = subprocess.run([node, '--test', 'tests/test_vercel_directives.mjs'], cwd=ROOT,
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_relative_dependencies_resolve_from_declaring_file(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            exporter = importlib.import_module('export_skill_group_b')
            prefix = '.agents/skills/vercel-optimize/'
            dependencies = [{'name': './citations.mjs', 'contract': 'Missing.', 'status': 'user-supplied-not-runtime-verified'},
                            {'name': './references/doctrine.md', 'contract': 'Missing.', 'status': 'user-supplied-not-runtime-verified'}]
            contents = {'lib/verify-claim.mjs': "import './citations.mjs';", 'lib/citations.mjs': 'export const citations = [];',
                        'SKILL.md': 'See ./references/doctrine.md', 'references/doctrine.md': '# Doctrine'}
            resolved = exporter.classify_dependencies(dependencies, contents, prefix)
            self.assertEqual({d['name'] for d in resolved}, {prefix + 'lib/citations.mjs', prefix + 'references/doctrine.md'})
            self.assertTrue(all(d['status'] == 'bundled' for d in resolved))
            self.assertEqual(resolved[0]['declared_by'], [prefix + 'lib/verify-claim.mjs'])
            self.assertEqual(exporter.classify_dependencies(resolved, contents, prefix), resolved)
            contract = exporter.dependency_sections(resolved)
            missing = contract.split('## Missing resources and configuration', 1)[1]
            self.assertNotIn('citations.mjs', missing)
            self.assertNotIn('doctrine.md', missing)
        finally:
            sys.path.pop(0)

    def test_provider_redaction_avoids_literal_identifier(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            exporter = importlib.import_module('export_skill_group_a')
            original = '- Local' + 'API: ' + 'synthetic' * 3
            clean, changes = exporter.sanitize(original)
            self.assertNotIn('synthetic' * 3, clean)
            self.assertIn('local-provider-reference-parameterized', changes)
        finally:
            sys.path.pop(0)
