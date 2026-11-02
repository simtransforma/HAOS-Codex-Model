# TikTok Shop API v2: referencia tecnica (validada em producao 11/06/2026)

Doc oficial: https://partner.tiktokshop.com/docv2 (paginas em /docv2/page/<slug>).
O importador_tiktok_shop.py ja implementa tudo isto; use-o como referencia de codigo.

## Hosts

| Host | Uso | Assinatura? |
|---|---|---|
| `auth.tiktok-shops.com` | token/get e token/refresh | NAO |
| `open-api.tiktokglobalshop.com` | TODA a Open API (orders, finance, shops...) | SIM (HMAC) + x-tts-access-token |

## Auth (sem assinatura)

- Get: `GET /api/v2/token/get?app_key&app_secret&auth_code&grant_type=authorized_code`
- Refresh: `GET /api/v2/token/refresh?app_key&app_secret&refresh_token&grant_type=refresh_token`
- Resposta `data`: access_token (prefixo ROW_/TTP_), access_token_expire_in (unix ts, ~7d),
  refresh_token, refresh_token_expire_in (unix ts, ~99 anos), seller_name, granted_scopes[].
- auth_code: gerado quando a LOJA autoriza pelo link services.tiktokshop.com/open/authorize?service_id=...
  O code aparece na URL DE REDIRECT (query `code=`), vale 30 minutos, uso UNICO.
- Tratar refresh_token como ROTATIVO (persistir o par novo a cada refresh).

## Assinatura HMAC-SHA256 (toda chamada da Open API)

Pseudocodigo exato (igual ao signer do importador, validado com --selftest-sign):
```
params_ordenados = sort(query_params SEM 'sign' e SEM 'access_token')
base = path + concat(chave+valor de cada param ordenado) + body_cru(se houver)
wrapped = app_secret + base + app_secret
sign = hex(hmac_sha256(key=app_secret, msg=wrapped))
```
Query obrigatoria: `app_key`, `timestamp` (unix segundos, REGENERAR a cada retry), `sign`,
`shop_cipher` (na maioria dos endpoints de loja). Header: `x-tts-access-token: <access_token>`,
`content-type: application/json`.

## Endpoints usados (versoes importam!)

| Endpoint | Metodo | O que da |
|---|---|---|
| `/authorization/202309/shops` | GET | lojas autorizadas + **shop_cipher** (pegar 1x e reusar) |
| `/order/202309/orders/search` | POST | pedidos paginados (body: page_size, page_token, create_time_ge/lt). Pedido: id (18 digitos), status (UNPAID/AWAITING_SHIPMENT/AWAITING_COLLECTION/IN_TRANSIT/DELIVERED/COMPLETED/CANCELLED), payment (total_amount etc.), line_items, create_time |
| `/finance/202309/statements` | GET | statements (lotes de liquidacao) por periodo |
| `/finance/202501/statements/{id}/statement_transactions` | GET | transacoes de um statement (pedidos liquidados nele) |
| `/finance/202501/orders/{id}/statement_transactions` | GET | detalhe financeiro DO PEDIDO: revenue_amount, fee_amount (NEGATIVO), tipos de fee, settlement_amount |

Paginacao: `page_token` (cursor) + `page_size` (max 100). Iterar ate page_token vazio.

## Fees reais observados (campo type nas statement_transactions do pedido)

`fee_per_item_sold` (maior fatia), `sfp_service_fee` (programa frete da loja),
`gmv_max_ad_fee` (Ads GMV Max), `platform_commission` (pequena), `affiliate_commission`,
`affiliate_ads_commission`. Valores chegam como STRING e fees/frete NEGATIVOS:
gravar como vem; usar abs() na agregacao. Conta que fecha:
`settlement_amount = revenue_amount - abs(fees) - abs(frete_seller)`.

## Pegadinhas (todas ja mordidas e resolvidas)

1. Finance so tem pedido JA LIQUIDADO (1-2 semanas pos-entrega + janela devolucao).
   Pedido ausente no Finance nao e erro.
2. `timestamp` velho em retry = assinatura invalida. Regenerar timestamp+sign a cada tentativa.
3. Rate limit: 429 com Retry-After; o importador ja faz backoff+jitter. Throttle entre paginas.
4. Historico Finance: somente apos 2023-07-01 (limite da API).
5. shop_cipher e por loja autorizada; sem ele a maioria dos endpoints da erro de credencial.
6. Erros comuns: 36009004 = access token invalido/ausente (renovar); 98001004 invalid params
   no token/get = falta auth_code (a loja nao autorizou ainda).

## Webhook (Partner Center)

Registrado por APP no Partner Center (nao ha API para gerenciar a assinatura).
Eventos de pedido chegam como POST JSON com type + data.order_id; o fluxo n8n
[TikTok] Dash-SIM filtra e grava raw.webhook_events source='tiktok_shop'
(dedup `type:order_id`, payload cru, skipOnConflict).

