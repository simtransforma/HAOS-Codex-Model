---
name: haos-task-loop
description: Use quando uma entrega tiver defeitos, revisao pedir correcao ou uma tentativa depender de novas verificacoes antes do aceite.
---

# Correcao finita com evidencia

## Entradas

Item e owner, aceite, defeito observado, baseline, dependencias e limite.
Padrao: tres ciclos de correcao por item. Definir limite antes de tentar;
revisao inicial identifica o problema e nao e correcao executada.
Um ciclo inclui hipotese, mudanca ou tentativa de resolucao e verificacao.

## Passos

1. Confirmar problema com evidencia localizavel. Agrupar achados pela causa
   raiz, distinguindo defeito real, falso positivo demonstrado e dependencia
   indisponivel. Urgencia nao altera criterio de aceite.
2. Registrar estado do item, contador atual e criterio de parada.
   Retomada, novo turno ou troca de agente preservam contador e historico;
   nao redefinir o item para burlar o limite.
3. Antes de cada ciclo, formular hipotese verificavel e acao dentro do
   ownership. Se nao houver nova hipotese ou acesso necessario, parar
   repeticao e declarar o bloqueio real.
4. Owner executa correcao; revisor permanece read-only. Registrar diferenca
   e repetir checks afetados apos a mudanca conforme `haos-quality-gates`.
   Comparar esperado e observado, incluindo regressao pertinente.
5. Se checks e aceite passarem, marcar item CONCLUIDO com provas.
   Se falharem, incrementar ciclo realizado, manter defeito aberto e avaliar
   se ha condicao util para nova tentativa dentro do limite.
6. Ao atingir tres ciclos sem aceite, encerrar a tentativa como
   REVISAO NECESSARIA, ou BLOQUEADO se dependencia real impede prosseguir.
   Nao transformar limite em sucesso, ocultar falha ou aumentar limite
   silenciosamente. Retomada exige condicao nova ou replanejamento explicito.
7. Main integra resultados e continua itens independentes com
   `haos-execution-waves`. Interrupcao ou revogacao do usuario para o escopo
   afetado prevalece imediatamente. Nao criar daemon, timer ou agente oculto
   para continuar depois de entregar o retorno.

## Estados e transicoes

| Estado observado | Condicao | Proximo estado |
| --- | --- | --- |
| Em verificacao | Criterios satisfeitos com prova | CONCLUIDO |
| Em verificacao | Defeito e tentativa util restante | Em correcao |
| Em correcao | Mudanca aplicada | Em verificacao com checks frescos |
| Qualquer estado ativo | Dependencia real indisponivel | BLOQUEADO |
| Em verificacao | Limite esgotado e defeito aberto | REVISAO NECESSARIA |

CONCLUIDO vale para o item e escopo verificados. Main decide fechamento da
tarefa; executor nao faz Evoluir, memoria, commit ou publicacao independente.

## Saida

`STATUS: CONCLUIDO | BLOQUEADO | REVISAO NECESSARIA`, item, owner, ciclos
usados/limite, tabela hipotese | acao | check | observado, defeitos restantes,
arquivos e evidencia. Para handoff, informar condicao objetiva de retomada,
proximo responsavel e ultimo estado verificado; usar `haos-session-handoff`.

## Criterios de aceite

Defeito resolvido ou tentativa encerrada honestamente; contador preservado;
checks apos ultima alteracao. Limite de ciclos protege contra repeticao sem
progresso e nunca substitui aceite. `haos-evidence` sustenta cada conclusao.

## Erros comuns

- "Tentamos o suficiente" como conclusao: manter defeito e registrar limite.
- Reexecutar comando sem nova hipotese: interromper e investigar a causa.
- Contratar outro executor para zerar contador: preservar historico do item.
- Prometer trabalho invisivel posterior: entregar handoff concreto.

## Cenarios de pressao

- Terceira correcao falha com prazo encerrado: REVISAO NECESSARIA e defeito
  documentado; nunca CONCLUIDO por esforco.
- Ferramenta externa indisponivel na primeira tentativa: BLOQUEADO no item
  dependente, sem consumir ciclos em repeticoes identicas.
- Usuario retoma em novo turno sem mudanca de condicao: recuperar contador e
  explicar a condicao necessaria; nao iniciar loop automatico.
