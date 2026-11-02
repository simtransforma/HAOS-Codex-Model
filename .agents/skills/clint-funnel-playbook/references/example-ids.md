# Exemplo parametrizavel: Assiny e Lia no mesmo funil

Este exemplo preserva o mapeamento operacional entre eventos e cards, sem IDs,
produtos, nomes de clientes, prefixos de IDs ou configuracao de tenant reais.
Resolver todos os parametros no ambiente do usuario antes de qualquer escrita.

## Grupo, suborigens e stages

No modelo origin + stage, selecionar um grupo `${CLINT_GROUP_NAME}` e resolver
as suborigens por `GET /origins` ou pelo painel. Nao assumir um pipeline ID.
Cada suborigem pode ter uma coluna por plataforma; conferir os stages de ambas.

| Suborigem | Parametro de origin_id |
|---|---|
| Carrinho Abandonado | `${ORIGIN_ABANDONED}` |
| Gerou Pagamento | `${ORIGIN_PAYMENT_CREATED}` |
| Compra Negada | `${ORIGIN_REFUSED}` |
| Compra Aprovada | `${ORIGIN_APPROVED}` |

A tag de pagamento `${PAID_TAG_ID}` pertence ao produto, nao a plataforma.
Aplicar somente em evento aprovado confirmado. Match por email normalizado.

## Assiny: eventos para suborigem

| Evento | Suborigem |
|---|---|
| `abandoned_purchase` / `abandoned_checkout` | Carrinho Abandonado |
| `pix_generated` / `bank_slip_generated` | Gerou Pagamento |
| `refused` | Compra Negada |
| `approved_purchase` | Compra Aprovada, com tag |

Filtrar `${TARGET_PRODUCT_ID}` antes da branch de upsert. Prefixar a origem UTM
com `${ASSINY_UTM_PREFIX}` configurado pelo usuario, sem substituir UTM existente.
Gerou/Negada da ganho no card anterior de Carrinho; Aprovada da ganho nos cards
anteriores de Carrinho, Gerou e Negada, sempre filtrando pelo origin_id correto.

Nao inventar endereco em checkout digital: `client.address` pode estar ausente.
Documentar os campos disponiveis, sem registrar CPF, IP ou payload de comprador.
Operacoes paralelas anteriores ao CRM nao devem abortar silenciosamente o upsert:
revisar ordem dos nodes, tratamento onError e evidencia de cada efeito.

## Lia: produtos, eventos e stages

Filtrar `data.offer.product.id` por uma allowlist local de produtos-alvo.
Excluir o produto generico de parcela: parcela paga nao e nova compra do produto.
Resolver `${LIA_STAGE_PENDING}`, `${LIA_STAGE_APPROVED}` e `${LIA_STAGE_REFUSED}`
nas colunas Lia das respectivas suborigens; nunca usar um prefixo truncado como ID.

| Status | Suborigem | Stage |
|---|---|---|
| `pending` / `waiting_payment` | Gerou Pagamento | `${LIA_STAGE_PENDING}` |
| `paid` / `finished` / `active` | Compra Aprovada | `${LIA_STAGE_APPROVED}`, com tag |
| `canceled` / `overdue` | Compra Negada | `${LIA_STAGE_REFUSED}` |
| Sem fonte de abandono | Carrinho Abandonado | Recebe somente ganho |

Conferir disponibilidade real dos eventos antes de criar webhooks aditivos:
Order(finished,canceled), Billing(waiting_payment,active,finished,canceled) e
Bill(paid,pending,overdue,canceled). URL e workflows sao configuracao do usuario.

Doc/endereco/UTM podem vir somente em `order`; `bill`/`billing` podem estar vazios.
O MERGE deve preencher com o order posterior sem apagar valores existentes.
Prefixar `data.metadata.utm_source`, se presente, com `${LIA_UTM_PREFIX}`.

## Upsert e verificacao cruzada

Ambas as plataformas usam o mesmo grupo, com seus proprios stages. Um lead que
abandona numa e paga na outra deve ter o card movido/ganho, nao duplicado.
Conferir o resultado por leitura do card, origin_id, stage_id e tags depois do
evento controlado. Aceite de webhook nao comprova a mutacao final no CRM.
Nao executar disparos nem escrita de producao sem autorizacao aplicavel.
