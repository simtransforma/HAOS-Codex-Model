---
name: miro-board-builder
description: "Criar boards no Miro (funis, estrat\u00e9gias, fluxos, explica\u00e7\u00f5es visuais) via MCP do Miro. Use quando o usuario pedir pra montar/ajustar fluxograma, jornada, estrat\u00e9gia visual, mapa mental ou qualquer board novo no Miro. Cobre DSL do diagrama, limita\u00e7\u00f5es conhecidas e workflow de corre\u00e7\u00e3o."
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

# Miro Board Builder — Skill HAOS

> **Manutenção:** Sempre que descobrir algo novo (limitação do MCP, padrão visual que funciona melhor, atalho, erro recorrente, preferência do usuario), **atualize esta skill antes de fechar a tarefa**. Esta é a fonte da verdade pra trabalho com Miro no HAOS.

---

## 1. Quando ativar

- usuario pede pra criar board no Miro (funil, estratégia, jornada, fluxo, mapa mental, explicação visual)
- usuario pede ajuste em board existente
- Necessidade de comunicação visual didática (mostrar fluxo pra alguém entender)

**Não ativar** pra: tarefas só de copy, código, infra. Só Miro.

---

## 2. MCP do Miro — Servidor `${USER_RESOURCE_000011}`

Tools disponíveis (carregar via ToolSearch antes de chamar):

| Tool | Uso |
|---|---|
| `board_create` | Criar board. **Não aceita pasta/projeto** — board nasce na raiz do team. |
| `board_search_boards` | Listar/buscar boards do team |
| `board_list_items` | Listar items de um board (paginado) |
| `diagram_get_dsl` | Spec da DSL pra `diagram_create`. **Chamar 1x por tipo de diagrama por conversa**. |
| `diagram_create` | Criar flowchart, uml_class, uml_sequence, entity_relationship |
| `layout_get_dsl` | Spec da DSL pra `layout_create` (frames, shapes, sticky, text, etc.) |
| `layout_create` | Criar items individuais a partir de DSL livre |
| `layout_read` | Ler DSL do board. ⚠️ **NÃO LÊ diagramas criados via `diagram_create`** (retorna "0 items, X unsupported") |
| `layout_update` | Find-replace na DSL do board (só funciona em items que `layout_read` enxerga) |
| `context_explore` | Listar frames/diagramas/docs/prototypes/tables do board |
| `context_get` | Resumo AI do board OU conteúdo de item específico (via `?moveToWidget=<id>`) |
| `comment_*` | Comentários e threads |
| `doc_create` / `doc_update` / `doc_get` | Docs embutidos no board |
| `image_create` / `image_get_data` | Imagens |
| `table_create` / `table_list_rows` / `table_sync_rows` | Tabelas |
| `code_widget_*` | Snippets de código (único tipo com `delete` próprio) |

---

## 3. Limitações conhecidas (NÃO esquecer)

### 3.1 Sem API de pasta/projeto
- Boards nascem na **raiz do team**.
- Mover pra pasta = manual pelo usuario (UI do Miro: breadcrumb → ⋯ → Move to).
- Sempre avisar isso ANTES de criar o board.

### 3.2 Diagramas são "unsupported" pra `layout_read` / `layout_update`
- `diagram_create` cria um item composto (stencil_shapes + connectors) que aparece como **1 item unsupported** no `layout_read`.
- **Não dá pra editar texto de nó, label de seta ou conexão individual via layout_update.**
- **Correção exige recriar o diagrama inteiro** numa posição abaixo/ao lado e pedir pro usuario deletar o antigo (clica → Delete).

### 3.3 Sem `diagram_delete` genérico
- Só existe `code_widget_delete` (pra code widgets).
- Outros tipos: deleção manual pelo usuario.

### 3.4 Browser fallback (Codex in Chrome) só com login do usuario
- Regra de segurança HAOS: não digitar credenciais nem completar SSO sem o usuario.
- Se precisar de UI do Miro: abrir tela de login e devolver a bola.

---

## 4. DSL do Flowchart (resumo prático)

```
graphdir <TB|LR|BT|RL>
palette #hex1 #hex2 #hex3

n1 <label> <object> <color_index>
n2 ...

c <source_id> <text|-> <target_id>
c ...

cluster c1 "<label>" n1 n2 ... [parent=c#]
```

**Objects válidos:**
- `flowchart-terminator` — start/end
- `flowchart-process` — ação/processo
- `flowchart-decision` — condição (diamante)
- `flowchart-data` — input/output (paralelograma)

**Connector text:**
- `-` = sem label
- Pra decisões: usar `SIM` / `NÃO` ou outcome curto
- Pra outras: descrição curta da transição

**Convenção de cores HAOS (default):**
| Cor | Hex | Uso |
|---|---|---|
| 🟢 Verde | `#adf0c7` | Start/end (terminators) |
| 🟡 Amarelo | `#fff6b6` | Process (ações) |
| 🔵 Azul | `#c6dcff` | Decision (condições) |

Palette default: `palette #fff6b6 #c6dcff #adf0c7`

**Outras cores Miro-friendly:** `#ffc6c6 #f8d3af #fff6b6 #dbfaad #adf0c7 #c3faf5 #ccf4ff #c6dcff #dedaff #ffd8f4 #e7e7e7`

---

## 5. Workflow recomendado

### Criação inicial
1. **Entender o fluxo** — confirmar entrada → ações → decisões → saída
2. **Avisar limitação da pasta** ANTES de criar (usuario moverá manualmente)
3. **`board_create`** → guardar URL
4. **`diagram_get_dsl flowchart`** → puxar spec (só 1x por conversa)
5. **`diagram_create`** com DSL na posição `(0, 0)`
6. **Entregar**:
   - Link do board
   - Walkthrough textual do fluxo (com símbolos `[ ]` `⬥` `→`)
   - Convenção de cores
   - Lembrete de mover pra pasta
   - Sugestões de branches futuros (opcional)

### Correção de diagrama existente
1. **Confirmar exatamente o que muda** — pedir print se houver ambiguidade
2. **Recriar o diagrama** corrigido em `(0, y+700)` (abaixo do antigo) com título tipo `(v2)`
3. **Avisar o usuario** que precisa deletar o antigo manualmente (1 clique + Delete)
4. **Não tentar editar via `layout_update`** — não funciona pra diagrama

### Quando o usuario manda print
- Olhar **setas vermelhas / círculos / anotações** desenhadas — são instruções visuais diretas
- "Seta vermelha apontando" = mudança a fazer, geralmente adição OU substituição (perguntar SE não tiver certeza, mas só 1 vez)

---

## 6. Estilo de comunicação com o usuario

- **PT-BR, direto, técnico, sem floreio**
- **Resultado antes do processo** — entregar link/output primeiro, explicação depois
- **Visual**: tabelas, listas, símbolos pra fluxos
- **Não perguntar demais** — se ele disse "que complicação é uma coisa simples", é sinal pra agir mais e perguntar menos
- **Quando perguntar via `AskUserQuestion`** — só quando ambiguidade real e custo de erro > custo de pergunta
- **Pedir print** quando texto é ambíguo (ele responde rápido com screenshot)
- **Confirmar com 1 mensagem curta** depois de entregar, com link e walkthrough

---

## 9. Templates rápidos de DSL

### Funil de conversão (4 etapas + decisão)
```
graphdir LR
palette #fff6b6 #c6dcff #adf0c7

n1 Topo do Funil flowchart-terminator 2
n2 Captura (lead magnet) flowchart-process 0
n3 Nutrição (email/whats) flowchart-process 0
n4 Convertido? flowchart-decision 1
n5 Venda flowchart-terminator 2
n6 Reengajamento flowchart-process 0

c n1 - n2
c n2 - n3
c n3 - n4
c n4 SIM n5
c n4 NÃO n6
c n6 - n3
```

### Decisão binária pós-evento
```
graphdir LR
palette #fff6b6 #c6dcff #adf0c7

n1 Evento (compra/inscrição) flowchart-terminator 2
n2 Comunicação imediata flowchart-process 0
n3 Atendeu critério? flowchart-decision 1
n4 Caminho A flowchart-process 0
n5 Caminho B flowchart-process 0
n6 Resultado final flowchart-terminator 2

c n1 - n2
c n2 - n3
c n3 SIM n4
c n3 NÃO n5
c n4 - n6
c n5 - n6
```

---

## 10. Quando algo der errado

| Sintoma | Causa provável | Ação |
|---|---|---|
| `layout_read` retorna 0 items mas o board tem coisa | É um diagrama ou item unsupported | Usar `context_explore` + `context_get` |
| Não consigo editar texto de nó | É diagrama (unsupported pra update) | Recriar o diagrama inteiro |
| `diagram_create` falha com erro de DSL | DSL malformada (id duplicado, object errado, color_index fora do palette) | Validar contra `diagram_get_dsl` |
| MCP demora muito | Board muito grande | Filtrar com `?moveToWidget=<id>` |
| Não consigo deletar diagrama via MCP | `diagram_delete` não existe | usuario deleta manual (clica + Delete) |
| Browser pede login no Miro | Sessão deslogada | Abrir tela e devolver pro usuario — não digitar credencial |

