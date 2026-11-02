---
name: lia-api
description: "Refer\u00eancia interna da API e dos eventos/webhooks da Lia EdTech (external-api.lia.com.br/external_api/v1), produtos, ofertas, pedidos, financeiro (bill/billing), estrutura do payload validada em produ\u00e7\u00e3o, pegadinhas cr\u00edticas (sem carrinho abandonado, doc/endere\u00e7o/UTM s\u00f3 no order, parcela de financiamento carrega produto gen\u00e9rico) e as integra\u00e7\u00f5es n8n existentes com a Lia. Use SEMPRE que a tarefa envolver a Lia em qualquer forma, \"Lia\", \"Lia API\", \"Lia EdTech\", \"evento/webhook da Lia\", \"produto na Lia\", \"curso na Lia\", \"registrar/criar webhook Lia\", \"pedido na Lia\", \"cobran\u00e7a/fatura da Lia\", \"financiamento Lia\", \"integrar Lia com X\", \"payload da Lia\", \"a Lia mandou um evento\", \"puxar produtos da Lia\", \"Practitioner na Lia\". Tem cliente Python pronto (auth + GET products + GET/POST webhooks) e o mapa dos 3 dom\u00ednios de evento. Padr\u00e3o validado em produ\u00e7\u00e3o (integra\u00e7\u00e3o Lia\u2192Clint Practitioner) 18/06/2026."
---

## Contrato publico de execucao

Material de dominio portado da fonte real, nao uma instalacao de infraestrutura.
As regras do usuario e do AGENTS.md prevalecem sobre comandos e exemplos abaixo.
Publicar, enviar, gastar, alterar servidores, reiniciar, apagar, push e merge
exigem consentimento explicito para o destino e a acao. Nao executar comandos
com placeholders. Nao buscar o cofre ou ambientes do autor. Ferramentas/MCPs
citados precisam existir na instalacao do usuario; nomes nao provam acesso.
Consulte [PORTABILITY.md](PORTABILITY.md) para dependencias, recursos omitidos,
licencas e adaptacoes. Exemplos preservados nao sao prova de estado vivo.

# Lia EdTech, API + eventos/webhooks

Como operar a API da Lia (EdTech com financiamento de cursos) e tratar os eventos/webhooks sem redescobrir as pegadinhas (sem evento de carrinho abandonado, doc/endereço/UTM só no `order`, parcela de financiamento com produto genérico). Edicao publica: contas, catalogos e destinos devem ser fornecidos pelo usuario.

## Quando usar

Triggers do user:
- "Lia", "Lia API", "Lia EdTech", "docs da Lia"
- "evento/webhook da Lia", "a Lia mandou um evento", "registrar/criar webhook Lia", "qual o payload da Lia"
- "produto/curso na Lia", "puxar/listar produtos da Lia", "criar produto na Lia"
- "pedido na Lia", "cobrança/fatura da Lia", "financiamento Lia", "parcela da Lia"
- "integrar Lia com [X]" (Clint, ActiveCampaign, BI, etc.)
- "Practitioner na Lia"

Use também quando um workflow n8n receber um webhook da Lia e precisar normalizar o payload.

## Acesso

- **Base (Prod):** `https://external-api.lia.com.br/external_api/v1`
- **Base (Sandbox):** `https://external-api-sandbox.lia.com.br/external_api/v1`
- **Auth:** header `Authorization: Bearer <LIA_API_KEY>` (do ${USER_SECRET_FILE}, NUNCA hardcode)
- **Docs:** https://docs.lia.com.br

```bash
# Smoke test (lista produtos)
curl -s -H "Authorization: Bearer $LIA_API_KEY" \
     "https://external-api.lia.com.br/external_api/v1/products?per_page=5"
```

## Cliente Python pronto

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".Codex" / "skills" / "lia-api" / "scripts"))
from lia_client import LiaClient

lia = LiaClient.from_master_env()      # lê LIA_API_KEY automaticamente
produtos = lia.list_products()         # GET /products (paginado)
prod = lia.get_product("${USER_RESOURCE_000006}")
hooks = lia.list_webhooks()            # GET /webhooks
lia.create_webhook(                    # POST /webhooks (ADITIVO, não substitui)
    name="Clint Lia Order",
    url="https://service.example.invalid/webhook/clint-lia-practitioner",
    entity="order",
    events=["finished", "canceled"],
)
```

Caminho: `${USER_WORKSPACE_ROOT}`

## Endpoints (40+ no total)

Os usados em produção em detalhe; o resto resumido. Lista completa em `<USER_DEPENDENCY:references/endpoints.md>`.

| Recurso | Endpoint | Uso |
|---|---|---|
| **Produtos** | `GET /products?search=&availability=&page=&per_page=` | listar (paginado) |
| | `GET /products/{id}` | buscar produto |
| | `POST /products` / `PATCH /products/{id}` / `DELETE /products/{id}` | CRUD |
| **Ofertas** | `GET /offers` / `GET /offers/{id}` | listar/buscar oferta |
| | `GET /offers/{id}/payment_info` | simular parcelas/financiamento |
| | `POST /offers` (amount_cents min 500) / `PUT /offers/{id}` | criar/editar |
| | `PUT /offers/{id}/enable` / `disable` | ativar/desativar |
| **Pedidos** | `GET /orders?search=&status=&created_at_start=&created_at_end=` | listar pedidos |
| | `GET /orders/{id}` / `GET /orders/{id}/payment_info` | buscar / elegibilidade financiamento |
| | `POST /orders` (offer_id, email, customer_name, CPF, address) | criar pedido |
| | `POST /orders/{id}/charge` | cobrar (boleto, pix, NÃO cartão) |
| **Financeiro** | `GET /bills` / `GET /bills/{id}` | faturas |
| | `GET /billings` / `GET /billings/{id}` | cobranças (assinatura/financiamento) |
| | `GET /payments` / `GET /payments/{id}` | pagamentos |
| | `GET /payments/{id}/download_boleto` | boleto PDF |
| **Contratos** | `GET /contracts` / `GET /contracts/{id}` | contratos de financiamento |
| **Webhooks** | `GET /webhooks` | listar |
| | `POST /webhooks` | criar (ADITIVO) |
| | `PUT /webhooks/{id}` / `DELETE /webhooks/{id}` | editar/excluir |
| **Referência** | `GET /kinds` / `GET /shifts` / `GET /states` / `GET /cities?state_id=` | tipos, turnos, estados, cidades |
| | `GET /payment_configurations/default` | config padrão de pagamento da empresa |
| **Validação** | `POST /contacts/{id}/send_validation_token` (sms/whatsapp/email) | enviar token |
| | `PUT /contacts/{id}/validate_token` (sandbox: 123456) | validar token |

## Eventos / webhooks, os 3 domínios

A Lia emite em 3 entidades (`entity`), cada uma com seu conjunto de eventos. Detalhe e amostra de payload por evento em `./references/events.md`.

| `entity` | Significado | Eventos |
|---|---|---|
| **bill** | Cobrança / fatura (boleto/pix individual, parcela) | `paid`, `pending`, `overdue`, `canceled` |
| **billing** | Assinatura / financiamento (o "contrato" recorrente) | `waiting_payment`, `active`, `finished`, `canceled` |
| **order** | Pedido (a compra em si) | `in_progress`, `finished`, `canceled` |

Lia é EdTech **com financiamento**, então o normal é um ciclo recorrente `bill pending` -> `bill paid` por parcela, sob um `billing`. Tratar parcela diferente de venda nova (ver pegadinha 3).

### Registrar webhook

`POST /webhooks` com body:

```json
{ "name": "Clint Lia Order", "url": "https://service.example.invalid",
  "entity": "order", "events": ["finished", "canceled"],
  "target": "standard", "verb": "post" }
```

- **É ADITIVO:** criar um webhook NÃO remove nem substitui os existentes. Sempre `GET /webhooks` ANTES e DEPOIS pra confirmar o que mudou (e não duplicar).
- `target: "standard"` é o formato padrão de payload (o que está documentado aqui).
- Um webhook por `entity`, com a lista de `events` daquela entidade.

## Estrutura do PAYLOAD (validada em produção)

Resumo. Mapa de campo completo (com todos os fallbacks) em `./references/payload.md`.

| O que | Caminho no payload |
|---|---|
| Evento | `body.event` |
| Status | `body.data.status` |
| **Produto (id)** | `body.data.offer.product.id` (objeto `{id,name}`) OU `body.data.product.id` |
| Contato | `data.contact.{name,email,phone,cellphone}` (fallbacks `customer`/`buyer`/`student`/`payer`/`client`) |
| Nome (alt) | `data.customer_name` |
| Valor (CENTAVOS) | `data.current_amount_cents` / `data.amount_cents` / `data.offer.amount_cents` -> **dividir por 100** |
| Pagamento | `data.payments[]` -> `payment_method` (boleto/pix), `url` (link do boleto), `barcode`, `paid_at` |
| Id da transação | `data.id` / `data.uuid` / `data.bill_id` |
| Doc/CPF | `data.customer_document` (**só em `order`**) |
| Endereço | `data.address.*` (**só em `order`**) |
| UTM | `data.metadata.utm_source` (**só se a Lia mandar**, e em geral só no `order`) |

> O produto na Lia, no payload de venda, é `data.offer.product.id`. O objeto `data.product` direto pode NÃO existir no payload, sempre tente `offer.product.id` primeiro.

## Pegadinhas críticas (mapeadas em produção)

| # | Pegadinha | Detalhe | Solução |
|---|---|---|---|
| 1 🔴 | **Lia NÃO emite carrinho abandonado** | Diferente da Assiny, não existe evento de checkout/carrinho abandonado | Não esperar esse evento; se o funil tem stage "Carrinho Abandonado", ele só recebe "ganho", nunca entrada |
| 2 🔴 | **doc/CPF, endereço e UTM só vêm no `order`** | Em `bill` e `billing` esses campos vêm **vazios** | Coletar PII no evento `order`; nos demais, merge não-destrutivo no destino (o Clint preenche quando o `order` chega) |
| 3 🔴 | **Parcela de financiamento carrega produto GENÉRICO** | `bill` de parcela (`bill_type: installment`) vem com produto `${USER_RESOURCE_000007}` ("Curso Sociedade Internacional do Mindset"), **NÃO** o produto real | **SEMPRE filtrar pelo product_id real.** Filtrar pelos ids reais descarta parcelas automaticamente -> sem deal/lead duplicado por parcela. Entrada (down_payment) e order/billing carregam o produto real |
| 4 | Valores em centavos | Todos os `*_amount_cents` são inteiros em centavos | Dividir por 100 antes de gravar/exibir |
| 5 | `charge` não aceita cartão | `POST /orders/{id}/charge` só boleto e pix | Não tentar cartão por essa rota |
| 6 | Oferta tem `amount_cents` mínimo | `POST /offers` exige `amount_cents >= 500` (R$ <USER_AMOUNT>) | Validar antes de criar oferta |

## Padrão de gravação no destino

A regra da casa (decisão do usuario, padrão FPV369/Practitioner) é gravar no Clint via **API REST direta** (não pelo webhook de integração do painel Clint). Cliente Python + pegadinhas do Clint na skill `clint-api`. Resumo do que importa ao integrar Lia->Clint:
- `POST /deals` do Clint respeita `stage_id` no body, e faz upsert de contato, mas NÃO é idempotente (checar deal existente antes).
- Custom fields NÃO entram via `POST /deals` (gravar via `POST /contacts/{id}`).
- Tag = `POST /contacts/{id}/tags` com body **array de strings**.
- Prefixar `utm_source` com `Lia_` quando vier no payload.

## Restrições / segurança

- **NUNCA** hardcode o token em node, expressão, log ou screenshot. Sempre `LIA_API_KEY` do ${USER_SECRET_FILE} (referenciar por nome).
- Header é `Authorization: Bearer <LIA_API_KEY>`.
- Ações externas irreversíveis (criar/cobrar pedido, criar/excluir webhook em produção) -> mostrar plano e pedir OK do usuario.
- `POST /webhooks` é aditivo; antes de criar, `GET /webhooks` e salvar backup da lista (`_secrets/backups/lia_webhooks_BEFORE_<data>.json`).
- Em logs, mascarar email/phone/CPF.

## Skills / refs relacionadas

- `clint-api`, cliente Python + pegadinhas da API do Clint (destino das integrações Lia->Clint).
- `haos-n8n-api`, operar/editar os workflows n8n que recebem webhooks da Lia.
- `haos-hetzner-map`, carregar antes de mexer no servidor.
- Memórias: `<USER_PROJECT_CONTEXT>`, `<USER_PROJECT_CONTEXT>` (padrão de integração).

