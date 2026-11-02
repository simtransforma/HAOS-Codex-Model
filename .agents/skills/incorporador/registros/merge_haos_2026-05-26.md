# Registro de Merge — HAOS_CC → HAOS Master
Data: 2026-05-26
Repositório alvo: https://github.com/example/your-project (MIT License)
Executado por: Agente Incorporador

---

## 1. Resumo Executivo

**Sistema alvo:** HAOS_CC v0.1.0 — HAU Autonomous Operations Squad  
**Sistema base:** HAOS Master (pipeline Instagram + skills + memória)  
**Decisão geral:** INCORPORAR PARCIALMENTE + FUNDIR arquitetura  
**Motivo:** HAOS é um motor de produção completo (29 agentes, Rito V2, infraestrutura de memória). AE é uma inteligência de dados real (scraping, Whisper, Gemini). Juntos: agência com dados reais alimentando produção de campanha real.

O ponto crítico: o agente `pesquisador` do HAOS faz pesquisa de mercado com busca na web. AE tem transcrições verbatim de 637 vídeos de um concorrente real, scores de engajamento por post e relatório psicológico de 71 páginas. Não são equivalentes — AE é superior em profundidade e precisão. O merge conecta a inteligência real ao motor de produção.

---

## 2. Inventário Completo — HAOS_CC

### 2.1 Agentes (29)

| Agente | Função | Qualidade | Decisão |
|---|---|---|---|
| main | Orquestrador, roteador, Rito V2 | ⭐⭐⭐⭐⭐ | INCORPORAR |
| estrategista-chefe | Estratégia, posicionamento | ⭐⭐⭐⭐ | INCORPORAR |
| cmo | CMO, decisões de produto/posicionamento | ⭐⭐⭐⭐ | INCORPORAR |
| copy-specialist | Copywriting, VSL, emails, ads | ⭐⭐⭐⭐⭐ | INCORPORAR |
| diretor-criativo | Aprovação criativa, direção visual | ⭐⭐⭐⭐ | INCORPORAR |
| designer | Briefing visual, criativos | ⭐⭐⭐⭐ | INCORPORAR |
| videomaker | Roteiros, legendas, edição | ⭐⭐⭐⭐ | INCORPORAR |
| content-strategist | Pauta, calendário editorial | ⭐⭐⭐⭐ | INCORPORAR + FUNDIR |
| email-marketer | Sequências de email | ⭐⭐⭐⭐ | INCORPORAR |
| crm-specialist | CRM, WhatsApp, mensageria | ⭐⭐⭐⭐ | INCORPORAR |
| funnel-architect | Funis, jornada do lead | ⭐⭐⭐⭐ | INCORPORAR |
| traffic-master | Estratégia de tráfego | ⭐⭐⭐⭐ | INCORPORAR |
| media-buyer | Compra de mídia, Meta/Google Ads | ⭐⭐⭐⭐ | INCORPORAR |
| tracking-engineer | Pixel, CAPI, GTM | ⭐⭐⭐⭐ | INCORPORAR |
| bi-engineer | Dashboards, relatórios de BI | ⭐⭐⭐⭐ | INCORPORAR |
| data-analyst | Análise de dados, insights | ⭐⭐⭐⭐ | INCORPORAR + FUNDIR |
| automation-engineer | Automações, webhooks | ⭐⭐⭐⭐ | INCORPORAR |
| dev-backend | Backend, APIs, banco de dados | ⭐⭐⭐⭐ | INCORPORAR |
| dev-frontend | Frontend, UI, otimização | ⭐⭐⭐⭐ | INCORPORAR |
| devops | Deploy, infraestrutura | ⭐⭐⭐⭐ | INCORPORAR |
| qa-reviewer | QA, testes, checklist de go-live | ⭐⭐⭐⭐ | INCORPORAR |
| compliance-officer | Conformidade, LGPD, políticas plataforma | ⭐⭐⭐⭐ | INCORPORAR |
| project-manager | Gestão de projeto, WBS, cronograma | ⭐⭐⭐⭐ | INCORPORAR |
| pesquisador | Pesquisa de mercado (web) | ⭐⭐⭐ | SUBSTITUIR por versão AE (dados reais) |
| product-manager | Produto, roadmap, features | ⭐⭐⭐⭐ | INCORPORAR |
| ux-researcher | UX, pesquisa de usuário | ⭐⭐⭐⭐ | INCORPORAR |
| sm-social | Social media, publicação | ⭐⭐⭐⭐ | INCORPORAR |
| concierge | Onboarding, primeiro contato | ⭐⭐⭐ | INCORPORAR |
| chuck-norris | Executa tarefas sem pedir permissão | ⭐⭐⭐ | INCORPORAR (uso específico) |

### 2.2 Slash Commands (45)

Todos os 45 comandos `/haos:*` — um por agente + comandos de orquestração:
`menu`, `agentes`, `departamentos`, `rito`, `base`, `orquestracao`, `conselho`, `emergencia`, `seguranca`, `setup`, `main`, `criativo`, `funnel`, `trafego`, `dados`, `produto`, `mb` (media buy) + um por agente.

Decisão: INCORPORAR todos, renomear namespace `/haos:` → `/ae:`

### 2.3 Skills (19)

| Skill | Utilidade para AE | Decisão |
|---|---|---|
| marketing-expert | ⭐⭐⭐⭐⭐ — 30+ gatilhos mentais, fórmulas, headlines | INCORPORAR imediatamente |
| landing-page-prd-architect | ⭐⭐⭐⭐⭐ — complementa vibe-designer | INCORPORAR |
| seo-optimizer | ⭐⭐⭐⭐ — útil para sites criados | INCORPORAR |
| youtube-content-generator | ⭐⭐⭐⭐ — roteiros, títulos, thumbnails | INCORPORAR |
| fullstack-dev | ⭐⭐⭐⭐ — dev completo | INCORPORAR |
| software-architecture | ⭐⭐⭐⭐ — arquitetura de sistemas | INCORPORAR |
| software-engineer | ⭐⭐⭐⭐ — engenharia de software | INCORPORAR |
| design-principles | ⭐⭐⭐⭐ — princípios de design | INCORPORAR + FUNDIR com vibe-designer |
| hero-visual-prompt-generator | ⭐⭐⭐⭐ — prompts visuais | INCORPORAR |
| prd-brainstorm | ⭐⭐⭐ — brainstorm de produtos | INCORPORAR |
| mobile-responsiveness | ⭐⭐⭐⭐ — mobile QA | INCORPORAR |
| sprint-context-generator | ⭐⭐⭐ — contexto de sprint ágil | INCORPORAR |
| long-running-agent | ⭐⭐⭐⭐ — tarefas longas (útil para pipeline AE) | INCORPORAR |
| skill-creator | ⭐⭐⭐ — similar ao skill-creator-pro de AE | SUBSTITUIR pelo de AE (mais avançado) |
| skill-auditor-v2 | ⭐⭐⭐ — auditoria de skills | INCORPORAR |
| ralph-prompt-builder | ⭐⭐⭐ — construção de prompts | INCORPORAR |
| lisa-prompt-engineering | ⭐⭐⭐ — engenharia de prompts | INCORPORAR |
| last30days-skill | ⭐⭐⭐ — análise de últimos 30 dias | AVALIAR |
| ffuf-skill | ⭐ — teste de segurança (não relevante para AE) | DESCARTAR |

### 2.4 Infraestrutura

| Componente | O que faz | Qualidade | Decisão |
|---|---|---|---|
| hooks/session_start.py | Injeta memória + sessões recentes + rito ativo no contexto | ⭐⭐⭐⭐⭐ | INCORPORAR |
| hooks/session_end.py | Salva resumo da sessão | ⭐⭐⭐⭐⭐ | INCORPORAR |
| hooks/post_compact.py | Atualiza memória após compactação | ⭐⭐⭐⭐⭐ | INCORPORAR |
| memory/rito_state.json | Estado persistente do Rito V2 | ⭐⭐⭐⭐⭐ | INCORPORAR |
| memory/bootstrap.md | Perfil do projeto (via /haos:setup) | ⭐⭐⭐⭐ | INCORPORAR + ADAPTAR |
| .claude-plugin/plugin.json | Manifest do plugin | ⭐⭐⭐⭐ | INCORPORAR + RENOMEAR |

### 2.5 Pipeline Rito V2 (13 fases)

O pipeline mais valioso do HAOS. Gates bloqueantes, persistência de estado, aprovações humanas em pontos críticos. Especialmente valioso:
- Fase 2 (Pesquisa) — onde AE se encaixa perfeitamente
- Fase 5 (Copy) — copy-specialist usa vocabulário do relatório AE
- Fase 13 (Debrief) — aprende e atualiza memória

---

## 3. Inventário Completo — HAOS Master (base)

| Componente | O que faz | Qualidade |
|---|---|---|
| rankear_posts.py | Scraping + scoring de 500+ posts | ⭐⭐⭐⭐⭐ |
| baixar_hits.py | Download MP3 dos top reels | ⭐⭐⭐⭐⭐ |
| transcrever_hits.py | Whisper → transcrição verbatim | ⭐⭐⭐⭐⭐ |
| relatorio_completo.py | 70+ páginas via Gemini 2.5 Flash | ⭐⭐⭐⭐⭐ |
| analisador-de-nicho (skill) | Orquestra o pipeline completo | ⭐⭐⭐⭐⭐ |
| incorporador (skill) | Análise e merge de sistemas | ⭐⭐⭐⭐ |
| vibe-designer (skill) | Direção criativa → prompt Lovable | ⭐⭐⭐⭐⭐ |
| head-de-marketing (skill) | CMO sênior, aprovação editorial | ⭐⭐⭐⭐⭐ |
| lovable-publisher (skill) | Deploy automático via Lovable MCP | ⭐⭐⭐⭐⭐ |
| page-analyst (skill) | Análise visual de páginas com screenshot | ⭐⭐⭐⭐⭐ |
| skill-creator-pro (skill) | Cria skills completas com pesquisa web | ⭐⭐⭐⭐⭐ |
| Memória (MEMORY.md + arquivos) | Sistema de memória persistente | ⭐⭐⭐⭐⭐ |

---

## 4. Matriz Comparativa

| Capacidade | HAOS | AE | Scores | Decisão |
|---|---|---|---|---|
| Inteligência de mercado (dados reais) | ❌ só web | ✅ Whisper + Gemini | 2 / 5 | AE GANHA — MANTER |
| Transcrição de vídeo concorrente | ❌ | ✅ | 0 / 5 | AE EXCLUSIVO |
| Score de engajamento por post | ❌ | ✅ | 0 / 5 | AE EXCLUSIVO |
| Relatório psicológico 70 páginas | ❌ | ✅ | 0 / 5 | AE EXCLUSIVO |
| Copywriting especializado | ✅ copy-specialist | ⚠️ via head-de-marketing | 5 / 3 | HAOS GANHA — INCORPORAR |
| Funil completo | ✅ funnel-architect | ❌ | 5 / 0 | HAOS — INCORPORAR |
| Tráfego pago | ✅ traffic-master + media-buyer | ❌ | 5 / 0 | HAOS — INCORPORAR |
| Tracking / Analytics | ✅ tracking-engineer + bi-engineer | ❌ | 5 / 0 | HAOS — INCORPORAR |
| Deploy / DevOps | ✅ devops | ❌ | 5 / 0 | HAOS — INCORPORAR |
| Criação de site (Lovable) | ❌ | ✅ vibe-designer + publisher | 0 / 5 | AE EXCLUSIVO |
| Análise visual de páginas | ❌ | ✅ page-analyst | 0 / 5 | AE EXCLUSIVO |
| Pipeline de produção (marketing) | ✅ Rito V2, 13 fases | ⚠️ fragmentado | 5 / 2 | HAOS GANHA — INCORPORAR |
| Memória persistente (hooks) | ✅ Python hooks | ✅ Claude Code built-in | 5 / 4 | FUNDIR os dois |
| Compliance / QA | ✅ compliance-officer + qa-reviewer | ❌ | 5 / 0 | HAOS — INCORPORAR |
| Skills de copywriting/marketing | ✅ marketing-expert (30+ gatilhos) | ⚠️ parcial | 5 / 3 | HAOS GANHA — INCORPORAR |
| Gestão de projeto (WBS, cronograma) | ✅ project-manager | ❌ | 5 / 0 | HAOS — INCORPORAR |
| CRM / Email / Mensageria | ✅ crm-specialist + email-marketer | ❌ | 5 / 0 | HAOS — INCORPORAR |
| Criação de skills | ✅ skill-creator | ✅ skill-creator-pro (melhor) | 3 / 5 | AE GANHA — AE substitui HAOS |
| Orquestração multi-agente | ✅ main (excelente) | ⚠️ orchestrador (parcial) | 5 / 3 | HAOS GANHA — FUNDIR |
| Desenvolvimento de produto | ✅ product-manager + ux-researcher | ❌ | 5 / 0 | HAOS — INCORPORAR |

---

## 5. O Que Cada Sistema Tem de Exclusivo

### AE Exclusivo (HAOS nunca vai ter sem o merge)
1. **Transcrições verbatim** de vídeos reais — o que o criador literalmente diz
2. **engajamento_score** quantitativo por post — o que o público realmente responde
3. **Relatório psicológico 71 páginas** — dores, gatilhos, vocabulário confirmados por dados
4. **Criação autônoma de sites** — vibe-designer → HM → Lovable publisher
5. **Análise visual de páginas** com Playwright (screenshot + visão)
6. **Incorporador** — meta-agente para merge de sistemas
7. **skill-creator-pro** — pesquisa web + entrevista + entrega ZIP

### HAOS Exclusivo (AE nunca vai ter sem o merge)
1. **copy-specialist** — VSL, headlines, sequências email, A/B obrigatório
2. **Rito V2** — pipeline de 13 fases com gates e estado persistente
3. **funnel-architect + automation-engineer** — funis completos testados
4. **traffic-master + media-buyer** — estratégia e compra de mídia paga
5. **tracking-engineer + bi-engineer** — pixel, CAPI, dashboards
6. **compliance-officer** — LGPD, políticas de plataforma
7. **Python hooks de memória** — injeção automática de contexto no SessionStart
8. **marketing-expert skill** — biblioteca de 30+ gatilhos mentais, fórmulas, exemplos

---

## 6. Plano de Merge Detalhado

### QUICK WINS — Prioridade Alta + Esforço Pequeno

**[M01] Importar skills de alta qualidade do HAOS**
- Ação: INCORPORAR
- Origem: `HAOS_CC/skills/marketing-expert/`, `landing-page-prd-architect/`, `seo-optimizer/`, `youtube-content-generator/`, `hero-visual-prompt-generator/`, `design-principles/`, `mobile-responsiveness/`
- Destino: `~/.claude/skills/` (cada uma em sua pasta)
- Adaptações: nenhuma — são skills standalone, funcionam imediatamente
- Ganho: biblioteca de copywriting de alta conversão, SEO, YouTube, design visual
- Status: ✅ CONCLUÍDO — 7 skills instaladas em 2026-05-26

**[M02] Instalar hooks Python de memória**
- Ação: INCORPORAR + ADAPTAR
- Destino: `~/.claude/hooks/agencia-express/` + settings.json
- Adaptações: branding "HAOS" → "HAOS Master"; hooks adicionados ao settings.json preservando pixel-agents
- Hooks instalados: session_start.py, session_end.py, post_compact.py
- Eventos: SessionStart, Stop, PostCompact
- Testado: session_start.py retorna JSON válido com MEMORY.md + sessões recentes
- Status: ✅ CONCLUÍDO — 2026-05-26

**[M03] Criar plugin.json da HAOS Master**
- Ação: CRIAR
- Destino: `${HAOS_PRIVATE_ROOT}`
- Conteúdo: nome, versão, 9 departamentos, pipeline Rito V2, stack de inteligência
- Status: ✅ CONCLUÍDO — 2026-05-26

---

### HIGH VALUE — Prioridade Alta + Esforço Médio

**[M04] Incorporar os 29 agentes de produção do HAOS**
- Ação: INCORPORAR
- Destino: `${HAOS_PRIVATE_ROOT}` (29 arquivos .md)
- Adaptações: `/haos:` → `/hm:` em todos os arquivos; main.md recebeu linha de inteligência Instagram e modo Rito V2 Enhanced
- Ganho: 29 especialistas de produção prontos para usar com namespace /hm:
- Status: ✅ CONCLUÍDO — 2026-05-26

**[M05] Integração de inteligência no main.md**
- Ação: FUNDIR
- Adicionado ao main.md: delegação para analisador-nicho, modo `# --intel @handle`
- O orquestrador agora conhece o pipeline de inteligência
- Status: ✅ CONCLUÍDO — 2026-05-26

**[M06] Rito V2 Enhanced documentado**
- Ação: CRIAR
- Criado `commands/intel-rito.md` com especificação completa do Rito V2 com --intel flag
- Documenta exatamente quais campos do relatório vão para cada fase (2, 3, 5, 6)
- Status: ✅ CONCLUÍDO — 2026-05-26

**[M07] Incorporar 45 comandos + 2 novos de inteligência**
- Ação: INCORPORAR + CRIAR
- Destino: `${HAOS_PRIVATE_ROOT}` (47 arquivos)
- 45 do HAOS original com namespace `/haos:` → `/hm:`
- 2 novos exclusivos HAOS Master: `intel.md` + `intel-rito.md`
- Status: ✅ CONCLUÍDO — 2026-05-26

---

### NOVOS ARTEFATOS A CRIAR

**[N01] Departamento @inteligencia (9º departamento)**
- Tipo: 3 novos agentes
- Agentes:
  - `pesquisador-instagram.md` — scraping + ranking (substitui pesquisador HAOS)
  - `analisador-nicho.md` — Whisper + Gemini + relatório 70 páginas
  - `estrategista-competitivo.md` — lê relatório, cruza com brief do cliente, entrega gaps
- Integração com Rito V2: são chamados na Fase 2
- Esforço: ~3 horas
- Prioridade: ALTA

**[N02] Comandos de inteligência `/ae:intel`**
- Tipo: 4 novos comandos
  - `/ae:pesquisar @handle` — scraping + ranking
  - `/ae:analisar @handle` — pipeline completo
  - `/ae:monitorar @handle --dias 30` — análise periódica
  - `/ae:intel-brief @handle @cliente` — brief pré-rito com dados reais
- Esforço: ~1 hora
- Prioridade: ALTA

**[N03] `${USER_PROJECT_ROOT}/memory/bootstrap.md` para HAOS Master**
- Conteúdo: perfil do projeto AE, clientes, metodologia, stack
- Injetado automaticamente no SessionStart via hooks
- Esforço: ~30 minutos
- Prioridade: MÉDIA

**[N04] Rito V2 Enhanced — com intelligence flag**
- Novo argumento: `/ae:rito # --intel @concorrente`
- Quando passado: Fase 2 pula pesquisa web e usa dados reais do @concorrente
- Fase 5 (copy) recebe vocabulario_de_marca do relatório como contexto obrigatório
- Fase 3 (estratégia) recebe gaps e oportunidades do relatório
- Esforço: ~3 horas
- Prioridade: ALTA

---

## 7. Conflitos e Resoluções

| Conflito | HAOS | AE | Resolução |
|---|---|---|---|
| Namespace de comandos | `/haos:*` | `/ae:*` | `/ae:*` — é um fork, tem identidade própria |
| Sistema de memória | Python hooks | Claude Code built-in | Usar AMBOS — hooks injetam no startup, Claude auto-memory é o registro primário |
| Skill de criação de skills | skill-creator (simples) | skill-creator-pro (com pesquisa web + entrevista) | AE vence — HAOS skill descartada |
| Orquestrador | main (sofisticado, Rito V2) | orchestrador (mais simples) | HAOS vence — main incorporado como `/ae:main` |
| Pesquisa de mercado | web search (estimativas) | dados reais Instagram | AE vence — pesquisador-instagram substitui pesquisador |
| CMO / Head de Marketing | cmo (agente HAOS) | head-de-marketing (skill AE) | Manter AMBOS: cmo para estratégia, HM para aprovação editorial |

---

## 8. Decisões de Arquitetura

1. **Fork, não plugin:** HAOS é instalado como plugin (`claude install`). AE é um produto independente. Estrutura: `agencia-express/` com `.claude-plugin/plugin.json` próprio, renomeado.

2. **Namespace `/ae:*`:** Todos os comandos usam `/ae:` — identidade clara e sem conflito caso o usuário tenha o HAOS original instalado paralelamente.

3. **9 departamentos, não 8:** HAOS tem 8. AE adiciona `@inteligencia` como o 9º — o diferencial competitivo real.

4. **Hooks Python são a fundação da memória:** Os hooks do HAOS (session_start/end/post_compact) são superiores à memória manual. Incorporar e adaptar para injetar o contexto do AE automaticamente.

5. **Rito V2 é o backbone de produção:** Não reinventar. Adotar o Rito V2 inteiro e adicionar uma extensão de inteligência opcional (flag `--intel`).

6. **pesquisador-instagram substitui pesquisador:** O agente pesquisador do HAOS é web-search only. AE o substitui com dados primários reais — mas mantém o fallback para quando não há relatório disponível.

7. **skills AE têm prioridade sobre HAOS quando há sobreposição:** vibe-designer > designer HAOS para criação de sites. skill-creator-pro > skill-creator HAOS. head-de-marketing AE + cmo HAOS coexistem (funções complementares).

---

## 9. Roadmap de Execução

```
SPRINT 1 — Quick Wins (1-2 horas)
  ⬜ [M01] Copiar 5 skills HAOS de alta qualidade para ~/.claude/skills/
  ⬜ [M02] Instalar e adaptar hooks Python de memória
  ⬜ [M03] Criar plugin.json da HAOS Master

SPRINT 2 — Motor de Produção (3-4 horas)
  ⬜ [M04] Incorporar 28 agentes HAOS
  ⬜ [M07] Incorporar 45 comandos com namespace /ae:

SPRINT 3 — Integração da Inteligência (5-6 horas)
  ⬜ [N01] Criar departamento @inteligencia (3 agentes)
  ⬜ [N02] Criar comandos /ae:intel
  ⬜ [M05] Substituir pesquisador HAOS por pesquisador-instagram AE
  ⬜ [M06] Adaptar Rito V2 Fase 2 com dados reais

SPRINT 4 — Polimento (2-3 horas)
  ⬜ [N03] Criar bootstrap.md do projeto AE
  ⬜ [N04] Implementar Rito V2 Enhanced com --intel flag
  ⬜ Testar pipeline end-to-end: /ae:analisar @handle → /ae:rito # --intel @handle
```

**Tempo total estimado: 12-16 horas de implementação.**

---

## 10. Fluxo Final Unificado

```
FLUXO HAOS Master v2.0

INTELIGÊNCIA (exclusivo AE)
  /ae:analisar @concorrente
  → scraping 500+ posts → download reels → Whisper → Gemini
  → relatorio_completo_{handle}.json (13 seções, 70 págs)

PRODUÇÃO (HAOS + intel AE)
  /ae:rito # Brief do cliente --intel @concorrente

  Fase 1 — Intake (main + project-manager)
    Gate: briefing validado pelo usuário

  Fase 2 — Pesquisa ENHANCED (pesquisador-instagram + data-analyst)
    Input: relatorio_completo_{concorrente}.json (dados reais)
    Gate: diagnóstico com dados reais documentados

  Fase 3 — Estratégia (estrategista-chefe + cmo + diretor-criativo)
    Input: gaps e oportunidades do relatório AE
    Gate: @conselho aprova

  Fase 4 — Planejamento (project-manager + traffic-master + funnel-architect)

  Fase 5 — Copy ENHANCED (copy-specialist + email-marketer)
    Input: vocabulario_de_marca + gatilhos_mentais + frases_de_impacto do relatório
    Gate: diretor-criativo + compliance

  Fase 6 — Design (designer + videomaker + content-strategist)
    Input: pilares_de_conteudo + tom_de_voz do relatório

  ... [Fases 7-13 padrão HAOS] ...

  Fase 13 — Debrief
    Output: memória atualizada, bootstrap.md enriquecido
```

---

