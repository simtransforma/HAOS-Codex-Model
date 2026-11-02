"""Reconcile the scoped public QA corrections without rerunning either exporter."""

import argparse
import json
import re
from pathlib import Path

from export_skill_group_b import classify_dependencies, dependency_sections
from model_exports import portable_sha256, safe_file
from model_client_examples import sanitize_client_examples


A_REASONS = {
    'haos-local-research': 'provider reference parameterized; no credential validity asserted',
    'clint-api': 'personal sandbox, broker and dated business facts replaced by conditional procedure',
    'clint-global': 'payment journey uses synthetic acceptance cases, not customer audits or metrics',
    'haos-replicacao-runtimes': 'dated live-state claims and personal sandbox facts replaced by unchecked conditional checklist',
}


INTEGRATION_MODEL = '''## Modelos condicionais de integracao

- **BI e tags:** se houver integracao autorizada, importar contatos e tags com paginacao completa, reconciliar totais e registrar descartes sem email. Definir conexao, limites e eventual uso de pooler para o ambiente do usuario; nenhuma contagem, cron ou banco e presumido instalado.
- **Audiencias:** se houver workflow n8n autorizado, comparar snapshots de tags por polling/diff e definir a agenda, a zona de horario e o destino de audiencia. Verificar consentimento, cotas e opt-out antes de qualquer efeito externo; nenhum workflow e apresentado como ativo.
- **Webhooks de venda:** se o provedor e o CRM suportarem a integracao, configurar o mapeamento autorizado de eventos para contatos, validando autenticacao, idempotencia e tratamento de falhas. Exigir teste controlado e readback antes de declarar entrega.
- **Broker local:** se o usuario fornecer um adaptador, revisar allowlist de rotas e leitura segura da credencial, testar sua interface e manter logs sem segredos. Nao presumir sandbox, comando ou infraestrutura pessoal de terceiros.

'''


def sanitize_two_private_contexts(root: Path, write: bool) -> None:
    clint = root / '.agents/skills/clint-api/SKILL.md'
    runbook = root / '.agents/skills/haos-replicacao-runtimes/references/runbook-por-destino.md'
    clint_text = clint.read_text(encoding='utf-8-sig')
    runbook_text = runbook.read_text(encoding='utf-8-sig')
    personal_heading = re.compile(r'^##\s+Destino\s+\d+[.:\u2014\u2013\s-]+(.+?)\s*\(sandbox\)\s*$', re.M | re.I)
    clint_text = re.sub(r'^## Integra[cç][oõ]es j[aá] existentes[^\n]*\n.*?(?=^## |\Z)',
                        INTEGRATION_MODEL, clint_text, flags=re.M | re.S)
    runbook_text = personal_heading.sub(
        '## Destino opcional: sandbox privado (modelo condicional)\n\n'
        'Se houver sandbox no escopo aprovado, confirmar seu estado ativo ou pausado, o responsavel autorizado e o runtime usado. '
        'Selecionar o metodo de entrega compativel, preservar outras skills e verificar o resultado no destino. '
        'Nao propagar conteudo para ambiente pessoal, pausado ou nao autorizado por presuncao.', runbook_text)
    pending = {clint: clint_text, runbook: runbook_text}
    for path, text in pending.items():
        if re.search(r'Integra[cç][oõ]es j[aá] existentes|Confirmado ao vivo em', text, re.I):
            raise ValueError('private-operational-context-still-present')
        if write:
            path.write_text(text, encoding='utf-8', newline='\n')
    print(f'PASS: two scoped conditional models; {len(pending)} scoped files reconciled; private values not displayed')


def reconcile(root: Path, write: bool, source: Path | None = None) -> None:
    sanitize_client_examples(root, write, source)
    sanitize_two_private_contexts(root, write)
    groups = {g: json.loads((root / f'docs/exports/group-{g}.json').read_text(encoding='utf-8')) for g in ('a', 'b')}
    originals = {e['source_folder']: e['sha256original'] for group in groups.values() for e in group}
    for entry in groups['a']:
        if entry['source_folder'] not in A_REASONS:
            continue
        prefix = entry['target_path'] + '/'
        files = []
        for original in entry['files']:
            item = {'path': original} if isinstance(original, str) else dict(original)
            item.setdefault('source_rel', item['path'][len(prefix):])
            item['sha256'] = portable_sha256(safe_file(root, item['path']).read_bytes())
            files.append(item)
        entry['files'] = files
        entry['status'] = 'adapted_private_config'
        entry['post_export_qa'] = [A_REASONS[entry['source_folder']]]
    entry = next(e for e in groups['b'] if e['source_folder'] == 'vercel-optimize')
    prefix = entry['target_path'] + '/'
    contents = {f['path'][len(prefix):]: safe_file(root, f['path']).read_text(encoding='utf-8-sig')
                for f in entry['files'] if f['path'].startswith(prefix)}
    entry['dependencies'] = classify_dependencies(entry['dependencies'], contents, prefix)
    contract = contents['PORTABILITY.md']
    starts = [contract.index(marker) for marker in ('## Bundled resources', '## Missing resources and configuration') if marker in contract]
    end = contract.index('## File transformations')
    contract = contract[:min(starts)] + dependency_sections(entry['dependencies']) + '\n\n' + contract[end:]
    if write:
        (root / prefix / 'PORTABILITY.md').write_text(contract, encoding='utf-8', newline='\n')
    entry['post_export_qa'] = ['complete ignored Cache-Control directive values removed; orphan values rejected',
                               'relative dependency references resolved from declaring files; bundled presence is not runtime proof']
    for item in entry['files']:
        data = contract.encode() if item['path'] == prefix + 'PORTABILITY.md' else safe_file(root, item['path']).read_bytes()
        item['sha256'] = portable_sha256(data)
    assert originals == {e['source_folder']: e['sha256original'] for group in groups.values() for e in group}
    if write:
        for group, entries in groups.items():
            (root / f'docs/exports/group-{group}.json').write_text(json.dumps(entries, ensure_ascii=True, indent=2) + '\n', encoding='utf-8', newline='\n')
    bundled = [d for d in entry['dependencies'] if d['status'] == 'bundled']
    required = {prefix + 'lib/citations.mjs', prefix + 'references/doctrine.md'}
    assert required <= {d['name'] for d in bundled}
    print(f'PASS: {len(originals)} original source hashes preserved; {len(bundled)} Vercel references bundled by declaring file; write={write}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--source', type=Path, help='Readonly source skills; used only for the geographic dictionary')
    args = parser.parse_args()
    reconcile(args.root, args.write, args.source)
