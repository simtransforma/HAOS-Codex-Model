---
name: haos-meta-stape-api
description: "Use when working on HAOS/SIM/${USER_BRAND} Meta Graph or Marketing API access, Meta Business Manager system-user tokens, ad account read-only audits, Pixel/CAPI diagnostics, Stape API access, Stape sGTM containers, server-side tracking, MASTER.env variables, or Meta/Stape credential validation without exposing secrets."
---

# HAOS Meta/Stape API

Use this skill for Meta Graph/Marketing API and Stape API work in the
HAOS/SIM/${USER_BRAND} environment.

## Guardrails

- Load HAOS bootstrap from `${HAOS_PRIVATE_ROOT}` before acting.
- Never print, quote, mask, commit, or store secrets in memory: access tokens,
  app secret, Stape API key, container API key, cookies, passwords, headers.
- Use `MASTER.env` only as a source for secrets:
  `${HAOS_PRIVATE_ROOT}`
  exact external change.
- Do not create, pause, activate, edit or delete campaigns, ad sets, ads,
  budgets, pixels, audiences, domains, containers, power-ups, schedules,
  billing, users, API keys or webhooks during access/audit work.
- Do not call Stape `GET /api/v2/users/api-key` unless you sanitize the response
  because it can expose API-key material.

## Specialist Routing

- `dev-backend`: OAuth/token handling, Graph/Stape API probes, script fixes.
- `tracking-engineer`: pixels, CAPI, Stape sGTM container, domains and event
  quality diagnostics.
- `traffic-master` and `media-buyer`: ad account/campaign/insights read-only
  interpretation after access is confirmed.
- `compliance-officer`: policy, LGPD, token/permission risk and change gates.

## Known Environment

- Meta Graph version validated: `v21.0`.
- Meta token variables observed in `MASTER.env`: `META_TOKEN_BM01`,
  `META_TOKEN_BM02`, `META_TOKEN_BM08`, `META_TOKEN_BM09`, `META_TOKEN_BM10`,
  `META_TOKEN_BM11`, `META_TOKEN_BM12`, `META_TOKEN_BM13`.
- Meta app variables observed: `META_APP_ID`, `META_APP_SECRET`.
- Stape token variable observed: `STAPE_API_KEY`.
- Stape auth header: `X-AUTH-TOKEN`.
- Stape base URL validated: `https://api.app.stape.io`.
- Stape container validated:
  - name: `${USER_BRAND}`
  - identifier: `efznyhks`
  - status: `Running`
  - zone: `SA East (Brazil)`
  - domain: `api.${USER_BRAND}.com.br`, status `Ready`

## Scripts

Run from `${HAOS_PRIVATE_ROOT}`.

```powershell
.\scripts\audit-meta-stape-master-env.ps1
.\scripts\probe-meta-readonly-access.ps1
.\scripts\probe-meta-readonly-access.ps1 -MaxAdAccounts 20
.\scripts\probe-stape-readonly-access.ps1
```

These scripts never print secrets. They return names of variables used, status
flags, account/container names, counts and sanitized errors only.

## Workflow

1. Confirm HAOS bootstrap and `claude-mem` health if available.
2. Run `audit-meta-stape-master-env.ps1`; expect presence only, never values.
3. Run `probe-meta-readonly-access.ps1`; validate:
   - token debug valid;
   - `ads_read` for read-only Ads/Insights;
   - `business_management` for Business/asset discovery;
   - ad accounts returned;
   - `campaigns`, `adspixels` and `insights` GETs succeed.
4. Run `probe-stape-readonly-access.ps1`; validate:
   - `GET /api/v2/containers`;
   - `GET /api/v2/containers/{identifier}`;
   - `GET /api/v2/containers/{identifier}/domains`;
   - `GET /api/v2/containers/{identifier}/analytics/info`.
5. Summarize by credential variable name and operational result only.
6. If a token is valid but no ad account appears, treat as asset assignment or
   permission scope issue, not as credential failure.

## Current Findings To Remember

- `META_TOKEN_BM01`: token valid, has `ads_read`, `ads_management`,
  `business_management`; six ad accounts were readable; campaigns, pixels and
  insights GETs succeeded.
- `META_TOKEN_BM02`: token valid, has `ads_read`, `ads_management`,
  `business_management`; one ad account was readable; campaigns, pixels and
  insights GETs succeeded.
- `META_TOKEN_BM08`: token valid but missing `ads_read`; no ad accounts were
  returned.
- `META_TOKEN_BM09` to `META_TOKEN_BM13`: tokens valid and include `ads_read`,
  but no ad accounts were returned by the tested GET routes. Likely missing
  asset/ad-account assignment or no accessible account on those BMs.
- Stape access is OK for the ${USER_BRAND} sGTM container and domain.

## Troubleshooting

- If `debug_token` fails, verify `META_APP_ID` and `META_APP_SECRET` exist in
  `MASTER.env` and match the app that issued the token.
- If token is valid but account count is zero, inspect Business Manager asset
  assignment in Meta UI before changing code.
- If Stape returns 401/403, check that the API key is account-level or has
  access to the expected workspace/container.
- If Stape returns a wrapper object with `body.body`, update the parser instead
  of printing raw response.
- If any secret appears in tool output, do not repeat it. Stop, summarize the

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
