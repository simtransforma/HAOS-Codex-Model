"""Scoped CRM example models; preserves geography, API keys and document layout."""

import ast
from pathlib import Path
import re


NOTICE = ('<!-- synthetic-client-examples -->\n'
          'Exemplos sinteticos: nomes de campanha, contatos, IDs, valores e configuracoes abaixo sao ficticios, '
          'nao um inventario de cliente nem evidencia de producao. Adaptar IDs e slugs ao contrato autorizado; '
          'conferir a versao da API e o resultado antes de qualquer efeito externo.\n\n')
CLIENT_FILES = (
    'clint-api/SKILL.md', 'clint-api/references/endpoints.md', 'clint-api/references/schema.md',
    'clint-api/references/troubleshooting.md', 'clint-api/scripts/clint_client.py.example',
    'clint-global/references/jornada-card-pagamento.md',
)
GEO_REPAIRS = {
    'São usuario-do-sandbox': 'São Paulo', 'Sao usuario-do-sandbox': 'Sao Paulo',
    'são usuario-do-sandbox': 'são paulo', 'sao usuario-do-sandbox': 'sao paulo',
    'sao-usuario-do-sandbox': 'sao-paulo', 'são-usuario-do-sandbox': 'são-paulo',
}
ORIGINS = '''### ORIGINS (Suborigens / colunas de funil): exemplo sintetico

#### `GET /origins?page=N&limit=100`
Paginar `data[]` usando `totalCount` e `hasNext`; nao presumir quantidade de origins ou campanha configurada.
No modelo origin-based, cada origin possui seus stages. Confirmar `origin_id` e `stage_id` antes de criar ou mover deals.

```json
{
  "id": "example-origin-a",
  "name": "Origem de exemplo A",
  "group": {"id": "example-group-a", "name": "Grupo sintetico"},
  "stages": [
    {"id": "example-stage-base", "name": "Entrada de exemplo", "order": 1, "type": "BASE"},
    {"id": "example-stage-won", "name": "Ganho de exemplo", "order": 2, "type": "WON"},
    {"id": "example-stage-lost", "name": "Perda de exemplo", "order": 3, "type": "LOST"}
  ],
  "created_at": null,
  "updated_at": null
}
```

- `group` pode organizar origins; filtrar `group.name` no cliente se a API nao oferecer filtro equivalente.
- Ordenar `stages[]` por `order`; confirmar o stage default e o pertencimento do stage a origin.
- `GET /origins/{id}` retorna a origin individual: conferir o envelope `data` da versao usada.
- Em um teste sintetico de abandono, gerada e aprovada, configurar IDs distintos para cada origin/stage. Nenhuma cadeia real de cliente e fornecida.

---

'''
TRACKING = '''#### Slugs de tracking: modelo sintetico, nao configuracao de tenant

| Slug de exemplo | Verificacao antes de gravar |
|---|---|
| `utm_source`, `utm_medium`, `utm_content`, `utm_term` | Confirmar cadastro e leitura de retorno. |
| `utm_campaign` | Conferir o slug real no painel e no contrato do cliente. |
| `utm_campaing` | Exemplo hipotetico de typo legado; nao presumir que exista. |
| `landing` | Criar somente com aprovacao se o campo estiver ausente. |

'''
TAG_MODEL = '''## Convencoes de nomenclatura: exemplos sinteticos

Uma automacao pode adotar `example_product_example_stage_010100` ou `example_action_example_context`.
Sao exemplos inventados, nao tags existentes. Definir o parser por contrato, testar entradas invalidas e
mapear explicitamente produto, etapa e origem; nao inferir pagamento ou identidade pelo nome de uma tag.
'''


def restore_geography(text: str) -> str:
    for broken, correct in GEO_REPAIRS.items():
        text = text.replace(broken, correct)
    return text


def state_map_literal(text: str) -> tuple[re.Match, dict]:
    match = re.search(r'(?ms)^STATE_MAP[ \t]*=[ \t]*(\{.*?^\})', text)
    if match is None:
        raise ValueError('geographic-state-map-missing')
    return match, ast.literal_eval(match[1])


def synthetic_payloads(text: str) -> str:
    def block(match):
        body = match[2]
        def value(item):
            key, quote, literal = item[1], item[2], item[3]
            if literal.startswith(('example-', '<EXAMPLE_')) or literal in {
                'Exemplo sintetico', 'Origem de exemplo A', 'Grupo sintetico', 'Entrada de exemplo',
                'Ganho de exemplo', 'Perda de exemplo', '2000-01-01T00:00:00Z', 'sp',
            }:
                return item[0]
            if literal in {'SP', 'BR', 'br', 'BRL', '55', 'São Paulo', 'Sao Paulo', 'são paulo', 'sao paulo',
                           'sao-paulo', 'OPEN', 'WON', 'LOST', 'open', 'won', 'lost', 'BASE'}:
                return item[0]
            if key in {'type', 'status', 'event', 'currency', 'ddi', 'country'}:
                return item[0]
            if key in {'created_at', 'updated_at', 'won_at', 'lost_at'}:
                replacement = '2000-01-01T00:00:00Z'
            elif key == 'email':
                replacement = 'contact@example.invalid'
            elif key == 'name':
                replacement = 'Exemplo sintetico'
            elif key in {'phone', 'fullPhone', 'phone_number', 'doc', 'cep'}:
                replacement = '<EXAMPLE_' + key.upper() + '>'
            else:
                replacement = 'example-' + re.sub(r'[^a-z0-9]+', '-', key.lower()).strip('-')
            start = item.start(3) - item.start()
            end = item.end(3) - item.start()
            return item[0][:start] + replacement + item[0][end:]
        body = re.sub(r'"([^"\n]+)"\s*:\s*(["\x27])([^"\x27\n]*)\2', value, body)
        body = re.sub(r'("(?:value|amount)"\s*:\s*)\d+(?:\.\d+)?', r'\g<1>100.00', body)
        body = re.sub(r'(\bvalue\s*=\s*)\d+(?:\.\d+)?', r'\g<1>100.00', body)
        body = re.sub(r'("totalCount"\s*:\s*)\d+', r'\g<1>2', body)
        body = re.sub(r'(\.find_tag_by_name\()(["\x27])[^"\x27\n]*\2', r'\g<1>"example-tag"', body)
        body = re.sub(r'\b(name|email|origin_id|stage_id|phone)\s*=\s*(["\x27])([^"\x27\n]*)\2',
                      lambda m: m[0][:m.start(3) - m.start()] + ('contact@example.invalid' if m[1] == 'email' else 'example-' + m[1]) + m[0][m.end(3) - m.start():], body)
        body = re.sub(r'(?m)^#.*Deals \+ custom fields.*$', '# Exemplo sintetico: deals e custom fields; validar contrato antes de executar.', body)
        return match[1] + body + match[3]
    return re.sub(r'(?ms)(^[ \t]{0,3}```(?:json|python)[ \t]*\r?\n)(.*?)(^[ \t]{0,3}```[ \t]*$)', block, text)


def replace_production_assertion(line: str) -> str:
    if re.search(r'(?i)\b(?:validad[oa]s?|confirmad[oa]s?|mapead[oa]s?)\b[^\n]{0,80}\bprodu[cç][aã]o', line):
        indent = re.match(r'[ \t]*', line)[0]
        ending = '\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
        return indent + 'Contrato de exemplo a verificar no ambiente autorizado; nenhuma execucao real e alegada.' + ending
    return line


def sanitize_document(relative: str, text: str) -> str:
    text = restore_geography(text)
    if relative.endswith('scripts/clint_client.py.example'):
        def module_docstring(match):
            body = ''.join(replace_production_assertion(line) for line in match[2].splitlines(keepends=True))
            return match[1] + body + match[3]
        text = re.sub(r'(?s)\A(.*?""")(.*?)(""")', module_docstring, text, count=1)
        text = re.sub(r'(?m)^(\s*)# Ordem priorizada ap[oó]s valida[cç][aã]o cross-session:[^\n]*\n\1#[^\n]*',
                      r'\1# Ordem de exemplo; configurar aliases conforme o contrato do usuario.\n\1# Nenhuma configuracao ou validacao de cliente e fornecida.', text)
        text = re.sub(r'(?m)^Backend validado em produ[cç][aã]o[^\n]*$',
                      'Backend de exemplo sintetico; nenhuma execucao em producao e alegada.', text)
        text = text.replace('bugs/pegadinhas mapeados em produção', 'comportamentos a testar em fixtures da versao usada')
        text = re.sub(r'(\.find_tag_by_name\()(["\x27])[^"\x27\n]*\2', r'\g<1>"example-tag"', text)
        return text
    if relative.endswith('references/endpoints.md'):
        fenced = False
        lines = []
        for line in text.splitlines(keepends=True):
            if re.match(r'^[ \t]{0,3}```', line):
                fenced = not fenced
                lines.append(line)
            else:
                repaired = line
                if not fenced and re.search(r'(?i)contrato de exemplo a verificar.*(?:\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})', line):
                    repaired = 'Contrato de exemplo a verificar no ambiente autorizado; nenhuma execucao real e alegada.' + ('\n' if line.endswith('\n') else '')
                lines.append(repaired if fenced else replace_production_assertion(repaired))
        text = ''.join(lines)
    text = synthetic_payloads(text)
    text = re.sub(r'(?i)(?:[,; ]*\(?\b(?:validado|validada|corrigido|testado|observado)(?:s|a)?(?: em)?\s+\d{2}/\d{2}/\d{4}\)?)', '', text)
    text = re.sub(r'(?i)\b(?:schema REAL, validado|validado exaustivamente|observados? por|validado em produ[cç][aã]o)\b', 'contrato de exemplo a verificar', text)
    if relative == 'clint-api/SKILL.md':
        text = re.sub(r'(?m)^(\| Pipelines \| `GET /pipelines` \|).*$', r'\g<1> conferir pipeline ou origin/stage no contrato da versao usada |', text)
        text = re.sub(r'(?m)^Token no .*$', 'Configurar a autenticacao local aprovada e conferir os aliases de ambiente aceitos pelo cliente. Nenhum cofre ou configuracao de cliente e fornecido.', text)
        text = text.replace('# lê token automaticamente', '# depende da configuracao local autorizada do usuario')
    elif relative.endswith('references/endpoints.md'):
        text = re.sub(r'(?ms)^### ORIGINS[^\n]*\n.*?(?=^### |\Z)', ORIGINS, text)
        text = re.sub(r'(?ms)^#### Slugs UTM[^\n]*\n.*?(?=^\*\*Pra registrar|^---|\Z)', TRACKING, text)
        text = re.sub(r'(?m)^- Documenta[cç][aã]o anterior.*$', '- Teste sintetico: comparar um array de IDs com o objeto incorreto e conferir a resposta, sem alegar validacao em producao.', text)
        text = re.sub(r'(?m)^#### Subendpoints de Deal.*$', '#### Subendpoints de Deal a verificar na versao usada', text)
        text = re.sub(r'(?m)^.*script `explore4\.py` salvou samples.*$', 'Conferir o esquema e guardar apenas fixtures sinteticas ou amostras autorizadas em area privada; nenhum dump operacional e embarcado.', text)
        text = re.sub(r'(?m)^- Uso t[ií]pico.*$', '- Exemplo sintetico: somente se o mapa aprovado exigir, concluir a etapa anterior e mover ou criar o card no destino, sem confundir ganho de etapa com pagamento.', text)
        text = re.sub(r'(?m)^- Deal cai no stage de menor.*$', '- Conferir o stage default pela ordem da origin. Se a API aceitar `stage_id` explicito, testar com um stage sintetico pertencente a essa origin e conferir o destino por GET.', text)
        text = re.sub(r'(?m)^- \*\*Status conhecidos:.*$', '- Status de exemplo: `OPEN`, `WON`, `LOST`. Conferir casing, transicoes permitidas e efeitos sobre `won_at`/`lost_at` no contrato da versao usada; nao alegar teste de tenant.', text)
        text = re.sub(r'(?m)^  - Teste reprodut[ií]vel.*$', '  - Teste sintetico: comparar um slug cadastrado e outro inexistente; conferir por GET quais campos persistiram antes de adotar o contrato.', text)
    elif relative.endswith('references/schema.md'):
        text = re.sub(r'(?m)^Estruturas validadas em produ[cç][aã]o.*$', 'Estruturas de exemplo sintetico: preservar nomes e tipos do contrato e conferir o esquema real da versao usada.', text)
        text = re.sub(r'(?m)^Slugs UTM existentes.*$', 'Exemplo sintetico: verificar `utm_source`, `utm_medium`, `utm_content`, `utm_term` e `utm_campaign`. Um typo como `utm_campaing` e apenas um caso de teste de slug legado, nao configuracao presumida.', text)
        text = re.sub(r'(?ms)^## Conven[cç][oõ]es de nomenclatura.*\Z', TAG_MODEL, text)
        text = re.sub(r'(?m)^.*Polling \+ diff.*workflow base.*$', 'Se eventos forem incompletos no teste autorizado, avaliar polling + diff com agenda e limites definidos pelo usuario; nenhum workflow e fornecido como ativo.', text)
    elif relative.endswith('references/troubleshooting.md'):
        text = re.sub(r'(?m)^Workflow base .*$', 'Modelo condicional: se o webhook nao atender ao contrato de entrega, usar polling/diff com intervalo configurado e teste de opt-out; nao presumir workflow existente.', text)
        text = re.sub(r'(?m)^1\. Pra ops em produ[cç][aã]o:.*$', '1. Para uma integracao autorizada, escolher agenda, zona de horario, paginacao e limite de carga; medir o universo e reconciliar totais sem copiar cron ou volumes de outro cliente.', text)
        text = re.sub(r'(?m)^2\. Pra sync menor.*$', '2. Se o caso exigir menor latencia, definir intervalo de polling/diff e validar carga, cotas e entrega no ambiente do usuario.', text)
        text = re.sub(r'\s*\(descoberto na integra[cç][aã]o[^)]*\)', '', text)
        text = re.sub(r'(?m)^1\. Restringir o universo por.*$', '1. Restringir o universo por tag autorizada (`list_contacts_by_tag`) e registrar o denominador medido, sem assumir volume de cliente.', text)
        text = re.sub(r'(?m)^N[aã]o vale varrer os .*$', 'Evitar lookup individual em toda a base: paginar o subconjunto autorizado e comparar email e telefone normalizados, sem inferir identidade a partir de um unico campo.', text)
    elif relative.endswith('jornada-card-pagamento.md'):
        text = re.sub(r'(?s)\A(# [^\n]+\n)\n.*?(?=## )', r'\1\nModelo sintetico de jornada CRM, independente de cliente ou campanha. Exige mapeamento e aprovacao do usuario antes de efeitos externos.\n\n', text)
        text = re.sub(r'(?ms)^Precedente operacional:.*\Z',
                      'Cenario sintetico adicional: criar fixtures de um contato e origens de exemplo, simular eventos repetidos e fora de ordem e conferir identidade unica do card, status, valor e tag. Nenhuma auditoria, metrica ou execucao real e alegada por este documento.\n', text)
    if '<!-- synthetic-client-examples -->' not in text:
        if text.startswith('---\n'):
            end = text.find('\n---', 4) + len('\n---')
            text = text[:end] + '\n\n' + NOTICE + text[end:]
        else:
            first = text.find('\n') + 1
            text = text[:first] + '\n' + NOTICE + text[first:]
    return text


def sanitize_client_examples(root: Path, write: bool, source: Path | None = None) -> None:
    base = root / '.agents/skills'
    changed = 0
    for relative in CLIENT_FILES:
        path = base / relative
        original = path.read_bytes().decode('utf-8-sig')
        text = sanitize_document(relative, original)
        if relative.endswith('scripts/clint_client.py.example'):
            current, values = state_map_literal(text)
            if source is not None:
                origin = source / 'clint-api/scripts/clint_client.py'
                source_text = origin.read_bytes().decode('utf-8-sig')
                source_map, values = state_map_literal(source_text)
                text = text[:current.start(1)] + source_map[1] + text[current.end(1):]
            if values.get('sao paulo', '').lower() != 'sp' or values.get('são paulo', '').lower() != 'sp':
                raise ValueError('readonly-source-required-to-restore-geography')
        if text != original:
            changed += 1
            if write:
                path.write_bytes(text.encode('utf-8'))
    print(f'PASS: scoped synthetic client examples; {changed} content files changed; geography preserved; write={write}')


def audit_client_scope(root: Path) -> tuple[int, list[dict]]:
    base = root / '.agents/skills'
    paths = {p for folder in ('clint-api', 'haos-replicacao-runtimes') for p in (base / folder).rglob('*')
             if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts}
    paths.add(base / 'clint-global/references/jornada-card-pagamento.md')
    rules = {
        'geographic-name-corrupted': r'(?i)s[aã]o[- ]usuario-do-sandbox',
        'private-customer-attribution': r'\b(?i:Clint|Tags|Slugs) do (?!usu[aá]rio|cliente|exemplo)[A-ZÀ-Ý]\w+',
        'private-tenant-model': r'(?i)\btenant\s+(?!de exemplo|do usu[aá]rio)[A-Za-z]+\s+usa\b',
        'private-operational-case': r'(?i)Precedente operacional|Integra[cç][oõ]es j[aá] existentes|auditoria de \d|valida[cç][aã]o cross-session',
        'unsupported-production-evidence': r'(?i)\b(?:validado|validada|confirmado|mapeados)\b[^\n]{0,80}\bprodu[cç][aã]o',
        'private-live-volume': r'(?i)\b(?:full\s+~?\d[\d.,]*k?\s+contatos|\d[\d.,]*\s+leads? importados|\d[\d.,]*\s+tags? em)\b',
    }
    findings = []
    checked = 0
    for path in sorted(paths):
        if re.match(r'^(?:license|notice|copying|copyright)', path.name, re.I):
            continue
        try:
            text = path.read_bytes().decode('utf-8-sig')
        except UnicodeError:
            continue
        checked += 1
        for rule, pattern in rules.items():
            for match in re.finditer(pattern, text):
                findings.append({'file': path.relative_to(root).as_posix(), 'rule': rule,
                                 'line': text.count('\n', 0, match.start()) + 1})
    return checked, findings
