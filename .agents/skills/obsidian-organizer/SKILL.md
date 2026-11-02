---
name: obsidian-organizer
description: "Organiza, formata e gera relat\u00f3rio master de todas as notas do vault Obsidian criadas pelo obsidian-logger. Reformata notas antigas, gera Dashboard com estat\u00edsticas, e pode criar novos temas (pastas) sob demanda. Triggers: \"organiza obsidian\", \"formata as notas\", \"gera relat\u00f3rio obsidian\", \"dashboard claude code\", \"beautify vault\", \"cria tema X no obsidian\", \"adiciona pasta X\", \"novo tema obsidian\"."
---

## Contrato publico de execucao

Material de dominio portado da fonte real, nao uma instalacao de infraestrutura.
As regras do usuario e do AGENTS.md prevalecem sobre comandos e exemplos abaixo.
Publicar, enviar, gastar, alterar servidores, reiniciar, apagar, push e merge
exigem consentimento explicito para o destino e a acao. Nao executar comandos
com placeholders. Nao buscar o cofre ou ambientes do autor. Ferramentas/MCPs
citados precisam existir na instalacao do usuario; nomes nao provam acesso.
Consulte [PORTABILITY.md](PORTABILITY.md) para dependencias, recursos omitidos,
licencas e adaptacoes. Exemplos preservados nao sao prova de estado vivo.

# Obsidian Organizer

Você é o editor e arquiteto do knowledge base de desenvolvimento. Opera em **dois modos** detectados automaticamente:

| Modo | Trigger | O que faz |
|------|---------|-----------|
| **ORGANIZAR** | "organiza", "formata", "beautify", "dashboard" | Reformata notas existentes + cria Dashboard |
| **NOVO TEMA** | "cria tema X", "adiciona pasta X", "novo tema Y" | Adiciona tema ao themes.json + cria pasta no vault |

---

## MODO 1 — ORGANIZAR VAULT

### Passo 1: Localizar vault e inventariar

```python
import json, os, sys
from pathlib import Path

config = Path.home() / ".claude" / "obsidian-logger" / "config.json"
cfg = json.loads(config.read_text(encoding="utf-8"))
vault_path = cfg.get("vault_path") or os.environ.get("OBSIDIAN_VAULT_PATH", "")
vault = Path(vault_path)

if not vault.exists():
    # Perguntar ao usuario e salvar no config antes de continuar
    pass

base = vault / "Claude Code"
sessoes_dir = base / "Sessoes"
daily_dir = base / "Daily"
skills_dir = base / "Skills"

# Inventario
all_sessions = list(sessoes_dir.rglob("*.md")) if sessoes_dir.exists() else []
all_daily = list(daily_dir.glob("*.md")) if daily_dir.exists() else []
all_skills = list(skills_dir.glob("*.md")) if skills_dir.exists() else []
```

Exibir para o usuario:
```
Encontrado no vault:
   X sessoes em X pastas tematicas
   Y dias no diario
   Z skills indexadas
```

### Passo 2: Reformatar notas de sessao (que ainda nao tem callouts)

Para cada nota em `Claude Code/Sessoes/**/*.md`:
1. Ler o conteudo
2. Verificar se ja tem callouts Obsidian (`> [!INFO]`) — se sim, pular
3. Se nao tem: reescrever com o template rico (ver secao de template abaixo)

**Template de sessao rica:**

```markdown
---
date: "YYYY-MM-DD"
time: "HH:MM"
fuso: "America/Sao_Paulo"
projeto: "Nome"
tema: "🌐 Sites"
skills_instaladas: []
sites_publicados: []
tags: ["claude-code", "sessao"]
---

# 🖥️ Sessão DD/MM/YYYY HH:MM (BRT) — Projeto

> **Tema:** 🌐 Sites

> [!INFO] Visão Geral
> 📅 **Data:** DD/MM/YYYY às HH:MM
> 📁 **Projeto:** Nome
> 🔧 **Skills instaladas:** nenhuma
> 🌐 **Sites publicados:** 0
> 📄 **Arquivos modificados:** X

---

## ✅ Resumo

> [!SUCCESS] O que foi feito
> bullet points do resumo

---

## 🎯 O que foi pedido

- 💬 Pedido 1
- 💬 Pedido 2

---

## 🔧 Skills Instaladas

| Skill | Descrição | Link |
|-------|-----------|------|
| `nome` | desc | [[Claude Code/Skills/nome\|nome]] |

---

## 🌐 Sites Publicados

> [!EXAMPLE] Sites ao vivo
> - url (user-supplied dependency; see PORTABILITY.md)

---

## 📁 Arquivos Criados/Modificados

**🐍 .py** (X)
```
caminho/arquivo.py
```

---

## ⚙️ Comandos Executados

```powershell
comando relevante
```

---

*🤖 Documentado automaticamente pelo [[obsidian-logger]] • Session `XXXXXXXX`*
```

### Passo 3: Reformatar Daily logs

Para cada arquivo em `Claude Code/Daily/YYYY-MM-DD.md` sem frontmatter adequado:

```markdown
---
date: "YYYY-MM-DD"
fuso: "America/Sao_Paulo"
tags: ["claude-code", "daily"]
---

# 📅 Diário Claude Code — DD/MM/YYYY (BRT)

## 🕐 HH:MM (BRT) — Projeto A

> [!ABSTRACT] Resumo
> bullet points do resumo

[[Claude Code/Sessoes/🌐 Sites/YYYY-MM-DD_HH-MM — Projeto|→ Ver sessão completa]]

## 🕑 HH:MM (BRT) — Projeto B
...
```

### Passo 4: Reformatar Skills index

Para cada `Claude Code/Skills/skill-name.md` simples (sem callouts):

```markdown
---
skill: "nome"
instalada_em: "YYYY-MM-DD"
fuso: "America/Sao_Paulo"
tags: ["claude-code", "skill"]
---

# 🔧 nome-da-skill

> [!INFO] Informações
> **Instalada em:** DD/MM/YYYY às HH:MM (BRT)
> **Origem:** [[caminho/sessao|Ver sessão de instalação]]

## Descrição

(buscar em ./SKILL.md o campo description: do frontmatter)

## Sessões que usaram esta skill

- [[caminho/sessao|DD/MM/YYYY HH:MM]]
```

Para buscar a descricao:
```python
skill_md = Path.home() / ".claude" / "skills" / skill_name / "SKILL.md"
content = skill_md.read_text(encoding="utf-8")
import re
m = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
desc = m.group(1).strip().strip('"').strip("'")[:120] if m else ""
```

### Passo 5: Gerar / Atualizar Dashboard Master

Criar ou sobrescrever `Claude Code/🏠 Dashboard.md`:

```markdown
---
tags: ["claude-code", "dashboard", "index"]
updated: "YYYY-MM-DD HH:MM BRT"
---

# 🏠 Claude Code — Dashboard

> [!NOTE] Workspace de Desenvolvimento com IA
> Gerado automaticamente pelo [[obsidian-organizer]]
> Atualizado em: **DD/MM/YYYY às HH:MM (BRT)**

---

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| 🗂️ Total de sessões | X |
| 📅 Dias trabalhados | Y |
| 🔧 Skills instaladas | Z |
| 🌐 Sites publicados | W |
| 📁 Arquivos modificados (total) | V |
| 🗓️ Primeira sessão | DD/MM/YYYY |
| 🗓️ Última sessão | DD/MM/YYYY |

---

## 🗂️ Pastas Temáticas

| Pasta | Sessões | Última atividade |
|-------|---------|-----------------|
| [[Claude Code/Sessoes/🌐 Sites\|🌐 Sites]] | X | DD/MM/YYYY |
| [[Claude Code/Sessoes/🔧 Skills\|🔧 Skills]] | X | DD/MM/YYYY |
| [[Claude Code/Sessoes/🤖 Agentes\|🤖 Agentes]] | X | DD/MM/YYYY |
| ... | ... | ... |

---

## 🕐 Sessões Recentes (10 últimas)

| Data/Hora (BRT) | Projeto | Tema | Skills | Sites |
|----------------|---------|------|--------|-------|
| [[link\|DD/MM HH:MM]] | Projeto | 🌐 Sites | skill1 | 1 |

---

## 📅 Últimos 7 Dias

| Data | Sessões | Skills | Sites |
|------|---------|--------|-------|
| [[Daily/YYYY-MM-DD\|DD/MM/YYYY]] | X | Y | Z |

---

## 🔧 Skills Instaladas

| Skill | Instalada em | Descrição |
|-------|-------------|-----------|
| [[Claude Code/Skills/nome\|nome]] | DD/MM/YYYY | desc |

---

## 🌐 Sites Publicados

| Site | URL | Data |
|------|-----|------|
| Nome | link (user-supplied dependency; see PORTABILITY.md) | DD/MM/YYYY |

_(se nenhum: omitir esta secao)_

---

*🤖 [[obsidian-logger]] + [[obsidian-organizer]]*
```

**Como calcular as estatísticas:**
```python
from datetime import datetime

total_sessions = len(all_sessions)
# Contar skills e sites varrendo frontmatter de cada sessao
skills_count = set()
sites_count = []
first_date = None
last_date = None

for sess in all_sessions:
    content = sess.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'^skills_instaladas:\s*(\[.*?\])', content, re.MULTILINE)
    if m:
        try:
            skills_count.update(json.loads(m.group(1)))
        except: pass
    m = re.search(r'^sites_publicados:\s*(\[.*?\])', content, re.MULTILINE)
    if m:
        try:
            sites_count.extend(json.loads(m.group(1)))
        except: pass
    m = re.search(r'^date:\s*"?([\d-]+)"?', content, re.MULTILINE)
    if m:
        d = m.group(1)
        if not first_date or d < first_date: first_date = d
        if not last_date or d > last_date: last_date = d
```

### Passo 6: Relatório final no terminal

```
Obsidian Organizer — Concluido

Vault: ${USER_WORKSPACE_ROOT}
Sessoes reformatadas: X
Diarios atualizados: Y
Skills indexadas: Z
Dashboard: Claude Code/Dashboard.md

Abra o vault no Obsidian para ver o resultado.
```

---

## MODO 2 — NOVO TEMA

Quando o usuário disser "cria tema X", "adiciona pasta Y", "quero um tema para Z":

### Passo 1: Entender o tema

Extrair do pedido:
- **Nome** da pasta (com emoji sugerido)
- **Palavras-chave** que vão trigger esse tema automaticamente

Se o usuário não forneceu palavras-chave, sugira 5-8 baseando-se no nome.

### Passo 2: Adicionar ao themes.json

```python
sys.path.insert(0, str(Path.home() / ".claude" / "obsidian-logger"))
import worker

worker.add_theme(
    slug="meu-tema",
    folder="🎯 Meu Tema",
    keywords=["palavra1", "palavra2", "palavra3"]
)
```

### Passo 3: Criar a pasta no vault

```python
nova_pasta = vault / "Claude Code" / "Sessoes" / "🎯 Meu Tema"
nova_pasta.mkdir(parents=True, exist_ok=True)

# Criar nota de index da pasta
index = nova_pasta / "_index.md"
index.write_text(
    f"---\ntags: [claude-code, tema]\n---\n\n"
    f"# 🎯 Meu Tema\n\n"
    f"Sessões relacionadas a este tema.\n\n"
    f"**Keywords:** palavra1, palavra2, palavra3\n\n"
    f"[[Claude Code/Dashboard|← Dashboard]]\n",
    encoding="utf-8"
)
```

### Passo 4: Confirmar ao usuário

```
Tema criado:
  Pasta: Claude Code/Sessoes/🎯 Meu Tema/
  Keywords: palavra1, palavra2, palavra3
  Proximas sessoes com essas palavras irao automaticamente para esta pasta.

Para forcar uma sessao existente para este tema:
  1. Edite o frontmatter: tema: "🎯 Meu Tema"
  2. Mova o arquivo para a pasta correta
```

---

## Regras gerais

1. **Nunca deletar conteúdo** — preservar dados, apenas reformatar
2. **Idempotente** — rodar duas vezes gera o mesmo resultado
3. **Timestamp sempre em SP (BRT/BRST)** — nunca UTC raw
4. **Callouts Obsidian:** `[!INFO]`, `[!SUCCESS]`, `[!WARNING]`, `[!TIP]`, `[!EXAMPLE]`, `[!ABSTRACT]`
5. **Emojis nos headings** — nunca em texto corrido
6. **Wikilinks** — sempre `[[path/to/Note|texto]]` para links internos
7. **Fuso no frontmatter** — sempre `fuso: "America/Sao_Paulo"`
8. **Sessões curtas** — usar callout `[!WARNING] Sessão Curta`

## Ferramentas a usar

- `Read` / `Write` — leitura e escrita direta no vault (mais confiável)
- `obsidian-cli` — se Obsidian estiver aberto (use `obsidian read`, `obsidian create overwrite`)
- `Glob` / `Grep` — para inventariar arquivos do vault
- `Bash` / `PowerShell` — para operações de massa
