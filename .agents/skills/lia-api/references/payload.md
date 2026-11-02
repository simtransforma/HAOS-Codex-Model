# Lia, mapa do payload de webhook (target standard)

Estrutura validada em produção (integração Lia->Clint Practitioner, 18/06/2026). O webhook chega como POST com corpo JSON. Os caminhos abaixo assumem o corpo já desserializado como `body`. Em n8n, normalmente é `$json.body` ou `$json` dependendo de como o Webhook node entrega.

## Topo

```
body.event              -> nome do evento, ex.: "paid", "finished", "waiting_payment"
body.entity             -> "bill" | "billing" | "order" (nem sempre presente; o webhook é registrado por entity)
body.data               -> o recurso (cobrança/financiamento/pedido)
```

## Campos dentro de `body.data`

### Status
```
data.status             -> status atual do recurso (espelha o event na maioria dos casos)
```

### Produto (CRÍTICO, ver pegadinha 3)
```
data.offer.product.id   -> id do produto (objeto offer.product = {id, name})   ← PREFERIR ESTE
data.offer.product.name -> nome do produto
data.product.id         -> pode NÃO existir no payload; usar só como fallback
```
- Parcela de financiamento (`data.bill_type == "installment"`) carrega o produto GENÉRICO `${USER_RESOURCE_000007}`. Filtrar pelos product_ids reais para descartar parcelas.

### Contato
```
data.contact.name
data.contact.email
data.contact.phone
data.contact.cellphone
```
Fallbacks de objeto de contato (a Lia varia o nome do nó conforme o evento): tentar nesta ordem
`data.contact` -> `data.customer` -> `data.buyer` -> `data.student` -> `data.payer` -> `data.client`.
Nome alternativo solto: `data.customer_name`.

### Valor (sempre em CENTAVOS, dividir por 100)
```
data.current_amount_cents   ← preferir (valor atual da cobrança)
data.amount_cents
data.offer.amount_cents
```

### Pagamento (lista)
```
data.payments[]                       -> array de pagamentos
data.payments[].payment_method        -> "boleto" | "pix"
data.payments[].url                   -> link do boleto (para enviar ao cliente)
data.payments[].barcode               -> linha digitável do boleto
data.payments[].paid_at               -> timestamp do pagamento (quando pago)
```

### Id da transação
```
data.id        ← preferir
data.uuid
data.bill_id
```

### PII e UTM (SÓ no evento `order`, vazio em bill/billing)
```
data.customer_document     -> CPF/doc
data.address.zipcode
data.address.street
data.address.number
data.address.neighborhood
data.address.city
data.address.state
data.address.country
data.metadata.utm_source   -> UTM (só se a Lia mandar; prefixar Lia_ no destino)
data.metadata.utm_medium / utm_campaign / utm_content / utm_term  (idem, se presentes)
```

### Financiamento
```
data.bill_type             -> "installment" (parcela) | "down_payment" (entrada) | ...
data.billing_id            -> id do billing (contrato) ao qual a bill pertence
data.installment_number    -> número da parcela (quando installment)
```

## Pseudo-código de normalização (referência)

```python
def normalize(body):
    data = body.get("data", {}) or {}
    contact = (data.get("contact") or data.get("customer") or data.get("buyer")
               or data.get("student") or data.get("payer") or data.get("client") or {})
    offer = data.get("offer") or {}
    product = offer.get("product") or data.get("product") or {}
    pay = (data.get("payments") or [{}])[0]
    cents = (data.get("current_amount_cents") or data.get("amount_cents")
             or offer.get("amount_cents") or 0)
    return {
        "event":      body.get("event"),
        "status":     data.get("status"),
        "product_id": product.get("id"),
        "name":       contact.get("name") or data.get("customer_name"),
        "email":      contact.get("email"),
        "phone":      contact.get("phone") or contact.get("cellphone"),
        "value":      cents / 100,
        "method":     pay.get("payment_method"),
        "boleto_url": pay.get("url"),
        "tx_id":      data.get("id") or data.get("uuid") or data.get("bill_id"),
        "doc":        data.get("customer_document"),         # só no order
        "address":    data.get("address") or {},            # só no order
        "utm_source": (data.get("metadata") or {}).get("utm_source"),  # só se mandar
        "is_installment": data.get("bill_type") == "installment",
    }
```

> Filtrar `product_id` contra a lista de ids reais ANTES de criar lead/deal, isso descarta as parcelas (que vêm com o produto genérico) e evita duplicação.

