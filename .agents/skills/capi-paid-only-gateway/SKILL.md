---
name: capi-paid-only-gateway
description: ">- Playbook da \"virada paid-only\" , ligar Purchase CAPI server-side que conta SO venda paga (1 por pedido) para um gateway de checkout (Yampi, Lia, Assiny, Eduzz, Hotmart, Asaas...), matando o Purchase fantasma de PIX/boleto gerado. Use SEMPRE que a tarefa for \"marcar so venda real no Meta\", \"Purchase duplicado/inflado\", \"pix gerado contando como venda\", \"ligar CAPI paid-only pra [plataforma]\", \"gateway novo precisa marcar evento no Meta\", \"virada do Purchase\", ou variacoes. Padrao provado em producao: Yampi (09/07/2026) e Lia (17/07/2026), pixel ${RESOURCE_ID}. INTERNA, nao vai pro HAOS_CC (repo privado desde 19/07/2026; skill fica em ${HAOS_PRIVATE_ROOT} - GPT-Codex/HAOS/your-private-project/.agents/skills por ser especifica de cliente, nao por exposicao publica)."
---

# Virada paid-only de gateway (Purchase CAPI so em venda paga)

Objetivo: o Meta contar **1 Purchase por pedido PAGO**, nunca PIX/boleto gerado, nunca parcela.
Inflacao tipica sem isso: **2,0-2,3x** (so ~27-78% dos pedidos criados viram caixa).

## Arquitetura (padrao provado)

```
Webhook da plataforma (SO evento de PAGO)
  -> workflow n8n feeder (filtro + contrato + POST, timeout 30s)
  -> sGTM ${RESOURCE_ID}: Data Client /<plataforma> -> trigger customEvent <plat>.order.paid
  -> tag Purchase S2S (template ${RESOURCE_ID}) -> pixel ${RESOURCE_ID}
```

## O contrato do POST (o que o feeder monta)

- `event`: `<plataforma>.order.paid` (bate com o trigger)
- `event_id`: **deterministico** `<plataforma>_<id_da_cobranca>` (dedup Meta ~48h; re-POST seguro)
- `order.total` (reais, nao centavos), `order.currency` (BRL), `order.contents` `[{id,quantity,item_price}]`, `order.product_ids/names`, `order.id`
- `customer.email` **LOWERCASE** + `first_name/last_name/phone` (DDI 55) + city/state/zip/country quando houver
- `page_location`/`event_source_url`: **URL REAL** , `checkout_url` do payload > URL real do checkout da plataforma como fallback. **NUNCA vazio** (enforcement `capi_no_url` DESCARTA o evento; foi o colapso de 14-17/07) e **NUNCA fake**
- `attribution.fbc/fbp` se vierem; senao a tag resolve (abaixo)

## A tag S2S (clonar da tag 142 Yampi / 176 Lia)

- `event_id` + value/currency/contents mapeados das vars `ed` do contrato
- **fbc/fbp com fallback duplo**: payload primeiro (`attribution.*`), senao **reader do Stape Store by-email** (template ${RESOURCE_ID}, documentId = var email-lowercase, documentPath fbc/fbp) via `convertNull/UndefinedToValue`
- `enableEventEnhancement=true`
- `event_source_url` com `setDefaultValue` = URL real da plataforma

## Regras duras (aprendidas com sangue)

1. **NUNCA 2 fontes contando juntas.** Desligar o prematuro (pixel browser da plataforma / tag browser / espelho GA4->CAPI) no MESMO ciclo que liga o paid , "virada casada", 1 publish. Meia-virada = ou dobra ou o evento pago e descartado como duplicata do prematuro.
2. **Filtro "1a cobranca paga do pedido"**: NAO confie num unico `bill_type`. Na Lia, a vista = `installment` + `installments=1` (nao existe tipo "a vista"); so `down_payment` descartou venda real. Levante os `bill_type` REAIS no historico (raw.webhook_events) antes de travar o filtro.
3. **Webhook n8n criado via API exige `webhookId`** no node, senao 404 silencioso com active=true (ver skill haos-n8n-api). Teste de fumaca: POST no path = 200.
4. **Validacao so com venda criada APOS o publish** (zona cinzenta de dedup ~48h). A 1a venda real e o teste E2E , acompanhar ela ate o `/stats` do dataset (ler buckets posicionalmente, labels de hora mentem).
5. **Nativa da plataforma**: verificar ANTES se ja e paid-only (Assiny e; provar por timing 1:1 com webhook de aprovacao). Se for, NAO mexer , so nao somar outra fonte sem dedup.
6. Backup de tudo antes (GTM live version + JSON dos workflows) = rollback em minutos.
7. Eventos de recuperacao/carrinho NAO entram aqui , Purchase e SO pago.

## Checklist da virada

- [ ] Payload real mapeado (campos + bill_types no historico)
- [ ] Feeder n8n (webhookId!, filtro paid+1a cobranca, contrato completo, timeout 30s, INATIVO)
- [ ] Workspace GTM: client + trigger + tag S2S + vars (email lowercase + readers Store + fallbacks URL)
- [ ] Webhook na plataforma SO do evento pago (aditivo, nao mexer nos existentes)
- [ ] Desligar a fonte prematura (se existir) no mesmo ciclo
- [ ] 1a venda real: execucao success no n8n + Purchase com event_id certo no /stats

## Adaptacao Codex HAOS

- Carregar `${HAOS_PRIVATE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
