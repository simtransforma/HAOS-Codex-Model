# Jornada do card: abandono, pagamento gerado e pagamento aprovado

<!-- synthetic-client-examples -->
Exemplos sinteticos: nomes de campanha, contatos, IDs, valores e configuracoes abaixo sao ficticios, nao um inventario de cliente nem evidencia de producao. Adaptar IDs e slugs ao contrato autorizado; conferir a versao da API e o resultado antes de qualquer efeito externo.


Modelo sintetico de jornada CRM, independente de cliente ou campanha. Exige mapeamento e aprovacao do usuario antes de efeitos externos.

## Uma origem com varias etapas

| Evento | Acao no card da pessoa nessa origem |
|---|---|
| Abandono | Buscar o card existente; criar apenas se nao houver. |
| Pagamento gerado | Atualizar o mesmo ID para Compra Gerada, ainda aberto. |
| Pagamento aprovado | Atualizar o mesmo ID para Compra Aprovada, Fechado/Ganho (`WON`), valor confirmado e tag paga do produto no contato. |
| Evento repetido ou atrasado | Reutilizar o ID; nunca duplicar nem reabrir um ganho por abandono, gerada ou recusa antiga. |

Um novo carrinho ou ID de evento nao justifica outro card para o mesmo contato
na mesma origem. Ledger financeiro e idempotencia de email continuam por
pedido/produto: nao confundir essa chave com a identidade do card no CRM.

## Etapas distribuídas em origens diferentes

Usar somente a cadeia de origens mapeada para o produto/campanha:

1. Abandono -> pagamento gerado: fechar como ganho o card existente na origem
   Abandono; buscar na origem Compra Gerada e atualizar ou criar se ausente.
   O card de Compra Gerada permanece aberto enquanto o pagamento estiver pendente.
2. Pagamento gerado -> pagamento aprovado: dar ganho nos cards existentes das
   origens anteriores da jornada e atualizar ou criar, se ausente, o card na
   origem Compra Aprovada. O card aprovado tambem fica Fechado/Ganho (`WON`).
3. Aplicar a tag paga somente com confirmacao financeira. Nao criar cards
   retroativos nas origens anteriores que o contato nao percorreu.
4. Se a entrega da transicao falhar parcialmente, retomar pelas acoes faltantes
   e conferir o destino antes de criar; nunca repetir criacao cegamente.

**Ganho de etapa nao e prova de dinheiro recebido.** Em origens separadas,
varios cards podem estar ganhos pela mesma jornada. Relatorios financeiros,
tag paga e email de compra usam o pagamento/pedido comprovado; nao somar todos
esses ganhos como vendas distintas nem enviar email ao apenas gerar pagamento.

## Invariantes de implementacao

- Identidade do CRM: contato validado + origem. Produto/oferta define a origem
  pelo mapa aprovado; nunca fechar negocios de outras campanhas por coincidencia
  de contato. Origem compartilhada por produtos distintos exige escopo explicito.
- Consultar todas as paginas/status relevantes (OPEN/WON/LOST); confirmar
  filtros e identidade. Resposta incompleta ou erro nao significa card ausente.
- Serializar lookup/criacao/atualizacao ate o readback. Persistir o ID e a
  intencao de criacao; resposta incerta exige reconciliacao, nao outro POST.
- Atualizar etapa, status e valor comprovado. Nao somar o mesmo pedido a cada
  evento nem deixar valor zero herdado do abandono depois de uma compra paga.
- Separar estado financeiro do pedido e estado da jornada CRM. Evento antigo
  nao reabre ganho; tag pertence ao contato e nao prova pagamento de cada card.
- Conferir por GET o mesmo ID, contato, origem, etapa, status, valor e tag.
- Duplicados historicos: preservar um card canonico e o historico; reconciliar
  separadamente com autorizacao. Nao marcar todos como ganhos nem excluir.

## Cenarios obrigatorios de aceite

- Abandono -> gerada -> paga na mesma origem: um unico ID, valor correto,
  Compra Aprovada/WON e tag paga ao final.
- Origens separadas: card anterior ganho; no destino, um unico card criado
  ou reaproveitado; origem aprovada com card WON. Gerada nao dispara tag/email pago.
- Repeticao, eventos simultaneos e evento atrasado: sem card extra ou regressao.
- Falha entre fechar a origem anterior e atualizar o destino: retomada sem duplicar.
- Pagamento recebido sem abandono/gerada anteriores: somente destino necessario.
- Confirmacao financeira e envio idempotente continuam por pedido; mudanca do
  ponteiro do card nao reenvia email nem duplica receita.

Cenario sintetico adicional: criar fixtures de um contato e origens de exemplo, simular eventos repetidos e fora de ordem e conferir identidade unica do card, status, valor e tag. Nenhuma auditoria, metrica ou execucao real e alegada por este documento.
