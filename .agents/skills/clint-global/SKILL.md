---
name: clint-global
description: "Use when working on global Clint CRM operations for HAOS/SIM/${USER_BRAND}, including tags, contacts, leads, deals, cobranca origins, n8n Clint webhooks, paid-close automations, spreadsheet imports, PMX26/PMEXP tags, category-to-tag mapping, bulk updates, tag migration/removal, or CLINT_API_KEY/CLINT_API_URL credential validation without exposing secrets."
---

# Clint Global

Use this skill for Clint CRM operations in the HAOS/SIM/${USER_BRAND}
environment, including API scripts, lead imports, tag maintenance, deal
updates, cobranca origins, n8n webhooks and paid-close automations.

## Regra obrigatoria: atualizar o card durante a jornada

existente para a etapa de compra aprovada e status `WON` (Fechado/Ganho),
com a tag de pago do produto. Nunca criar outro card na mesma origem apenas
porque chegou um evento novo, outro cart_token ou outra notificacao do pedido.**

- **Etapas na mesma origem:** Abandono -> Compra Gerada -> Compra Aprovada
  usam o mesmo `deal_id`; no pagamento, atualizar tambem o valor comprovado.
- **Etapas em origens separadas:** dar ganho no card da origem anterior e
  criar **somente se ainda nao existir** o card na origem seguinte; se existir,
  atualizar esse card. Na aprovacao, o card de destino tambem fica `WON`.
- Gerar pagamento nao comprova pagamento recebido. Ganho por avancar de
  origem representa conversao daquela etapa; tag paga e email de confirmacao
  exigem pagamento confirmado, nunca apenas um status `WON` anterior.
- Buscar e validar contato + origem antes de criar; proteger contra eventos
  simultaneos, repetidos e atrasados. Um card ganho nao volta a aberto.
- Ler [a regra completa e os cenarios de aceite](references/jornada-card-pagamento.md)
  antes de construir, corrigir ou revisar automacoes de negocios.

## Protecoes operacionais

- Load HAOS bootstrap from `${HAOS_PRIVATE_ROOT}` before acting.
- Never print, quote, mask, commit, or store Clint API tokens, headers,
  cookies, passwords, raw `MASTER.env` values, or raw lead PII.
- Use `MASTER.env` only as a source for secrets:
  `${HAOS_PRIVATE_ROOT}`
  mutation: create/update contact, create/delete/migrate tag, or bulk import.
- Always run a dry-run first for bulk work, then apply only after validating
  counts, categories, duplicate policy and target tags.
- Summarize results with counts, tag names, IDs, Excel row numbers for errors,
  and `printed_secret=false`; do not output names, emails or phones.

## Specialist Routing

- `crm-specialist`: category mapping, lifecycle meaning, segment/tag naming.
- `dev-backend`: Clint API scripts, pagination, retries, endpoint contracts.
- `compliance-officer`: LGPD/PII, export/import safety and mutation gates.

## Known Environment

- Clint secret variables observed in `MASTER.env`:
  `CLINT_API_KEY`, `CLINT_API_URL`.
- Clint auth header: `api-token`.
- Reusable scripts in the HAOS repo:
  - `scripts\probe-clint-tags-readonly.ps1`
  - `scripts\clint-pmx26-bulk-sync.py`
  - `scripts\clint-transaction-report-sync.py`
- Reusable scripts in the HAOS Systen workspace:
  - `ops\n8n\clint-asaas-lia-webhooks.ps1`
  - `ops\n8n\sync-clint-asaas-billing-enrichment.ps1`
  - `ops\n8n\sync-clint-paid-close-workflows.ps1`
  - `ops\n8n\backfill-clint-conference-direct.py`
  - `ops\n8n\probe-clint-cobrancas-origin-readonly.ps1`
  - `ops\n8n\probe-clint-cobrancas-tag-overlap-readonly.py`
- PMX26 category mapping currently used:
  - `Prata` -> `${RESOURCE_ID}` (`${RESOURCE_ID}`)
  - `Ouro` -> `${RESOURCE_ID}` (`${RESOURCE_ID}`)
  - `Diamante` -> `${RESOURCE_ID}` (`${RESOURCE_ID}`)

## Quick Commands

Run from `${HAOS_PRIVATE_ROOT}`.

```powershell
.\scripts\probe-clint-tags-readonly.ps1 -Terms PMEXP,PMX26,Online,Presencial
```

Dry-run a PMX26 spreadsheet sync:

```powershell
& $py .\scripts\clint-pmx26-bulk-sync.py --workers 8
```


```powershell
& $py .\scripts\clint-pmx26-bulk-sync.py --apply --workers 8
```

Verify leads/tags without mutating:

```powershell
& $py .\scripts\clint-pmx26-bulk-sync.py --verify-leads --workers 8
```

Dry-run a paid transaction CSV report sync:

```powershell
& $py .\scripts\clint-transaction-report-sync.py --workers 8
```


```powershell
& $py .\scripts\clint-transaction-report-sync.py --apply --workers 8
```

Run Clint cobranca webhook/origin helpers from
`${HAOS_PRIVATE_ROOT}`:

```powershell
.\ops\n8n\clint-asaas-lia-webhooks.ps1 -Mode list-provider-webhooks
.\ops\n8n\sync-clint-asaas-billing-enrichment.ps1
.\ops\n8n\sync-clint-asaas-billing-enrichment.ps1 -Apply
.\ops\n8n\sync-clint-paid-close-workflows.ps1
.\ops\n8n\sync-clint-paid-close-workflows.ps1 -Apply
python .\ops\n8n\probe-clint-cobrancas-tag-overlap-readonly.py
```

## Workflow

1. Confirm HAOS bootstrap and `claude-mem` health if available.
2. Confirm the user has explicitly approved any requested Clint mutation.
3. Inspect the spreadsheet structure before applying:
   - sheet name;
   - row count;
   - required columns;
   - category distribution;
   - duplicate count;
   - missing email/phone count.
4. Audit current tags using `probe-clint-tags-readonly.ps1`.
5. Run the bulk script in dry-run and verify:
   - expected tag changes;
   - number of unique leads;
   - would-update vs would-create;
   - ambiguous matches;
   - tag assignment count.
6. Apply sequential Clint mutations only after the dry-run is coherent.
7. Verify final tag state and lead/tag membership with `--verify-leads`.
8. For Asaas vencido cobrança workflow, verify enrichment shape before
   applying: Asaas credential reference, `/customers/{id}`,
   `/payments/{id}/billingInfo`, `/payments/{id}/pixQrCode`, and final
   connection from `Montar payload Asaas Clint` to `Enviar para Clint`.
9. For cobranca paid-close workflows, verify workflow shape and target stage
   before applying: workflow active, managed nodes present, close node using
   the Clint API credential, code node still forwarding to the Clint webhook
   in parallel, and tag-removal node guarded by the remaining-open-deals check.
10. Report concise counts, failures and tag/stage IDs. Do not report PII.

## Clint Global Reference

Read [references/clint-global.md](references/clint-global.md) before
implementing or patching Clint contact, tag, deal, cobranca or n8n scripts.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
