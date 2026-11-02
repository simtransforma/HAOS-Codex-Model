---
name: haos-claim-verification
description: Use quando for necessario validar afirmacoes factuais, numeros, resultados de testes ou alegacoes de funcionamento antes de comunicar uma conclusao.
---

# Verificacao de afirmacoes

Acione com `$haos-claim-verification`. Julgue cada claim pelo que a evidencia
permite afirmar, sem converter configuracao, intencao ou tentativa em resultado.

## Entradas

Receba texto ou lista de claims, finalidade da decisao, risco, fontes acessiveis,
periodo relevante e observacoes coletadas. Para numeros, exija unidade, base de
comparacao, denominador, intervalo temporal e metodo de calculo.

## Passos

1. Separe frases compostas em claims atomicos. Preserve o sentido original e
   atribua identificadores para conectar revisao, fonte e redacao corrigida.
2. Classifique como fato, observacao, estimativa, inferencia, hipotese ou opiniao.
   Opiniao nao precisa virar fato, mas suas premissas factuais precisam de prova.
3. Determine a evidencia necessaria e sua atualidade. Estado operacional exige
   observacao no ambiente e versao pertinentes; historico orienta a busca.
4. Leia a fonte e registre localizador preciso, data, metodo e observacao literal
   curta ou parafrase fiel. Avalie qualidade com `$haos-source-quality-auditor`.
5. Procure contraevidencia proporcional ao risco. Confira causalidade, escopo,
   amostra e alternativas explicativas; ausencia de erro nao prova efeito.
6. Emita veredito por claim: SUSTENTADO, PARCIAL, CONTRADITO ou NAO VERIFICADO.
   Registre confianca qualitativa e justificativa, sem percentuais inventados.
7. Proponha manter, qualificar, remover ou coletar evidencia adicional. Pare ao
   concluir a lista ou atingir o limite acordado; marque itens nao avaliados.

## Saida

| ID e claim | Tipo | Fonte e data | Observacao | Atualidade e escopo | Incerteza | Veredito e acao |
| --- | --- | --- | --- | --- | --- | --- |
| Enunciado verificavel | Categoria | Localizador consultado | O que foi visto | Ambiente e periodo | Lacuna ou alternativa | Decisao fundamentada |

Entregue tambem o texto corrigido e as verificacoes pendentes, com prioridade
conforme o impacto da decisao. Uma fonte ausente permanece ausente na tabela.

## Criterios de aceite

Cada veredito deve ser reproduzivel a partir da observacao registrada. Health
saudavel prova somente o sinal observado; configuracao presente prova existencia
da configuracao. Para afirmar efeito, verifique execucao e resultado correspondente.
Um teste local nao demonstra entrega externa nem funcionamento em outro ambiente.

## Erros e recuperacao

Se a fonte nao abrir, marque NAO VERIFICADO e registre a tentativa. Se um numero
nao puder ser recalculado, informe a falta de dados. Nao escolha a fonte que
favorece a conclusao ignorando divergencias. Alegacao temporal exige data; uma
captura antiga nao confirma estado vivo. Nao execute operacao sensivel para obter
prova sem autorizacao aplicavel.

## Cenarios de verificacao

- Servico responde ao health, mas nenhuma entrega foi observada: sustentar health;
  manter claim de entrega NAO VERIFICADO.
- Arquivo declara um agente: confirmar declaracao; nao afirmar spawn ou hot reload.
- Taxa sem denominador: marcar PARCIAL ou NAO VERIFICADO e pedir a base faltante.
- Evidencias contemporaneas divergem: expor conflito e reduzir a conclusao.
## Material portavel da origem (lote A)

Consultar [procedimento de origem](references/source-procedure.md), adaptado sem dados privados.
O nucleo publico acima prevalece em gates, opt-outs, fechamento e ferramentas.
Consultar [contrato de dependencias](EXPORT_DEPENDENCIES.md) antes de comandos dependentes.
