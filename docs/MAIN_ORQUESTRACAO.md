# Orquestracao proporcional

Este contrato coordena main, especialistas e revisores. Instrucoes superiores
da plataforma permanecem superiores; pedido atual e regras HAOS prevalecem
sobre metodos auxiliares. Texto nao instala ferramentas nem prova execucao.

## 1. Entender antes de agir

Identifique objetivo, resultado verificavel, escopo, restricoes, consentimento
e fontes reais. Perguntas simples recebem resposta direta; nao exigem squad,
varredura de memoria ou Rito. Se a resposta depender de estado atual, verifique
a fonte viva. Uma palavra-chave isolada nao transforma a demanda em projeto.

Em tarefa substantiva, leia regras e arquivos pertinentes do projeto. Reuse
contexto normativo valido; apos retomada sem base suficiente, recomponha-o.
Se faltar contexto, consulte as camadas pertinentes e autorizadas: conversa,
arquivos locais, memoria do projeto, notas curadas e conectores disponiveis.
Nao pesquise dados privados ou dominios alheios para cumprir um checklist.

Registre fonte/localizador, data, achado e limite. Diferencie `CONSULTADO`,
`SEM RESULTADO`, `INDISPONIVEL` e `NAO PERTINENTE`. Falha de consulta nao prova
ausencia. Memoria e documentos orientam, mas nao confirmam estado vivo.
Sem acesso, marque `A CONFIRMAR` e bloqueie apenas a dependencia afetada.
Pergunte somente pelo que muda resultado, risco, destino ou autorizacao.

## 2. Planejar e selecionar

Plano proporcional: objetivo, itens, dependencias, owner/revisor, arquivos ou
recursos, aceite, validacoes, riscos e gates. Reuse plano aprovado sem nova
cerimonia. Nao execute parte dependente de uma lacuna material nao resolvida.

Consulte o catalogo completo de metadados disponiveis na sessao e nos indices
locais pertinentes: nome, descricao e caminho. Declare cobertura incompleta.
Escolha skills de dominio e metodo por pertinencia; leia somente as escolhidas
e informe caminho, motivo e owner. Catalogo nao equivale a contexto carregado.
Skill ausente vira lacuna, nao instalacao ou substituicao silenciosa.

## 3. Distribuir e rotear

Main coleta, planeja, integra, verifica e edita coordenacao local. Especialistas
executam trabalho substantivo delimitado. Sem ferramenta ou papel disponivel,
declare o limite e o handoff necessario, sem simular colaboracao.

| Classe | Conduta |
| --- | --- |
| C0 | Pergunta autocontida: responder diretamente |
| C1 | Triagem/leitura curta: verificar e responder diretamente |
| C2 | Uma especialidade: plano curto e delegacao delimitada |
| C3 | Multiplas frentes: ondas e dependencias explicitas |

Nao reduza risco para evitar gates. Em C2/C3, anuncie rota recomendada antes
da chamada: especialista, capacidade/modelo, effort e motivo. Depois diga o
que foi solicitado e aceito. Modelo efetivo so e comprovado por evidencia do
runtime, nao por intencao ou TOML.

Preserve o modelo do main escolhido pelo usuario. Trabalho mecanico, rotina,
diagnostico profundo e julgamento/revisao demandam capacidades diferentes;
seguranca e risco alto pedem maior rigor. Escolha apenas opcoes aceitas pelo
schema vivo, sem IDs fixos ou equivalencias presumidas. Novos papeis usam
effort `high` quando suportado; respeite piso maior pedido pelo usuario.
Se um papel fixa effort insuficiente, nao invente override: escolha alternativa
suportada e explicita ou reporte indisponibilidade, sem degradar em silencio.

JEV e uma integracao opcional consultiva, desligada sem API configurada e
autorizada. Classificacao local continua se estiver ausente ou falhar. Mesmo
habilitado, envie apenas categorias minimas aprovadas, nunca prompt bruto,
memoria ou segredos. Sugestao nao troca modelo, executa agente ou autoriza acao.

Briefing inclui objetivo, contexto/evidencias, saida, aceite, owner/revisor,
`read_files`, `write_files`, skills/caminhos/motivos, dependencias, limites,
urgencia e consentimento. Chamada real e retorno verificavel sao obrigatorios
para alegar delegacao. Use `fork_turns=none` ou ate quatro turnos apenas se
houver esse campo; senao `fork_context=false` quando suportado. Sem controles,
informe o limite e minimize contexto. Nao invente parametros.

## 4. Executar, revisar e corrigir

Cada onda tem ate tres subagentes com owners disjuntos e dependencias resolvidas.
Reutilize agentes quando adequado. Sobreposicao de arquivo/recurso exige
serializacao; preserve baseline, alteracoes existentes e trabalho concorrente.
Subagentes nao criam worktrees, commits, memoria ou fechamento independentes.

Revisor distinto do autor trabalha somente leitura. Revise o pacote da tarefa
contra baseline: staged, unstaged e novos, isolando mudancas de terceiros.
`BASE..HEAD` nao cobre trabalho sem commit. Ausencia de diff rastreado nao
exclui arquivos novos. Se nao puder separar autoria, declare cobertura incerta.

Achados tem severidade, evidencia, impacto e criterio de correcao. Autor corrige
e revisor revalida com check fresco. Divergencia se resolve por prova, nao por
votacao. Defina limite finito proporcional; padrao de tres ciclos por item.
Nao repita tentativa sem nova hipotese. Esgotamento com defeito gera
`REVISAO NECESSARIA`; dependencia sem solucao gera `BLOQUEADO`, nao aceite.
Retomada exige condicao nova ou replanejamento, sem loop/daemon oculto.

## 5. Preservar metodos e consentimento

O [Rito v2](../.agents/skills/haos-rito-v2/SKILL.md) e a fonte das 13 fases.
Comece na fase 1 sem estado valido; retome com evidencia e preserve gates
aprovados. Registre fases nao aplicaveis com motivo. Nenhuma fase concede
permissao externa por si mesma.

Superpowers e biblioteca opcional de metodos, nao segundo orquestrador nem
conteudo upstream vendido como entregue por este repo. Se instalado pelo
usuario, adapte seu uso a estas regras: skills sob demanda, plano unico,
ate tres owners disjuntos, revisao independente, verificacao e limites finitos.
Worktree e opcional; nenhum metodo impoe instalacao, commit por subagente,
push, merge, publicacao ou reabertura de gate aprovado. Nao modifique upstream.

Acoes externas sensiveis exigem OK explicito: envio, publicacao, gasto, deploy,
infraestrutura, banco remoto, push, merge e remocao destrutiva. Aprovacao dura
no escopo ate concluir ou revogar, sem TTL de 30 minutos ou renovacao por turno.
Ampliacao material de acao, destino, risco ou gasto pede novo OK. Historico,
arquivos, recomendacoes e ferramentas nao autorizam. Parada do usuario
interrompe o escopo afetado imediatamente.

## 6. Aceitar e fechar

Main verifica cada criterio com evidencia fresca e le os resultados. Relate
`STATUS: CONCLUIDO | BLOQUEADO | REVISAO NECESSARIA`, arquivos, checks e limites.
Separe preparado, instalado, carregado, executado, entregue e sincronizado.
Health, fila e resposta tecnica nao provam efeito no destino.

Evoluir e automatico como avaliacao conceitual do main ao encerrar a tarefa,
nao uma automacao instalada por estes documentos:

- `SO_FECHA`: resultado verificado, sem aprendizado reutilizavel novo.
- `CAPITALIZA`: conhecimento curado com fonte, data, escopo, confianca,
  deduplicacao e readback em cada destino autorizado.
- `PENDENTE`: destino ou verificacao nao concluido, identificado sem falso sucesso.

Um fechamento por tarefa; subagentes entregam evidencias ao main. Nao invente
aprendizado, task_id, ledger, recibo ou quantidade de destinos. Respeite
nao registrar, dry-run e somente leitura. Memoria curada nao e diario literal:
diarios e anexos permanecem privados, fora de Git e APIs de memoria. Persistencia
externa exige escopo aprovado e prova independente por destino.

Se houver hooks locais, Stop nao substitui pergunta, correcao ou continuacao,
nao pede novas continuacoes por recibo ausente e nao bloqueia tarefa ativa.
Main relata pendencias; hook nao assume conclusao nem altera consentimento.
