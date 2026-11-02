---
name: haos-google-ads-gtm-api
description: "Use when working on HAOS/SIM/${USER_BRAND} Google Ads API or Google Tag Manager API access, MCC setup, API Center developer token, OAuth scopes, MASTER.env variables, read-only Ads/GTM audits, account suspension diagnostics, or Google Ads/GTM credential validation without exposing secrets."
---

# HAOS Google Ads/GTM API

Use this skill for Google Ads API and GTM API work in the HAOS/SIM/${USER_BRAND} environment.

## Guardrails

- Load HAOS bootstrap from `${HAOS_PRIVATE_ROOT}` before acting.
- Never print, quote, mask, commit, or store secrets in memory: developer token,
  client secret, refresh token, access token, cookies, passwords.
- Use `MASTER.env` only as a source/sink for secrets:
  `${HAOS_PRIVATE_ROOT}`
  the exact external change.
- Never use MCC/API access to bypass a Google Ads suspension.
- Do not activate campaigns, budgets, ads, bids, billing, audiences, tags, or
  publishes during access/audit work.

## Known Accounts

- MCC: `552-214-6221` / `${RESOURCE_ID}`, `${USER_BRAND} - MCC`, auth user `contact@example.invalid`.
- Ads client: `282-397-2901`, `${USER_BRAND}`, status observed `ENABLED`.
- Ads client: `640-403-7852`, `${USER_BRAND}`, status observed `SUSPENDED`.
- GTM containers expected:
  - `${RESOURCE_ID}` - Edson Buger | Server
  - `${RESOURCE_ID}` - Edson Buger | Server | Backup
  - `${RESOURCE_ID}` - ${USER_BRAND} | Web
  - `${RESOURCE_ID}` - Yampi mapeamento

## Scripts

Run from `${HAOS_PRIVATE_ROOT}`.

```powershell
.\scripts\audit-google-master-env.ps1
.\scripts\probe-google-oauth-scopes.ps1
.\scripts\probe-google-ads-readonly-access.ps1
.\scripts\probe-google-ads-readonly-access.ps1 -ProbeCustomerIds '${RESOURCE_ID},${RESOURCE_ID},${RESOURCE_ID}'
.\scripts\probe-gtm-readonly-access.ps1
```

To save a Google Ads developer token without printing it:

```powershell
.\scripts\save-google-ads-api-token-from-clipboard.ps1 -LoginCustomerId '${RESOURCE_ID}' -TokenFromClipboard
```

If extracting through a temporary file, delete the temporary file immediately;
the script supports `-TokenFile` and removes that file after reading.

## Workflow

1. Confirm bootstrap and `claude-mem` health if available.
2. Run `audit-google-master-env.ps1`; it must show presence only, never values.
3. Run `probe-google-oauth-scopes.ps1`; require `adwords` and `tagmanager.readonly`.
4. If `GOOGLE_ADS_DEVELOPER_TOKEN` is missing, use Google Ads MCC API Center.
5. API Center fields used successfully:
   - Company: `${USER_BRAND}`
   - URL: `https://service.example.invalid`
   - Company type: `Anunciante`
   - Intended use: internal read-only reporting/audit for own Google Ads accounts, no campaign/ad/budget/bid/user/billing mutations.
6. Save token only into `MASTER.env`.
7. Set `GOOGLE_ADS_LOGIN_CUSTOMER_ID` to MCC ID without hyphens: `${RESOURCE_ID}`.
8. Run Ads and GTM probes.
9. Record conclusions without secrets.

## Troubleshooting

- If Google Ads UI says API Center is only for manager accounts, select the MCC
  `552-214-6221`.
  pause/allowlist the ad blocker manually for `ads.google.com`.
- If Ads API `listAccessibleCustomers` lists an account but GAQL via MCC returns
  `USER_PERMISSION_DENIED`, try the read-only direct route. This happened with
  `${RESOURCE_ID}`; direct access confirmed `SUSPENDED`.
- If a web OAuth client redirects to `service.example.invalid` with
  `state_parse_error`, use the desktop OAuth client and localhost listener
  instead of the web client callback.
- If a token appears in a tool output accidentally, do not repeat it, summarize

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
