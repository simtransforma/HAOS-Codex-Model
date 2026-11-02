---
name: haos-rito-v2
description: "Use quando o usuário iniciar um projeto com"
---

# HAOS Rito v2

Execute projetos complexos em 13 fases, com gate entre fases.

## Regra central

Antes de qualquer resposta substantiva, carregue o bootstrap HAOS Codex do repo `${HAOS_PRIVATE_ROOT}`: `AGENTS.md`, `${USER_PROJECT_ROOT}/memory/bootstrap.md`, `${USER_PROJECT_ROOT}/memory/MEMORY.md`, `workspace/SOUL.md`, `workspace/USER.md`, `workspace/IDENTITY.md`, `workspace/TOOLS.md`, `commands/`, `.codex/agents/` e `.agents/skills/`.

Se `claude-mem` isolado estiver pronto em `example.invalid:37778`, consulte contexto recente do projeto `your-private-project` antes do plano. Se nao estiver pronto, registre o bloqueio e use a memoria versionada como fallback.

`your-private-project` nao e memoria global do HAOS Codex. Carregue esse workspace apenas quando a tarefa envolver OpenClaw, servidor Hetzner ou componentes daquele ambiente.

## Fases
1. Intake & Validação
2. Pesquisa & Diagnóstico
3. Estratégia & Posicionamento
4. Planejamento Tático
5. Copywriting & Mensagens
6. Design & Criativos
7. Funil & Automação
8. Tráfego & Mídia
9. Tracking & Dados
10. QA & Compliance
11. Deploy & Ativação — exige OK
12. Monitoramento & Otimização
13. Debrief & Aprendizados

## Skills por fase
- Refatoracao estrutural: ao detectar arquivo grande/gigante/monolitico, modulo inchado, limite de linhas, `max-lines`, decomposicao modular, split por responsabilidade, refatoracao estrutural ou manutencao dificil por tamanho/acoplamento, carregar `haos-structural-refactor` em `AUDIT` read-only.
- Em implementacao de codigo substancial sobre modulos existentes, executar o scanner read-only no menor escopo afetado durante o diagnostico, antes de qualquer edicao.
- Fase 2: produzir diagnostico estrutural read-only e evidencias, sem editar arquivos.
- Fase 4: registrar baseline, plano, dependencias, ownership, validacoes e gate explicito. Propagar `haos-structural-refactor`, `haos-quality-gates`, `haos-execution-waves` e `haos-multi-agent-review` nos briefings aplicaveis.
- Fase de implementacao adequada: usar `APPLY` somente quando o usuario pedir claramente para executar a refatoracao e, em alteracao ampla, depois do gate explicito.
- Fase 5: carregar `edson-burger-copy` quando a entrega de mensagem envolver ${USER_BRAND}, SIM, ${USER_BRAND}, ${USER_BRAND}, manifestacao, PNL ou Codigos de Grabovoi.
- Fase 6 e qualquer implementacao de interface posterior: carregar `haos-design` + `impeccable`.
- Fase 10: revisar a refatoracao estrutural em modo read-only com baseline e gates frescos; revisar os artefatos contra todas as skills ativadas. Em pagina Edson/SIM, validar texto com `edson-burger-copy` e interface com `impeccable`.
- Registrar as skills exigidas no briefing de cada agente; acionar Rito ou squad nao substitui essa propagacao.

## Saída por fase
- Objetivo da fase
- Agentes acionados
- Evidências usadas
- Entregáveis
- Bloqueios
- Gate de aprovação
- Próxima fase

## Estado
Salvar estado em `runtime/state/rito-atual.md` e `runtime/state/fase-atual.md` quando estiver executando rito longo. `${USER_PROJECT_ROOT}/memory/rito_state.json` fica como legado/fallback.
