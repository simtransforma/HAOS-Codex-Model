---
name: ga4
description: "Operar o Google Analytics 4 do grupo (${USER_BRAND}): propriedades, streams, measurement IDs, eventos (generate_lead, page_view) e a GA4 Data API (runReport) pra puxar relatorio de leads/visitas por periodo, host e UTM. Use SEMPRE que a tarefa for GA4 em qualquer forma, \"quantos leads no GA4\", \"puxa o relatorio do analytics\", \"evento generate_lead\", \"ga4 data api\", \"runReport\", \"qual a propriedade GA4\", \"qual o property id\", \"measurement id do service.example.invalid\", \"qual o G- do service.example.invalid\", \"leads de site por periodo\", \"page_view por host\", \"o GA4 ta atualizando a dash?\", \"conecta o GA4\", \"o refresh token do GA4 caiu\", \"GA4 nao puxa mais\". Tambem implicitamente sempre que for medir trafego de site (visitantes/leads/UTM) ou alimentar a camada de leads/visitantes da dash SIM. NAO use pra Google Ads API nem GTM API (= haos-google-ads-gtm-api), nem pra tracking generico de marketplace (= analytics-tracking), nem pra Pretty Links (= pretty-links). Esta skill e SO Google Analytics 4.\n"
---

# GA4 (Google Analytics 4 do grupo)

GA4 e a camada de medicao de SITE do grupo: visitantes, leads de site (`generate_lead`),
page_views e UTMs. Alimenta a dash SIM (camadas Visitantes e Leads do funil). Esta skill cobre
a estrutura de propriedades, a autenticacao OAuth e a **GA4 Data API (`runReport`)** pra puxar
relatorio. Tudo aqui e LEITURA. Mudar tag/medicao do site = GTM (skill `haos-google-ads-gtm-api`).

## Guardrails

- Skill INTERNA. Pode citar property IDs e measurement IDs (privados). Segredo so por NOME de
  variavel (nunca o valor): le tudo do `MASTER.env`
  (`...\HAO IA Operation System\_secrets\MASTER.env`, ver `project_credentials.md`).
- GA4 e read-only por natureza (relatorio). Nao "ativar" nem "publicar" nada.
- Nao fabricar numero: se a Data API nao respondeu, dizer que nao respondeu. Nao chutar lead.
- Confirmar AO VIVO os itens marcados `TODO:` antes de cravar (propriedade exata, nome de var).

## Conceito que mais confunde: measurement ID vs property ID

| | Measurement ID | Property ID |
|---|---|---|
| Formato | `${RESOURCE_ID}` (ex. `${RESOURCE_ID}`) | numerico (ex. `${RESOURCE_ID}`) |
| Onde vive | no `gtag`/GTM da PAGINA (coleta) | no admin da propriedade GA4 |
| Pra que serve | COLETAR evento no browser (envia pro GA4) | LER relatorio via **Data API** |
| Pertence a | um data stream (web) | a propriedade inteira (N streams) |

Regra de ouro: **medir/coletar = measurement `G-`; puxar relatorio = property numerico.**
Confundir os dois e o erro #1. A Data API SO aceita `properties/{PROPERTY_ID}` numerico.

## Autenticacao (OAuth refresh token)

A Data API autentica via OAuth de usuario (refresh token salvo) ou service account.
No grupo, o caminho em producao e **OAuth refresh token**:

- Variaveis no `MASTER.env` (ler por nome, nunca imprimir):
  `GA4_REFRESH_TOKEN`, e o client OAuth (`GOOGLE_*_CLIENT_ID` / `GOOGLE_*_CLIENT_SECRET`).
  TODO (vivo): confirmar os nomes EXATOS do client id/secret usados pelo GA4 no `MASTER.env`
  (pode reusar o client `GOOGLE_GTM_*` ou ter `GA4_CLIENT_ID/SECRET` proprios).
- Scope: `https://www.googleapis.com/auth/analytics.readonly`.
- Token endpoint: `https://oauth2.googleapis.com/token` (troca refresh -> access).

### CASCATA: trocar a senha do Google revoga TODOS os tokens

Regra duravel (ver `learning_n8n_google_oauth.md`): **toda vez que a senha de uma conta Google
e trocada, o Google revoga os refresh tokens daquela conta.** Sintoma tipico: GA4 para de
atualizar a dash, importador retorna `invalid_grant`. Acao: reautorizar o OAuth do GA4 e regravar
`GA4_REFRESH_TOKEN` no `MASTER.env`. Mitigacao: client OAuth proprio com consent "Em producao".

## GA4 Data API, `runReport`

Endpoint (sempre property numerico):

```
POST https://analyticsdata.googleapis.com/v1beta/properties/${RESOURCE_ID}:runReport
Authorization: Bearer <ACCESS_TOKEN>   (obtido do refresh token)
Content-Type: application/json
```

### Exemplo 1, leads (`generate_lead`) por dia, com filtro de evento

```json
{
  "dateRanges": [{ "startDate": "2026-06-01", "endDate": "today" }],
  "dimensions": [{ "name": "date" }],
  "metrics":    [{ "name": "eventCount" }],
  "dimensionFilter": {
    "filter": {
      "fieldName": "eventName",
      "stringFilter": { "value": "generate_lead" }
    }
  }
}
```

`eventCount` com o filtro `eventName = generate_lead` = numero de leads. Sem o filtro, `eventCount`
conta TODOS os eventos (inflado). Pra "leads no periodo", use `keyEvents`/`eventCount` filtrado,
nunca `sessions`.

### Exemplo 2, leads por host e UTM (atribuicao de origem)

```json
{
  "dateRanges": [{ "startDate": "${RESOURCE_ID}", "endDate": "today" }],
  "dimensions": [
    { "name": "hostName" },
    { "name": "sessionSource" },
    { "name": "sessionMedium" }
  ],
  "metrics": [{ "name": "eventCount" }],
  "dimensionFilter": {
    "filter": {
      "fieldName": "eventName",
      "stringFilter": { "value": "generate_lead" }
    }
  },
  "orderBys": [{ "metric": { "metricName": "eventCount" }, "desc": true }]
}
```

### Exemplo 3, visitantes / page_view por dia (camada Visitantes do funil)

```json
{
  "dateRanges": [{ "startDate": "${RESOURCE_ID}", "endDate": "today" }],
  "dimensions": [{ "name": "date" }, { "name": "hostName" }],
  "metrics":    [{ "name": "sessions" }, { "name": "screenPageViews" }]
}
```

Cuidado de contagem (aprendido na dash SIM): `sessions` e a metrica HONESTA pro funil macro;
`screenPageViews` por UTM e a unica aditiva (delta ~0). Quebrar por UTM **infla** `sessions`
(~+18%) e `totalUsers` (~+25%) por dupla contagem. Escolha a metrica conforme o corte.

### Dimensoes e metricas uteis (GA4)

- Dimensoes: `date`, `eventName`, `hostName`, `pagePath`, `pageLocation`,
  `sessionSource`, `sessionMedium`, `sessionCampaignName`, `firstUserSource`, `deviceCategory`,
  `country`, `landingPage`.
- Metricas: `eventCount`, `keyEvents` (antes `conversions`), `sessions`, `totalUsers`,
  `activeUsers`, `newUsers`, `screenPageViews`, `engagedSessions`, `userEngagementDuration`.
- Datas relativas aceitas: `today`, `yesterday`, `NdaysAgo`. Realtime e endpoint a parte
  (`:runRealtimeReport`, janela ~30min, dimensoes reduzidas).

### Pegadinhas da Data API

- Sempre `properties/{ID_NUMERICO}`. Passar `G-...` = 400/403. Property errada = 403 PERMISSION.
- Quota: API tem limite de tokens por property/dia. Lote grande = paginar (`limit`/`offset`).
- `(not set)` em source/medium = trafego sem UTM/referrer (direto/app). Nao e erro.
- "Threshold/amostragem": GA4 pode aplicar data thresholds quando o volume e baixo (esconde linha).
- O dado de HOJE e parcial (ingestao tem lag de horas). Pra fechar dia, use ate `yesterday`.

## Workflow padrao

1. Identificar o que se quer: leads, visitas/page_view, ou descoberta de estrutura.
2. Resolver a propriedade certa (leads reais => `${RESOURCE_ID}`). Property numerica, nao `G-`.
3. Obter access token: refresh (`GA4_REFRESH_TOKEN` + client) -> `oauth2.googleapis.com/token`.
4. Montar `runReport` (date range + dimensions + metrics + dimensionFilter por `eventName`).
5. POST em `.../properties/{ID}:runReport`. Ler `rows[]` (dimensionValues / metricValues).
6. Sanidade: dado de hoje e parcial; `(not set)` e sem-UTM; filtrar evento certo.
7. Se for alimentar a dash, e via `importador_ga4_leads.py` -> `dwh.fct_lead` (nao chamar a API
   na mao pra gravar no warehouse).

## Saida esperada

- **Pergunta pontual (leads/visitas por periodo):** numero(s) + recorte (host/UTM/dia) + a
  propriedade e o evento usados + ressalva de parcialidade do dia corrente. Zero numero inventado.
- **Diagnostico "GA4 nao atualiza":** causa provavel (token revogado por troca de senha / quota /
  property errada) + acao (reautorizar e regravar `GA4_REFRESH_TOKEN`), sem expor segredo.
- **Descoberta de estrutura:** lista de propriedades/streams/measurement IDs com qual tem dado.

## Troubleshooting rapido

- `403 PERMISSION_DENIED`: a conta OAuth nao tem acesso aquela property, ou usou property errada.
  Confirmar que o usuario do refresh token e Viewer+ na ${RESOURCE_ID}.
- `400 INVALID_ARGUMENT` em property: passou `G-...` no lugar do ID numerico.
- `invalid_grant` ao trocar refresh: token revogado (troca de senha Google) -> reautorizar.
- Relatorio vazio numa property SIM-named: esperado, elas estao vazias; usar a ${RESOURCE_ID}.
- Numero de "leads" alto demais: faltou o `dimensionFilter` por `eventName = generate_lead`.

## TODOs a confirmar ao vivo

- TODO: nomes EXATOS no `MASTER.env` do client OAuth do GA4 (`GA4_CLIENT_ID/SECRET` proprios ou
  reuso do `GOOGLE_GTM_*`?). Confirmado so `GA4_REFRESH_TOKEN`.
- TODO: vinculo property<->stream de `${RESOURCE_ID}` (esperado ${RESOURCE_ID}) + measurement IDs dos
  dominios SIM/HAU/Editora.
- TODO: linha de cron atual do importador GA4 no Hetzner e se inclui `--pageviews`.
- TODO: confirmar via Admin API se ha outras propriedades alem das 3 conhecidas (HAU/Editora).

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
