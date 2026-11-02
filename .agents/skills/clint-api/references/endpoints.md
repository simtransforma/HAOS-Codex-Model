# Clint API, Endpoints mapeados

<!-- synthetic-client-examples -->
Exemplos sinteticos: nomes de campanha, contatos, IDs, valores e configuracoes abaixo sao ficticios, nao um inventario de cliente nem evidencia de producao. Adaptar IDs e slugs ao contrato autorizado; conferir a versao da API e o resultado antes de qualquer efeito externo.



Base URL: `https://api.clint.digital/v1`
Auth: header `api-token: <token>` + `accept: application/json`

## Convenção de paginação

- Query params: `page=N&limit=100` (max 100 por página)
Contrato de exemplo a verificar no ambiente autorizado; nenhuma execucao real e alegada.
  ```json
  {
    "status": "success",
    "totalCount": 2,
    "page": 1,
    "totalPages": 20,
    "hasNext": true,
    "hasPrevious": false,
    "data": [...]
  }
  ```
- ⚠️ Sempre é `data` (NUNCA `items` ou `results`, confirmado em /contacts, /tags, /deals)
- ⚠️ `hasNext` é confiável na MAIORIA dos endpoints, mas redundante com `page < totalPages`. Break também se `len(data) < limit` por segurança.
- `totalCount` é confiável e útil pra log/progresso.

## Convenção de filtros

- Filtros vão como query params (ex: `?tag_ids=uuid&pipeline_id=uuid`)
- Múltiplos valores: array CSV (`?tag_ids=uuid1,uuid2`)
- Datas: ISO 8601 (`?created_at_from=2026-01-01T00:00:00Z`), **MAS** confirmar se o endpoint suporta antes de confiar

## Endpoints validados

### TAGS

#### `GET /tags`
Lista todas as tags do workspace.

**Params:**
- `page`, `limit` (paginação)
- `search` ⚠️ **BUG: não filtra de fato**, retorna 100 quaisquer

**Resposta:**
```json
{
  "data": [
    {"id": "example-id", "name": "Exemplo sintetico", "color": "example-color", "created_at": "2000-01-01T00:00:00Z"}
  ],
  "hasNext": true
}
```

**Workaround pra busca por nome:** paginar tudo + filtrar client-side. Ver `ClintClient.find_tag_by_name()`.

#### `POST /tags`
Cria nova tag.

**Body:**
```json
{"name": "Exemplo sintetico", "color": "example-color"}
```

---

### CONTACTS

#### `GET /contacts`
Lista contatos com filtros.

**Params úteis:**
- `tag_ids=uuid`, filtra por tag
- ✅ `email=<exato>`, **FILTRA** (match exato). ⚠️ **Mas NÃO é confiável p/ lookup em massa:** pode retornar 0 pra comprador real (dedupe interno por telefone liga o evento a um contato com email diferente). Match robusto = email **+** telefone, restringindo o universo por **tag**. (Cuidado também com `+` no email cru → encoding, ver troubleshooting #17.)
- `page`, `limit`
- Possíveis (não confirmados): `pipeline_id`, `stage_id`, `phone`

**Resposta `data[]`:** ver `schema.md` (PII em `fields.*`!)

#### `GET /contacts/{id}`
Contato individual completo.

#### `POST /contacts`
Cria contato.

**Body mínimo:**
```json
{
  "name": "Exemplo sintetico",
  "email": "contact@example.invalid",
  "fullPhone": "<EXAMPLE_FULLPHONE>",
  "tag_ids": ["uuid_tag1"],
  "fields": {
    "doc": "<EXAMPLE_DOC>",
    "cep": "<EXAMPLE_CEP>",
    "cidade": "São Paulo",
    "estado": "SP"
  }
}
```

#### `POST /contacts/{id}`, UPDATE de contato
⚠️ **Update de contato é via `POST /contacts/{id}` (NÃO PUT/PATCH).** `PUT /contacts/{id}` e `PATCH /contacts/{id}` retornam **404** "Cannot PUT/PATCH". O verbo correto é **POST no recurso com id**.

**Gravar custom fields:**
```json
POST /contacts/{id}
{"fields": {"utm_source": "example-utm-source", "doc": "<EXAMPLE_DOC>", "ip_1": "example-ip-1"}}
```

- **Faz MERGE, não overwrite:** preenche campo **vazio**, mas **NÃO sobrescreve** campo já preenchido. Seguro pra backfill não-destrutivo.
- Sujeito ao **silent-drop de slug** (ver seção CUSTOM FIELDS): chave que não bate slug registrado some sem erro.
- Esta é a ÚNICA forma de gravar custom fields num contato, `POST /deals` ignora `fields` (ver POST /deals).
- `DELETE /contacts/{id}` = **204** (remove o contato; valida em fake).

#### `POST /contacts/{id}/tags`, ⚠️
Adiciona tag(s) a contato.

**Body = ARRAY de strings de tag_id** (NÃO objeto):
```json
["${RESOURCE_ID}", "outro-uuid"]
```
- ❌ `{"tag_id": "uuid"}` → **400** `"Body must be an array of strings"`.
- ✅ `["uuid1", "uuid2"]` → ok (aceita 1 ou N tags de uma vez).
- Teste sintetico: comparar um array de IDs com o objeto incorreto e conferir a resposta, sem alegar validacao em producao.

#### `DELETE /contacts/{id}/tags/{tag_id}`
Remove tag de contato. Sucesso = 204.

---

### ORIGINS (Suborigens / colunas de funil): exemplo sintetico

#### `GET /origins?page=N&limit=100`
Paginar `data[]` usando `totalCount` e `hasNext`; nao presumir quantidade de origins ou campanha configurada.
No modelo origin-based, cada origin possui seus stages. Confirmar `origin_id` e `stage_id` antes de criar ou mover deals.

```json
{
  "id": "example-origin-a",
  "name": "Origem de exemplo A",
  "group": {"id": "example-group-a", "name": "Grupo sintetico"},
  "stages": [
    {"id": "example-stage-base", "name": "Entrada de exemplo", "order": 1, "type": "BASE"},
    {"id": "example-stage-won", "name": "Ganho de exemplo", "order": 2, "type": "WON"},
    {"id": "example-stage-lost", "name": "Perda de exemplo", "order": 3, "type": "LOST"}
  ],
  "created_at": null,
  "updated_at": null
}
```

- `group` pode organizar origins; filtrar `group.name` no cliente se a API nao oferecer filtro equivalente.
- Ordenar `stages[]` por `order`; confirmar o stage default e o pertencimento do stage a origin.
- `GET /origins/{id}` retorna a origin individual: conferir o envelope `data` da versao usada.
- Em um teste sintetico de abandono, gerada e aprovada, configurar IDs distintos para cada origin/stage. Nenhuma cadeia real de cliente e fornecida.

---

### DEALS (Negócios)

#### `GET /deals`
Lista deals.

**Params:**
- ✅ `contact_id=<uuid>`, **FILTRA DE VERDADE** (deals de um contato). Único filtro confiável testado.
- ⚠️ `origin=<uuid>`, **NÃO filtra** (ignora, retorna tudo, igual bug do `search`). Para filtrar por origin: pegar deals do contato via `contact_id` e filtrar `d.origin_id == X` client-side.
- `page`, `limit`
- `pipeline_id` / `stage_id` / `status`, não confirmados nesse tenant (modelo é origin-based).

**Resposta `data[]` (contrato de exemplo a verificar):** `id`, `origin_id`, `stage_id`, `stage` (label), `status` (OPEN/WON/LOST), `value`, `currency`, `contact` (objeto: id/name/email/phone/ddi), `created_at`, `won_at`, `lost_at`, `fields`.

**Resposta `data[]`:**
```json
{
  "id": "example-id",
  "title": "example-title",
  "value": 100.00,
  "currency": "BRL",
  "pipeline_id": "example-pipeline-id",
  "stage_id": "example-stage-id",
  "contact": {...},  // objeto contact ou só id?
  "status": "open",
  "created_at": "2000-01-01T00:00:00Z",
  "updated_at": "2000-01-01T00:00:00Z"
}
```

#### `GET /deals/{id}`
Deal individual.

#### Subendpoints de Deal a verificar na versao usada

| Endpoint | O que retorna |
|---|---|
| `GET /deals/{id}/history` | Histórico de mudanças de stage (pra timeline de funil) |
| `GET /deals/{id}/activities` | Atividades vinculadas (calls, meetings, tasks) |
| `GET /deals/{id}/logs` | Logs de mudanças no objeto deal |
| `GET /deals/{id}/timeline` | Timeline cronológica unificada (mais útil pra UI/CRM) |

Conferir o esquema e guardar apenas fixtures sinteticas ou amostras autorizadas em area privada; nenhum dump operacional e embarcado.

#### `POST /deals` (faz UPSERT de contato embutido)

Cria deal. **Faz upsert do contato automaticamente** (match por email/telefone), NÃO precisa criar contato antes.

**Body mínimo (um dos params de contato é obrigatório):**
```json
{
  "origin_id": "example-origin-id",
  "email": "contact@example.invalid",
  "name": "Exemplo sintetico",
  "phone": "<EXAMPLE_PHONE>",
  "ddi": "55",
  "value": 100.00,
  "fields": {"doc": "<EXAMPLE_DOC>", "cidade": "São Paulo", "estado": "SP", "utm_source": "example-utm-source"}
}
```
- Erro 400 se faltar contato: `"One of the following contact params are required: contact_id, name, phone or email"`.
- Aceita `contact_id` direto (se já tiver o id) OU `email`/`name`/`phone` (faz upsert/dedupe).
- Dedupe de contato no upsert contrato de exemplo a verificar **telefone** (mesmo phone → mesmo contact_id, mesmo com emails diferentes). Email também serve de match.
- `value` persiste. ⚠️ **`fields` no `POST /deals` é IGNORADO SILENCIOSAMENTE** (volta `{}`; nenhum custom field grava), bug crítico que fazia campos nunca chegarem no CRM. **Custom field só grava via `POST /contacts/{id}` separado** (ver acima). Fluxo correto: POST /deals (cria deal + upsert contato) → pega `contact_id` da resposta → `POST /contacts/{contact_id}` com `{"fields":{...}}`.
- Conferir o stage default pela ordem da origin. Se a API aceitar `stage_id` explicito, testar com um stage sintetico pertencente a essa origin e conferir o destino por GET.
- Resposta 201: `data` com `id`, `contact_id`, `origin_id`, `stage`, `stage_id`, `value`, `status: OPEN`.
- ⚠️ **NÃO é idempotente:** 2 POSTs = 2 deals na mesma origin pro mesmo contato. Para dedupe: `GET /deals?contact_id=X` e checar `origin_id` antes de criar.

#### `POST /deals/{id}`, UPDATE / marcar GANHO
Atualiza um deal existente (mesmo padrão de update do contato: POST no recurso com id, NÃO PUT/PATCH).

**Marcar deal como GANHO:**
```json
POST /deals/{id}
{"status": "WON"}
```
- Seta `won_at` automaticamente (timestamp do servidor).
- Status de exemplo: `OPEN`, `WON`, `LOST`. Conferir casing, transicoes permitidas e efeitos sobre `won_at`/`lost_at` no contrato da versao usada; nao alegar teste de tenant.
- Exemplo sintetico: somente se o mapa aprovado exigir, concluir a etapa anterior e mover ou criar o card no destino, sem confundir ganho de etapa com pagamento.

#### `DELETE /deals/{id}` / `DELETE /contacts/{id}`
Ambos retornam **204** no sucesso. Deletar contato remove vínculo dos deals.

---

### PIPELINES

#### `GET /pipelines`
Lista todos pipelines.

**Resposta:**
```json
{
  "data": [
    {"id": "example-id", "name": "Exemplo sintetico", "stages_count": 5}
  ]
}
```

#### `GET /pipelines/{id}/stages`
Lista estágios de um pipeline.

---

### ORGANIZATIONS

#### `GET /organizations`
Lista organizações (empresas dos contatos).

**Resposta:**
```json
{
  "data": [
    {
      "id": "example-id",
      "name": "Exemplo sintetico",
      "fields": {"state": "SP", "city": "example-city"}
    }
  ]
}
```

#### `GET /organizations/{id}`
Organização individual.

---

---

### CUSTOM FIELDS (campos personalizados)

⚠️ **NÃO EXISTE endpoint público de custom fields.** contrato de exemplo a verificar:

| Tentativa | Resultado |
|---|---|
| `GET/POST /custom_fields`, `/fields`, `/custom-fields`, `/contact_fields`, `/customfields`, `/properties`, `/settings/custom_fields` | **404 Cannot GET/POST** |
| `GET/POST /contacts/custom_fields`, `/contacts/fields`, `/contacts/schema` | **400 "Param ID must be a valid UUID"**, o router trata o segmento como `{id}` de `GET /contacts/{id}`. Ou seja, não há subcoleção de fields. |

**Conclusão:** Custom fields **só podem ser criados/listados no painel web do Clint.** A API REST não expõe CRUD de definição de campo.

#### Como custom field é representado e como persiste

- O contato guarda custom fields num **mapa `fields`** (chave→valor string), keyado pelo **slug** do campo.
- O **slug** é derivado do nome do campo no painel: minúsculo, espaços→`_`, **acentos/caracteres especiais mantidos** (ex.: `n°_do_endereco`, `nº_pedido_de_retorno`).
- **Pegadinha crítica (silent drop):** no `POST /contacts`, qualquer chave em `fields` que **não corresponda a um slug já registrado** é **descartada silenciosamente** (sem erro, status 201 normal). Só persistem as chaves de campos que já existem no painel.
  - Teste sintetico: comparar um slug cadastrado e outro inexistente; conferir por GET quais campos persistiram antes de adotar o contrato.
- `PUT /contacts/{id}` **NÃO existe** (404). Update de contato não é via PUT, usar outro verbo/caminho (a confirmar; PATCH provável).

#### Slugs de tracking: modelo sintetico, nao configuracao de tenant

| Slug de exemplo | Verificacao antes de gravar |
|---|---|
| `utm_source`, `utm_medium`, `utm_content`, `utm_term` | Confirmar cadastro e leitura de retorno. |
| `utm_campaign` | Conferir o slug real no painel e no contrato do cliente. |
| `utm_campaing` | Exemplo hipotetico de typo legado; nao presumir que exista. |
| `landing` | Criar somente com aprovacao se o campo estiver ausente. |

**Pra registrar campo novo (manual, painel Clint):** criar custom field de **tipo texto**, escopo contato, com **nome que gere o slug exato** esperado pelo workflow (`utm_campaign`, `landing`). Conferir o slug que o Clint gera após salvar (pode acentuar/underscore-ar diferente do nome digitado).

---

## Endpoints documentados mas NÃO validados ainda

Memory diz "27 endpoints no total". Os abaixo são prováveis (baseado em CRM padrão), validar antes de usar:

- `GET /users`, usuários do workspace Clint
- `GET /webhooks` / `POST /webhooks`, gerenciar webhooks
- `GET /custom_fields`, definições de campos custom
- `GET /activities`, atividades (calls, meetings, emails)
- `GET /notes`, notas em contatos/deals
- `GET /files`, anexos
- `GET /workflows`, automações
- `GET /forms`, formulários
- `GET /reports`, relatórios

⚠️ Quando explorar qualquer um destes, **atualizar este arquivo** com schema + pegadinhas.

## Testar endpoint novo (template)

```bash
# 1. GET pra ver estrutura
curl -H "api-token: $CLINT_API_TOKEN" \
     -H "accept: application/json" \
     "https://api.clint.digital/v1/{novo-endpoint}?limit=2" | jq .

# 2. Anotar:
# - Estrutura da resposta (data[] / items[] / outro)
# - hasNext funciona?
# - Campos críticos onde estão? (raiz vs fields.* vs aninhado)
# - Params de filtro que realmente funcionam (cuidado com bug search)

# 3. Adicionar ao ClintClient + este arquivo
```

## Rate limiting

Não documentado oficialmente. Heurística testada:
- 200ms entre páginas em loops longos = sem 429
- Bulk write (criar 100+ contatos), não testado, usar com cautela

Se receber 429: backoff exponencial (`2 ** attempt` segundos).

