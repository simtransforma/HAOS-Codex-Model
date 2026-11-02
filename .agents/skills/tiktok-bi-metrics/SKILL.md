---
name: tiktok-bi-metrics
description: "BI e analytics para TikTok Ads + TikTok Shop \u2014 KPIs e f\u00f3rmulas (CPM/CPC/CTR/CVR/CPA/ROAS/MER/CAC/Hook Rate/Hold Rate, GMV/AOV/refund rate/repeat/LTV), Marketing API Reporting (sync/async, 180d lookback, m\u00e9tricas e dimens\u00f5es), Shop Open API (orders/finance/webhooks), pipelines ETL (Fivetran/Airbyte/Funnel/Supermetrics/Windsor), schemas star (BigQuery/Snowflake), SQL exemplos (ROAS por creative, contribution margin Shop, anti-fraud IVT), BI tools (Looker Studio/Metabase/PowerBI/Hex/Lightdash), MMM (Robyn/Meridian/PyMC/Recast), Conversion Lift, attribution windows e MTA (Triple Whale/Northbeam/Rockerbox/Hyros/Haus). Use sempre que precisar montar dashboard, calcular KPI, escrever SQL, escolher MTA/MMM ou puxar dados via API."
---

## Contrato publico de execucao

Material de dominio portado da fonte real, nao uma instalacao de infraestrutura.
As regras do usuario e do AGENTS.md prevalecem sobre comandos e exemplos abaixo.
Publicar, enviar, gastar, alterar servidores, reiniciar, apagar, push e merge
exigem consentimento explicito para o destino e a acao. Nao executar comandos
com placeholders. Nao buscar o cofre ou ambientes do autor. Ferramentas/MCPs
citados precisam existir na instalacao do usuario; nomes nao provam acesso.
Consulte [PORTABILITY.md](PORTABILITY.md) para dependencias, recursos omitidos,
licencas e adaptacoes. Exemplos preservados nao sao prova de estado vivo.

# TikTok BI & Métricas — Skill Operacional

Use ao montar dashboard, calcular KPI, escrever SQL, escolher MTA/MMM ou puxar dados via API.

---

## 1. KPIs — fórmulas

### 1.1 Tráfego pago
| Métrica | Fórmula |
|---|---|
| CPM | `spend / impressions * 1000` |
| CTR | `clicks / impressions` |
| CPC | `spend / clicks` |
| CVR | `conversions / clicks` |
| CPA | `spend / conversions` |
| ROAS (platform) | `attributed_revenue / spend` |
| **MER / Blended ROAS** | `total_revenue / total_spend_all_channels` |
| nCAC | `spend / new_customers` |
| CAC payback (meses) | `nCAC / contribution_margin_per_customer_per_month` |
| Contribution margin % | `(revenue - cogs - fees - shipping - ad_spend) / revenue` |
| **Hook rate** | `video_views_3s / impressions` |
| **Hold rate** | `video_views_p100 / video_views_3s` |

### 1.2 TikTok Shop
| Métrica | Fórmula |
|---|---|
| GMV | `sum(item_price * qty)` (antes de descontos) |
| Net GMV | `GMV - refunds - cancelled` |
| AOV | `GMV / orders` |
| Units per order | `units / orders` |
| Refund rate | `refunded_value / GMV` |
| Fulfillment SLA | `% pedidos enviados dentro do seller SLA` |
| Repeat rate 90d | `repeat_buyers_90d / total_buyers_90d` |
| LTV (cohort) | `sum(net_revenue) by cohort_month` |
| Shipping subsidy % | `seller_shipping_cost / GMV` |

---

## 2. Marketing API — Reporting

### 2.1 Endpoints
- **Sync**: `POST /open_api/v1.3/report/integrated/get/` — até 20.000 ads/request.
- **Async**: `POST /report/task/create/` → recebe `task_id` → `GET /report/task/check/` → `GET /report/task/download/`.
- Volumes > 1M linhas / > 100d: **sempre async**.

### 2.2 Parâmetros principais
| Param | Valor |
|---|---|
| `advertiser_id` | obrigatório |
| `report_type` | `BASIC` · `AUDIENCE` · `PLAYABLE_MATERIAL` · `CATALOG` · `BC` |
| `data_level` | `AUCTION_AD` · `AUCTION_ADGROUP` · `AUCTION_CAMPAIGN` · `AUCTION_ADVERTISER` · `RESERVATION_*` |
| `dimensions` | array (ex.: `["ad_id","stat_time_day","country_code"]`) |
| `metrics` | array |
| `start_date`/`end_date` | YYYY-MM-DD |
| `lifetime` | bool |
| `page`/`page_size` | até 1000 |

### 2.3 Lookback
- BASIC `AUCTION_AD`: até **180 dias** retroativos.
- Granularidade **hour**: **30 dias**.
- Métricas de vídeo: até **90 dias**.
- > 180d: precisa ter feito sync prévio para DW.

### 2.4 Métricas BASIC principais
- Spend: `spend`, `cpc`, `cpm`, `cpa`, `cost_per_conversion`, `cost_per_1000_reached`.
- Volume: `impressions`, `clicks`, `ctr`, `reach`, `frequency`.
- Vídeo: `video_play_actions`, `video_views_p25`, `video_views_p50`, `video_views_p75`, `video_views_p100`, `video_watched_2s`, `video_watched_6s`, `average_video_play`, `average_video_play_per_user`.
- Engajamento: `likes`, `comments`, `shares`, `profile_visits`, `follows`.
- Conversão: `conversion`, `conversion_rate`, `cost_per_conversion`, `total_purchase_value`, `total_complete_payment_rate`, `total_complete_payment`, `value_per_complete_payment`, `roas` (`real_time_total_roas`).
- Shop: `total_onsite_shopping`, `onsite_shopping`, `onsite_shopping_roas`, `gmv`.

### 2.5 Dimensões / Breakdowns
`ad_id`, `adgroup_id`, `campaign_id`, `advertiser_id`, `stat_time_day`, `stat_time_hour`, `country_code`, `province_id`, `dma_id`, `placement`, `platform`, `gender`, `age`, `language`, `interest_category`, `device_type`, `os`, `creative_id`, `video_id`.

### 2.6 Outras APIs úteis
- Pixel: `/pixel/list/`, `/pixel/event/stats/`.
- Audience (DMP): create, file upload (até 1 GB CSV/TXT), file apply.
- Creative Asset: `/file/video/ad/upload/`, `/file/image/ad/upload/`.
- Campaign / AdGroup / Ad CRUD: `/campaign/create/`, `/adgroup/create/`, `/ad/create/`, `/ad/update/`.
- BC Reporting: `report_type=BC` agrega múltiplos advertisers.

### 2.7 Exemplo: sync report ad-level
```bash
curl -G "https://business-api.tiktok.com/open_api/v1.3/report/integrated/get/" \
  -H "Access-Token: $AT" \
  --data-urlencode "advertiser_id=$AID" \
  --data-urlencode "report_type=BASIC" \
  --data-urlencode "data_level=AUCTION_AD" \
  --data-urlencode 'dimensions=["ad_id","stat_time_day"]' \
  --data-urlencode 'metrics=["spend","impressions","clicks","ctr","cpc","conversion","total_purchase_value","real_time_total_roas","video_watched_6s"]' \
  --data-urlencode "start_date=2026-05-01" \
  --data-urlencode "end_date=2026-05-30" \
  --data-urlencode "page_size=1000"
```

---

## 3. TikTok Shop Open API — para BI

### 3.1 Autenticação (resumo; full em **tiktok-shop-fundamentals**)
- OAuth 2.0 via `services.tiktokshop.com/open/authorize`.
- Token endpoint: `https://service.example.invalid`.
- **Access token**: 90 dias. **Refresh token**: 365 dias.
- Assinatura HMAC-SHA256 obrigatória.

### 3.2 Grupos de endpoints (v202309+)
| Grupo | Endpoints principais |
|---|---|
| Authorization | `/authorization/202309/shops`, `/authorization/202309/seller/authorize` |
| Product | `/product/202309/products/search`, `/product/202309/products/{id}`, POST create, PUT update |
| Order | `/order/202309/orders/search`, `/order/202309/orders/{id}`, `/orders/multi_get` |
| Fulfillment | `/fulfillment/202309/packages/ship`, `/logistics/202309/shipping_providers`, `/logistics/202309/warehouses` |
| Return & Refund | `/return_refund/202309/returns/search`, `/returns/{id}/approve|reject` |
| Promotion | `/promotion/202309/activities`, `/promotion/202309/coupons` |
| **Finance** (BI-key) | `/finance/202309/statements`, `/finance/202309/payments`, `/finance/202309/orders/settlements` |
| Seller Performance | `/seller/202309/shops/{cipher}/performance` |
| Webhook | `/event/202309/webhooks` |

### 3.3 Rate limits
- Padrão: **10 QPS** por loja (alguns endpoints sensíveis 3 QPS).
- Sliding window 1 min; 429 = `rate_limit_exceeded`.

### 3.4 Webhooks (real-time)
| event_type | Trigger |
|---|---|
| ORDER_STATUS_CHANGE | UNPAID, AWAITING_SHIPMENT, AWAITING_COLLECTION, IN_TRANSIT, DELIVERED, COMPLETED, CANCELLED |
| RECIPIENT_ADDRESS_UPDATE | Comprador atualizou endereço |
| PACKAGE_UPDATE | Status do pacote/tracking |
| RETURN_STATUS_CHANGE | Devolução solicitada/aprovada/recusada |
| REFUND_STATUS_CHANGE | Reembolso |
| CANCELLATION_STATUS_CHANGE | Cancelamento |
| PRODUCT_STATUS_CHANGE | Produto aprovado/recusado/desativado |
| PRODUCT_AUDIT | Auditoria de listagem |
| SELLER_PERFORMANCE | Mudança em scores |
| INVOICE_STATUS_CHANGE | NF-e BR/MX |
| AUTHORIZATION_REVOKE | Seller revogou app |

Validar HMAC; responder `200 OK` em <5s; retry exponencial caso contrário.

### 3.5 Exemplo: buscar pedidos
```bash
curl -X POST "https://service.example.invalid" \
  -H "Content-Type: application/json" \
  -d '{"create_time_ge": 1735689600, "create_time_lt": 1738368000, "order_status": "AWAITING_SHIPMENT", "page_size": 50}'
```

---

## 4. ETL/ELT providers

| Provider | TikTok Ads | TikTok Shop | Pricing-from |
|---|---|---|---|
| **Fivetran** | Sim (managed) | Não nativo (HTTP source) | US$0,01/MAR; ~US$300+/mês BR |
| **Airbyte** | Sim (OSS + cloud) | Beta/community | Free OSS / Cloud US$10/credit |
| **Stitch** | Sim | Não | US$100/mês |
| **Supermetrics** | Sim BQ/Snowflake | Não | US$190+/mês |
| **Funnel.io** | Sim, 230 sources | Não | US$400+/mês |
| **Windsor.ai** | Sim | Não | US$23–99+/mês |
| **Adverity** | Sim | Não | Enterprise |
| **Improvado** | Sim | Limitado | Enterprise |
| **Coupler.io** | Sim Looker Studio | Não | US$49+/mês |
| **OWOX BI** | Sim | Não | Custom |
| **Hevo Data** | Sim | Não | US$240+/mês |

**TikTok Shop**: maioria dos ETLs ainda não tem conector managed (mai/2026) → solução comum é **lambda Python/Node** batendo na Shop API diariamente, gravando em S3/GCS + Fivetran/Airbyte com generic HTTP source ou DuckDB.

---

## 5. Schema canônico (Star — BigQuery)

```sql
-- DIMENSÕES
CREATE TABLE dim_date     (date DATE, day INT64, week INT64, month INT64, ...);
CREATE TABLE dim_campaign (campaign_id STRING, campaign_name STRING, objective STRING, ...);
CREATE TABLE dim_adgroup  (adgroup_id STRING, campaign_id STRING, billing_event STRING, optimization_goal STRING, ...);
CREATE TABLE dim_ad       (ad_id STRING, adgroup_id STRING, creative_id STRING, video_id STRING, ad_name STRING, ad_format STRING, ...);
CREATE TABLE dim_creative (creative_id STRING, video_url STRING, thumbnail_url STRING, duration_seconds INT64, hook_type STRING, ...);
CREATE TABLE dim_product  (sku STRING, product_id STRING, category STRING, brand STRING, cogs FLOAT64, list_price FLOAT64, ...);
CREATE TABLE dim_geo      (country_code STRING, state STRING, city STRING, dma_id STRING, ...);

-- FATOS
CREATE TABLE fact_ad_performance_daily (
  date DATE, ad_id STRING, advertiser_id STRING,
  spend NUMERIC, impressions INT64, clicks INT64, video_watched_6s INT64,
  conversions INT64, conversion_value NUMERIC, real_time_roas NUMERIC,
  partition_date DATE
) PARTITION BY date CLUSTER BY ad_id;

CREATE TABLE fact_shop_order (
  order_id STRING, shop_id STRING, buyer_id STRING,
  order_status STRING, create_time TIMESTAMP, paid_time TIMESTAMP, shipped_time TIMESTAMP,
  gmv NUMERIC, discount NUMERIC, shipping_fee NUMERIC, platform_fee NUMERIC,
  refund_amount NUMERIC, item_count INT64, currency STRING, sku_array ARRAY<STRING>
) PARTITION BY DATE(create_time);

CREATE TABLE fact_shop_order_item (
  order_id STRING, order_line_id STRING, sku STRING, qty INT64,
  unit_price NUMERIC, item_total NUMERIC, seller_sku STRING, is_returned BOOL
);
```

### dbt packages
- `fivetran/tiktok_ads_source` + `fivetran/tiktok_ads`.
- `fivetran/ad_reporting` — combina Facebook + Google + TikTok + LinkedIn + Snapchat + Reddit + Pinterest + Amazon + Apple Search numa única `ad_reporting` table.

---

## 6. SQL essenciais

### 6.1 Reconciliação Shopify ↔ TikTok Ads
```sql
WITH ads AS (
  SELECT date, SUM(spend) spend, SUM(conversion_value) tt_attributed_revenue
  FROM fact_ad_performance_daily WHERE date BETWEEN '2026-05-01' AND '2026-05-30'
  GROUP BY 1
),
shop AS (
  SELECT DATE(created_at) date, SUM(total_price) gross_revenue,
         SUM(CASE WHEN referring_site LIKE '%tiktok%' OR utm_source='tiktok' THEN total_price END) shopify_tiktok_revenue
  FROM shopify_orders WHERE created_at >= '2026-05-01'
  GROUP BY 1
)
SELECT a.date, a.spend, a.tt_attributed_revenue, s.shopify_tiktok_revenue, s.gross_revenue,
       a.tt_attributed_revenue / NULLIF(s.shopify_tiktok_revenue,0) AS inflation_ratio,
       a.tt_attributed_revenue / NULLIF(a.spend,0)                  AS platform_roas,
       s.gross_revenue / NULLIF(a.spend,0)                          AS blended_mer
FROM ads a JOIN shop s USING (date) ORDER BY 1;
```

### 6.2 ROAS por criativo (creative-level)
```sql
SELECT
  d.date,
  c.creative_id, c.video_url, c.duration_seconds,
  SUM(a.spend) AS spend,
  SUM(a.impressions) AS impressions,
  SUM(a.clicks) AS clicks,
  SAFE_DIVIDE(SUM(a.clicks), SUM(a.impressions)) AS ctr,
  SUM(a.video_watched_6s) AS v6s,
  SAFE_DIVIDE(SUM(a.video_watched_6s), SUM(a.impressions)) AS hook_rate_6s,
  SUM(a.conversions) AS conv,
  SUM(a.conversion_value) AS revenue,
  SAFE_DIVIDE(SUM(a.conversion_value), SUM(a.spend)) AS roas
FROM fact_ad_performance_daily a
JOIN dim_ad ad      USING (ad_id)
JOIN dim_creative c USING (creative_id)
JOIN dim_date d     ON a.date = d.date
WHERE a.date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AND CURRENT_DATE()
GROUP BY 1,2,3,4
HAVING spend > 50
ORDER BY roas DESC;
```

### 6.3 Contribution Margin TikTok Shop
```sql
SELECT
  DATE_TRUNC(create_time, MONTH) AS month,
  COUNT(DISTINCT order_id)      AS orders,
  SUM(gmv)                       AS gmv,
  SUM(refund_amount)             AS refunds,
  SUM(gmv - refund_amount)       AS net_gmv,
  SUM(platform_fee)              AS platform_fees,
  SUM(shipping_fee)              AS shipping_subsidy,
  SUM(it.qty * p.cogs)           AS total_cogs,
  ads.spend                      AS ad_spend,
  SUM(gmv - refund_amount - platform_fee - shipping_fee - (it.qty * p.cogs)) - ads.spend AS contribution_margin,
  SAFE_DIVIDE(
    SUM(gmv - refund_amount - platform_fee - shipping_fee - (it.qty * p.cogs)) - ads.spend,
    SUM(gmv - refund_amount)
  ) AS cm_pct
FROM fact_shop_order o
JOIN fact_shop_order_item it USING (order_id)
JOIN dim_product p ON it.sku = p.sku
LEFT JOIN (
  SELECT DATE_TRUNC(date, MONTH) month, SUM(spend) spend
  FROM fact_ad_performance_daily GROUP BY 1
) ads ON DATE_TRUNC(o.create_time, MONTH) = ads.month
GROUP BY 1, ads.spend
ORDER BY 1;
```

### 6.4 Anti-fraud / IVT detection
```sql
SELECT ad_id,
  SAFE_DIVIDE(clicks, impressions) ctr,
  SAFE_DIVIDE(conversions, clicks) cvr,
  spend, clicks, impressions
FROM fact_ad_performance_daily
WHERE date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) AND CURRENT_DATE()
GROUP BY 1,5,6,7
HAVING ctr > 0.05 AND cvr < 0.001 AND spend > 100
ORDER BY spend DESC;
```

---

## 7. BI tools

| BI | TikTok Ads | TikTok Shop | Limitações |
|---|---|---|---|
| **Looker Studio** | Não nativo (3rd party) | Não | 5 connector req/s, refresh manual ou 1×/12h |
| **Metabase** | Via warehouse | Via warehouse | Nativo Postgres/BQ/Snowflake; sem conector direto |
| **Power BI** | Connectors marketplace (Windsor/Supermetrics) | Não | Refresh 8/dia (Pro), 48/dia (Premium) |
| **Tableau** | Via TabPy / 3rd party | Não | Custo licença alto |
| **Hex** | Via warehouse | Via warehouse | Python + SQL + notebook; ad-hoc |
| **Lightdash** | Via dbt | Via dbt | OSS dbt-first |
| **Preset/Superset** | Via warehouse | Via warehouse | OSS, custo zero |

**Padrão agência BR**: Fivetran/Airbyte → BigQuery → dbt → **Looker Studio** (C-level) + **Metabase** (operacional).

---

## 8. Attribution

### 8.1 Janelas padrão atuais
| Plataforma | Click | View | Opções click | Opções view |
|---|---|---|---|---|
| TikTok | 7d | 1d | 1d, 7d, 14d, 28d | 1d, 7d, none |
| Meta | 7d | 1d | 1d, 7d | 1d, none |
| Google Ads | 30d (Search) | n/a | 1d–90d | n/a |
| GA4 | data-driven (90d max) | – | – | – |

**TikTok Attribution Manager** → Performance Comparison compara janelas lado a lado sem refazer campanhas.

### 8.2 Click-only undervalues TikTok
- TikTok internal: click-only subestima conversões em **73% para app**.
- TransUnion 2024: TikTok gera **iROAS 2.35× maior** que reportado.
- **52% das conversões incrementais TikTok são exclusivas**.

### 8.3 Modelos
- Last-click (default).
- Data-driven (GA4 / TikTok Smart+).
- Position-based / Linear / Time-decay (Triple Whale, Northbeam).
- MTA: Hyros, Northbeam, Rockerbox, Triple Whale.
- **Incrementality (CLS / GeoLift)**: padrão-ouro.

### 8.4 Reconciliação cross-platform
Erro comum BR: somar TikTok (7d/1d) + Meta (7d/1d) + Google (30d) = 130%+ "atribuídos". Usar **MER**:
```
MER = Receita Total Shopify / Spend Total (Meta+TikTok+Google+Affiliate)
```

---

## 9. MMM (Marketing Mix Modeling)

### 9.1 Frameworks abertos
| Framework | Mantenedor | Status 2026 | Abordagem |
|---|---|---|---|
| **Robyn** | Meta | Mantido | Ridge + Nevergrad + Prophet |
| **Meridian** | Google | Substitui LightweightMMM | Bayesiano MCMC, geo+nacional |
| **LightweightMMM** | Google | **Deprecated jan/2025** | Bayesiano JAX |
| **PyMC-Marketing** | PyMC Labs | Mantido | Bayesiano PyMC |
| **Recast** | Recast (paid) | SaaS | Bayesiano semanal automatizado |

### 9.2 TikTok em MMM
- Canal típico com adstock + saturação (Hill ou Weibull).
- **Adstock TikTok**: half-life curto (2–5 dias) — viralização rápida, fadiga rápida.
- **Saturação**: forte (alcance limitado em LATAM/BR ainda crescendo).
- Last-click sub-pesa TikTok → MMM pode também sub-pesar se calibrar com conv. click-only. **Calibrar com Conversion Lift Studies do próprio TikTok**.

### 9.3 Conversion Lift Study (CLS) — TikTok nativo
- Test/control randomizado em **nível de usuário**.
- Reporta: incremental conversions, **iROAS**, **CPIC**, relative lift %.
- Requer **~USD 30–50k/mês** na vertical + 14–30 dias.
- Solicitar via account manager.

### 9.4 Geo-holdout (DIY)
- Dividir estados/cidades em test (com TT) vs control (sem) por 4–8 semanas.
- BR: clusters naturais por estado funcionam bem (SP/RJ/MG vs Sul/NE).
- Pacotes: `GeoLift` (Meta), `Causal Impact` (Google), `MarketMatch` (Robyn).

### 9.5 Stack recomendada por escala
- DTC <R$ <USER_AMOUNT>/mês: Triple Whale ou Northbeam + calibração CLS 1×/ano.
- R$ <USER_AMOUNT>–1M: Robyn ou Recast trimestral + GeoLift semestral.
- Enterprise >R$ <USER_AMOUNT>: Meridian/Robyn semanal + CLS contínuo + Haus/Recast.

---

## 10. MTA / Atribuição third-party

| Tool | From | Modelo | TikTok | Forte em | Fraco em |
|---|---|---|---|---|---|
| **Triple Whale** | US$129/mês | Last-click + linear + time-decay; Sonar (DDA add-on) | Bom (UTM+click) | Shopify, AI agents, brands $1M–40M | View-through fraco; escala caro |
| **Northbeam** | US$1k+/mês | Click + deterministic views (parceria oficial Meta+TikTok 2025) | **Excelente (view+click híbrido)** | Spenders >US$100k/mês, causal validation | Caro, complexo |
| **Rockerbox** | ~US$30k/ano | MTA omnichannel | View-through forte | Brick-and-mortar + offline + omni | Setup demorado |
| **Hyros** | US$99–230/mês | Click-deterministic | OK (UTM) | High-ticket / long sales cycle / info-products | Ops suite limitada |
| **Haus.io** | Enterprise | Geo experiments + MMM | Calibração TikTok | DTC scale-up | Caro |
| **Recast** | Enterprise | Bayesian MMM semanal | Calibração via CLS | Spenders maduros | Histórico 18m+ |
| **SegmentStream** | Enterprise | ML attribution | Sim | E-commerce EU | Pouca presença BR |
| **OWOX BI** | US$$ flexível | Funnel-based + GA4 raw | Sim via warehouse | GA4-heavy stacks | Curva |
| **Funnel.io** | US$400+/mês | ETL + reporting | Sim, 230 sources | Agências multi-cliente | Não é MTA puro |

### Recomendação agência BR por escala
- Cliente até R$ <USER_AMOUNT>/mês: Looker Studio + Windsor.ai + GA4 + UTM disciplinado.
- R$ <USER_AMOUNT>–500k/mês: Triple Whale ou Northbeam + GA4 + sGTM Stape.
- R$ <USER_AMOUNT>–2M/mês: Northbeam + Robyn trimestral + TikTok CLS.
- >R$ <USER_AMOUNT>/mês: Northbeam OU Rockerbox + Haus/Recast + Meridian/Robyn + DW próprio (BigQuery + dbt).

---

## 11. Anti-fraud / quality

TikTok IVT rate (Lunio): **24,20%** — o maior entre grandes plataformas.

### Sinais de IVT
| Sinal | Threshold |
|---|---|
| CTR alto + CVR baixíssimo | CTR >5% e CVR <0,1% |
| Bounce rate LP | >80% |
| Tempo de sessão | <3s |
| Geo mismatch | target BR mas IPs em outros países |
| Conv. horários atípicos | picos 2–5h madrugada |
| Pangle network spike | desligar se >30% do spend |
| Device anomaly | %ge alta de Android 5.x |

### Ferramentas
DoubleVerify · IAS (parceiros oficiais TikTok) · Lunio · Spider AF · ClickGUARD · Opticks Security · Tapper.

---

## 12. BR-specific watchouts

- **NF-e**: integração Bling / Tiny / Omie obrigatória — TikTok Shop BR exige NFe por venda.
- **Frete**: Correios/Loggi/J&T; medir custo de frete por canal.
- **PIX**: maior CVR vs cartão; medir `payment_method` no event properties; AOV menor mas abandono menor.
- **LGPD**: hashed PII em audiências exige base legal documentada — ver **tiktok-tracking-setup** §7.

---

## 13. Dashboard mínimo (Looker Studio, modelo)

### Páginas
1. **Overview** — MER, spend total, GMV/Receita, ROAS blended, CAC, contribution margin, vs mês anterior.
2. **TikTok Ads** — spend, conv., ROAS plataforma, CPM/CPC/CTR/CVR por campanha, top 10 ads por ROAS, hook rate por creative.
3. **TikTok Shop** — GMV, AOV, units, refund rate, repeat 90d, top SKUs, contribution margin por SKU.
4. **Creative** — todos os ads com hook rate, hold rate, ROAS, status (winner/learner/dead), tagging.
5. **Audience** — performance por age/gender/state, top interest categories, LAL performance vs cold.
6. **MMM/CLS** — output do MMM trimestral, CPIC do último CLS, geo holdout summary.

### Filtros globais
Date range · Cliente · Campanha · Ad Account · Vertical.

---

## 14. Checklist BI / handoff

1. Marketing API token guardado em secret manager.
2. Shop Open API tokens com refresh job (90d access, 365d refresh).
3. Fivetran/Airbyte sync diário → DW.
4. Webhook listener (Cloud Functions / Lambda) gravando em `fact_shop_order`.
5. dbt models build diário.
6. Dashboard Looker Studio com 6 páginas acima.
7. Alerts (Slack/email): IVT >5%, EMQ <6, ROAS <0,7×target, refund rate >X%.
8. Audience refresh automático mensal (high-LTV, lapsed, repeat).
9. Reporting cliente semanal (CSV + dashboard link).
10. MMM trimestral + CLS quando spend permitir.

---

## Skills relacionadas
- **tiktok-ads-fundamentals** — métricas e dimensões na fonte.
- **tiktok-shop-fundamentals** — Shop API e take-rate real.
- **tiktok-tracking-setup** — Pixel/CAPI/EMQ (qualidade dos sinais).

## Fontes
Lista em `./references/sources.md`.
