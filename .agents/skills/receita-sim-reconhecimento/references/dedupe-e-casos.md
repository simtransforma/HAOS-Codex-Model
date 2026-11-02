# Dedupe cross-plataforma e casos de inflacao (referencia da skill receita-sim-reconhecimento)

Detalhamento operacional. A regra resumida esta no SKILL.md; aqui ficam as chaves de dedupe e os casos reais. Tudo aplicado sobre o projeto do usuario (`fct_venda`, schemas `raw`/`stg`/`dwh`/`app`). Nunca a dash `dados-view`.

## 1. Chaves de dedupe (anti dupla contagem)

### Yampi espelhada pelo Bling
- O Bling importa/espelha os pedidos da Yampi. O MESMO pedido existe nos dois lados.
- Regra: o registro do Bling VENCE. A venda crua da Yampi e REMOVIDA quando ha o espelho Bling correspondente.
- Chave de match: numero/id do pedido Yampi referenciado no pedido Bling (canal Yampi no Bling). Se casou, mantem so o Bling.
- Erro a evitar: somar Bling + Yampi do mesmo pedido = receita dobrada naquele pedido.

### Asaas como gateway transversal
- Asaas NAO e so uma plataforma de venda; e gateway que pode estar POR TRAS de outra plataforma (a venda aparece na plataforma de origem E no Asaas).
- Regra: deduplicar por `externalReference`. O `externalReference` da cobranca Asaas aponta para o pedido na plataforma de origem.
- Se o `externalReference` casa com um pedido ja reconhecido em outra plataforma, NAO somar o Asaas de novo; e a mesma venda, outro angulo (o caixa/gateway).
- Asaas so entra como venda PROPRIA quando nao ha origem externa correspondente.

### Status de pago por plataforma
- Nao existe status generico de "pago". Cada plataforma tem o seu:
  - Yampi: status `[4, 6]` = pago.
  - TikTok Shop: pedido pago/entregue (settlement vem depois, e caixa).
  - Asaas: `PAYMENT_CONFIRMED` / `PAYMENT_RECEIVED`.
  - Eduzz / Hotmart / Assiny: status de aprovado/pago proprio de cada uma.
- Status de gerado, pendente, aguardando pagamento, expirado: NUNCA reconhece receita.

## 2. Casos reais de inflacao (detectar e expurgar)

### Caso Assiny: R$ <USER_AMOUNT> de receita FALSA (10/06)
- O que aconteceu: entrou na base um bloco de ~R$ <USER_AMOUNT>il de receita que NAO correspondia a pagamento real (registros sem confirmacao de pagamento valido contados como venda paga).
- Como detectar:
  - Salto de receita sem lastro de pagamento confirmado linha a linha.
  - Registros com status que nao e pago real, mas que vazaram pra contagem.
  - Valor agregado fora do padrao historico da plataforma (sanity check vs media).
- Acao: expurgar do total de receita reconhecida e registrar o motivo no fechamento. Nao apagar silenciosamente; deixar rastro de quanto e por que saiu.

### PIX/boleto gerado contado antes do pagamento
- Sintoma: evento de compra (Purchase) disparado na GERACAO do PIX/boleto, nao no pagamento. A venda "existe" mas o dinheiro nao entrou.
- Risco: contar PIX gerado infla a receita e ainda contamina tracking (Purchase inflado).
- Regra: so conta pagamento CONFIRMADO. Filtrar tudo que esta apenas gerado/aguardando.

### Reembolso e chargeback
- Venda reembolsada ou estornada (chargeback) SAI da receita reconhecida.
- Tratamento: subtrair (linha negativa) ou excluir a venda do periodo. Nunca manter o valor cheio de uma venda que voltou.
- Observar a data: reembolso pode cair em periodo diferente da venda original; refletir no periodo correto conforme a politica de regime adotada.

### Parcela de financiamento Lia como venda fantasma
- Parcela (`bill`) de financiamento carrega o produto GENERICO `${USER_RESOURCE_000024}`, nao o produto real do curso.
- Se a parcela for contada como venda nova, cada parcela vira uma venda fantasma e infla tanto receita quanto contagem de pedidos.
- Regra: descartar `product_id == '${USER_RESOURCE_000024}'` da contagem de VENDAS. A receita do curso ja foi reconhecida UMA vez no `order` (competencia). Parcelas sao so caixa.

## 3. Ordem recomendada de processamento

1. Trazer pago real por plataforma (aplicar status de pago proprio de cada uma).
2. Filtrar parcela Lia (`e3f6cf36`) da contagem de vendas.
3. Dedupe Yampi -> Bling (remover Yampi crua espelhada).
4. Dedupe Asaas por `externalReference` contra origens externas.
5. Expurgar receita falsa detectada (sanity check vs historico) e PIX/boleto so gerado.
6. Subtrair reembolso/chargeback.
7. Rodar `dwh.fn_dq_checks()` e ler `dwh.dq_log` (duplicidade, liquido menor ou igual ao bruto, recon Yampi x gateway).
8. So entao declarar o total como receita reconhecida, com o regime explicito.

## 4. Skills irmas (quando aprofundar)

- `cfo-dash-sim`: visao consolidada do CFO.
- `margem-sim-multiplataforma`: margem por plataforma (custo, comissao, taxa).
- `lia-api`: eventos order/billing/bill, produtos e a pegadinha do `e3f6cf36`.
- `tiktok-shop-sim`: lag de liquidacao, `raw.tiktok_settlements`, comissao real.
- `yampi`: status de pago `[4, 6]` e espelhamento Bling.
- `bling`: registro vencedor sobre a Yampi, canais de origem.

