# Diario global e fechamento curado

## Procedimento operacional

1. O diario literal pertence somente ao Obsidian privado, em
   `01-Sessoes/session--<hash-estavel>/Chat/`. Nunca versionar Chat, anexos ou
   transcripts, nem enviar esses dados ao Mnemoverse ou GBrain.
2. A configuracao canonica `${USER_PROJECT_ROOT}/.codex/haos-automatic-memory.json` usa `mode=local`
   para todas as sessoes locais suportadas. `pilot` restringe IDs. A ativacao
   precisa de teste real de uma segunda sessao e revisao independente.
3. O primeiro registro e prospectivo: nao importar historico antigo. Fontes
   de subagentes, nuvem ou identidade divergente nao recebem cobertura presumida.
4. Opt-out por sessao permanece ativo apos habilitacao global. Desligar e religar
   nao pode recuperar o intervalo recusado. Testar pelo hook real, nao apenas
   pela API interna do motor.
   Se nao houve hooks enquanto desligado, executar disable/enable por sessao
   autorizada antes da reativacao; apenas editar enabled=true nao descarta o
   intervalo. Nao remover vetos individuais em massa.
5. Orquestrador fecha tarefas com identidade e revisao persistentes. SO_FECHA
   nao fabrica aprendizado; CAPITALIZA atualiza conhecimento tematico e usa
   `finish-task-haos.ps1 -Integrator` para commits locais seletivos e readback.
6. Destinos locais: your-private-project, HAOS_Memory e Obsidian. HAOS_CC e o
   ambiente Claude Code nao sao destinos deste fluxo. Push continua separado.
7. No GBrain, fila de ingestao nao comprova ingestao. Consultar equivalente,
   persistir somente sintese curada com proveniencia e confirmar com get_page.
8. No Mnemoverse, uma credencial rejeitada fica pendente. Nao substituir pela
   credencial de outro runtime. Preservar resumo sanitizado local para retomada.

## Verificacao

- Testar replay: sem novos eventos, hashes e quantidade de blocos nao mudam.
- Conferir eventos user/assistant sem imprimir o conteudo do diario.
- Registrar latencia, bytes, cursor e lacunas; historico excluido nao e perda
  comprovada. Nao apagar marcadores para aparentar captura completa.
- Sessao aberta recebe regras nos proximos eventos suportados dos hooks.
  Nao prometer execucao quando o aplicativo esta fechado nem suporte a nuvem.
- Fila pendente, erro de ACL, lock ou erro remoto nao equivalem a sucesso.

Evidencia de implantacao: `${USER_PROJECT_ROOT}/docs/ATIVACAO_GLOBAL_EVOLUIR_2026-09-18.md`.
