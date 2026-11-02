"""Export owner A's real source skills, sanitizing in memory before any write.

Offline only. Requires an explicit source tree; never reads credentials or runs
imported programs. The source is unchanged. Run without --write to inspect.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from urllib.parse import urlsplit

sys.stdout.reconfigure(encoding='utf-8')

from model_safety import (
    EMAIL, PHONE, LABELED_PHONE, PRODUCTION_ID, LABELED_ID,
    SECRET_PATTERNS, SECRET_ASSIGNMENT, sensitive_rules,
)
from validate_model import frontmatter
from model_links import local_targets, prose

EXCLUDED = {'.git', 'node_modules', '__pycache__', '.cache', '.pytest_cache',
            '.venv', 'venv', 'build', 'dist', 'logs', 'dumps', '.DS_Store'}
TEXT = {'.md', '.txt', '.py', '.ps1', '.sh', '.bash', '.cmd', '.json', '.yaml', '.yml',
        '.toml', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.css', '.html',
        '.sql', '.csv', '.xml', '.ini', '.cfg', '.gitignore', '.rst'}
RESTRICTED = re.compile(r'all rights reserved|todos os direitos reservados|'
                        r'no redistribution|redistribution (?:is )?prohibited|'
                        r'proprietary and confidential|nao redistribuir|'
                        r'n[aã]o (?:pode|permitido) redistribuir', re.I)
LICENSE_FILE = re.compile(r'^(?:licen[cs]e|copying|notice|copyright)(?:[._-]|$)', re.I)
PRIVATE_LINE = re.compile(r'Gian|\bS\d{2,}\b|'
                          r'\b(?:validado|verificado|executado|aprovado) em 202[0-9]|'
                          r'\b(?:historico|histórico|precedente|incidente) (?:real|pessoal)|'
                          r'\b(?:CPF|CNPJ)\s*[:=]|\b(?:ja foi|j[aá] (?:testado|validado|executado)|'
                          r'j[aá] adotada|remotes mortos|estado documentado|saneamento de disco|'
                          r'foi \*\*executado|chave SSH solta|resolvido\]|feito 202\d)', re.I)
PRIVATE_SECTION = re.compile(r'^#{1,6}\s+.*(?:hist[oó]rico|caso real|caso concreto|'
                             r'precedentes?|sess[aã]o de|estado (?:atual|validado)|'
                             r'contexto (?:local|real)|li[cç][oõ]es aprendidas|'
                             r'exemplo real|verificado ao vivo|refer[eê]ncias vivas|'
                             r'estrutura conhecida|integra[cç][aã]o com a dash|'
                             r'pend[eê]ncias conhecidas|perfil (?:real|operacional)|'
                             r'fixos? (?:da|de) (?:opera[cç][aã]o|produ[cç][aã]o))', re.I)
QUOTED_PATH = re.compile(r'([`"\'])(?:[A-Za-z]:[/\\]|/(?:home|root|opt|srv|var/www|mnt|Users)/)[^\n\r`"\']*\1')
ABS_PATH = re.compile(r'(?<![\w])(?:[A-Za-z]:[/\\][^\s`"\'<>|)]+|'
                      r'/(?:home|root|opt|srv|var/www|mnt|Users)/[^\s`"\'<>|)]+)')
URL = re.compile(r'https?://[^\s<>`"\]\)]+')
IP = re.compile(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])')
UUID = re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', re.I)
PRIVATE_HOST = re.compile(r'(?:hausolucoes|edsonburger|simtransforma|mindset|hetzerclaw|'
                          r'edson\.club|osimtransforma|clubedamanifestacao|'
                          r'optimus|hostinger-vps|srv\d{4,}|hstgr\.cloud)', re.I)
PERSONAL = re.compile(r'\b(?:gian_cell_pessoal|optimus-pg|HAOS_Hetzerclaw|'
                      r'Codex_HAOS-Xtreme3|HAOS-Systen-Workspace)\b', re.I)
OPAQUE_ID = re.compile(r'(?<![\w-])[a-zA-Z0-9_-]{20,}(?![\w-])')
PRIVATE_RESOURCES = {'references/p9k-ads-visual-20260925.md',
                     'references/transcricao-voz.md', 'references/oferta.md',
                     'references/perfil-trilha.md'}
REF_PATH = re.compile(r'(?:\.agents/skills|\.codex|scripts|docs|memory|runtime|workspace|'
                      r'references|assets|templates|examples)/[\w./@+ -]+\.(?:md|py|ps1|json|toml|sh|ts|js|yaml|yml|csv|txt)')


def is_link(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & 0x400)


def safe_name(name: str) -> bool:
    return not sensitive_rules(name) and not PRIVATE_HOST.search(name) and not UUID.search(name)


def inventory(root: Path):
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir()):
            rel = path.relative_to(root).as_posix()
            if is_link(path):
                yield path, rel, 'symlink-or-reparse'
            elif path.name in EXCLUDED:
                yield path, rel, 'generated-or-dependency-cache'
            elif not safe_name(rel):
                yield path, 'private-artifact', 'private-artifact-name'
            elif rel in PRIVATE_RESOURCES:
                yield path, rel, 'private-client-copy-or-deployment-profile'
            elif path.is_dir():
                pending.append(path)
            elif not stat.S_ISREG(path.lstat().st_mode):
                yield path, rel, 'nonregular'
            elif path.name.startswith('.env') or path.suffix.lower() in {
                '.env', '.log', '.db', '.sqlite', '.sqlite3', '.dump', '.bak', '.key', '.pem',
                '.p12', '.pfx', '.pyc', '.zip', '.tar', '.gz', '.skill', '.lock',
            }:
                yield path, rel, 'private-or-generated-artifact'
            elif path.stat().st_size > 2_000_000:
                yield path, rel, 'large-artifact-needs-audit'
            elif path.suffix.lower() not in TEXT and not LICENSE_FILE.match(path.name):
                yield path, rel, 'binary-or-unsupported-artifact-needs-audit'
            else:
                yield path, rel, None


def sanitize(text: str, *, notice: bool = False) -> tuple[str, set[str]]:
    if notice:
        # Authorship and license grants are public provenance, not customer PII.
        # The caller must block real secrets; never invent a replacement author.
        return text, set()
    changes: set[str] = set()
    text, count = re.subn(
        r'(?im)^\s*-\s*LocalAPI\s*:.*$',
        '- LocalAPI: usar a fonte local aprovada e configurada pelo usuario; obter identificadores e autenticacao da configuracao local, nunca deste documento, e verificar cobertura antes da consulta.',
        text,
    )
    if count:
        changes.add('local-provider-reference-parameterized')
    def sub(pattern, replacement, value, reason):
        result, count = pattern.subn(replacement, value)
        if count:
            changes.add(reason)
        return result

    if not notice:
        lines = []
        skipping = None
        fenced = False
        for line in text.splitlines():
            if line.lstrip().startswith(('```', '~~~')):
                fenced = not fenced
            heading = re.match(r'^(#{1,6})\s', line) if not fenced else None
            if skipping is not None and heading and len(heading[1]) <= skipping:
                skipping = None
            if heading and PRIVATE_SECTION.search(line):
                skipping = len(heading[1])
                changes.add('private-history-removed')
            if skipping is not None:
                continue
            if PRIVATE_LINE.search(line):
                changes.add('personal-precedent-removed')
                continue
            lines.append(line)
        text = '\n'.join(lines) + '\n'
    text = sub(QUOTED_PATH, lambda m: m[1] + '${HAOS_PRIVATE_ROOT}' + m[1], text, 'private-path-config')
    text = sub(ABS_PATH, '${HAOS_PRIVATE_ROOT}', text, 'private-path-config')
    text = sub(EMAIL, 'contact@example.invalid', text, 'contact-redacted')
    for pattern in SECRET_PATTERNS:
        text = sub(pattern, '${USER_SECRET}', text, 'credential-redacted')
    text = sub(SECRET_ASSIGNMENT, lambda m: m[0].replace(m[1], '${USER_SECRET}'), text, 'credential-config')
    text = sub(PHONE, '${USER_PHONE}', text, 'phone-config')
    text = sub(LABELED_PHONE, lambda m: m[0].replace(m[1], '${USER_PHONE}'), text, 'phone-config')
    text = sub(PRODUCTION_ID, '${RESOURCE_ID}', text, 'production-id-config')
    text = sub(LABELED_ID, lambda m: m[0].replace(m[1], '${RESOURCE_ID}') if re.search(r'\d', m[1]) else m[0], text, 'resource-id-config')
    text = sub(UUID, '${RESOURCE_ID}', text, 'resource-id-config')
    def opaque(m):
        value = m[0]
        if re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', value):
            return value
        if re.search(r'\d', value) and (re.search(r'[a-z]', value) and re.search(r'[A-Z]', value) or re.fullmatch(r'[0-9a-f]{32}', value)):
            changes.add('opaque-id-config')
            return '${RESOURCE_ID}'
        return value
    text = OPAQUE_ID.sub(opaque, text)
    def short_identifier(m):
        value = m[0]
        if re.fullmatch(r'[A-Z][A-Z0-9_]+', value) and '_' in value:
            return value
        if (re.search(r'[A-Z]', value) and re.search(r'\d', value) and len(value) >= 8) or value.startswith('cvt_'):
            changes.add('opaque-id-config')
            return '${RESOURCE_ID}'
        return value
    text = re.sub(r'\b[A-Za-z0-9_]{6,64}\b', short_identifier, text)
    text = sub(re.compile(r'(?<![\w])\d{8,}(?![\w])'), '${RESOURCE_ID}', text, 'long-id-config')
    text = sub(IP, 'example.invalid', text, 'infrastructure-host-config')
    def url(m):
        value = m[0]
        host = urlsplit(value).hostname or ''
        if PRIVATE_HOST.search(value) and host not in {'github.com', 'raw.githubusercontent.com'}:
            changes.add('private-host-config')
            return 'https://service.example.invalid'
        if host == 'github.com' and PRIVATE_HOST.search(value):
            changes.add('private-repository-config')
            return 'https://github.com/example/your-project'
        return value
    text = URL.sub(url, text)
    text = sub(PERSONAL, 'your-private-project', text, 'private-project-config')
    if not notice:
        text = sub(re.compile(r'Edson\s*Burger|EdsonBurger|Editora Mindset|Sociedade Internacional do Mindset|HAU/SIM/EdsonBurger/Editora|\bsim-make\b|\bP9K\b|\bVida\s*369\b', re.I), '${USER_BRAND}', text, 'private-brand-config')
        text = sub(re.compile(r'\b(?:29 workflows|14 credentials|23 chars|RTO ~10 min)\b', re.I), '${USER_INVENTORY}', text, 'private-inventory-config')
        text = sub(re.compile(r'\b(?:1Hwih5|18PJFW)\.{3}'), '${RESOURCE_ID}', text, 'private-id-prefix-config')
    text = sub(re.compile(r'\b(?:[\w-]+\.)*(?:hausolucoes\.com\.br|edsonburger\.[a-z.]+|hstgr\.cloud)\b', re.I), 'service.example.invalid', text, 'private-host-config')
    text = sub(re.compile(r'\b(?:[\w-]+\.)*(?:edson\.club|osimtransforma\.com\.br)\b', re.I), 'service.example.invalid', text, 'private-host-config')
    return text, changes


def clean_json(raw: str):
    changes = set()
    def visit(value):
        if isinstance(value, dict):
            output = {}
            for key, item in value.items():
                new_key, changed = sanitize(key)
                changes.update(changed)
                new_key = new_key.rstrip('\n')
                if new_key in output:
                    raise ValueError('sanitized-json-key-collision')
                output[new_key] = visit(item)
            return output
        if isinstance(value, list):
            return [visit(item) for item in value]
        if isinstance(value, str):
            clean, changed = sanitize(value)
            changes.update(changed)
            return clean.rstrip('\n')
        if isinstance(value, int) and abs(value) >= 10_000_000:
            changes.add('numeric-resource-config')
            return '${RESOURCE_ID}'
        return value
    return json.dumps(visit(json.loads(raw)), ensure_ascii=False, indent=2) + '\n', changes


CLINT_EXAMPLE = '''# Exemplo parametrizavel: Assiny e Lia no mesmo funil

Este exemplo preserva o mapeamento operacional entre eventos e cards, sem IDs,
produtos, nomes de clientes, prefixos de IDs ou configuracao de tenant reais.
Resolver todos os parametros no ambiente do usuario antes de qualquer escrita.

## Grupo, suborigens e stages

No modelo origin + stage, selecionar um grupo `${CLINT_GROUP_NAME}` e resolver
as suborigens por `GET /origins` ou pelo painel. Nao assumir um pipeline ID.
Cada suborigem pode ter uma coluna por plataforma; conferir os stages de ambas.

| Suborigem | Parametro de origin_id |
|---|---|
| Carrinho Abandonado | `${ORIGIN_ABANDONED}` |
| Gerou Pagamento | `${ORIGIN_PAYMENT_CREATED}` |
| Compra Negada | `${ORIGIN_REFUSED}` |
| Compra Aprovada | `${ORIGIN_APPROVED}` |

A tag de pagamento `${PAID_TAG_ID}` pertence ao produto, nao a plataforma.
Aplicar somente em evento aprovado confirmado. Match por email normalizado.

## Assiny: eventos para suborigem

| Evento | Suborigem |
|---|---|
| `abandoned_purchase` / `abandoned_checkout` | Carrinho Abandonado |
| `pix_generated` / `bank_slip_generated` | Gerou Pagamento |
| `refused` | Compra Negada |
| `approved_purchase` | Compra Aprovada, com tag |

Filtrar `${TARGET_PRODUCT_ID}` antes da branch de upsert. Prefixar a origem UTM
com `${ASSINY_UTM_PREFIX}` configurado pelo usuario, sem substituir UTM existente.
Gerou/Negada da ganho no card anterior de Carrinho; Aprovada da ganho nos cards
anteriores de Carrinho, Gerou e Negada, sempre filtrando pelo origin_id correto.

Nao inventar endereco em checkout digital: `client.address` pode estar ausente.
Documentar os campos disponiveis, sem registrar CPF, IP ou payload de comprador.
Operacoes paralelas anteriores ao CRM nao devem abortar silenciosamente o upsert:
revisar ordem dos nodes, tratamento onError e evidencia de cada efeito.

## Lia: produtos, eventos e stages

Filtrar `data.offer.product.id` por uma allowlist local de produtos-alvo.
Excluir o produto generico de parcela: parcela paga nao e nova compra do produto.
Resolver `${LIA_STAGE_PENDING}`, `${LIA_STAGE_APPROVED}` e `${LIA_STAGE_REFUSED}`
nas colunas Lia das respectivas suborigens; nunca usar um prefixo truncado como ID.

| Status | Suborigem | Stage |
|---|---|---|
| `pending` / `waiting_payment` | Gerou Pagamento | `${LIA_STAGE_PENDING}` |
| `paid` / `finished` / `active` | Compra Aprovada | `${LIA_STAGE_APPROVED}`, com tag |
| `canceled` / `overdue` | Compra Negada | `${LIA_STAGE_REFUSED}` |
| Sem fonte de abandono | Carrinho Abandonado | Recebe somente ganho |

Conferir disponibilidade real dos eventos antes de criar webhooks aditivos:
Order(finished,canceled), Billing(waiting_payment,active,finished,canceled) e
Bill(paid,pending,overdue,canceled). URL e workflows sao configuracao do usuario.

Doc/endereco/UTM podem vir somente em `order`; `bill`/`billing` podem estar vazios.
O MERGE deve preencher com o order posterior sem apagar valores existentes.
Prefixar `data.metadata.utm_source`, se presente, com `${LIA_UTM_PREFIX}`.

## Upsert e verificacao cruzada

Ambas as plataformas usam o mesmo grupo, com seus proprios stages. Um lead que
abandona numa e paga na outra deve ter o card movido/ganho, nao duplicado.
Conferir o resultado por leitura do card, origin_id, stage_id e tags depois do
evento controlado. Aceite de webhook nao comprova a mutacao final no CRM.
Nao executar disparos nem escrita de producao sem autorizacao aplicavel.
'''


def metadata(text: str, folder: str) -> tuple[str, str, str]:
    try:
        data = frontmatter(text)
        original_name = data['name']
        desc = data['description']
    except ValueError:
        match = re.search(r'^name:\s*(.+)$', text, re.M)
        original_name = match[1].strip(' "\'') if match else folder
        match = re.search(r'^description:\s*(.+)$', text, re.M)
        desc = match[1].strip(' "\'') if match and match[1] not in {'|', '>'} else 'Procedimento especializado de ' + folder + '; consultar requisitos e evidencias antes de executar.'
    lines = text.splitlines()
    if lines and lines[0].strip() == '---':
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == '---'), None)
        body = '\n'.join(lines[end + 1:]) if end is not None else text
    else:
        body = text
    header = '---\nname: ' + folder + '\ndescription: ' + json.dumps(desc, ensure_ascii=False) + '\n---\n'
    return header + '\n' + body.strip() + '\n', original_name, desc


def dependencies(text: str, root: Path, target_root: Path):
    found = set()
    for m in REF_PATH.finditer(text):
        found.add(m[0].strip())
    links, _ = local_targets(prose(text))
    for link in links:
        if not urlsplit(link).scheme and link and not link.startswith('#'):
            found.add(link.split('#')[0])
    output = []
    for name in sorted(found):
        if not safe_name(name):
            name = '${USER_PRIVATE_ARTIFACT}'
        path = root / name
        repo_path = target_root / name
        supplied = repo_path.is_file()
        output.append({'reference': name, 'status': 'public-present' if supplied else 'missing',
                       'required': not supplied,
                       'contract': 'Provide and review this dependency in your own environment before dependent commands; not bundled or verified here.' if not supplied else 'Verify exported relative path before use.'})
    for var in sorted(set(re.findall(r'\$\{([A-Z_]+)\}', text))):
        output.append({'reference': var, 'status': 'user-config-required', 'required': True,
                       'contract': 'Set locally outside the public repository; never put secrets or production identifiers in examples.'})
    return output


def repair_links(text: str, rel: str, exported: set[str], repo: Path, deps: list[dict]) -> str:
    base = Path(rel).parent
    def available(target):
        if target.startswith(('#', 'http:', 'https:', 'mailto:', 'tel:')):
            return True
        if re.match(r'^[a-zA-Z]:|^[/~]|\$\{', target):
            return False
        normalized = os.path.normpath(str(base / target.split('#')[0])).replace('\\', '/')
        return normalized in exported or (repo / normalized).exists()
    def inline(m):
        label, target = m.groups()
        return m[0] if available(target) else label + ' (dependency not bundled: ' + target + ')'
    text = re.sub(r'\[([^\]\n]+)\]\(([^)\n]+)\)', inline, text)
    def code(m):
        value = m[1]
        if re.match(r'^(?:\.agents|\.codex|docs|scripts|tests|playbooks|hooks|memory)/', value):
            if not (repo / value).exists() and not any(c in value for c in '*<> {}\n'):
                return '`' + '${USER_PROJECT_ROOT}/' + value + '`'
        return m[0]
    return re.sub(r'(?<!`)`([^`\n]+)`(?!`)', code, text)


def run(args):
    source = args.source.resolve()
    target = Path(__file__).resolve().parent.parent
    if source == target or is_link(source) or not source.is_dir():
        raise SystemExit('invalid-source')
    folders = sorted((p for p in source.iterdir() if p.is_dir() and not is_link(p) and (p / 'SKILL.md').is_file()), key=lambda p: p.name)
    group = [p for p in folders if p.name <= 'incorporador']
    if len(group) != 97 or group[0].name != 'ab-testing' or group[-1].name != 'incorporador':
        raise SystemExit('owner-boundary-mismatch')
    manifest = []
    old_manifest = target / 'docs/exports/group-a.json'
    previous_exports = {e['source_folder']: e for e in json.loads(old_manifest.read_text(encoding='utf-8'))} if old_manifest.exists() else {}
    for directory in group:
        folder = directory.name
        skill_raw = (directory / 'SKILL.md').read_bytes()
        original = skill_raw.decode('utf-8-sig')
        skill_text, alias, _ = metadata(original, folder)
        payloads = {}
        file_list = []
        omitted = []
        changes = set()
        license_info = {'status': 'unknown-provenance-not-license-audited', 'notices': [],
                        'note': 'Source supplied for publication by the owner; upstream rights not independently audited. No MIT relicensing of imported material.'}
        declaration = re.search(r'^license:\s*([^\n]+)', original, re.M)
        if declaration:
            license_info['source_declaration'] = declaration[1].strip()
            license_info['status'] = 'source-declared-license-not-independently-audited'
        for path, rel, reason in inventory(directory):
            if reason:
                omitted.append({'source_rel': folder + '/' + rel, 'reason': reason})
                continue
            data = path.read_bytes()
            try:
                raw = data.decode('utf-16') if data.startswith((b'\xff\xfe', b'\xfe\xff')) else data.decode('utf-8-sig')
            except UnicodeError:
                try:
                    raw = data.decode('cp1252')
                except UnicodeError:
                    omitted.append({'source_rel': folder + '/' + rel, 'reason': 'binary-or-encoding-needs-audit'})
                    continue
            if '\x00' in raw:
                omitted.append({'source_rel': folder + '/' + rel, 'reason': 'binary-artifact-needs-audit'})
                continue
            notice = bool(LICENSE_FILE.match(path.name))
            if notice:
                license_info['notices'].append(rel)
                license_info['status'] = 'original-notice-preserved-not-independently-audited'
            restrictive = RESTRICTED.search(raw)
            permissive = re.search(r'Permission is hereby granted|Apache License|Licensed under the MIT|SPDX-License-Identifier: (?:MIT|Apache)', raw, re.I)
            if restrictive and not (permissive and restrictive[0].lower() in {'all rights reserved', 'todos os direitos reservados'}):
                omitted.append({'source_rel': folder + '/' + rel, 'reason': 'explicit-rights-restriction-requires-clearance'})
                continue
            if rel == 'SKILL.md':
                raw = skill_text
            if folder == 'clint-funnel-playbook' and rel == 'references/example-ids.md':
                raw = CLINT_EXAMPLE
                changes.add('private-case-replaced-with-parameterized-domain-example')
            try:
                clean, changed = clean_json(raw) if path.suffix.lower() == '.json' else sanitize(raw, notice=notice)
            except ValueError:
                omitted.append({'source_rel': folder + '/' + rel, 'reason': 'invalid-source-json-or-key-collision'})
                continue
            safety = sensitive_rules(clean) - ({'personal-email'} if notice else set())
            if safety:
                omitted.append({'source_rel': folder + '/' + rel, 'reason': 'unresolved-sensitive-content', 'rules': sorted(sensitive_rules(clean))})
                continue
            changes.update(changed)
            if rel == 'SKILL.md':
                clean, _, _ = metadata(clean, folder)
            # A syntax-valid program can still have altered semantics. Never
            # represent configuration-redacted programs as runnable helpers.
            if path.suffix.lower() in {'.py', '.ps1', '.sh', '.bash', '.cmd', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx'} and changed:
                rel += '.example'
            elif path.suffix.lower() == '.py':
                try:
                    ast.parse(clean)
                except SyntaxError:
                    rel += '.example'
                    changes.add('nonrunnable-source-example')
            payloads[rel] = clean
        deps = dependencies(original, directory, target)
        for rel, value in payloads.items():
            for dep in dependencies(value, directory, target):
                if dep not in deps:
                    deps.append(dep)
        deps = [{**d, 'reference': sanitize(d['reference'])[0].strip()} for d in deps]
        for dep in deps:
            ref = dep['reference']
            if ref in payloads or (target / ref).is_file() or (target / '.agents/skills' / folder / ref).is_file():
                dep['status'] = 'bundled' if ref in payloads else 'public-present'
                dep['required'] = False
                dep['contract'] = 'File present in the exported package; static presence is not execution verification.'
            elif dep['status'] != 'user-config-required':
                dep['required'] = True
                dep['status'] = 'missing'
                dep['contract'] = 'Not bundled. Supply and review this dependency locally before dependent commands; source presence does not count as delivery.'
        for rel in payloads:
            if rel.endswith('.example'):
                deps.append({'reference': rel[:-8], 'status': 'nonrunnable-example', 'required': True,
                             'example_path': '.agents/skills/' + folder + '/' + rel,
                             'contract': 'Only a sanitized .example is delivered. Review configuration and semantics, restore valid syntax, test in isolation and obtain authorization before use. Not a working helper.'})
        all_exported = set(payloads)
        for rel in list(payloads):
            payloads[rel] = repair_links(payloads[rel], rel, all_exported, target, deps)
        destination = target / '.agents/skills' / folder
        collision = (destination / 'SKILL.md').exists() and (folder not in previous_exports or 'public-core-preserved' in previous_exports[folder]['sanitization'])
        # Existing public core is authoritative. Import detail as a real reference,
        # never replace its gates, opt-outs, closure or environment envelope.
        if collision and 'SKILL.md' in payloads:
            previous = (destination / 'SKILL.md').read_text(encoding='utf-8-sig')
            marker = '\n## Material portavel da origem (lote A)\n'
            if marker not in previous:
                payloads['references/source-procedure.md'] = payloads.pop('SKILL.md')
                payloads['SKILL.md'] = previous.rstrip() + marker + '\nConsultar [procedimento de origem](references/source-procedure.md), adaptado sem dados privados.\nO nucleo publico acima prevalece em gates, opt-outs, fechamento e ferramentas.\nConsultar [contrato de dependencias](EXPORT_DEPENDENCIES.md) antes de comandos dependentes.\n'
                changes.add('public-core-preserved')
            else:
                # Idempotent re-export keeps the public core, replacing only the
                # source detail and preserving its original relative references.
                payloads['references/source-procedure.md'] = payloads.pop('SKILL.md')
                payloads['SKILL.md'] = previous
                changes.add('public-core-preserved')
        if collision and 'references/source-procedure.md' in payloads:
            value = payloads['references/source-procedure.md']
            for ref in payloads:
                if ref.startswith('references/') and ref != 'references/source-procedure.md':
                    value = value.replace('](' + ref + ')', '](' + ref.removeprefix('references/') + ')')
            payloads['references/source-procedure.md'] = value
        status = 'adapted_private_config' if changes or omitted or any(d['required'] for d in deps) else 'ported_full'
        if 'SKILL.md' not in payloads:
            status = 'blocked'
        reason = 'Real source procedure and available resources ported; no imported code executed.'
        if status == 'blocked':
            reason = 'Source entry point blocked by explicit rights or unresolved privacy; see blocking artifacts.'
        contract = '# Portability, dependencies and provenance\n\nThis is a sanitized source port, not proof that integrations work in your environment.\nNo credentials, production resources, infrastructure configuration or historical cases are supplied.\nImported material is not relicensed by the public repository license. Preserve original author and license notices.\n\nFiles ending in .example are NONRUNNABLE SOURCE EXAMPLES: sanitization may change syntax and semantics. Do not rename and run blindly. Commands copied from the procedure that refer to missing helpers are not ready to execute.\n\n'
        contract += '## Required Setup\n\nConfigure endpoints, credentials and resource identifiers locally. Confirm tool availability and obtain authorization before external effects. Do not execute an unresolved command. Missing files are dependencies, not installed features.\n\n'
        contract += '\n'.join('- Dependency ' + d['reference'] + ' -> ' + d['status'] + '. ' + d['contract'] for d in deps) + '\n\n'
        contract += '## Omitted Artifacts\n\n' + ('\n'.join('- ' + o['source_rel'].split('/', 1)[1] + ': ' + o['reason'] for o in omitted) or 'None.') + '\n'
        if status != 'blocked':
            payloads['EXPORT_DEPENDENCIES.md'] = contract
            if 'Material portavel da origem (lote A)' not in payloads['SKILL.md']:
                payloads['SKILL.md'] += '\n## Portabilidade\n\nConsultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.\n'
        for rel, clean in sorted(payloads.items()):
            safety = sensitive_rules(clean) - ({'personal-email'} if LICENSE_FILE.match(Path(rel).name) else set())
            if safety or sensitive_rules(rel):
                raise SystemExit('post-sanitization-safety-failure: ' + folder + '/' + rel + ' ' + ','.join(sorted(sensitive_rules(clean) | sensitive_rules(rel))))
            full_path = '.agents/skills/' + folder + '/' + rel
            file_list.append(full_path)
            if args.write and status != 'blocked':
                out = destination / rel
                if not out.resolve().is_relative_to(destination.resolve()) or any(is_link(p) for p in out.parents if p.exists() and p.is_relative_to(target)):
                    raise SystemExit('unsafe-target')
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(clean, encoding='utf-8', newline='\n')
        entry = {'source_folder': folder, 'target_path': '.agents/skills/' + folder,
                 'status': status, 'files': file_list if status != 'blocked' else [],
                 'dependencies': deps, 'license': license_info,
                 'sha256original': hashlib.sha256(skill_raw).hexdigest(),
                 'source_rel': folder + '/SKILL.md', 'original_name': sanitize(alias)[0].strip(),
                 'reason': reason, 'sanitization': sorted(changes), 'blocking_missing_refs': [d for d in deps if d['required']],
                 'file_licenses': {'.agents/skills/' + folder + '/' + p: {'status': license_info['status'], 'notices': license_info['notices']} for p in payloads},
                 'omitted_artifacts': omitted}
        manifest.append(entry)
        if args.preview and (args.preview == '*' or folder in args.preview.split(',')):
            print('=== ' + folder + ' ===')
            print(payloads.get('references/source-procedure.md', payloads.get('SKILL.md', 'BLOCKED')))
        if args.inventory:
            print(json.dumps({'folder': folder, 'files': sorted(payloads), 'omitted': omitted,
                              'status': status, 'license': license_info, 'changes': sorted(changes)}, ensure_ascii=True))
    if args.write:
        output = target / 'docs/exports/group-a.json'
        data = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
        if sensitive_rules(data):
            raise SystemExit('unsafe-manifest')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(data, encoding='utf-8', newline='\n')
    print(json.dumps({'owner': 'A', 'skills': len(manifest), 'status': dict(Counter(e['status'] for e in manifest)),
                      'files': sum(len(e['files']) for e in manifest), 'written': args.write}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--preview')
    run(parser.parse_args())
