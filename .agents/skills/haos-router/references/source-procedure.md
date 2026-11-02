---
name: haos-router
description: "Use para interpretar comandos /haos:agente, /haos:departamento, Rito, mb e EMERGENCIA, selecionar skills pertinentes e orquestrar especialistas no Codex."
---

# HAOS Router

## Contrato do main

Checklist de aplicacao: [playbook operacional](main-orchestration-playbook.md).

Carregar `${HAOS_PRIVATE_ROOT}`
para orquestracao substantiva. Instrucoes superiores prevalecem. Sempre obter
contexto e evidencias antes da acao; pergunta simples autocontida recebe resposta
direta, sem plano formal ou delegacao desnecessaria.

Duvida/falta de contexto exige consultar TODAS as camadas pertinentes: local,
HAOS_Memory, Obsidian, claude-mem, GBrain, Mnemoverse e RAGs do dominio quando
aplicaveis. Registrar fontes, resultados, indisponibilidade e buscas sem resultado;
memoria nao prova estado atual, que exige fonte viva. Nao inventar contexto.

Comecar com consultas dirigidas por assunto/projeto/runtime, com poucos itens
completos e expansao explicita quando houver lacuna ou overflow. No claude-mem,
usar `${USER_PROJECT_ROOT}/scripts/haos_memory_context.py` do repo canonico; `limit` da rota legada
`context/inject` nao e garantia de limite. Preservar precedentes antigos: nao
restringir toda recuperacao ao task_id. O indice de abertura nao equivale a leitura
do bootstrap; reutilizar contexto valido e recompor o ausente em retomadas.

Depois, preparar plano e consultar o catalogo completo das skills disponiveis
por metadados, nao carregar todas. Selecionar as melhores por tarefa/fase/risco,
com caminho e motivo, e propagar aos especialistas. Cada implementacao substantiva
e correcao e delegada; main fica com leituras/triagem, plano, integracao,
verificacao e edicoes de coordenacao. Indisponibilidade de delegacao exige
handoff honesto, nao execucao ficticia. Delegacao exige chamada real ao agente
e retorno verificavel; mencionar o especialista no texto nao prova execucao.

Usar `haos-execution-waves` e `haos-multi-agent-review` conforme pertinencia:
ondas independentes de ate tres, ownership exclusivo, QA read-only distinto do
autor e verificacao fresca. Perguntas objetivas refinam lacunas materiais, sem
repetir respostas ou travar itens independentes. Correcao e QA ate aceite ou
bloqueio real, com limite finito no plano, sem loops infinitos/daemons; falha
apos limite segue aberta. Usar apenas schema real: sem `fork_turns`, usar
`fork_context=false` quando suportado e briefing enxuto, sem inventar campos.

## Superpowers por pertinencia

Antes de aplicar workflows Superpowers, carregar `haos-superpowers` do repo
canonico. Consultar `${USER_PROJECT_ROOT}/.codex/haos-superpowers-routing.json` e propagar skills,
caminhos, motivos e restricoes aos owners em qualquer modo. HAOS prevalece;
nao carregar tudo nem confundir sugestao de skill com autorizacao de acao.

## Fechamento automatico

Ao concluir uma tarefa do usuario com evidencia, main aplica `haos-evoluir` e
`haos-memory-provenance` antes da resposta final, sem esperar comando manual.
Seguir `${HAOS_PRIVATE_ROOT}`.
Propagar este contrato em squad, Rito, departamentos e agentes diretos. Subagentes
apenas entregam evidencias; main integra. Turno nao e tarefa. Reutilizar identidade
no comando manual, respeitar opt-out e nao enviar diario privado aos destinos de
memoria curada. Mnemoverse continua no fechamento com readback.


## Prefixos
- Sem prefixo: Concierge.
- `/haos:rito` ou `#`: Rito v2.
- `/haos:agente`: custom agent especifico em `.codex/agents/`.
- `/haos:departamento`: conjunto de agentes do departamento.
- `/haos:mb` ou `mb:`: Mega Brain Lite.
- `EMERGENCIA`: suspender fluxo normal e acionar segurança/conselho.

`@` e reservado para plugins/menções do Codex e nao deve ser usado como roteador HAOS.

Antes de roteamento HAOS substantivo, carregar bootstrap do repo `${HAOS_PRIVATE_ROOT}`: `AGENTS.md`, `${USER_PROJECT_ROOT}/memory/bootstrap.md`, `${USER_PROJECT_ROOT}/memory/MEMORY.md`, `workspace/SOUL.md`, `workspace/USER.md`, `workspace/IDENTITY.md`, `workspace/TOOLS.md`, `commands/`, `.codex/agents/` e `.agents/skills/`. Consultar `claude-mem` quando pronto.

## Skills automaticas
- UI/frontend, site, landing page, dashboard, app, componente ou auditoria de interface: carregar `haos-design` + `impeccable`.
- Copy, roteiro, oferta, pagina, email, anuncio, social, WhatsApp ou mensagem comercial para ${USER_BRAND}, SIM, ${USER_BRAND}, ${USER_BRAND}, manifestacao, PNL ou Codigos de Grabovoi: carregar `edson-burger-copy`.
- Arquivo grande/gigante/monolitico, modulo inchado, limite de linhas, `max-lines`, decomposicao modular, split por responsabilidade, refatoracao estrutural ou manutencao dificil por tamanho/acoplamento: carregar `haos-structural-refactor` em `AUDIT` read-only.
- Alteracao de codigo substancial em modulos existentes: executar automaticamente o scanner de `haos-structural-refactor` no menor escopo afetado antes da edicao. Mudanca trivial e isolada pode dispensar a varredura, com justificativa curta no briefing.
- Aplicar a deteccao estrutural em qualquer entrada main, squad, Rito, departamento ou agente direto. Mudar para `APPLY` somente quando o usuario pedir claramente para executar a refatoracao; mudanca ampla exige baseline, plano e gate explicito antes de editar.
- Em briefing estrutural, declarar o modo e propagar `haos-structural-refactor`, `haos-quality-gates`, `haos-execution-waves` e `haos-multi-agent-review`.
- Compor as skills quando mais de um contexto estiver presente, preservando as regras de Impeccable e Edson. Propagar a selecao no briefing do main, squad, Rito, departamento e agente direto; nunca presumir que o subagente herdou a skill.

## Departamentos
- `/haos:conselho`: estrategista-chefe, diretor-criativo, cmo
- `/haos:criativo`: copy-specialist, content-strategist, designer, videomaker, sm-social
- `/haos:trafego`: traffic-master, media-buyer, tracking-engineer
- `/haos:dados`: data-analyst, bi-engineer, pesquisador
- `/haos:funnel`: funnel-architect, automation-engineer, crm-specialist, email-marketer
- `/haos:produto`: product-manager, ux-researcher, dev-frontend, dev-backend
- `/haos:orquestracao`: qa-reviewer, project-manager, compliance-officer, devops
- `/haos:seguranca`: chuck-norris, devops, compliance-officer
