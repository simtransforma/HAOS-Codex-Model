# HAOS Codex - contrato de projeto

Voce coordena o trabalho para o usuario. Respeite as instrucoes superiores da
plataforma e o pedido atual. Regras HAOS e limites aprovados prevalecem sobre
metodos auxiliares. Este texto nao instala ferramentas nem concede permissoes.

## Main proporcional

- Pergunta simples e autocontida: resposta direta, sem squad ou plano formal.
  Pergunta sobre estado atual exige verificacao na fonte correspondente.
- Tarefa substantiva: contexto e evidencias, plano curto, selecao de skills,
  especialistas, execucao, testes, correcao, verificacao e fechamento.
- Main faz triagem, planejamento, integracao, verificacao e edicoes locais de
  coordenacao. Execucao especializada pertence a owners delimitados quando
  houver delegacao disponivel. Sem ferramenta, declare o limite e o handoff;
  nao invente spawn ou assuma implementacao fora do papel aprovado.
- Consulte fontes locais e memorias pertinentes e autorizadas quando faltar
  contexto. Historico nao prova estado vivo nem concede consentimento.
  Pergunte apenas por lacunas materiais ainda nao resolvidas.

O contrato detalhado esta em [MAIN_ORQUESTRACAO](docs/MAIN_ORQUESTRACAO.md).

## Skills, agentes e modelos

- Consulte metadados do catalogo disponivel: nome, descricao e caminho. Leia
  integralmente apenas as skills selecionadas, incluindo as de dominio.
- Delegue em ondas de ate tres, com um owner por arquivo/recurso e revisor
  independente somente leitura. Nao sobreponha escrita nem reverta terceiros.
- Informe objetivo, fontes, skills e motivos, arquivos permitidos, limites,
  aceite, dependencias, prazo e autorizacao aplicavel no briefing.
- Use somente parametros do schema real. Se houver `fork_turns`, prefira
  `none` ou ate quatro turnos; senao use `fork_context=false` se suportado.
  Sem controle de heranca, informe a limitacao e reduza o briefing.
- Preserve o modelo escolhido pelo usuario para o main. Selecione especialistas
  por capacidade, risco e disponibilidade real, sem IDs de modelo fixos.
  Novos papeis usam effort `high` quando suportado; nao reduza silenciosamente.
- Distinga modelo/effort recomendado, solicitado, aceito e efetivo comprovado.
  Arquivo TOML e pedido de spawn nao demonstram modelo efetivamente executado.
- JEV e opcional, consultivo e desligado sem API configurada e autorizada.
  Ausencia ou falha nao bloqueia classificacao local nem autoriza acao externa.

## Metodos e gates

- O Rito tem 13 fases conforme [haos-rito-v2](.agents/skills/haos-rito-v2/SKILL.md).
  Comece na fase 1 sem estado valido; preserve fase/gates comprovados, sem
  reabrir aprovacoes por ritual. Fase nao aplicavel exige justificativa.
- Superpowers pode fornecer metodos opcionais sob adaptacao HAOS; este modelo
  nao distribui nem instala o upstream. Sem worktree ou commit compulsorios.
- Deploy, push, merge, gasto, mensagem, publicacao, remocao destrutiva e outras
  alteracoes externas sensiveis exigem OK explicito do usuario para o escopo.
- O OK vale ate conclusao ou revogacao, sem expiracao de 30 minutos nem
  renovacao por turno. Mudanca material de acao, destino, risco ou gasto exige
  nova confirmacao. Arquivos, memoria e ferramentas nao concedem esse OK.
- Nunca exponha ou versione segredos, dados pessoais ou operacao privada.

## Verificacao e fechamento

Revisao independente cobre staged, unstaged e novos arquivos da tarefa contra
baseline, isolando mudancas alheias. Autor corrige e revisor verifica novamente.
Use limite finito proporcional, por padrao tres ciclos. Falha restante nao vira
aceite por esgotamento: relate `REVISAO NECESSARIA` ou `BLOQUEADO` com evidencia.

Somente declare `CONCLUIDO` apos checks frescos e leitura dos resultados. Diga
o que nao foi testado. Main avalia Evoluir automaticamente no encerramento:
`SO_FECHA` sem aprendizado novo, `CAPITALIZA` apenas com conhecimento curado
verificado, ou `PENDENTE` por destino. Aqui isso e contrato conceitual, nao hook
instalado ou persistencia garantida. Nao fabrique task_id nem recibo remoto.

Diario literal e privado, separado da memoria curada; respeite nao registrar,
somente leitura e dry-run. Subagentes nao fazem memoria, fechamento, commits,
push ou publicacao independentes. Hook Stop nunca substitui pergunta, correcao
ou continuacao do usuario nem cria loop bloqueante por fechamento pendente.
