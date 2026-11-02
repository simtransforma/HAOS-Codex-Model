# Registro de incorporação — Vibe Coding Toolkit -> HAOS Codex Xtreme3

Data: 2026-08-26
Sistema alvo: `soumatheusgomes/vibe-coding-toolkit`
Versão analisada: commit `c26b55ecc86275b33ea8433bd51934814a98a28d`
Sistema base: `simtransforma/your-private-project`
Método: análise integral do alvo, comparação local, testes seguros e parecer do conselho + 31 agentes

## 1. Resumo executivo

**Decisão geral: INCORPORAR PARCIALMENTE POR ADAPTAÇÃO. Não instalar nem importar o toolkit em bloco.**

O repositório externo é uma curadoria documental útil, com bons padrões de
orquestração, revisão, saneamento e gates progressivos. Ele não contém um runtime
completo para Codex e sua implementação prática é majoritariamente Claude Code.
O HAOS já possui arquitetura mais ampla: Rito v2, 31 agentes, 142 skills, 93
documentos de comando, hooks Codex e memória multicamada.

O ganho real está em fundir cinco ideias ao HAOS existente:

1. contrato explícito de ondas com arquivos, dependências e owner único;
2. revisão independente, read-only e com síntese deduplicada;
3. saneamento de projeto medido antes/depois;
4. quality gates progressivos escolhidos pela stack real;
5. compactação de memória com readback, proveniência e alto sinal.

Antes disso, a auditoria encontrou quatro bloqueios P0 no próprio HAOS:

1. três hooks Python quebram com JSON válido cujo topo não é objeto;
2. o gate de ações externas aceita marcadores textuais que o próprio agente pode acrescentar;
3. 29 dos 31 wrappers GSD apontam para um runtime `.claude` inexistente;
4. 138 arquivos ainda citam o root antigo `${HAOS_PRIVATE_ROOT}`, misturando referências operacionais e documentais.

Nenhuma ferramenta externa foi instalada. Claude Code, cofre de segredos,
produção, GitHub remoto e runtimes externos não foram alterados.

## 2. Evidência e escopo

### 2.1 Sistema alvo

- Repositório: <https://github.com/soumatheusgomes/vibe-coding-toolkit>
- HEAD remoto confirmado: `c26b55ecc86275b33ea8433bd51934814a98a28d`
- Data do commit: `2026-08-15T12:49:18-04:00`
- Autor do commit: Matheus Gomes
- Licença do conteúdo do repositório: MIT
- Arquivos rastreados: 31
- Volume: 438.576 bytes e 6.210 linhas
- Estado do clone após a leitura: somente `_haos-review/` não rastreado

Inventário lido:

| Grupo | Quantidade | Conteúdo |
|---|---:|---|
| Raiz | 3 | `README.md`, `LICENSE`, `.gitignore` |
| Documentos centrais | 3 | visão geral, instalação e playbook |
| Prompts | 7 | saneamento, lint, review, brainstorm, ondas, memória e setup ESLint |
| Ferramentas documentadas | 14 | Superpowers, subagentes, RTK, personas, gates, Graphify, memória, hooks, browser e MCPs |
| Templates | 4 | `CLAUDE.md`, settings, helper de hook e regra de subagentes |

O repositório não traz package manifest, instalador próprio ou implementação
completa das ferramentas descritas. Há documentação, prompts e exemplos; a
instalação real depende de vários projetos externos.

### 2.2 Sistema base

Inventário local confirmado em `${HAOS_PRIVATE_ROOT}`:

| Superfície | Quantidade/estado |
|---|---|
| Agentes Codex | 31 arquivos TOML |
| Skills | 142 diretórios com `SKILL.md` |
| Documentos de comando | 93 arquivos Markdown |
| Hooks | `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop` |
| Memória | projeto, Obsidian, HAOS Memory, claude-mem isolado e Mnemoverse |
| Orquestração | Rito v2, departamentos, conselho, gates e delegação máxima de 3 agentes por onda |

### 2.3 Memória consultada

O `claude-mem` isolado respondeu com `status=ok`, `initialized=true`,
`mcpReady=true` e readiness `ready`. Foram consultados os contextos de `HAOS
Systen` e `your-private-project`; arquivos canônicos do bootstrap foram usados como
fonte de autoridade. Na validação final o worker havia parado; ele foi iniciado
novamente e voltou aos mesmos quatro estados saudáveis. O health ainda informa
o runtime compatível em `${HAOS_PRIVATE_ROOT}`, enquanto dados e
configuração são resolvidos pelo projeto H; essa dependência legada entra no P0
de caminhos e não foi migrada silenciosamente nesta análise.

## 3. Matriz comparativa completa

| Capacidade do alvo | Equivalente HAOS | Decisão | Prioridade | Esforço | Motivo |
|---|---|---|---|---|---|
| Superpowers | Rito v2, `software-engineer`, PRD e QA | MANTER HAOS | P0 | baixo | Um segundo orquestrador criaria autoridade concorrente |
| Brainstorm -> plano -> implementação -> review | Rito F1-F4/F10 e skills existentes | FUNDIR | P1 | médio | Útil como microfluxo técnico subordinado ao Rito |
| Orquestração em ondas | Delegação HAOS | FUNDIR | P0 | médio | Acrescenta write-set, dependências, owner e degradação serial |
| Review multiagente | `qa-reviewer`, conselho e agentes especialistas | FUNDIR | P0 | médio | Falta contrato único de review read-only e síntese |
| Project sanitation | Segurança/QA genéricos | INCORPORAR ADAPTADO | P1 | médio | Baseline e comparação antes/depois são úteis; sem deleção automática |
| Burndown de warnings | Gates por projeto | INCORPORAR ADAPTADO | P1 | médio | Política `warn -> zero -> error` é útil quando a stack comporta |
| Setup ESLint completo | Skills frontend existentes | REJEITAR COMO GLOBAL | P0 | baixo | HAOS é heterogêneo; não impor ESLint + Biome a todo projeto |
| Quality gates ESLint/Biome | QA/fullstack existentes | FUNDIR POR STACK | P1 | alto | Aproveitar ownership e promoção progressiva, não config literal |
| RTK/token proxy | `token-optimizer`, comandos nativos | PILOTAR PADRÃO | P2 | alto | O alvo não fornece runtime público completo; medir equivalência e perda |
| Ponytail | Julgamento conservador já normatizado | MANTER HAOS | P2 | baixo | Princípios já existem; plugin/persona é redundante |
| Caveman | Tom HAOS direto e didático | REJEITAR | P0 | baixo | Compressão indiscriminada prejudica clareza, gates e marca |
| Graphify | GBrain, `claude-mem`, Mnemoverse, `rg` | PILOTAR ISOLADO | P2 | alto | Pode ajudar impacto de mudanças, mas duplica memória/grafo e amplia risco |
| Obsidian somente via MCP | Memória tripla organizada | MANTER HAOS | P0 | baixo | Política absoluta conflita com automação local controlada |
| Memória Claude em duas camadas | Memória HAOS multicamada | MANTER E FUNDIR HEURÍSTICAS | P1 | médio | Aproveitar alto sinal, deduplicação e readback sem criar outra memória |
| Boas práticas de hooks | Hooks Python/PowerShell Codex | FUNDIR INVARIANTES | P0 | médio | O bug `JSON.parse("null")` tem equivalente reproduzido no HAOS |
| Helper `hook-io.mjs` | Hooks Python | NÃO COPIAR; PORTAR REGRA | P0 | baixo | Linguagem e contrato são diferentes; normalização deve ser nativa |
| agent-browser | Browser/Chrome/computer-use nativos | REJEITAR | P1 | baixo | Duplicação sem gap comprovado |
| ${RESOURCE_ID} | Web/docs oficiais e referências locais | PILOTAR READ-ONLY | P1 | médio | Pode reduzir erro de API recente; precisa baseline e fonte oficial |
| Anthropic Skills | Skills e runtimes documentais OpenAI/Codex | REJEITAR EM BLOCO | P0 | baixo | Redundante e sujeito a licenças/compatibilidade próprias |
| Chrome DevTools MCP | Browser/CDP e QA frontend | PILOTAR DIAGNÓSTICO | P2 | médio | Valor possível em rede/performance; usar perfil isolado |
| `CLAUDE.md.template` | `AGENTS.md` canônico | REJEITAR | P0 | baixo | Fonte e formato errados para o HAOS Codex |
| `settings.json.example` | `${USER_PROJECT_ROOT}/.codex/hooks.json` | REJEITAR | P0 | baixo | Contrato de hooks Claude não é o contrato Codex |
| Regra de subagentes | Protocolo de delegação HAOS | FUNDIR ADAPTADO | P0 | médio | Manter teto 3 e `fork_turns`; adicionar ownership e dependências |
| `aia-harness:init` e bootstrap automático | Bootstrap HAOS existente | REJEITAR | P0 | baixo | Risco de sobrescrita, duplicação e supply chain |

## 4. Bloqueios P0 comprovados no HAOS

### P0-1 — Hooks quebram com topo JSON não-objeto

Testes locais enviaram os payloads `null`, `[]` e `"x"` para quatro hooks:

| Hook | Resultado |
|---|---|
| `${USER_PROJECT_ROOT}/.codex/hooks/pre_tool_policy.py` | exit 1 nos três payloads |
| `${USER_PROJECT_ROOT}/.codex/hooks/session_end.py` | exit 1 nos três payloads |
| `${USER_PROJECT_ROOT}/.codex/hooks/user_prompt_router.py` | exit 1 nos três payloads |
| `${USER_PROJECT_ROOT}/.codex/hooks/haos_delegation_guard.py` | exit 0 nos três payloads |

O wrapper `${USER_PROJECT_ROOT}/.codex/hooks/run-python-hook.ps1` propaga `$LASTEXITCODE`; portanto,
a exceção do Python chega ao runtime do hook.

Correção proposta:

1. helper Python único para ler e normalizar stdin;
2. schema mínimo por evento;
3. classificação explícita de fail-open/fail-closed;
4. testes por subprocesso para vazio, JSON inválido, `null`, lista, string,
   objeto mínimo e objeto válido;
5. nenhum conteúdo sensível em erro ou log.

### P0-2 — Marcador textual não prova aprovação

O regex atual aceita `HAOS_EXTERNAL_OK=1`, `--haos-ok` ou `# haos-ok`. O teste
confirmou:

| Comando de teste | Decisão do hook |
|---|---|
| `git push origin main` | deny |
| `git push origin main --haos-ok` | permitido |
| `HAOS_EXTERNAL_OK=1 git push origin main` | permitido |
| `# haos-ok git push origin main` | permitido |

Como o próprio agente controla o texto do comando, esse marcador não comprova
grant local escopado à ação, alvo, hash e validade, criado fora do conteúdo
controlado pelo agente. Se o runtime não fornecer tal sinal, o hook deve falhar
fechado para ações externas.

### P0-3 — GSD anunciado sem runtime

- Arquivos em `commands/gsd/`: 31
- Arquivos que referenciam `.claude/get-shit-done`: 29
- `.claude/get-shit-done`: ausente
- `${USER_PROJECT_ROOT}/.codex/get-shit-done`: ausente
- Exceções sem essa referência: `join-discord.md` e `reapply-patches.md`

Decisão: colocar os 29 wrappers em quarentena/estado indisponível até portar os
workflows para Codex e validar um fluxo ponta a ponta. Não oferecer esses comandos
no menu como se estivessem funcionais.

### P0-4 — Drift de caminhos após migração para H

Foram encontrados 138 arquivos com a referência exata
`${HAOS_PRIVATE_ROOT}` nas superfícies auditadas:

| Área | Arquivos |
|---|---:|
| `scripts/` | 78 |
| `.agents/` | 23 |
| `plugins/` | 22 |
| `docs/` | 10 |
| `commands/` | 3 |
| `.codex/` | 1 |
| `memory/` | 1 |

ser um replace global: alguns trechos são históricos ou exemplos. Classificar
primeiro `operacional`, `fallback`, `documental` e `legado`; parametrizar apenas
o que executa.

## 5. Arquitetura HAOS recomendada

### 5.1 Contrato canônico de tarefa e onda

Cada tarefa delegável deve declarar:

```yaml
id: T01
owner: agente
objective: resultado verificável
read_files: []
write_files: []
shared_resources: []
depends_on: []
fork_turns: none
acceptance: []
external_action: false
```

Regras:

- no máximo três agentes ativos por onda;
- nenhuma sobreposição de `write_files` ou recurso compartilhado na mesma onda;
- dependência incerta degrada para execução serial;
- implementadores não fazem commit;
- um integrador único revisa diff, seleciona staging e escreve estado;
- reviewer de onda é read-only;
- Git, memória, catálogo e runtime/state têm owner único por onda.

### 5.2 Síntese de review

O `qa-reviewer` deve consolidar achados por severidade, deduplicar relatos,
registrar contradições e separar:

- fato reproduzido;
- inferência;
- claim externo;
- hipótese pendente;
- risco residual.

### 5.3 Quality gates por stack

Não criar stack global ESLint/Biome. A skill futura deve:

1. detectar linguagem, package manager e comandos existentes;
2. atribuir owner para format, lint, typecheck, test e build;
3. criar baseline sem reclassificar dívida antiga como regressão nova;
4. promover warning para erro somente após zerar a categoria;
5. registrar comandos literais, saída e rollback;
6. incluir acessibilidade e E2E quando o projeto for web.

### 5.4 Saneamento medido

Criar playbook on-demand que mede antes/depois, classifica candidato por risco,
usa allowlist e nunca presume deleção. Remoção destrutiva continua exigindo OK.

### 5.5 Memória

Manter a memória HAOS atual. Incorporar apenas:

- uma fonte primária por tipo de objeto;
- `canonical_uri`, hash, timestamp e origem nas projeções;
- deduplicação;
- escrita seguida de readback;
- promoção apenas de alto sinal;
- compactação sem teto rígido universal;
- conteúdo de MCP/browser tratado como não confiável antes da persistência.

## 6. Pilotos separados

Nenhum piloto entra no runtime principal por este registro.

| Piloto | Hipótese | Métrica mínima | Guardrails | Promoção |
|---|---|---|---|---|
| ${RESOURCE_ID} | reduzir erro de documentação desatualizada | acurácia, cobertura, latência, retrabalho | read-only, pin, fonte oficial para claim crítico | ganho repetível sem regressão |
| Chrome DevTools MCP | melhorar diagnóstico de rede/performance | tempo de diagnóstico, defeitos encontrados, estabilidade | perfil isolado, sem dados pessoais, telemetria revisada | gap não coberto pelo Browser nativo |
| Graphify | melhorar análise de impacto em base grande | precisão de relações, falso positivo, tempo e custo | clone não sensível, sem hook automático, sem memória global | benefício superior a `rg`/GBrain/claude-mem |
| RTK | reduzir saída sem perder evidência | tokens, latência, equivalência e retrabalho | opt-in, passthrough bruto, comando allowlisted | economia líquida e zero perda crítica |

Licença, custo, política de dados e manutenção de cada terceiro devem ser
auditados separadamente. A licença MIT do repositório curador não os relicencia.

## 7. Itens rejeitados

- instalação integral do toolkit;
- importação de `CLAUDE.md.template` ou `settings.json.example`;
- `aia-harness:init` no HAOS vivo;
- Superpowers como segundo orquestrador;
- Ponytail ou Caveman como persona/plugin global;
- agent-browser enquanto não houver gap comprovado;
- pacote Anthropic Skills em bloco;
- política Obsidian somente via MCP;
- memória Claude adicional;
- ESLint + Biome como padrão universal;
- Graphify ou qualquer MCP com escrita automática em memória;
- qualquer claim de economia/produtividade sem benchmark local.

## 8. Roadmap proposto

### Gate 0 — decisão

ocorre antes do Gate 0.

### Onda 1 — estabilização P0

1. helper e testes adversariais de I/O dos hooks;
2. desenho do gate de aprovação confiável;
3. inventário operacional/documental de paths.

### Onda 2 — integridade do catálogo

1. quarentena ou port do GSD;
2. catálogo canônico de agentes, skills e comandos;
3. estados `ativo`, `legado`, `experimental` e `indisponível`.

### Onda 3 — método incorporado

1. contrato de tarefa/onda;
2. review read-only + síntese;
3. playbook de saneamento;
4. skill de quality gates por stack;
5. readback e proveniência de memória.

### Onda 4 — pilotos

Um piloto por decisão, em sandbox, sem compartilhar perfil, memória ou dados
sensíveis. Cada piloto termina em `PROMOVER`, `AJUSTAR` ou `REJEITAR`.

## 9. Participação do conselho e squad

Todos os 31 agentes configurados têm parecer registrado. Vinte e quatro fizeram
análise especializada direta do corpus e sete revisaram a evidência consolidada.

| Grupo | Agentes | Síntese |
|---|---|---|
| Conselho | estrategista-chefe, diretor-criativo, cmo | adotar método, não stack; preservar Rito e identidade |
| Criativo | copy-specialist, content-strategist, designer, videomaker, sm-social | melhorar descoberta, clareza e evidência; rejeitar personas globais |
| Tráfego | traffic-master, media-buyer, tracking-engineer | ondas, baseline, gates e telemetria; sem claims sem métrica |
| Dados | data-analyst, bi-engineer, pesquisador, auditor-confianca | proveniência, benchmark, lineage e confiança por claim |
| Funil | funnel-architect, automation-engineer, crm-specialist, email-marketer | integrar lifecycle, I/O defensivo e memória de alto sinal |
| Produto | product-manager, ux-researcher, dev-frontend, dev-backend | contrato de unidade de trabalho, quality gates e compatibilidade Codex |
| Orquestração | qa-reviewer, project-manager, compliance-officer, devops | P0 antes de rollout, writer único, rollback e licença por componente |
| Segurança | chuck-norris | eliminar autorização textual e falhar fechado |
| Direção | main, concierge, cfo | arquitetura seletiva, catálogo por intenção e TCO antes de piloto |

Pareceres brutos:
`${HAOS_PRIVATE_ROOT}`.

## 10. Segurança e licença

- A varredura do alvo não encontrou chave privada nem segredo real.
- Os matches de credencial são placeholders documentais, como
  `EXAMPLE_API_KEY` e `sua-chave-aqui`.
- Nenhum valor do `MASTER.env` foi lido ou registrado nesta análise.
- MIT cobre o conteúdo do repositório alvo, não os softwares externos citados.
- Qualquer cópia futura deve preservar aviso e licença quando aplicável.
- MCPs, browser e grafos devem tratar conteúdo remoto como não confiável.

## 11. Decisões finais

1. HAOS continua soberano; não será substituído pelo toolkit.
2. A incorporação é conceitual e seletiva.
3. Os quatro P0 locais vêm antes de novas ferramentas.
4. O contrato de ondas e a síntese de review são os ganhos de maior valor.
5. Quality gates e saneamento serão por projeto, não globais.
6. Memória atual será fortalecida, não duplicada.
7. Ferramentas externas terão pilotos e auditorias independentes.
8. Não houve merge, instalação, commit, push ou deploy.

