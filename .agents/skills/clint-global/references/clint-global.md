# Clint Tags And Lead Sync Reference

## Authentication

- Load `CLINT_API_KEY` and `CLINT_API_URL` from `MASTER.env`.
- Send the token only as the `api-token` header.
- Never print the token, header object, secret value length, prefix or suffix.
- Normalize `CLINT_API_URL` to a `/v1` base. If it already ends in `/v1/tags`,
  trim to `/v1` before composing other routes.

## Tag Endpoints

Observed useful endpoints:

| Operation | Route | Notes |
|---|---|---|
| List tags | `GET /v1/tags` | Paginate with `limit` and `page`. |
| Create tag | `POST /v1/tags` | Body: `{ "name": "...", "color": "#hex" }`. |
| Delete tag | `DELETE /v1/tags/{id}` | Expected status `204`. |
| Add tag to contact | `POST /v1/contacts/{id}/tags` | Body is an array of string tag IDs. |

Important body detail:

```json
["tag-uuid-here"]
```

The contact-tag endpoint rejected object-shaped bodies such as
`{"tag_id":"..."}` and accepted an array of string IDs with status `204`.

For removing provider overdue tags from contacts, the n8n paid-close workflow
uses a guarded `DELETE /v1/contacts/{id}/tags/{tag_id}` HTTP node with
`continueOnFail=true`. Keep the guard: remove only when the matching paid card
is the last open cobrança deal found for that contact in the cobrança origin.

## Rename/Migration Reality

Do not assume Clint supports in-place tag rename. In the PMX26 operation,
`POST /v1/tags/{id}` was not reliable for renaming. The safe pattern was:

1. Ensure the new tag exists.
2. Confirm `GET /v1/contacts?tag_ids=<old_id>` works.
3. For every contact with the old tag, add the new tag via
   `POST /v1/contacts/{id}/tags` with body `["new_tag_id"]`.
4. Delete the old tag with `DELETE /v1/tags/{old_id}`.
5. Verify old tag is absent and new tag is present.

Before relying on `tag_ids`, query a sentinel impossible UUID and expect zero
contacts. If the sentinel returns contacts, stop; the filter is unsafe.

## Contact Endpoints

Observed useful endpoints:

| Operation | Route | Notes |
|---|---|---|
| Search contacts | `GET /v1/contacts?email=...` | Use for matching existing leads. |
| Search contacts | `GET /v1/contacts?phone=...` | Normalize Brazil phones before searching. |
| Search by tag | `GET /v1/contacts?tag_ids=...` | Use for migration/verification after sentinel check. |
| Create contact | `POST /v1/contacts` | Expected `200` or `201`; re-search if ID is not returned. |
| Update contact | `POST /v1/contacts/{id}` | Expected `200`. |

## Deal, Origin And Stage Endpoints

Observed useful endpoints for cobrança backfills:

| Operation | Route | Notes |
|---|---|---|
| List origins | `GET /v1/origins` | Each origin includes `stages`; stage labels are in `label`, not `name`. |
| List deals | `GET /v1/deals` | Supports `origin_id` and `contact_id`; sentinel invalid `origin_id` returned zero, so that filter is safe. |
| Create deal | `POST /v1/deals` | Body can include `origin_id`, `stage_id`, `contact_id`, `name`, `email`, `phone`, `value`, and `fields`. |
| Update deal | `POST /v1/deals/{id}` | Use to move/update an open deal into the target stage. |
| Account fields | `GET /v1/account/fields` | Fields are grouped by `CONTACT`, `DEAL`, `ORGANIZATION`; deal field technical keys are under `data.fields.DEAL`. |

Validated cobrança origin:

| Entity | Name | ID |
|---|---|---|
| Origin | `LIA + ASAAS | Cobranças Vencidas` | `${RESOURCE_ID}` |
| Stage | `Conferência Asaas` | `${RESOURCE_ID}` |
| Stage | `Conferência Lia` | `${RESOURCE_ID}` |
| Stage | `Fechado` | `${RESOURCE_ID}` |
| Stage | `❌[Fila Lia] [Não usar]❌` | `${RESOURCE_ID}` |
| Tag | `Asaas-SIM_vencido` | `${RESOURCE_ID}` |
| Tag | `Lia_vencida` | `${RESOURCE_ID}` |

Useful cobrança custom field keys observed:

| Scope | Label | Key |
|---|---|---|
| DEAL | `Descrição Produto` | `descricao_produto` |
| DEAL | `Link do boleto` | `link_do_boleto` |
| DEAL | `ID da Transacao` | `id_da_transacao` |
| DEAL | `Status Pagamento` | `status_pagamento` |
| DEAL | `Método de Pagamento` | `metodo_de_pagamento` |
| CONTACT | `Link Boleto` | `link_boleto` |
| CONTACT | `Código do Boleto` | `codigo_do_boleto` |
| CONTACT | `Código do Pix` | `codigo_do_pix` |

Lia/Asaas cobrança lessons:

- Live Lia webhook intentionally creates in the queue stage; manual backfill may need direct Clint deal API to place records in `Conferência Lia`.
- The Asaas vencido webhook can receive events without email/phone. Enrich
  before sending to Clint using Asaas `customers`, `billingInfo` and
  `pixQrCode`; otherwise boleto/pix fields may be present in the event but not
  attach to the correct Clint contact.
- Lia `status=overdue` bills can arrive with API status values such as `pending`; treat the query/event as the overdue signal and do not require the returned status text to equal `overdue`.
- Lia `/orders/{id}` may return an envelope with `data`; unwrap before reading `email.address` and `phone.address`.
- Lia can return `429`; retry with exponential backoff and lower worker counts.
- For lead-level backfills, dedupe by normalized contact key before applying, not by bill/payment ID, unless the task explicitly wants one deal per cobrança.
- Do not blindly clean contacts that have both `Asaas-SIM_vencido` and
  `Lia_vencida`; classify open deals first because a contact can legitimately
  owe in both providers.
- Existing Asaas cards created before the enrichment workflow may be missing
  `link_boleto`, `codigo_do_boleto`, `codigo_do_pix`, `link_do_boleto` and/or
  `id_da_transacao`. Use
  `ops\n8n\repair-clint-asaas-billing-fields.py --aggressive-open-search` as
  `dry-run -> apply -> verify`. This repair must only fill empty fields; it
  must not move stages, change status, create cards or alter tags.
- For retroactive Asaas field repair, prefer exact `id_da_transacao` matches
  against current `OVERDUE` payments. The aggressive fallback may search Asaas
  customers by email/CPF-CNPJ and consider only open `PENDING`/`OVERDUE`
  payments. Update only when the match is unique by value, single due/open
  payment, or exact transaction; skip `customer_not_found`,
  `customer_without_payments` and ambiguous open-payment cases.

## Cobranca Paid-Close Workflow

When a payment is confirmed for the `LIA + ASAAS | Cobranças Vencidas`
origin, the target behavior is to close the existing cobrança card:

- move/update the deal to stage `Fechado`
  (`${RESOURCE_ID}`);
- set deal `status` to `WON`;
- keep the original contact attached;
- do not create a new card if no confident existing deal is found.

Validated Clint close payload shape:

```json
{
  "origin_id": "${RESOURCE_ID}",
  "stage_id": "${RESOURCE_ID}",
  "contact_id": "contact-uuid-here",
  "status": "WON"
}
```

The payload above was accepted idempotently by `POST /v1/deals/{id}` on an
already closed/won deal. Observed deal statuses include `OPEN`, `WON` and
`LOST`; closed/won deals may also carry `won_at`.

Safe matching policy for paid-close automations:

1. Search contact by email first; if absent, search by normalized phone.
2. Query deals with both `origin_id` and `contact_id`.
3. Prefer an open, non-closed deal whose `fields.id_da_transacao` matches the
   provider external/payment ID.
4. If there is no exact transaction match, close only when exactly one open,
   non-closed deal exists for that contact in the cobrança origin.
5. If the match is ambiguous, do nothing and log/return the skip instead of
   closing the wrong card.

## Clint Integrations And n8n Lessons

Public Clint `/v1` API is useful for contacts, tags, origins, stages and deals,
but do not assume it can edit Clint app integrations. Routes such as public
integration/webhook/app-integration endpoints were probed and did not expose a
usable app integration contract with the `api-token`. The internal
`appIntegration` path is tied to the web app/session app auth and should not be
treated as a stable public API.

For n8n workflow automation, prefer updating the n8n workflow JSON and calling
Clint API from n8n with the existing credential:

- n8n credential name: `Clint API (api-token header)`;
- n8n credential type: `httpHeaderAuth`;
- do not embed Clint tokens in workflow JSON.

Validated paid workflows:

| Purpose | n8n workflow name | n8n workflow ID |
|---|---|---|
| Asaas-SIM vencido cobrança | `[Clint] [Asaas-SIM] [Pagamento Vencido] [Cobranca]` | `${RESOURCE_ID}` |
| Asaas-SIM paid cobrança | `[Clint] [Asaas-SIM] [Paga] [Cobranca]` | `${RESOURCE_ID}` |
| Lia paid cobrança | `[Clint] [Lia] [Pago] [Cobranca]` | `${RESOURCE_ID}` |

Asaas vencido enrichment:

- n8n credential name: `Asaas API (access_token header)`;
- n8n credential type: `httpHeaderAuth`;
- header name: `access_token`;
- do not embed the Asaas token in workflow JSON;
- managed nodes added by
  `ops\n8n\sync-clint-asaas-billing-enrichment.ps1`:
  - `Asaas: Buscar cliente`
  - `Asaas: Buscar boleto`
  - `Asaas: Buscar pix`
  - `Montar payload Asaas Clint`
- expected API paths:
  - `/customers/{{ CustomerId }}`
  - `/payments/{{ PaymentId }}/billingInfo`
  - `/payments/{{ PaymentId }}/pixQrCode`

On this n8n version, credential/workflow API writes can return
`object is not iterable` even after applying the state. After any such error,
verify by reading the workflow and checking node count, managed nodes and
connections before retrying.

The helper `ops\n8n\sync-clint-paid-close-workflows.ps1` adds managed nodes to
each workflow:

- `Clint: Buscar contato`
- `Selecionar contato Clint`
- `Clint: Buscar negocios`
- `Selecionar negocio para fechar`
- `Clint: Fechar negocio`
- `Filtrar remocao tag vencido`
- `Clint: Remover tag vencido`

The paid workflow should continue sending the incoming event to the configured
Clint webhook while, in parallel, closing the matching existing cobrança deal.
The tag-removal branch should remove only the provider tag for that paid event:

| Workflow | Tag removed when safe |
|---|---|
| `[Clint] [Asaas-SIM] [Paga] [Cobranca]` | `Asaas-SIM_vencido` (`${RESOURCE_ID}`) |
| `[Clint] [Lia] [Pago] [Cobranca]` | `Lia_vencida` (`${RESOURCE_ID}`) |

The `Selecionar negocio para fechar` code returns `remove_tag=true` only when
no other open, non-closed cobrança deal remains for that contact in the origin.

Provider webhook checks that were useful:

| Provider | Paid event filter | Provider webhook ID |
|---|---|---|
| Asaas-SIM | `PAYMENT_CONFIRMED`, `PAYMENT_RECEIVED` | `${RESOURCE_ID}` |
| Lia | `paid` | `${RESOURCE_ID}` |

n8n connection shape gotcha: `connections.<node>.main` must be an array of
arrays. In PowerShell helpers, return `,(,$targets)` for a single output with
multiple targets. Returning a flat list can make n8n reject the update with an
`object is not iterable` error.

Verification for paid-close workflow updates:

```powershell
.\ops\n8n\sync-clint-asaas-billing-enrichment.ps1
.\ops\n8n\sync-clint-asaas-billing-enrichment.ps1 -Apply
.\ops\n8n\sync-clint-paid-close-workflows.ps1
.\ops\n8n\sync-clint-paid-close-workflows.ps1 -Apply
.\ops\n8n\clint-asaas-lia-webhooks.ps1 -Mode list-provider-webhooks
python .\ops\n8n\probe-clint-cobrancas-tag-overlap-readonly.py
```

After apply, verify each workflow is active, has the expected managed nodes, the
close node uses `Clint API (api-token header)`, and the code node connects to
both `Enviar para Clint` and `Clint: Buscar contato`.

## Spreadsheet Import Policy

- Required PMX26 import columns:
  - `Nome Completo`
  - `Telefone`
  - `Email`
  - `Categoria`
- Optional columns can be read but should only be sent if matching Clint account
  fields exist.
- Normalize matching keys:
  - prefer phone;
  - fallback to email;
  - remove non-digits from phone;
  - strip leading Brazil DDI `55` when present and length is greater than 11.
- Deduplicate by normalized phone/email:
  - last row wins for contact fields;
  - union categories/tags across duplicate rows.
- If one contact appears in multiple categories, assign every target category
- Report duplicate and missing-identifier counts, not PII.

## PMX26 Mapping

Current default mapping:

| Categoria | Clint tag | Canonical ID |
|---|---|---|
| `Prata` | `${RESOURCE_ID}` | `${RESOURCE_ID}` |
| `Ouro` | `${RESOURCE_ID}` | `${RESOURCE_ID}` |
| `Diamante` | `${RESOURCE_ID}` | `${RESOURCE_ID}` |

For PowerMind routines, treat those IDs as canonical. If a tag name resolves to
another ID, stop before applying the sync.

Previously migrated aliases:

| Old tag | New tag |
|---|---|
| `${RESOURCE_ID}` | `${RESOURCE_ID}` |
| `${RESOURCE_ID}` | `${RESOURCE_ID}` |

`PMEXP_Pago` was removed in the PMX26 cleanup flow.

## Paid Transaction Report Mapping

For CSV transaction exports with columns such as `NomeDoProduto`,
`NomeDaOferta`, `Status`, `NomeCompletoDoCliente`, `TelefoneDoCliente` and
otherwise.

Known paid report mapping:

| Source condition | Clint tag |
|---|---|
| `NomeDoProduto` contains `Formação Practitioner em PNL` | `Practitioner_pago` |
| `FPV369` / `Formação Practitioner em PNL \| ${USER_BRAND}` | `Practitioner_pago` |
| Product contains `POWERMIND` and offer contains `PRATA` | `${RESOURCE_ID}` |
| Product contains `POWERMIND` and offer contains `OURO` | `${RESOURCE_ID}` |
| Product contains `POWERMIND` and offer contains `DIAMANTE` | `${RESOURCE_ID}` |

## Verification Checklist

- `GET /v1/tags` confirms expected target tags exist.
- `GET /v1/tags` confirms removed/old tags are absent.
- `GET /v1/contacts?tag_ids=<target_id>` returns contacts for each target tag.
- Cross-check every imported lead's resolved contact ID against its expected
  target tag membership.
- Final report should include:
  - input rows;
  - unique leads;
  - created/updated contacts;
  - tag assignment confirmations;
  - failures count;
  - final tag IDs;
  - no raw lead PII.
