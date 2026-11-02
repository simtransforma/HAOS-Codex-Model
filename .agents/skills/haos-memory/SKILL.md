---
name: haos-memory
description: Use quando uma tarefa depender de historico, decisoes anteriores, preferencias ou candidatos a conhecimento duravel.
---

# Memoria como contexto verificavel

## Entradas

Assunto, projeto, pergunta que depende do historico, fontes configuradas,
restricoes de acesso e modos no-memory, read-only ou dry-run. Identificar
task_id/revision se ja disponivel; sua ausencia nao obriga hook ou autostart.

## Passos

1. Separar recuperacao de persistencia. Ler apenas fontes pertinentes e
   autorizadas. Em no-memory, nao consultar nem persistir memoria; trabalhar
   com pedido e artefatos fornecidos. Read-only permite leitura autorizada,
   sem escrita; dry-run descreve o que seria feito, sem persistir.
2. Comecar pelo contexto local e ampliar para destinos configurados quando
   a pergunta exigir. Buscar por assunto/projeto, nao apenas pela tarefa
   atual. Abrir o registro pela origem e localizador se o resumo for
   insuficiente; preservar precedentes antigos relevantes.
3. Registrar cada fonte como CONSULTADO, SEM RESULTADO, INDISPONIVEL ou
   NAO PERTINENTE, com motivo e limite de atualidade. Destino disabled fica
   DESABILITADO: nao e falha e nao exige instalar servico.
4. Confrontar contradicoes e identificar quem decidiu, em qual contexto e
   quando. Memoria nao concede autorizacao atual nem prova estado vivo.
   Confirmar na fonte atual aquilo de que a acao depende.
5. Selecionar candidatos duraveis: decisao, causa raiz ou procedimento
   reutilizavel comprovado. Descartar rotina sem novidade e dados excessivos.
   Nunca persistir segredos, dados pessoais desnecessarios, transcricao bruta
   ou raciocinio interno.
6. Entregar candidatos e fontes ao main. Apenas ele decide persistencia e
   fechamento com `haos-evoluir` e `haos-memory-provenance`, dentro do escopo
   autorizado. Usar `haos-session-handoff` para continuidade e
   `haos-dump-import` quando houver importacao explicitamente solicitada.
7. Declarar salvo somente apos readback de cada destino habilitado e
   autorizado. Falha num destino nao apaga resultados confirmados dos demais.

## Saida

Contexto recuperado com fato/inferencia/pendencia separados, mapa de fontes
e candidatos curados com origem. Informar o que nao foi consultado ou salvo.
Executor entrega ao main; nao emite recibo de fechamento independente.

## Criterios de aceite

Cada decisao usada tem fonte rastreavel e limite de atualidade.
Opt-outs respeitados. Candidato sem prova continua pendente, e ausencia de
integracao nao e confundida com ausencia de conhecimento.
Consultar `haos-evidence` antes de afirmar estado operacional.

## Erros comuns

- Recuperar tudo para "garantir": limitar por pertinencia e ampliar por lacuna.
- Reutilizar permissao escrita em memoria: buscar autorizacao no pedido valido.
- Criar memoria para toda tarefa: exigir valor duravel comprovado.
- Enviar novamente apos timeout: reconciliar conforme proveniencia.

## Cenarios de pressao

- Usuario pede no-memory e ha historico util: cumprir opt-out e declarar a
  lacuna sem consultar a memoria.
- Fonte antiga contradiz ambiente atual: preservar o historico e usar prova
  atual; preparar supersessao apenas se houver escopo de persistencia.
- Destino desabilitado e prazo de fechamento: registrar DESABILITADO sem
  inventar falha, instalar servico ou simular readback.
