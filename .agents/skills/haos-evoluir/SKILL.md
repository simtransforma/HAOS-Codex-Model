---
name: haos-evoluir
description: Use quando o main encerrar uma tarefa com evidencia ou houver pedido de avaliar aprendizado reutilizavel e capitalizacao.
---

# Fechamento unico pelo main

## Entradas

Entrega e verificacoes, escopo autorizado, candidatos a aprendizado,
destinos explicitamente habilitados e opt-outs. Reutilizar task_id/revision
quando disponiveis; se ausentes, declarar identidade nao fornecida.
Esta skill nao exige autostart, hook, servico, commit ou publicacao.

## Passos

1. Confirmar quem executa: subagente apenas entrega evidencias e candidatos
   ao main. O main avalia automaticamente ao encerrar a tarefa, sem confundir
   turno, comentario ou retorno de executor com nova tarefa.
2. Conferir aceite com `haos-evidence`. Tarefa em andamento ou reaberta segue
   seu trabalho; fechamento nunca substitui pergunta, correcao ou continuacao
   do usuario. Pendencia material de entrega nao pode virar conclusao.
3. Aplicar opt-outs antes de persistir. No-memory impede uso e escrita de
   memoria; read-only, dry-run e nao evoluir impedem mutacoes de fechamento.
   Entregar avaliacao textual sem executar escrita, hooks ou comandos.
4. Julgar valor: procedimento novo, causa raiz, decisao ou contradicao resolvida
   precisa de prova e utilidade futura. Rotina, duplicata ou novidade incerta
   recebe SO_FECHA, sem fabricar aprendizado.
5. Havendo novidade, selecionar artefato tematico existente e destinos dentro
   do escopo. Registrar CREATE/UPDATE/SKIP e motivo; nao gravar toda novidade
   nesta skill. Destino disabled fica DESABILITADO, sem falha e sem exigir
   servico. Habilitado nao significa autorizado: confirmar escopo de escrita.
6. Main aplica `haos-memory-provenance`: sanitiza, deduplica, escreve somente
   onde permitido e faz readback. Reentrada manual reutiliza identidade e
   revisao, conferindo recibos antes de repetir. Timeout ambiguo exige
   reconciliacao, nao reenvio cego.
7. Avaliar as cinco verificacoes de qualidade abaixo, separadas da contagem
   de destinos. Classificar resultado e mostrar recibo coerente com o observado.

## Cinco verificacoes locais

| Verificacao | Evidencia para PASS |
| --- | --- |
| Valor | Novidade comprovada e diferenca em relacao ao conhecimento existente |
| Escopo e privacidade | Pacote sanitizado, owners e autorizacao dos destinos |
| Proveniencia e dedupe | Origem/localizador, identidade e decisao sobre equivalentes |
| Artefato | Conteudo tematico escrito e validado dentro do escopo |
| Reconciliacao | Readback comparado em cada destino habilitado e autorizado |

Estas verificacoes avaliam qualidade do pacote, nao quantidade de destinos.
Ajustar subchecks ao dominio antes de executar e registrar N/A com motivo quando
irrelevante. N/A nao conta como PASS. Nunca usar cinco checks locais para obter
um recibo de cinco destinos.

Na contagem X/Y, Y e o conjunto de destinos distintos configurados, habilitados
e autorizados para a tarefa; X conta somente aqueles com readback real comparado
da revisao correta. Declarar o conjunto antes da escrita. Destinos disabled nao
entram na contagem nem exigem instalacao. Nao excluir destino falho do denominador
para esconder pendencia. Cinco checks locais ou um destino verificado nao sao
cinco destinos. A notacao 5/5 fica reservada a exatamente cinco destinos previstos
e efetivamente verificados; o formato publico padrao abaixo nao usa esse atalho.

## Saida

Somente o main emite um recibo de fechamento:

- `Evoluir: SO_FECHA (<task_id>)`: sem valor novo, persistencia vedada ou todos
  os destinos desabilitados; indicar motivo e eventual proposta nao aplicada.
- `Evoluir: CAPITALIZA (<task_id>) | destinos verificados X/Y`: novidade
  realmente incorporada, criterios de qualidade satisfeitos e readback real
  de todos os destinos previstos (X = Y e Y maior que zero).
- `Evoluir: PENDENTE <motivo> (<task_id>)`: entrega bloqueada, prova insuficiente
  de escrita pretendida ou destino habilitado obrigatorio sem readback.

Se nao houver task_id, substituir o campo por "sem identidade fornecida";
nao inventar registro. Incluir revision quando conhecida no relato de evidencia.
Desabilitacao prevista e opt-out, isoladamente, nao sao pendencias.
Zero destinos nao demonstra capitalizacao: nao emitir CAPITALIZA com 0/0,
instalar servicos ou inventar sucesso. Informar a proposta nao aplicada.

## Criterios de aceite

Um fechamento por tarefa/revisao; estado condizente com prova; memoria curada
sem diario literal; nenhuma mutacao em modo proibido. CAPITALIZA requer
readback real, nao fila, health, resposta de escrita ou mera intencao.

## Erros comuns

- Confundir cinco checks de qualidade com cinco destinos: manter as contagens
  separadas e informar somente readbacks realmente observados.
- Falha em destino habilitado virar disabled: manter PENDENTE e causa.
- Subagente encerrar tarefa inteira: retornar ao main sem recibo independente.

## Cenarios de pressao

- Tarefa rotineira, todos destinos disabled e cobranca de capitalizacao: usar
  SO_FECHA; nao instalar servicos nem inventar descoberta.
- Novidade valida em dry-run: apresentar proposta e SO_FECHA sem persistencia.
- Escrita retorna timeout e prazo acabou: manter PENDENTE, consultar identidade
  e reconciliar antes de qualquer nova tentativa.
