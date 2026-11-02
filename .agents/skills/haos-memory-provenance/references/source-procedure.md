---
name: haos-memory-provenance
description: "Persistencia de memoria HAOS com alto sinal, proveniencia, deduplicacao e readback nas camadas locais, Obsidian, HAOS_Memory e Mnemoverse."
---

# HAOS Memory Provenance

Use junto de `haos-memory-triple` e do comando `evoluir`.

## O que merece memoria

Registre apenas fatos duraveis, decisoes, causa raiz, procedimento reutilizavel,
restricoes, evidencias e proximo passo. Nao grave conversa inteira, raciocinio
interno, dados pessoais desnecessarios, tokens, cookies ou conteudo de cofre.

## Envelope obrigatorio

```yaml
session_slug: nome-estavel-da-sessao
scope: projeto-ou-sistema
kind: decisao | aprendizado | procedimento | incidente | handoff
summary: fato compacto
source: arquivo-comando-ou-evidencia
observed_at: ISO-8601
confidence: confirmed | inferred | pending
supersedes: id-ou-null
```

## Escrita idempotente

1. Procure registro equivalente pelo `session_slug`, `kind` e causa raiz.
2. Atualize o item existente; nao crie duplicata por execucao.
3. Grave a versao sanitizada no repo da sessao e em `HAOS_Memory`.
4. Atualize a subpasta organizada da sessao no Obsidian.
5. Envie ao Mnemoverse como camada adicional redigida, nunca como fonte unica.
6. Deixe `claude-mem` capturar contexto operacional pelo runtime isolado; nao
   escreva diretamente no banco dele salvo por API documentada.
7. Faca readback de cada destino e compare campos-chave antes de declarar salvo.

Git commit deve selecionar somente os artefatos da sessao. Push continua exigindo
OK explicito. Falha em uma camada deve ser reportada sem apagar as camadas que
passaram.

Para diario global, opt-out, captura prospectiva e separacao dos destinos,
aplicar tambem `references/diario-global.md`.

## Prova de fechamento remoto

Aplicar `references/readback-remoto.md` ao fechar tarefas automaticamente.
Fila local, health HTTP 200 e busca semantica vazia nao provam, respectivamente,
ingestao, processamento concluido ou ausencia de um registro. Usar identidade
de tarefa/revisao, leitura exata e recibo independente por destino.

No Mnemoverse, transportar o delta curado da revisao, ligado a `task_id`,
`revision` e ao hash da proveniencia completa mantida no recibo local. Nao
repetir um envelope por destino: o filtro semantico pode rejeitar esse pacote
redundante como baixa novidade. Uma resposta `IMPORTANCE_FILTERED` nao e
readback nem sucesso. Ela autoriza repacotar somente quando o servidor confirmou
que nenhum atom foi criado, nao existe recibo remoto e a identidade + hash da
proveniencia permanecem iguais. Timeout, resposta ambigua e conflito continuam
fail-closed e nunca podem ser reenviados por inferencia.

Para falhas de captura, atraso e erros do provider, aplicar
`references/diagnostico-captura-fila.md`. Preservar registros nao confirmados;
nao apagar lacunas ou filas para transformar um indicador em sucesso.

## Integridade do fechamento automatico

- Tarefas `running` ou `reopened` passam silenciosamente pelo hook `Stop`:
  preservar o estado, nao bloquear a resposta e nunca disputar com pergunta,
  correcao ou continuacao do usuario. Mesmo tarefa terminal conhecida sem
  recibo nao solicita continuacao: main reconcilia antes da resposta final.
- O catalogo privado deve vincular cada sessao ao hash canonico de seu indice;
  marcador `complete` isolado nao prova integridade.
- Divergencia, indice conhecido ausente ou migracao pendente resultam em
  `UNKNOWN`, nunca em ausencia presumida de tarefa.
- Preservar `current_task_id` depois de estado terminal para validar o recibo
  mesmo sem ponteiro automatico.
- Se o ponteiro automatico e o `current_task_id` apontarem para tarefas
  terminais diferentes da mesma sessao, o indice canonico prevalece. Qualquer
  tarefa ativa, ponteiro corrompido ou identidade ausente continua fail-closed.
- Aceitar o recibo Evoluir somente como ultima linha nao vazia, com um unico
  marcador coerente com task_id, gate e readbacks.
- Varredura integral do legado pertence a migracao administrativa; hooks de
  abertura e fechamento devem permanecer limitados e fail-closed.
