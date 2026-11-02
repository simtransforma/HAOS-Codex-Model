# Lia, catálogo de eventos / webhooks (entity + event)

A Lia emite webhooks em 3 entidades (`entity`). Cada webhook é registrado com `entity` + lista de `events` daquela entidade. O payload chega com `body.event` (o nome do evento) e `body.data` (o recurso). `target: "standard"` é o formato documentado aqui.

## Domínio `bill` (cobrança / fatura individual)

Uma `bill` é uma cobrança concreta: um boleto, um pix, ou uma parcela de financiamento. É o nível em que o dinheiro entra de fato.

| event | Quando dispara | Observação |
|---|---|---|
| `pending` | Boleto/pix gerado, aguardando pagamento | gera "Gerou Pagamento" no funil |
| `paid` | Cobrança paga | a venda (ou a parcela) foi quitada |
| `overdue` | Cobrança vencida sem pagamento | tratar como negada/vencida |
| `canceled` | Cobrança cancelada | |

> 🔴 Em financiamento, cada PARCELA é uma `bill` própria, com seu ciclo `pending` -> `paid`. A parcela carrega o produto GENÉRICO (ver pegadinha 3 na SKILL.md), filtrar pelo product_id real para não duplicar lead/deal a cada parcela.

## Domínio `billing` (assinatura / financiamento)

O `billing` é o "contrato" recorrente que agrupa as `bill` (parcelas). É o nível da assinatura/financiamento como um todo.

| event | Quando dispara | Observação |
|---|---|---|
| `waiting_payment` | Financiamento/assinatura criado, aguardando 1º pagamento | equivalente a "gerou pagamento" no nível do contrato |
| `active` | Financiamento ativo (em dia) | venda efetivada / aluno ativo |
| `finished` | Financiamento concluído (todas as parcelas quitadas) | |
| `canceled` | Financiamento cancelado | |

## Domínio `order` (pedido)

O `order` é a compra em si (o checkout). É o ÚNICO evento que traz PII completa (doc/CPF, endereço) e UTM.

| event | Quando dispara | Observação |
|---|---|---|
| `in_progress` | Pedido criado, em andamento | normalmente ignorado em funil de venda |
| `finished` | Pedido concluído | dispara matrícula/entrega (ex.: lista Alunos no AC) |
| `canceled` | Pedido cancelado | |

> 🔴 doc/CPF (`data.customer_document`), endereço (`data.address.*`) e UTM (`data.metadata.utm_source`) **só vêm no `order`**. Em `bill`/`billing` esses campos vêm vazios.

## Mapeamento usado na integração Practitioner (Lia -> Clint)

Referência do funil G369, stage "Lia" (memória `<USER_PROJECT_CONTEXT>`):

| status Lia | suborigem Clint | stage "Lia" |
|---|---|---|
| `pending` / `waiting_payment` | Gerou Pagamento | stage Gerou |
| `paid` / `finished` / `active` | Compra Aprovada (+ tag `Practitioner_pago`) | stage Aprovada |
| `canceled` / `overdue` | Compra Negada | stage Negada |
| (não existe) Carrinho Abandonado | só recebe "ganho", nunca entrada | |

Dar ganho (status WON no Clint): Gerou/Negada -> ganha(Carrinho); Aprovada -> ganha(Carrinho + Gerou + Negada).

