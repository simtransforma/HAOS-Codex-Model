# Template — Registro de Merge

Salvar como: `registros/merge_{sistema_alvo}_{YYYY-MM-DD}.md`

---

```markdown
# Registro de Merge — {Sistema Alvo} → {Sistema Base}
Data: {YYYY-MM-DD}
Versão do sistema alvo: {commit/tag/versão}
Executado por: Agente Incorporador

---

## 1. Resumo Executivo

**Sistema alvo analisado:** {nome, repositório, link}
**Objetivo do merge:** {o que queremos ganhar}
**Decisão geral:** {INCORPORAR TOTALMENTE / PARCIALMENTE / DESCARTAR}
**Motivo principal:** {1-2 frases}

---

## 2. Inventário — Sistema Alvo

### Agentes / Especialistas
| Nome | Departamento | Responsabilidade | Decisão |
|---|---|---|---|
| {nome} | {dept} | {função} | INCORPORAR/MANTER/FUNDIR/DESCARTAR |

### Comandos / Slash Commands
| Comando | Função | Decisão |
|---|---|---|
| /{cmd} | {o que faz} | INCORPORAR/DESCARTAR |

### Skills
| Skill | Trigger | Decisão |
|---|---|---|
| {nome} | {quando aciona} | INCORPORAR/ADAPTAR/DESCARTAR |

### Pipelines / Workflows
| Pipeline | Fases | Decisão |
|---|---|---|
| {nome} | {N fases} | INCORPORAR/FUNDIR/DESCARTAR |

### Infraestrutura (hooks, memória, etc.)
| Componente | Função | Decisão |
|---|---|---|
| {nome} | {função} | INCORPORAR/DESCARTAR |

---

## 3. Matriz Comparativa Completa

| Capacidade | Sistema Alvo | Sistema Base | Scores (Alvo/Base) | Decisão |
|---|---|---|---|---|
| {capacidade} | ✅/❌/⚠️ | ✅/❌/⚠️ | {A}//{B} | {decisão} |

---

## 4. Plano de Merge — Detalhado

### QUICK WINS (Prioridade Alta + Esforço Pequeno)
Execute imediatamente:

**[M01] {Título}**
- Ação: INCORPORAR / SUBSTITUIR / FUNDIR
- Origem: `{sistema_alvo}/{arquivo}`
- Destino: `{sistema_base}/{onde_vai}`
- Adaptações: {o que muda}
- Resultado esperado: {o que ganhamos}
- Status: ⬜ Pendente

---

### HIGH VALUE (Prioridade Alta + Esforço Médio)

**[M02] {Título}**
- Ação: {ação}
- Origem: `{arquivo}`
- Destino: `{onde_vai}`
- Adaptações: {detalhes}
- Dependências: {outros itens}
- Resultado esperado: {ganho}
- Status: ⬜ Pendente

---

### BACKLOG (Prioridade Baixa)

**[M03] {Título}**
- Ação: {ação}
- Nota: {por que é baixa prioridade}
- Status: ⬜ Pendente

---

## 5. Novos Artefatos a Criar

Itens que nenhum sistema tem mas que o merge abre necessidade:

| ID | Artefato | Tipo | Descrição | Prioridade |
|---|---|---|---|---|
| N01 | {nome} | Agente/Skill/Script | {o que faz} | ALTA/MÉDIA/BAIXA |

---

## 6. Conflitos Identificados

Casos onde os dois sistemas fazem a mesma coisa de formas diferentes:

| Conflito | Sistema Alvo | Sistema Base | Resolução |
|---|---|---|---|
| {área} | {como faz} | {como faz} | {qual vence e por quê} |

---

## 7. Decisões de Arquitetura

Decisões estruturais que impactam o sistema como um todo:

1. **{Decisão}:** {motivo}
2. **{Decisão}:** {motivo}

---

## 8. Roadmap de Execução

```
SEMANA 1 (Quick Wins)
  □ [M01] {título} — ~{tempo}
  □ [M02] {título} — ~{tempo}

SEMANA 2 (High Value)
  □ [M03] {título} — ~{tempo}
  □ [N01] {artefato novo} — ~{tempo}

BACKLOG
  □ [M04] {título}
```

---

## 9. Histórico de Atualizações

| Data | Mudança | Quem |
|---|---|---|
| {YYYY-MM-DD} | Análise inicial | Agente Incorporador |
```
