# Capacidades e importabilidade

## Escopo da selecao

Inventario por nomes e metadados: 193 entradas com SKILL.md entre 195
diretorios consultados; dois diretorios sem SKILL.md nao sao skills verificadas.
A estimativa de 196 nao foi tratada como contagem confirmada. Inventariar nao e
ler todo o conteudo, conceder licenca nem tornar um catalogo privado distribuivel.
Os identificadores sensiveis/operacionais nao sao publicados neste inventario.

Este modelo tem 29 skills originais: 8 existentes ampliadas e 21 novas. Inclui
34 papeis (30 preservados e 4 novos) e 21 rotas declarativas. A matriz
[skill-routing](../.codex/skill-routing.json) contem apenas caminhos repository-root,
nomes reais, descricoes e associacoes. **Arquivos nao sao runtime.** Nao ha plugin
de slash commands, hook ativo, registro automatico de agentes ou prova de hot reload.

## Incluidos

- Melhorias nas oito skills-base: engenharia, evidencia, ondas, memoria, Rito,
  roteamento, seguranca e isolamento Git opcional.
- Skills novas de fechamento/proveniencia, roteamento consultivo de modelos,
  adaptacao de metodos, gates, loop finito, pesquisa/claims/fontes, design/copy,
  revisao, refatoracao, conhecimento, menu, conselho, departamentos e squad.
- Handoff, dump saneado e importacao nao confiavel sao operacoes distintas.
- Templates sao apenas schema/exemplo inativo, sem estado operacional real.

## Criterios dos papeis novos

| Papel | Lacuna coberta | Limite |
| --- | --- | --- |
| main | Integracao e fechamento unico da tarefa | Nao confundir orquestracao com execucao especializada. |
| oraculo | Precedentes, contradicoes e pontos cegos antes da estrategia | Nao transforma memoria em fato atual nem parecer juridico. |
| brabo | Analise juridica baseada em jurisdicao e documentos primarios | Nao substitui profissional habilitado nem seguranca tecnica. |
| relacionamento-editorial | Triagem editorial autorizada com origem e direitos | Nao inclui comunicacao pessoal, monitoramento ou publicacao automatica. |

O papel security-reviewer permanece exclusivo de seguranca tecnica. O conselho
preserva estrategista-chefe, diretor-criativo e cmo como nucleo decisor. Oraculo e
brabo fornecem insumos; cfo participa quando houver decisao financeira. Primeiro
coletar insumos, depois deliberar com o nucleo, em ondas de ate tres e sem
prometer uma ferramenta indisponivel.

## Classes de importabilidade

| Classe | Significado | Quantidade |
| --- | --- | --- |
| incluido | Capacidade realmente escrita neste modelo | 29 skills / 34 papeis |
| adaptado | Metadado selecionado orientou sintese original; conteudo nao foi copiado | 26 fontes genericas |
| dependency_opt | Metodo, ferramenta ou conteudo externo nao embarcado | 40 fontes genericas |
| excluido | Fora de escopo ou direitos/conteudo nao auditados | 84 fontes genericas |
| excluido restrito | APIs operacionais, dominio privado, clientes ou pessoal; identificadores omitidos | 43 entradas |

As 150 entradas genericas abaixo e as 43 exclusoes restritas reconciliam
as 193 entradas verificadas. dependency_opt nao significa que a ferramenta esteja
instalada ou que sua licenca tenha sido verificada. Uma capacidade incluida pode
reunir varias fontes conceituais, e nao promete paridade com cada skill original.

## Inventario nominal generico

| Nome no catalogo consultado | Classe | Decisao |
| --- | --- | --- |
| `ab-testing` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `active-prospecting` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `ad-creative` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `ads` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `ai-seo` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `amazon-seller` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `analytics` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `assess-ticketing-security` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `benchmark-modelo-llm` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `cashflow-forecast` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `churn-prevention` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `claude-handoff-to-codex` | adaptado | Sintese original em `haos-dump-import`; nao copia o arquivo de origem. |
| `clean-prospect-lists` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `cloudflare` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `cold-email` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `community-marketing` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `competitor-profiling` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `composition-patterns` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `content-strategy` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `copy-editing` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `copywriting` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `cro` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `customer-research` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `data-quality-frameworks` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `deploy-to-vercel` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `design-principles` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `design-taste-frontend` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `emails` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `escrita-ptbr` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `feedback-interpreter` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `ffuf-skill` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `find-skills` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `fullstack-dev` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `ga4` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `google-ads-copy-format` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-auto-brain` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-catalog-integrity` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-caveman-compression` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `haos-chrome-devtools-mcp` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `haos-claim-verification` | adaptado | Sintese original em `haos-claim-verification`; nao copia o arquivo de origem. |
| `haos-company-trust-audit` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-context7-docs` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `haos-deep-research` | adaptado | Sintese original em `haos-deep-research`; nao copia o arquivo de origem. |
| `haos-design` | adaptado | Sintese original em `haos-design`; nao copia o arquivo de origem. |
| `haos-evoluir` | adaptado | Sintese original em `haos-evoluir`; nao copia o arquivo de origem. |
| `haos-execution-waves` | adaptado | Sintese original em `haos-execution-waves`; nao copia o arquivo de origem. |
| `haos-external-approval` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-find-skills` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-forja-agente` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-graphify-code-map` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `haos-local-research` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-mega-brain` | adaptado | Sintese original em `haos-mega-brain`; nao copia o arquivo de origem. |
| `haos-mega-brain-lite` | adaptado | Sintese original em `haos-mega-brain`; nao copia o arquivo de origem. |
| `haos-memory-provenance` | adaptado | Sintese original em `haos-memory-provenance`; nao copia o arquivo de origem. |
| `haos-memory-triple` | adaptado | Sintese original em `haos-memory`; nao copia o arquivo de origem. |
| `haos-model-router` | adaptado | Sintese original em `haos-model-router`; nao copia o arquivo de origem. |
| `haos-multi-agent-review` | adaptado | Sintese original em `haos-multi-agent-review`; nao copia o arquivo de origem. |
| `haos-project-sanitation` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-quality-gates` | adaptado | Sintese original em `haos-quality-gates`; nao copia o arquivo de origem. |
| `haos-query-expansion` | adaptado | Sintese original em `haos-deep-research`; nao copia o arquivo de origem. |
| `haos-radar-semanal` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-rag-corpus-oficial` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `haos-ralph-loop` | adaptado | Sintese original em `haos-task-loop`; nao copia o arquivo de origem. |
| `haos-research-report-writer` | adaptado | Sintese original em `haos-deep-research`; nao copia o arquivo de origem. |
| `haos-rito-v2` | adaptado | Sintese original em `haos-rito-v2`; nao copia o arquivo de origem. |
| `haos-router` | adaptado | Sintese original em `haos-router`; nao copia o arquivo de origem. |
| `haos-source-quality-auditor` | adaptado | Sintese original em `haos-source-quality-auditor`; nao copia o arquivo de origem. |
| `haos-structural-refactor` | adaptado | Sintese original em `haos-structural-refactor`; nao copia o arquivo de origem. |
| `haos-superpowers` | adaptado | Sintese original em `haos-superpowers`; nao copia o arquivo de origem. |
| `hero-visual-prompt-generator` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `impeccable` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `instagram-carousel` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `interface-design` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `interpretar-video` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `javascript-testing-patterns` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `json-canvas` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `landing-page-prd-architect` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `last30days-skill` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `launch` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `lead-magnets` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `ler-pdf-local` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `limpar-lista-contatos` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `lisa-prompt-engineering` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `long-running-agent` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `marketing-expert` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `marketing-ideas` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `marketing-psychology` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `media-kit-builder` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `mega-brain` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `meta-ads-copy-format` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `meta-ads-policy` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `miro-board-builder` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `mnemoverse-codex` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `mobile-responsiveness` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-ai-agent-link-governance` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-binary-and-data-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-code-nodes-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-credentials-and-security-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-debugging-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-error-handling-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-expressions-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-loops-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-node-configuration-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-subworkflows-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `n8n-workflow-lifecycle-official` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `obsidian-bases` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `obsidian-cli` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `obsidian-markdown` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `obsidian-organizer` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `openapi-spec-generation` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `outlier-post-finder` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `page-analyst` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `prd-brainstorm` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `product-marketing` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `project-artifact-governance` | adaptado | Sintese original em `haos-memory-provenance`; nao copia o arquivo de origem. |
| `prompt-master` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `ralph-prompt-builder` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `react-best-practices` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `react-native-skills` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `react-view-transitions` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `review-ticketing-business-logic` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `run-security-assessment-playbooks` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `saga-orchestration` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `schema` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `second-opinion` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `seo-optimizer` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `session-full-dump` | adaptado | Sintese original em `haos-session-dump`; nao copia o arquivo de origem. |
| `session-handoff` | adaptado | Sintese original em `haos-session-handoff`; nao copia o arquivo de origem. |
| `skill-auditor-v2` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `skill-creator` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `social` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `software-architecture` | adaptado | Sintese original em `haos-engineering`; nao copia o arquivo de origem. |
| `software-engineer` | adaptado | Sintese original em `haos-engineering`; nao copia o arquivo de origem. |
| `sprint-context-generator` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `supabase` | dependency_opt | Conteudo/implementacao nao distribuidos; exige selecao, licenca e configuracao independentes. |
| `tiktok-ads-copy-format` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `tiktok-ads-fundamentals` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `tiktok-bi-metrics` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `tiktok-creative-playbook` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `tiktok-shop-fundamentals` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `tiktok-tracking-setup` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `token-optimizer` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `trend-discovery` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `unit-economics` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `vercel-cli-with-tokens` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `vercel-optimize` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `vibe-designer` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `youtube-content-generator` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `youtube-media-kit-generator` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |
| `youtube-seo` | excluido | Fora do recorte funcional desta entrega ou licenca/conteudo nao auditados; nenhum texto redistribuido. |

## Integracoes e exclusoes

Toqi e JEV sao somente integracoes opcionais mencionadas: nenhum cliente, endpoint,
modelo, token, transporte ou classificador desses sistemas e incluido. Configurar
qualquer integracao exige tarefa propria, documentacao vigente, escopo e validacao.
Memoria remota, browser, mapa de codigo e metodos auxiliares tambem sao opcionais;
indisponibilidade e registrada, nao simulada. Sem fallback para conta pessoal.

Nao se distribuem voz proprietaria, personas privadas, APIs/configuracoes de negocio,
segredos, paths privados, memoria real, dumps brutos ou conteudo terceiro sem licenca.
O adaptador Superpowers nao contem o upstream. writing-skills orientou a verificacao
por cenarios, nao foi copiado. Ver [proveniencia](provenance.md) e
[autoria de skills](skill-authoring.md) para limites das evidencias.
