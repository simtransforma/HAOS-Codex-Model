---
name: haos-quality-gates
description: Use quando uma mudanca precisar de criterios de verificacao, houver falhas herdadas ou for necessario decidir se a entrega pode ser aceita.
---

# Gates proporcionais e resultados frescos

## Entradas

Aceite, risco, stack e versoes reais, comandos existentes, baseline e revisao
da entrega. Descobrir ferramentas pelo projeto; nao impor instalacao global,
novo framework de testes ou mudanca de configuracao para cumprir este metodo.

## Passos

1. Definir criterios antes da mudanca. Escolher checks que detectem falhas
   relevantes, observando manifests e pipeline existentes. Para documento,
   validar estrutura, referencias e coerencia; para codigo, cobrir comportamento
   afetado. Nao exigir testes unitarios sem utilidade para a entrega.
2. Executar baseline seguro e registrar falhas preexistentes. Se impossivel,
   declarar baseline indisponivel; nao atribuir automaticamente todas as
   falhas ao autor nem presumir que sao antigas.
3. Criar matriz de gates por risco conforme tabela. Definir alvo, procedimento,
   resultado esperado, evidencia, owner e condicao bloqueante.
4. Executar apos a ultima alteracao pertinente; ler codigo de retorno e
   resultado. Vincular evidencia ao artefato/revisao observado.
5. Usar PASS para criterio demonstrado, FAIL para criterio violado,
   NAO EXECUTADO para ausencia de execucao e N/A apenas para irrelevancia
   justificada antes do aceite. N/A nunca e falso PASS.
6. Corrigir pelo owner e repetir checks afetados com `haos-task-loop`.
   Resolver flakiness por investigacao; nao repetir ate obter um verde
   conveniente, suprimir regra ou excluir arquivo para esconder falha.
7. Revisar diff completo contra baseline e riscos residuais. Aceitar apenas
   com criterios bloqueantes atendidos; gates externos seguem autorizacao
   especifica. Usar `haos-evidence` e revisao independente quando pertinente.

## Selecao de checks

| Tipo de risco | Verificacao pertinente | Limite da conclusao |
| --- | --- | --- |
| Formato/documentacao | Parsing, links, contrato e cenarios documentais | Nao prova comportamento de agente |
| Codigo e tipos | Lint/tipos existentes e teste do contrato alterado | Build sozinho nao cobre regressao |
| Integracao | Sucesso, erro e recuperacao em ambiente autorizado | Mock nao prova estado remoto |
| Interface | Jornada critica, tamanhos e acessibilidade pertinentes | Screenshot nao prova interacao |
| Seguranca | Segredos, acesso e entradas no escopo | Scanner nao substitui analise |
| Entrega executavel | Build e smoke pertinentes | Artefato local nao prova deploy |

## Falhas herdadas

Separar baseline de regressao. Pode-se observar, conter novas falhas e reduzir
as antigas por lotes. Uma falha herdada que viole o aceite atual continua
bloqueante; as demais ficam explicitamente fora do escopo com impacto descrito.
Promover regra para bloqueio de pipeline e mudanca separada, sem suprimir
falhas para chegar artificialmente a zero.

## Saida

Tabela gate | alvo/revisao | comando/procedimento | esperado | observado |
status | motivo/limite. Acrescentar
`STATUS: CONCLUIDO | BLOQUEADO | REVISAO NECESSARIA`, cobertura nao executada
e riscos. Contagens distinguem PASS, FAIL, NAO EXECUTADO e N/A.

## Criterios de aceite

Checks frescos, pertinentes e lidos; nenhum defeito bloqueante aberto;
N/A fundamentado; escopo real inclui arquivos novos. Sem teste disponivel,
declarar limite e verificar se outro procedimento prova o mesmo criterio.

## Erros comuns

- Check anterior a correcao como prova final: repetir verificacao afetada.
- Ferramenta ausente virar N/A: marcar NAO EXECUTADO e avaliar alternativa.
- Verde por exclusao de arquivos: restaurar cobertura prevista e corrigir causa.

## Cenarios de pressao

- Build passou, teste do contrato falhou: manter FAIL e impedir aceite.
- Gate de tipos em documento puro: N/A com motivo; validar estrutura e texto.
- Tres execucoes alternam sucesso/falha: registrar instabilidade e investigar,
  sem selecionar apenas o ultimo resultado favoravel.
## Material portavel da origem (lote A)

Consultar [procedimento de origem](references/source-procedure.md), adaptado sem dados privados.
O nucleo publico acima prevalece em gates, opt-outs, fechamento e ferramentas.
Consultar [contrato de dependencias](EXPORT_DEPENDENCIES.md) antes de comandos dependentes.
