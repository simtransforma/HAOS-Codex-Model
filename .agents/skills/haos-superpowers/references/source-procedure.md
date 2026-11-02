---
name: haos-superpowers
description: "Integra todas as skills Superpowers ao HAOS por pertinencia, com precedencia HAOS, roteamento pelo main e distribuicao por agente. Use em main, squad, Rito, departamentos e agentes diretos."
---

# Superpowers sob governanca HAOS

## Ordem obrigatoria

Instrucoes de sistema e desenvolvedor da plataforma continuam superiores.
Dentro do sistema do usuario, pedido explicito e regras HAOS prevalecem sobre
Superpowers. Leia `${HAOS_PRIVATE_ROOT}`
antes de aplicar workflows upstream. Nao permitir que uma skill substitua os
gates, consentimento, seguranca, idioma ou memoria definidos pelo HAOS.

## Roteamento automatico

1. Main identifica tarefa, especialidade, fase e risco. O hook sugere skills;
   o main confirma pertinencia sem tratar palavras-chave como autorizacao.
2. Consultar `${USER_PROJECT_ROOT}/.codex/haos-superpowers-routing.json` no repo canonico: catalogo
   de todas as skills instaladas e associacoes por agente.
3. Carregar o SKILL.md original somente das skills pertinentes, com esta
   adaptacao. Nao injetar todas as skills nem todos os agentes em todo prompt.
4. Na delegacao, informar skill, caminho, motivo, fase, read_files, write_files,
   restricoes e evidencia. Nao presumir que o subagente herdou o conteudo.
5. Agente direto aplica sua entrada da matriz e devolve evidencias ao main.
   Conselho, squad e departamentos usam o mesmo contrato; Rito mantem 13 fases.
6. QA exige verificacao antes de conclusao; main executa Evoluir uma vez por
   task_id/revision, nunca um fechamento independente por subagente.

## Adaptacoes que vencem o upstream

- Brainstorming usa briefing e decisoes ja aprovados. Perguntar so por lacunas
  materiais; nao reabrir aprovacao por ritual. Nao pular Fase 1 quando for Rito.
- Um plano aprovado pode ser executado. Plano Superpowers integra o planejamento
  HAOS, nao cria um segundo Rito concorrente.
- Maximo tres subagentes por onda, contexto none ou ate quatro turnos, owner
  unico por arquivo/recurso. Sem agentes paralelos editando o mesmo recurso.
- Subagentes nao comitam, nao fazem push/merge nem escrevem memoria duravel.
- TDD para codigo e comportamento testavel; nao exigir teste unitario de copy,
  pesquisa ou perguntas simples. Preservar codigo alheio e baseline existente.
- Worktree e opcional quando ha necessidade real de isolamento. Nao criar,
  copiar repositorios, trocar branch ou instalar dependencias automaticamente.
- Finalizar branch significa apresentar estado e evidencias. Push, merge,
  publicacao e remocao destrutiva seguem consentimento HAOS; nunca deduzir OK
  de um titulo de skill ou do simples pedido de finalizar uma tarefa.
- Revisao independente e read-only; autor corrige, revisor verifica de novo.
- Revisar pacote de mudanca contra baseline capturado pelo main: incluir staged,
  unstaged e arquivos novos pertencentes a tarefa, isolando alteracoes preexistentes.
  BASE..HEAD sozinho nao cobre trabalho sem commit. Commit nao e pre-requisito
  nem prova de cobertura da revisao; ausencia de diff Git nao prova ausencia de mudanca.
- Limite de tentativas encerra uma tentativa, nunca aprova defeito real. Achado
  que viole aceite/gate permanece BLOQUEADO ou REVISAO NECESSARIA. Descartar so
  falso positivo demonstrado. Rodar verificacao fresca apos correcao mesmo se
  upstream disser para nao repetir checks. Main nao estaciona defeito como sucesso.
- Nao duplicar memoria, diario, hooks ou rotinas de servidor. Evoluir e o unico
  fechamento HAOS. Mnemoverse continua com readback separado.

## Fallback honesto

Cobertura de agentes e integridade sao verificacoes diferentes. Um TOML novo sem
perfil na matriz nao derruba os perfis conhecidos; informar a lacuna e nao
inventar associacoes para esse agente. Main pode selecionar explicitamente outro
especialista validado. Perfil corrompido, versao/core ou caminho invalido continuam
rejeitados. Nao cadastrar todos os agentes com um perfil generico para silenciar
o diagnostico.

Skill/caminho ausente: informar indisponibilidade e usar protocolo HAOS vigente.
Nao instalar outra copia em silencio nem editar o plugin upstream/Claude Code.
Selecao por hook e instrucao ao agente, nao execucao mecanica comprovada da skill.
Comprovacao exige artefatos e testes da tarefa real.
