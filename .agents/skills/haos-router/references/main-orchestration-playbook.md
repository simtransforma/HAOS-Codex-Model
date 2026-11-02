# Playbook operacional do main

Usar como checklist, nao como segundo contrato. Fonte normativa:
MAIN_ORQUESTRACAO.md (dependency not bundled: <${HAOS_PRIVATE_ROOT} - GPT-Codex/HAOS/your-private-project/docs/MAIN_ORQUESTRACAO.md>).
Instrucoes superiores, escopo aprovado e opt-outs prevalecem.

1. **Classificar:** pergunta simples e autocontida recebe resposta direta;
   aplicar os passos seguintes somente quando pertinentes ao trabalho substantivo.
2. **Contextualizar:** conferir pedido, evidencias e lacunas. Se faltar contexto,
   consultar todas as camadas pertinentes da secao 1 do contrato; registrar fonte,
   resultado ou indisponibilidade. Estado atual exige fonte viva.
3. **Planejar:** definir itens, dependencias, owners, arquivos, aceite, validacoes
   e limite finito de correcao; reutilizar decisoes e gates ja aprovados.
4. **Selecionar:** consultar catalogo completo por metadados; carregar apenas
   skills pertinentes e levar nome, caminho e motivo ao briefing.
5. **Delegar:** atribuir implementacao substantiva ao especialista, com briefing
   enxuto e schema real. Exigir chamada real e retorno verificavel. Executar
   ondas de ate tres, sem escritas sobrepostas;
   main mantem triagem, coordenacao, integracao e verificacao.
6. **Refinar:** perguntar somente lacunas materiais ainda nao respondidas;
   continuar itens independentes e preservar consentimento externo aplicavel.
7. **Validar:** autor corrige, revisor independente verifica em read-only.
   Repetir checks necessarios conforme secao 4; limite esgotado com falha nao e
   aceite. Registrar bloqueio real ou revisao necessaria, sem loop ou daemon.
8. **Entregar:** informar STATUS, evidencias, alteracoes e proximos passos.
   Main integra e fecha Evoluir uma unica vez; subagente nao cria memoria,
   commit ou fechamento independente.

Saida esperada: evidencias por item e pendencias identificadas, sem alegar
delegacao, consulta ou teste que nao aconteceu. A tabela "Exemplos de comportamento
esperado" do contrato serve para conferir pergunta simples, execucao e falta de
contexto; nao substituem teste comportamental real.

## Manutencao de fluidez

- Separar inventario de integridade: adicionar agente sem perfil nao deve derrubar
  rotas existentes. Validar o perfil solicitado; nunca adivinhar skills do novo.
- Registrar causa especifica quando indisponivel. Um fallback HAOS explicito nao
  transforma configuracao corrompida em roteamento Superpowers valido.
- Contexto de abertura e indice de fontes. Carregar bootstrap pertinente, reutilizar
  leitura ainda disponivel e recompor apos perda de contexto; nao injetar documentos
  truncados nem afirmar leitura integral so porque o caminho foi listado.
- Recuperar memoria por assunto/projeto, com itens completos, teto de saida e
  expansao dirigida. Preservar precedentes antigos e distinguir historico de regra
  atual. O adapter Codex esta em `${USER_PROJECT_ROOT}/scripts/haos_memory_context.py`.
- Testar o predicado completo de protecao de segredo com dados sinteticos: `.Keys`
  e identificador, mas arquivo `.key` continua protegido. Uma regex isolada nao
  comprova o comportamento do guard inteiro.
- Medir hooks por evento/origem/duracao/resultado, nunca por payload. Timeout e
  teto, nao duracao observada. Contagem declarativa nao demonstra execucao duplicada.
- UserPromptSubmit fornece o contrato do main; o guard de delegacao fica
  silencioso por padrao. Nao repetir orientacao em cada ferramenta. Distinguir
  log proprio do guard da telemetria rotativa sem payload do wrapper.
- Manter Stop, gates, memoria e capacidade existentes ate evidencia de regressao
  ou equivalencia. Sem fila/daemon adicional para compensar uma causa nao medida.

Aceite: saudacao direta, pergunta sobre estado vivo, Rito e retomada coerentes,
agente novo, perfil corrompido, duas tarefas no mesmo projeto, precedente antigo,
worker indisponivel, pedido novo durante Stop e segredos sinteticos. Comparar com
baseline por arquivo, preservar mudancas alheias e pedir QA independente.
