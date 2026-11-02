"""Offline, fail-closed export of the 96 real skills in owner B's name range.

Read private inputs only in memory. Never stage raw inputs, follow links, fetch
dependencies, execute imported code, or write outside the explicitly owned paths.
This exporter is not a runtime installer or a license audit.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
import os
import posixpath
from pathlib import Path
import re
import stat
import sys
from urllib.parse import unquote, urlsplit

from model_safety import (
    EMAIL, LABELED_ID, LABELED_PHONE, PHONE, PRODUCTION_ID,
    SECRET_ASSIGNMENT, SECRET_PATTERNS, sensitive_rules,
)
from validate_model import frontmatter


SKIP_DIRS = {
    '.git', 'node_modules', '__pycache__', '.cache', '.pytest_cache',
    '.mypy_cache', '.ruff_cache', '.venv', 'venv', 'dist', 'build',
    'logs', 'dumps', 'thumbnails', '.next', '.turbo', 'coverage',
}
TEXT_SUFFIXES = {
    '.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.py', '.js',
    '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.html', '.css', '.xml',
    '.sh', '.ps1', '.cmd', '.bat', '.csv', '.ini', '.cfg', '.sql',
}
RESTRICTIVE = re.compile(
    r'nenhuma\s+parte\s+deste\s+livro|todos\s+os\s+direitos.{0,60}reservados|'
    r'no\s+redistribution|redistribution\s+(?:is\s+)?prohibited|'
    r'not\s+for\s+redistribution|all\s+rights\s+reserved', re.I | re.S,
)
URL = re.compile(r'https?://[^\s<>`"\'\]\)]+')
UUID = re.compile(r'(?<![0-9a-f])[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}(?![0-9a-f])', re.I)
IP = re.compile(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])')
PRIVATE_WINDOWS = re.compile(
    r'(?i)(?<![\w+.-])(?:[a-z]:[/\\]+|\\\\[\w.-]+\\)[^\n`"\'<>|]*'
)
PRIVATE_UNIX = re.compile(r'(?:/root/|/home/|/opt/|/srv/|/var/www/)[^\s`"\'<>|;]+')
MENTION = re.compile(r'(?<![\w.+-])@[a-zA-Z][\w.-]{2,}')
CHANNEL = re.compile(r'\bUC[A-Za-z0-9_-]{22}\b')
IDENTIFIER_FIELD = re.compile(
    r'(?:prod(?:uction)?|account|campaign|pixel|waba|phone_number|business|tenant|'
    r'project|workflow|product|offer|shop|channel|board|customer|contact)[_ -]?id\Z|'
    r'(?:phone|telefone|celular|cpf|cnpj|customer_document|cpf_cnpj)\Z', re.I,
)
QUOTED_IDENTIFIER = re.compile(
    r'\b(?:account|campaign|pixel|waba|business|tenant|project|workflow|product|'
    r'offer|shop|channel|board|customer|contact)[_ -]?id\s*(?:==|!=|:|=)\s*[`\"\']([a-z0-9_-]{6,})', re.I,
)
CONTEXTUAL_NUMBER = re.compile(
    r'\b(?:pixel|account|campaign|waba|business|tenant|project|workflow|produto|'
    r'product|offer|shop|channel|canal|board)(?:[_ -]?id)?(?:\s+(?:Meta|GA4|ID))?'
    r'\s*[:=]?\s*[`\"\'( ]{1,4}(\d{8,})', re.I,
)
FILE_REF = re.compile(
    r'(?<![\w/])(?:[\w.-]+/)*[\w.-]+\.(?:py|ps1|sh|mjs|js|json|yaml|yml|md|xlsx|csv|png|pdf)\b'
)
PUBLIC_DOMAINS = {
    'example.com', 'example.net', 'example.org', 'example.invalid',
    'github.com', 'raw.githubusercontent.com', 'githubusercontent.com',
    'apache.org', 'opensource.org', 'choosealicense.com', 'spdx.org',
    'openai.com', 'anthropic.com', 'claude.ai', 'google.com', 'googleapis.com',
    'gstatic.com', 'microsoft.com', 'python.org', 'pypi.org', 'npmjs.com',
    'nodejs.org', 'react.dev', 'reactjs.org', 'nextjs.org', 'vercel.com',
    'vercel.app', 'svelte.dev', 'sveltekit.io', 'nuxt.com', 'astro.build',
    'supabase.com', 'supabase.co', 'obsidian.md', 'jsoncanvas.org',
    'n8n.io', 'mautic.org', 'docs.mautic.org', 'facebook.com', 'meta.com',
    'instagram.com', 'tiktok.com', 'tiktokshop.com', 'youtube.com',
    'youtu.be', 'linkedin.com', 'x.com', 'twitter.com', 'reddit.com',
    'x.ai', 'miro.com', 'lovable.dev', 'clint.digital', 'lia.com.br',
    'curseduca.com', 'yampi.com.br', 'hostinger.com', 'hetzner.com',
    'cloudflare.com', 'docker.com', 'wordpress.org', 'w3.org', 'wikipedia.org',
    'developer.mozilla.org', 'mozilla.org', 'web.dev', 'tailwindcss.com',
    'vitest.dev', 'jestjs.io', 'testing-library.com', 'playwright.dev',
    'ffmpeg.org', 'pymupdf.readthedocs.io', 'pymupdf.io', 'fonts.googleapis.com',
    'fonts.google.com', 'fontshare.com', 'unpkg.com', 'jsdelivr.net',
    'scrapecreators.com', 'scrapecreators.org', 'scrapecreators.app',
    'shopify.com', 'stripe.com', 'paddle.com', 'hubspot.com', 'mailchimp.com',
    'zapier.com', 'canva.com', 'figma.com', 'unsplash.com', 'pexels.com',
    'notion.com', 'turborepo.dev',
    'dribbble.com', 'behance.net', 'awwwards.com', 'producthunt.com',
}
PRIVATE_BRAND = re.compile(
    r'\b(?:Gian(?:s)?|Edson(?:\s+Burger)?|Paulo|Loriane|PowerMind|P9K|'
    r'Vida\s*369|Clube\s+da\s+Manifesta[cç][aã]o|Protocolo\s+G[eê]nesis)\b', re.I,
)
PRIVATE_DOMAIN_WORD = re.compile(
    r'(?i)\b[\w.-]*(?:simtransforma|hausolucoes|edsonburger|gian)[\w.-]*\.[a-z]{2,}(?:\.[a-z]{2,})?\b'
)
RESOURCE_BINDINGS: dict[str, str] = {}


def linked(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & 0x400)


def safe_rel(value: str) -> str:
    if sensitive_rules(value) or '..' in Path(value).parts or not re.fullmatch(r'[\w./ -]+', value):
        return 'withheld-artifact-' + hashlib.sha256(value.encode()).hexdigest()[:12]
    return value


def walk(root: Path):
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir()):
            rel = path.relative_to(root).as_posix()
            if linked(path):
                yield path, rel, 'symlink-or-reparse-point'
            elif path.is_dir():
                if path.name.lower() in SKIP_DIRS:
                    yield path, rel, 'generated-or-runtime-directory'
                else:
                    pending.append(path)
            else:
                yield path, rel, None


def remove_sections(text: str, patterns: list[str]) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    out = []
    skip_level = None
    removed = 0
    for line in lines:
        heading = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading and skip_level is not None and len(heading[1]) <= skip_level:
            skip_level = None
        if heading and any(re.search(p, heading[2], re.I) for p in patterns):
            skip_level = len(heading[1])
            removed += 1
        if skip_level is None:
            out.append(line)
    return ''.join(out), removed


def sanitize(text: str, *, code: bool = False) -> tuple[str, list[str]]:
    original = text
    changes = []

    def sub(pattern, replacement, label):
        nonlocal text
        text, count = re.subn(pattern, replacement, text)
        if count:
            changes.append(label)

    for pattern in SECRET_PATTERNS:
        sub(pattern, 'secret_placeholder', 'credential-pattern-removed')
    def secret_assignment(m):
        start = m.start(1) - m.start(0)
        if code and m[0][start - 1:start] not in ('\"', "'") and re.fullmatch(r'[A-Za-z_]\w*(?:\.\w+)*', m[1]):
            # Parenthesize dynamic expressions, preserving semantics instead of
            # replacing a variable/environment lookup with a fake credential.
            return m[0][:start] + '(' + m[1] + ')' + m[0][start + len(m[1]):]
        return m[0][:start] + 'secret_placeholder' + m[0][start + len(m[1]):]
    sub(SECRET_ASSIGNMENT, secret_assignment, 'credential-values-parameterized')
    sub(EMAIL, lambda m: 'user-' + resource_binding(m[0]).removeprefix('${USER_RESOURCE_').removesuffix('}') + '@account.example.invalid', 'contacts-parameterized')
    sub(PHONE, lambda m: resource_binding(m[0]), 'contacts-parameterized')
    sub(LABELED_PHONE, lambda m: m[0].replace(m[1], resource_binding(m[1])), 'contacts-parameterized')
    sub(PRODUCTION_ID, lambda m: resource_binding(m[0]), 'production-ids-parameterized')
    def labeled_identifier(m):
        start = m.start(1) - m.start(0)
        if code and m[0][start - 1:start] not in ('\"', "'") and re.fullmatch(r'[A-Za-z_]\w*(?:\.\w+)*', m[1]):
            replacement = '(' + m[1] + ')'
        elif re.search(r'\d', m[1]):
            replacement = resource_binding(m[1])
        else:
            return m[0]
        return m[0][:start] + replacement + m[0][start + len(m[1]):]
    sub(LABELED_ID, labeled_identifier, 'production-ids-parameterized')
    sub(UUID, lambda m: m[0] if set(m[0]) <= {'0', '-'} else resource_binding(m[0]), 'installation-ids-parameterized')
    sub(CHANNEL, lambda m: resource_binding(m[0]), 'channel-ids-parameterized')
    sub(PRIVATE_WINDOWS, lambda m: m[0] if code and any(c in m[0] for c in '*?[]{}') else '${USER_WORKSPACE_ROOT}', 'private-paths-parameterized')
    sub(PRIVATE_UNIX, '${USER_SERVICE_ROOT}/resource', 'private-paths-parameterized')
    sub(r'~/(?:\.claude|\.codex)/skills/[^/\s`"\']+/', './', 'skill-paths-localized')
    sub(r'~/(?:\.claude|\.codex)/[^\s`"\']+', '${USER_PROFILE_ROOT}/resource', 'profile-paths-parameterized')
    sub(IP, lambda m: m[0] if m[0] in ('127.0.0.1', '0.0.0.0') else '192.0.2.1', 'network-addresses-parameterized')
    sub(PRIVATE_DOMAIN_WORD, 'service.example.invalid', 'private-hosts-parameterized')

    def url(match):
        value = match[0]
        # Reddit's public helper uses f"https://www.reddit.com{path}.json".
        # urlsplit treats {path} as part of the hostname; it is a path expression,
        # not a tenant or a literal private host. Preserve this known API idiom.
        if code and re.match(r'https?://(?:www\.)?reddit\.com\{', value):
            return value
        try:
            parsed = urlsplit(value)
            host = (parsed.hostname or '').lower()
        except ValueError:
            changes.append('service-urls-parameterized')
            return 'https://service.example.invalid'
        if host in ('localhost', '127.0.0.1', '0.0.0.0'):
            return value
        if host == 'github.com' and re.match(r'/(?:simtransforma|[^/]+/HAOS)[/\w-]*', parsed.path, re.I):
            changes.append('private-repository-parameterized')
            return 'https://github.com/example/private-adapter'
        if host in ('youtu.be', 'studio.youtube.com', 'drive.google.com', 'docs.google.com') or (
            host.endswith('youtube.com') and re.search(r'/(?:watch|channel|live|shorts)', parsed.path)
        ):
            changes.append('private-media-parameterized')
            return 'https://media.example.invalid/user-asset'
        if host.endswith(('vercel.app', 'supabase.co', 'lovable.app')):
            changes.append('tenant-hosts-parameterized')
            return 'https://service.example.invalid'
        if not any(host == d or host.endswith('.' + d) for d in PUBLIC_DOMAINS):
            changes.append('service-urls-parameterized')
            return 'https://service.example.invalid'
        if parsed.query and re.search(r'(?:token|key|secret|signature|credential|auth|nonce)=', parsed.query, re.I):
            changes.append('url-credentials-removed')
            return value.split('?', 1)[0]
        return value

    sub(URL, url, 'url-review')
    # Magnitude alone never identifies private data: limits, timestamps and math
    # must survive. Only explicitly identified resources are parameterized.
    sub(CONTEXTUAL_NUMBER, lambda m: m[0].replace(m[1], resource_binding(m[1])), 'contextual-identifiers-parameterized')
    sub(QUOTED_IDENTIFIER, lambda m: m[0][:(m.start(1)-m.start(0))] + resource_binding(m[1]) if re.search(r'\d', m[1]) else m[0], 'quoted-resource-identifiers-parameterized')
    if not code:
        sub(r'(?i)@(?:cortes[\w.-]*|[\w.-]*(?:edsonburger|simtransforma|hausolucoes|gian)[\w.-]*)', '@example', 'handles-parameterized')
        sub(PRIVATE_BRAND, 'usuario', 'private-names-parameterized')
        sub(r'\bMASTER\.env\b', '${USER_SECRET_FILE}', 'secret-source-configurable')
        sub(r'(?i)\b(?:tag\s+)?id\s+`?(\d+)`?', lambda m: m[0].replace(m[1], resource_binding(m[1])), 'small-resource-ids-parameterized')
        sub(r'(?i)\bproduto\s+GEN[EÉ]RICO\s+[`\"\']([a-f0-9-]{8,})', lambda m: m[0].replace(m[1], resource_binding(m[1])), 'product-identifiers-parameterized')
        sub(r'(?i)\bproject_[a-z0-9_]+\b', '<USER_PROJECT_CONTEXT>', 'private-memory-pointers-removed')
        sub(r'R\$\s*[\d.,]+\s*[kKmM]?', 'R$ <USER_AMOUNT>', 'private-amounts-parameterized')
        sub(r'SUPABASE_BIGDATA_SIM_[A-Z_]+', 'SUPABASE_DATABASE_URL', 'database-config-parameterized')
        sub(r'(?i)Caso real:[^\n]*', 'Validar pagamento confirmado, status e proveniencia antes de reconhecer valores.', 'personal-incident-removed')
        sub(r'(?i)INTERNA, cont[^\n]*HAOS_CC\.', 'Edicao publica: contas, catalogos e destinos devem ser fornecidos pelo usuario.', 'private-classification-updated')
        sub(r'(?i)zero produtos com pre[cç]o de custo cadastrado no Bling', 'cadastro de custos a verificar no catalogo do usuario', 'private-catalog-state-removed')
        sub(r'(?i)\(cerca de \d+% da receita\)', '(participacao a medir)', 'private-revenue-share-removed')
        sub(r'(?i)j[aá] reconciliado', 'a reconciliar com evidencia atual', 'live-state-claim-removed')
    # Keep only changes that actually altered the input, not a URL scan with no edits.
    return text, sorted(set(changes)) if text != original else []


def resource_binding(value: str) -> str:
    # Synthetic names are stable across repeated references but contain no raw
    # identifier. Each distinct resource remains a separate user configuration.
    value = str(value)
    if UUID.fullmatch(value):
        value = value.lower()
    if value not in RESOURCE_BINDINGS:
        # Do not expose hashes of low-entropy contacts or identifiers. Stable
        # sorted traversal supplies opaque ordinal bindings; reverse map stays
        # exclusively in memory and is never emitted.
        RESOURCE_BINDINGS[value] = '${USER_RESOURCE_' + str(len(RESOURCE_BINDINGS) + 1).zfill(6) + '}'
    return RESOURCE_BINDINGS[value]


def json_sanitize(value, field: str = ''):
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            clean_key = sanitize(str(key))[0]
            if clean_key in result:
                raise ValueError('sanitized-json-key-collision')
            result[clean_key] = json_sanitize(item, str(key))
        return result
    if isinstance(value, list):
        return [json_sanitize(v, field) for v in value]
    if isinstance(value, str):
        if IDENTIFIER_FIELD.fullmatch(field) and re.search(r'\d', value) and not value.startswith(('${', '<')):
            return resource_binding(value)
        return sanitize(value)[0]
    if type(value) is int and IDENTIFIER_FIELD.fullmatch(field):
        return resource_binding(str(value))
    return value


def unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('source-json-duplicate-key')
        result[key] = value
    return result


def code_structure(text):
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            node.value = '<literal:' + type(node.value).__name__ + '>'
    return ast.dump(tree, include_attributes=False)


def guard_template(text: str, suffix: str) -> str:
    message = 'requires_user_config: render placeholders, review bindings and remove this guard only after local validation'
    lines = text.splitlines(keepends=True)
    if suffix == '.py':
        tree = ast.parse(text)
        offset = 0
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                offset = node.end_lineno
            elif isinstance(node, ast.ImportFrom) and node.module == '__future__':
                offset = node.end_lineno
            else:
                break
        guard = '\nraise RuntimeError(' + repr(message) + ')\n\n'
    elif suffix in {'.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx'}:
        offset = 1 if lines and lines[0].startswith('#!') else 0
        guard = '\nthrow new Error(' + json.dumps(message) + ');\n\n'
    elif suffix == '.sh':
        offset = 1 if lines and lines[0].startswith('#!') else 0
        guard = "\nprintf '%s\\n' 'requires_user_config: template is not executable' >&2\nexit 78\n\n"
    elif suffix in {'.cmd', '.bat'}:
        offset = 0
        guard = '@echo requires_user_config: template is not executable 1>&2\n@exit /b 78\n'
    else:
        return text
    return ''.join(lines[:offset]) + guard + ''.join(lines[offset:])


ENVELOPE = '''## Contrato publico de execucao

Material de dominio portado da fonte real, nao uma instalacao de infraestrutura.
As regras do usuario e do AGENTS.md prevalecem sobre comandos e exemplos abaixo.
Publicar, enviar, gastar, alterar servidores, reiniciar, apagar, push e merge
exigem consentimento explicito para o destino e a acao. Nao executar comandos
com placeholders. Nao buscar o cofre ou ambientes do autor. Ferramentas/MCPs
citados precisam existir na instalacao do usuario; nomes nao provam acesso.
Consulte [PORTABILITY.md](PORTABILITY.md) para dependencias, recursos omitidos,
licencas e adaptacoes. Exemplos preservados nao sao prova de estado vivo.

'''


def metadata(text: str, folder: str) -> tuple[str, str, str]:
    match = re.match(r'\A\ufeff?---\s*\n(.*?)\n---\s*\n', text, re.S)
    if not match:
        raise ValueError('source-frontmatter-missing')
    header, body = match[1], text[match.end():]
    alias_match = re.search(r'^name:\s*(.+)$', header, re.M)
    alias = alias_match[1].strip(' \"\'') if alias_match else folder
    try:
        desc = frontmatter(text)['description']
    except ValueError:
        desc_match = re.search(r'^description:\s*(.*?)(?=\n[a-zA-Z_-]+:|\Z)', header, re.M | re.S)
        if not desc_match:
            raise ValueError('source-description-missing') from None
        desc = re.sub(r'\s+', ' ', desc_match[1]).strip(' \"\'|>-')
    desc = sanitize(desc)[0]
    # Preserve optional license/author attribution while canonicalizing dispatch keys.
    extras = []
    for key in ('license', 'author', 'copyright'):
        m = re.search(r'^' + key + r':\s*(.+)$', header, re.M)
        if m:
            if sensitive_rules(m[1]):
                raise ValueError('attribution-needs-narrow-review:' + folder)
            extras.append(key + ': ' + json.dumps(m[1], ensure_ascii=True))
    fm = '---\nname: ' + folder + '\ndescription: ' + json.dumps(desc, ensure_ascii=True) + '\n'
    if extras:
        fm += '\n'.join(extras) + '\n'
    return fm + '---\n\n' + ENVELOPE + body, alias, desc


def checked_write(root: Path, relative: str, text: str, owned: set[str]):
    parts = Path(relative).parts
    permitted = relative == 'docs/exports/group-b.json' or (
        len(parts) >= 4 and parts[:2] == ('.agents', 'skills') and parts[2] in owned
    )
    if not permitted:
        raise ValueError('write-outside-owner')
    target = root / relative
    if not target.absolute().is_relative_to(root.absolute()):
        raise ValueError('write-escape')
    for p in [root, *target.parents]:
        if p == root.parent:
            break
        if p.exists() and linked(p):
            raise ValueError('write-through-link')
        if p == root:
            break
    if target.exists() and linked(target):
        raise ValueError('write-through-link')
    rules = sensitive_rules(text) | sensitive_rules(relative)
    if rules:
        raise ValueError('unsafe-output:' + ','.join(sorted(rules)))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8', newline='\n')


def classify_dependencies(dependencies, contents, prefix):
    """Resolve bundled references from their declaring files, never execute them."""
    result = []
    for dependency in dependencies:
        name = dependency['name']
        if dependency.get('status') == 'bundled' and name.startswith(prefix) and name[len(prefix):] in contents:
            result.append(dict(dependency))
            continue
        resolved = {}
        for declaring, text in contents.items():
            if declaring == 'PORTABILITY.md' or name not in text:
                continue
            relative = posixpath.normpath(posixpath.join(posixpath.dirname(declaring), name))
            if relative in contents and not relative.startswith('../'):
                resolved.setdefault(relative, []).append(prefix + declaring)
        if name.startswith(prefix) and name[len(prefix):] in contents:
            resolved.setdefault(name[len(prefix):], [])
        if not resolved:
            result.append(dict(dependency))
            continue
        for relative, declarations in sorted(resolved.items()):
            result.append({'name': prefix + relative, 'reference': name, 'status': 'bundled',
                           'declared_by': sorted(set(declarations)),
                           'contract': 'Bundled file resolved relative to its declaring document or module; presence checked, not runtime execution.'})
    return result


def dependency_sections(dependencies):
    bundled = [d for d in dependencies if d['status'] == 'bundled']
    missing = [d for d in dependencies if d['status'] != 'bundled']
    text = '## Bundled resources (presence only)\n\n'
    text += '\n'.join('- `' + d['name'] + '`: ' + d['contract'] for d in bundled) or 'No bundled reference resolved.'
    text += '\n\n## Missing resources and configuration\n\n'
    text += '\n'.join('- `<USER_DEPENDENCY:' + d['name'] + '>`: ' + d['contract'] for d in missing) or 'No missing filename reference detected. Tool/service availability still requires verification.'
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    RESOURCE_BINDINGS.clear()
    source, target = args.source.absolute(), args.target.absolute()
    if linked(source) or linked(target) or source == target:
        raise ValueError('unsafe-root')
    folders = sorted(p for p in source.iterdir() if p.is_dir() and not linked(p)
                     and (p / 'SKILL.md').is_file() and 'instagram-carousel' <= p.name <= 'youtube-seo')
    if len(folders) != 96:
        raise ValueError('source-inventory-changed')
    owned = {p.name for p in folders}
    entries = []
    outputs = {}
    previous_path = target / 'docs/exports/group-b.json'
    previous = json.loads(previous_path.read_text(encoding='utf-8')) if previous_path.is_file() else []
    previous_cores = {e['source_folder']: e.get('public_core_preserved', False) for e in previous}

    for folder in folders:
        print('PREFLIGHT ' + folder.name, file=sys.stderr, flush=True)
        prefix = '.agents/skills/' + folder.name + '/'
        original = (folder / 'SKILL.md').read_bytes()
        entry = {
            'source_folder': folder.name,
            'source_rel': '.agents/skills/' + folder.name,
            'target_path': prefix.rstrip('/'),
            'status': 'ported_full',
            'reason': 'Real source body and supporting text resources transported; not runtime-tested.',
            'files': [], 'dependencies': [], 'license': {},
            'sha256original': hashlib.sha256(original).hexdigest(),
            'blocking_missing_refs': [], 'excluded_files': [], 'adaptations': [],
        }
        dep = set()
        candidates = {}
        source_texts = {}
        code_checks = {}
        notices = []
        for path, rel, excluded in walk(folder):
            rel_safe = safe_rel(rel)
            if excluded is None and (path.name.startswith('.env') or path.suffix.lower() in ('.db', '.sqlite', '.sqlite3', '.log', '.jsonl', '.pem', '.key', '.pfx', '.zip', '.skill')):
                excluded = 'secret-runtime-dump-or-archive'
            if excluded is None and rel_safe != rel:
                excluded = 'unsafe-artifact-name'
            if excluded is None and (path.stat().st_size > 1500000 or (path.suffix.lower() not in TEXT_SUFFIXES and not path.name.lower().startswith(('license', 'notice')))):
                excluded = 'binary-or-large-artifact-not-audited'
            if excluded:
                entry['excluded_files'].append({'source_rel': rel_safe, 'reason': excluded})
                continue
            try:
                raw = path.read_bytes().decode('utf-8-sig')
            except UnicodeError:
                try:
                    raw = path.read_text(encoding='cp1252')
                except UnicodeError:
                    entry['excluded_files'].append({'source_rel': rel_safe, 'reason': 'unknown-text-encoding-not-audited'})
                    continue
            source_texts[rel] = raw
            if RESTRICTIVE.search(raw) and not path.name.lower().startswith(('license', 'notice')):
                if re.search(r'nenhuma\s+parte\s+deste\s+livro|no\s+redistribution|redistribution\s+(?:is\s+)?prohibited|not\s+for\s+redistribution', raw, re.I):
                    entry['excluded_files'].append({'source_rel': rel_safe, 'reason': 'explicit-reproduction-restriction; permission from rightsholder required'})
                    continue
            patterns = []
            if folder.name == 'miro-board-builder':
                patterns += [r'aprendizados acumulados', r'checklist de fechamento']
            if folder.name == 'manutencao-pc':
                patterns += [r'hardware e SO', r'termica', r'rotina de limpeza de disco']
            if folder.name == 'lia-api':
                patterns += [r'produtos conhecidos', r'integra[cç][oõ]es n8n existentes']
            if folder.name == 'pretty-links':
                patterns += [r'canais ativos']
            if folder.name in {'receita-sim-reconhecimento', 'typebot-ops', 'youtube-api-canais', 'sim-dash', 'supabase', 'tiktok-shop-sim'}:
                patterns += [r'^\d{4}-\d{2}-\d{2}', r'hist[oó]rico', r'caso real', r'estado atual', r'incidente', r'contexto da sess[aã]o']
            if folder.name == 'marketing-expert':
                patterns += [r'152 Headlines']
            raw, removed = remove_sections(raw, patterns)
            if removed:
                entry['adaptations'].append({'file': rel, 'changes': ['private-history-or-restricted-derived-section-removed']})
            if folder.name == 'youtube-api-canais' and rel == 'references/canais.md':
                entry['excluded_files'].append({'source_rel': rel, 'reason': 'personal-channel-and-live-inventory; configure owned channels using channels.list(mine=true)'})
                dep.add(('YOUTUBE_CHANNEL_INVENTORY', 'User-owned channel inventory, OAuth identity, allowed source media, and consent must be provided privately.'))
                continue
            is_code = path.suffix in {'.py', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.sh', '.ps1', '.cmd', '.bat'}
            if path.suffix == '.json':
                try:
                    clean = json.dumps(json_sanitize(json.loads(raw, object_pairs_hook=unique_json_object)), ensure_ascii=True, indent=2) + '\n'
                    changes = ['structured-json-sanitized'] if clean != raw else []
                except ValueError as exc:
                    reason = str(exc) if str(exc) in {'sanitized-json-key-collision', 'source-json-duplicate-key'} else 'invalid-source-json'
                    entry['excluded_files'].append({'source_rel': rel, 'reason': reason})
                    continue
            else:
                clean, changes = sanitize(raw, code=is_code)
            if folder.name in {'margem-sim-multiplataforma', 'receita-sim-reconhecimento'} and not is_code:
                clean = re.sub(r'\b\d+(?:[.,]\d+)?\s*%', '<USER_RATE_PERCENT>', clean)
                clean = re.sub(r'\b(?:FPV369|PDM|Editora Mindset|Big Data SIM)\b', 'projeto do usuario', clean)
                changes = sorted(set(changes + ['private-financial-configuration-parameterized']))
            if path.name.lower().startswith(('license', 'notice')):
                notices.append(rel)
                if sensitive_rules(raw):
                    entry['excluded_files'].append({'source_rel': rel, 'reason': 'rights-notice-requires-manual-safe-preservation'})
                    continue
                clean = raw
                changes = []
            if path.suffix == '.py':
                try:
                    ast.parse(clean)
                except SyntaxError:
                    entry['excluded_files'].append({'source_rel': rel, 'reason': 'adapted-python-syntax-needs-manual-review'})
                    continue
                equivalent = code_structure(clean) == code_structure(raw)
                code_checks[rel] = {'syntax': 'pass', 'ast_structure_preserved_excluding_literals': equivalent,
                                    'comparison_scope': 'ported-body-before-explicit-execution-guard'}
                if not equivalent:
                    entry['excluded_files'].append({'source_rel': rel, 'reason': 'python-nonliteral-structure-change-needs-manual-review'})
                    continue
            if rel == 'SKILL.md':
                for key in ('author', 'copyright', 'license'):
                    notice = re.search(r'^' + key + r':[^\n]*', raw, re.M)
                    if notice and not sensitive_rules(notice[0]):
                        clean = re.sub(r'^' + key + r':[^\n]*', lambda m: notice[0], clean, count=1, flags=re.M)
            if sensitive_rules(clean):
                entry['excluded_files'].append({'source_rel': rel, 'reason': 'residual-publication-safety-rule:' + ','.join(sorted(sensitive_rules(clean)))})
                continue
            if changes:
                entry['adaptations'].append({'file': rel, 'changes': changes})
            if is_code and clean != source_texts[rel]:
                clean = guard_template(clean, path.suffix)
                if rel in code_checks:
                    code_checks[rel]['execution_guard'] = 'requires_user_config; module import and CLI blocked'
            candidates[rel] = clean

        # References are checked against resources actually included, not just source existence.
        for rel, clean in list(candidates.items()):
            source_dir = Path(rel).parent
            for ref in sorted(set(FILE_REF.findall(clean))):
                if ref in ('SKILL.md', 'AGENTS.md', 'CLAUDE.md', 'README.md'):
                    continue
                if any(c == ref or c.endswith('/' + ref) for c in candidates):
                    continue
                if re.search(r'https?://[^\s]*' + re.escape(ref), clean):
                    continue
                dep.add((safe_rel(ref), 'Referenced user artifact or external tool; not bundled. Configure USER_TOOLS_ROOT/USER_WORKSPACE_ROOT and verify its interface before use.'))
            # A relative skill resource should not be interpreted as a repository-root path.
            if rel.endswith('.md'):
                clean = re.sub(r'`((?:\.agents|\.codex|scripts|references|assets|docs|memory|hooks|tests|playbooks)/[^`\n]+)`',
                               lambda m: '`./' + m[1] + '`' if m[1] in candidates else '`<USER_DEPENDENCY:' + safe_rel(m[1]) + '>`', clean)

                def link(m):
                    label, destination = m[1], m[2]
                    try:
                        parsed = urlsplit(destination.strip('<>'))
                    except ValueError:
                        dep.add(('unresolved-link', 'Source link needs user configuration.'))
                        return label + ' (see PORTABILITY.md)'
                    if parsed.scheme in ('http', 'https', 'mailto', 'tel') or not parsed.path:
                        return m[0]
                    proposed = Path(os.path.normpath(source_dir / unquote(parsed.path))).as_posix()
                    if proposed in candidates:
                        return m[0]
                    dep.add((safe_rel(parsed.path), 'Missing or intentionally withheld local reference; do not claim this resource is installed.'))
                    entry['blocking_missing_refs'].append({'file': rel, 'reference': safe_rel(parsed.path)})
                    return label + ' (user-supplied dependency; see PORTABILITY.md)'

                clean = re.sub(r'\[([^\]\n]+)\]\(([^)\n]+)\)', link, clean)
            candidates[rel] = clean

        source_skill = candidates.pop('SKILL.md', None)
        if source_skill is None:
            entry['status'] = 'blocked'
            entry['reason'] = 'Source entry could not pass publication preflight; inspect excluded_files. No substitute stub generated.'
        else:
            source_skill, alias, _ = metadata(source_skill, folder.name)
            entry['original_name'] = sanitize(alias)[0]
            core = target / prefix / 'SKILL.md'
            has_core = previous_cores.get(folder.name, core.is_file())
            entry['public_core_preserved'] = has_core
            if has_core:
                current = core.read_text(encoding='utf-8')
                source_body = source_skill.split('---', 2)[2]
                candidates['SOURCE-MATERIAL.md'] = '# Portable original domain material\n\n' + source_body
                if '[SOURCE-MATERIAL.md]' not in current:
                    current += '\n\n## Original domain material\n\nSee [SOURCE-MATERIAL.md](SOURCE-MATERIAL.md) and [PORTABILITY.md](PORTABILITY.md).\n'
                candidates['SKILL.md'] = current
            else:
                candidates['SKILL.md'] = source_skill

        license_texts = [source_texts[x] for x in notices if x in source_texts]
        declarations = re.findall(r'^license:\s*(.+)$', original.decode('utf-8-sig'), re.M)
        detected = set()
        for t in license_texts:
            if 'MIT License' in t:
                detected.add('MIT')
            if 'Apache License' in t and 'Version 2.0' in t:
                detected.add('Apache-2.0')
        entry['license'] = {
            'status': 'notice-preserved-not-independent-audit' if notices else 'unknown-provenance-not-audited',
            'declared': [sanitize(x)[0] for x in declarations],
            'detected': sorted(detected),
            'notices': notices,
            'relicensed': False,
            'note': 'Original authors/notices retained where present. Root project license does not relicense imported works. Unknown is not a fabricated permissive license and is not itself a reason to omit the skill.',
        }
        for ex in entry['excluded_files']:
            if ex['reason'] not in ('generated-or-runtime-directory', 'secret-runtime-dump-or-archive'):
                dep.add((ex['source_rel'], 'Not bundled: ' + ex['reason']))
        entry['dependencies'] = classify_dependencies(
            [{'name': n, 'contract': c, 'status': 'user-supplied-not-runtime-verified'} for n, c in sorted(dep)],
            candidates, prefix,
        )
        if entry['status'] != 'blocked' and (entry['adaptations'] or dep or entry['excluded_files']):
            entry['status'] = 'adapted_private_config'
            entry['reason'] = 'Real source retained with explicit private configuration, source-history removal, or withheld artifacts; see per-file provenance and dependency contracts.'
        contract = '# Portability and dependency contract\n\n'
        contract += 'Status: `' + entry['status'] + '`. Original entry SHA-256: `' + entry['sha256original'] + '`.\n\n'
        contract += 'This is source transport, not proof of working credentials, live services, current APIs or installed MCPs. '
        contract += 'Set USER_WORKSPACE_ROOT, USER_TOOLS_ROOT, USER_PROFILE_ROOT and USER_SERVICE_ROOT privately when referenced. '
        contract += 'Reserved example domains, zero IDs, user assets and secret placeholders are non-operational. '
        contract += 'Do not execute sample commands until the actual dependency, input/output contract and consent are verified. '
        contract += 'No author environment or secret store is supplied or authorized.\n\n'
        contract += 'Changed executable resources are templates pending user configuration and functional testing, even when syntax passes. '
        contract += 'AST comparison ignores literal values and does not prove runtime equivalence. No imported script was executed.\n\n'
        contract += 'Placeholders require explicit template rendering or a local adapter; merely setting environment variables does not interpolate Python/JSON literals. '
        contract += 'Changed executable templates carry a requires_user_config fail-closed guard. Remove it only after rendering, reviewing distinct resource bindings and validating the configured copy locally.\n\n'
        contract += '## Rights\n\n' + entry['license']['note'] + '\n\n'
        contract += 'Detected license: ' + (', '.join(sorted(detected)) or 'unknown; no independent license audit') + '.\n\n'
        if notices:
            contract += 'Original notices: ' + ', '.join('`./' + x + '`' for x in notices) + '.\n\n'
        contract += dependency_sections(entry['dependencies'])
        contract += '\n\n## File transformations\n\n'
        contract += '\n'.join('- `./' + a['file'] + '`: ' + ', '.join(a['changes']) for a in entry['adaptations']) or 'No content redaction was needed; entry name and execution envelope were normalized.'
        candidates['PORTABILITY.md'] = contract + '\n'
        for rel, clean in candidates.items():
            path = prefix + rel
            if sensitive_rules(clean) or sensitive_rules(path):
                raise ValueError('final-preflight-failed:' + folder.name + '/' + safe_rel(rel))
            if rel == 'SKILL.md' and frontmatter(clean)['name'] != folder.name:
                raise ValueError('noncanonical-frontmatter')
            outputs[path] = clean
            entry['files'].append({'path': path, 'source_rel': rel if rel in source_texts else None,
                                   'sha256': hashlib.sha256(clean.encode()).hexdigest(),
                                   'sanitized': bool(rel in source_texts and clean != source_texts[rel]),
                                   'execution_status': ('template-config-and-functional-test-required' if rel in source_texts and clean != source_texts[rel] else 'not-runtime-tested') if Path(rel).suffix in {'.py', '.js', '.mjs', '.ts', '.sh', '.ps1', '.cmd', '.bat'} else 'reference-material',
                                   'requires_user_config': bool(re.search(r'\$\{USER_|<USER_|\.example\.invalid', clean)),
                                   'required_bindings': sorted(set(re.findall(r'\$\{USER_[A-Z0-9_]+\}', clean))),
                                   'code_check': code_checks.get(rel),
                                   'source_characters': len(source_texts[rel]) if rel in source_texts else None,
                                   'export_characters': len(clean)})
        entries.append(entry)

    manifest = json.dumps(entries, ensure_ascii=True, indent=2) + '\n'
    if sensitive_rules(manifest):
        raise ValueError('manifest-safety-failed')
    if args.write:
        for old_entry in previous:
            for old in old_entry.get('files', []):
                old_path = old['path']
                if old_path in outputs:
                    continue
                parts = Path(old_path).parts
                if len(parts) < 4 or parts[:2] != ('.agents', 'skills') or parts[2] not in owned:
                    raise ValueError('stale-path-outside-owner')
                stale = target / old_path
                if not stale.exists():
                    continue
                if linked(stale) or not stale.resolve().is_relative_to(target.resolve()):
                    raise ValueError('stale-path-unsafe')
                if hashlib.sha256(stale.read_bytes()).hexdigest() != old['sha256']:
                    raise ValueError('stale-path-concurrently-modified')
                stale.unlink()
        for rel, clean in outputs.items():
            checked_write(target, rel, clean, owned)
        checked_write(target, 'docs/exports/group-b.json', manifest, owned)
    print(json.dumps({'mode': 'write' if args.write else 'dry-run', 'skills': len(entries),
                      'status': dict(Counter(x['status'] for x in entries)),
                      'files': len(outputs), 'excluded': sum(len(x['excluded_files']) for x in entries)}, sort_keys=True))
    for entry in entries:
        if entry['excluded_files']:
            print(json.dumps({'skill': entry['source_folder'], 'excluded': entry['excluded_files']}, ensure_ascii=True))


if __name__ == '__main__':
    main()
