# Clint API — Schema dos objetos principais

<!-- synthetic-client-examples -->
Exemplos sinteticos: nomes de campanha, contatos, IDs, valores e configuracoes abaixo sao ficticios, nao um inventario de cliente nem evidencia de producao. Adaptar IDs e slugs ao contrato autorizado; conferir a versao da API e o resultado antes de qualquer efeito externo.


Estruturas de exemplo sintetico: preservar nomes e tipos do contrato e conferir o esquema real da versao usada.

## Contact (Contato)

Objeto retornado por `GET /contacts/{id}` e em `data[]` de `GET /contacts`.

```json
{
  "id": "example-id",
  "name": "Exemplo sintetico",
  "email": "contact@example.invalid",
  "username": "example-username",             // identificador opcional (raro)
  "fullPhone": "<EXAMPLE_FULLPHONE>",          // ⭐ CANÔNICO — usar este
  "phone": "<EXAMPLE_PHONE>",            // raw, formato variado
  "complete_phone": null,                 // legado, geralmente vazio
  "ddi": "55",                            // ⚠️ separado de phone/fullPhone
  "valid_phone": true,
  "duplicate_phone": false,

  "tags": [
    {"id": "example-id", "name": "Exemplo sintetico"},
    {"id": "example-id", "name": "Exemplo sintetico"}
  ],

  "fields": {                             // ⭐ PII e custom fields AQUI dentro
    "cep": "<EXAMPLE_CEP>",                   // CEP só dígitos
    "doc": "<EXAMPLE_DOC>",                // CPF só dígitos
    "sobrenome": "example-sobrenome",                // ⚠️ Clint separa sobrenome aqui
    "bairro": "example-bairro",
    "cidade": "São Paulo",
    "estado": "SP",                       // pode vir "SP" ou "São Paulo"
    "endereco": "example-endereco",
    "n°_do_endereco": "example-n-do-endereco",            // ⚠️ chave tem caractere especial
    "complemento": "example-complemento",
    "pais": "example-pais",
    "produto": "example-produto",                  // produto associado ao lead
    "utm_source": "example-utm-source",            // ⭐ tracking UTM vai aqui
    "whatsapp_number": "example-whatsapp-number",   // pode diferir de fullPhone
    "cobranca_vigente": "example-cobranca-vigente",
    "metodo_de_pagamento": "example-metodo-de-pagamento",
    "notes": "example-notes"
  },

  "organization": {                       // empresa associada (se houver)
    "id": "example-id",
    "name": "Exemplo sintetico",
    "fields": {
      "state": "SP"                       // ⚠️ às vezes estado vem aqui
    }
  },

  "status": "active",
  "stage": "example-stage",
  "value": 100.00,
  "lost_status": null,
  "won_at": null,
  "lost_at": null,
  "origin": "example-origin",

  "user_email": "example-user-email",  // vendedor responsável
  "user_name": "example-user-name",
  "user_phone": null,
  "user_link": null,

  "created_at": "2000-01-01T00:00:00Z",
  "updated_at": "2000-01-01T00:00:00Z"
}
```

### ⚠️ Edge cases de Contact validados

- `c["fields"]` pode ser **dict vazio `{}`** pra contatos antigos / importados sem custom fields. Sempre usar `(c.get("fields") or {}).get(k)`.
- `c["username"]` é raro mas existe — útil se Clint integra com plataforma externa que usa username.
- **IP do contato NÃO está disponível** via API — nem em /contacts nem em /deals nem em custom fields).
- A chave `"n°_do_endereco"` tem caractere especial (`°`) — cuidado ao acessar via `getattr` ou copiar pra schemas Python.

### Campos derivados úteis

| Quer | Onde está |
|---|---|
| Email canônico | `email` |
| Telefone canônico (E.164) | `fullPhone` |
| CPF | `fields.doc` |
| CEP | `fields.cep` |
| Sobrenome | `fields.sobrenome` (ou último token de `name`) |
| Cidade | `fields.cidade` |
| Estado (UF 2 letras) | `fields.estado` (mapear pelo STATE_MAP) |
| Tags como lista de strings | `[t["name"] for t in contact["tags"]]` |
| Origem do lead | `origin` |
| Data captura | `created_at` (ISO 8601 UTC) |

⚠️ Sempre acessar `c["fields"].get(k)` com fallback em `c.get(k)`. Nem todo contato tem `fields` populado.

## Tag

```json
{
  "id": "example-id",
  "name": "Exemplo sintetico",
  "color": "example-color",                     // opcional
  "created_at": "2000-01-01T00:00:00Z",
  "contacts_count": 685                   // pode ou não vir
}
```

⚠️ Bug crítico: `?search=` em `/tags` **não filtra**. Use `find_tag_by_name()` da `ClintClient`.

## Deal (Negócio)

```json
{
  "id": "example-id",
  "title": "example-title",
  "value": 100.00,
  "currency": "BRL",

  "pipeline_id": "example-pipeline-id",
  "stage_id": "example-stage-id",
  "status": "open",                       // open | won | lost
  "lost_reason": null,

  "contact": {
    "id": "example-id",
    "name": "Exemplo sintetico",
    "email": "contact@example.invalid"
  },
  "organization": {...},

  "expected_close_date": "example-expected-close-date",
  "won_at": null,
  "lost_at": null,

  "fields": {
    "produto": "example-produto",
    "fonte": "example-fonte"
  },

  "created_at": "2000-01-01T00:00:00Z",
  "updated_at": "2000-01-01T00:00:00Z"
}
```

## Pipeline

```json
{
  "id": "example-id",
  "name": "Exemplo sintetico",
  "stages_count": 5,
  "deals_count": 124,
  "created_at": "2000-01-01T00:00:00Z"
}
```

## Stage (Estágio do pipeline)

```json
{
  "id": "example-id",
  "name": "Exemplo sintetico",
  "pipeline_id": "example-pipeline-id",
  "order": 2,                             // posição na sequência
  "probability": 0.4,                     // % de fechamento estimado
  "deals_count": 18
}
```

## Organization

```json
{
  "id": "example-id",
  "name": "Exemplo sintetico",
  "domain": "example-domain",
  "fields": {
    "state": "SP",
    "city": "São Paulo",
    "cnpj": "example-cnpj"
  },
  "contacts_count": 4
}
```

## Webhook payload (eventos Clint → externo)

Quando Clint dispara webhook (se configurado), payload típico:

```json
{
  "event": "contact.tag.added",           // ou .removed, .created, .updated
  "timestamp": "example-timestamp",
  "data": {
    "contact_id": "example-contact-id",
    "tag_id": "example-tag-id",
    "tag_name": "example-tag-name",
    "contact": {...}                      // payload completo do Contact
  }
}
```

Se eventos forem incompletos no teste autorizado, avaliar polling + diff com agenda e limites definidos pelo usuario; nenhum workflow e fornecido como ativo.

## Custom Fields (campos personalizados) —

⚠️ **A API REST NÃO tem endpoint de custom fields** (todos `/custom_fields`, `/fields`, etc. dão 404; `/contacts/custom_fields` dá 400 "Param ID must be a valid UUID" porque cai na rota `/contacts/{id}`). **Definição de campo só pelo painel web.** Ver `endpoints.md` seção CUSTOM FIELDS.

Como o custom field aparece e persiste num contato:

- Fica dentro do mapa `fields` do contato, keyado pelo **slug** (minúsculo, espaço→`_`, acentos mantidos: `n°_do_endereco`).
- **Silent drop:** `POST /contacts` descarta sem erro qualquer chave de `fields` cujo slug não exista no painel. Só persiste o que já é campo registrado.
- Pra ler: `c["fields"].get(slug)`.

Exemplo sintetico: verificar `utm_source`, `utm_medium`, `utm_content`, `utm_term` e `utm_campaign`. Um typo como `utm_campaing` e apenas um caso de teste de slug legado, nao configuracao presumida.

## Mapping pra outras plataformas

### → Meta Ads Custom Audience (SHA-256 multi-key)

| Meta field | Clint field |
|---|---|
| EMAIL | `email.lower()` |
| PHONE | `fullPhone` (já E.164) |
| FN | `name.split()[0].lower()` |
| LN | `fields.sobrenome` ou `name.split()[-1]` |
| ZIP | `fields.cep` (8 dig) |
| CT | `fields.cidade.lower()` |
| ST | `STATE_MAP[fields.estado.lower()]` → 2 letras |
| COUNTRY | `"br"` fixo |
| EXTERN_ID | `fields.doc` (CPF 11 dig) |

Ver `normalize_contact()` no `clint_client.py` — já implementado e validado.

### → Mailchimp / ActiveCampaign

Email + nome + tags. Telefone se a plataforma aceitar.

### → WhatsApp Business / Evolution

`fullPhone` direto. Validar `valid_phone == true` antes.

## Convencoes de nomenclatura: exemplos sinteticos

Uma automacao pode adotar `example_product_example_stage_010100` ou `example_action_example_context`.
Sao exemplos inventados, nao tags existentes. Definir o parser por contrato, testar entradas invalidas e
mapear explicitamente produto, etapa e origem; nao inferir pagamento ou identidade pelo nome de uma tag.
