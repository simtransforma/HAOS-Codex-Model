---
name: tiktok-tracking-setup
description: "Implementa\u00e7\u00e3o completa de tracking TikTok \u2014 Pixel client-side (snippet, ttq.track, ttq.identify), Events API CAPI server-side (payload, dedupe via event_id, Advanced Matching), EMQ score (como chegar a 8+), ttclid e _ttp (lifetime, propaga\u00e7\u00e3o cross-subdomain), Standard Events list, integra\u00e7\u00f5es server-side (Stape, GTM Server, Segment, RudderStack, Snowplow, mParticle, Tealium), partner integrations (Shopify, WooCommerce, VTEX, Tray, Nuvemshop), debug (Pixel Helper, Test Events), Custom Audiences upload SHA-256 e LGPD/ANPD/consent. Use sempre que precisar instalar, debugar ou auditar tracking de TikTok no Brasil."
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

# TikTok Tracking Setup — Skill Operacional

Use ao instalar, debugar ou auditar tracking TikTok (Pixel + CAPI + EMQ + audiences) no Brasil.

---

## 1. TikTok Pixel (client-side)

### 1.1 Base snippet (no `<head>`)

```html
<script>
!function (w, d, t) {
  w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];
  ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie","holdConsent","revokeConsent","grantConsent"];
  ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};
  for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);
  ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e};
  ttq.load=function(e,n){var r="https://analytics.tiktok.com/i18n/pixel/events.js",o=n&&n.partner;
    ttq._i=ttq._i||{};ttq._i[e]=[];ttq._i[e]._u=r;ttq._t=ttq._t||{};ttq._t[e]=+new Date;ttq._o=ttq._o||{};ttq._o[e]=n||{};
    n=document.createElement("script");n.type="text/javascript";n.async=!0;n.src=r+"?sdkid="+e+"&lib="+t;
    e=document.getElementsByTagName("script")[0];e.parentNode.insertBefore(n,e)};
  ttq.load('SEU_PIXEL_ID');
  ttq.page();
}(window, document, 'ttq');
</script>
```

### 1.2 Standard Events (atualizado mai/2025; nomes legados ainda funcionam)

| Evento | Quando disparar | Parâmetros |
|---|---|---|
| `ViewContent` | PDP/conteúdo visualizado | content_type, content_id, content_name, content_category, currency, value, quantity, contents[] |
| `ClickButton` | CTA genérico | content_type, content_id, description |
| `Search` | Busca interna | query, content_category |
| `AddToWishlist` | Wishlist | content_id, content_name, currency, value |
| `AddToCart` | Cart | content_type, content_id, currency, value, quantity, contents[] |
| `InitiateCheckout` | Início checkout | content_type, currency, value, contents[] |
| `AddPaymentInfo` | Método de pagto | currency, value |
| `PlaceAnOrder` (legacy: `CompletePayment`/`Purchase`) | Compra concluída | content_type, content_id, currency, value, quantity, contents[], order_id |
| `Subscribe` | Assinatura | currency, value, predicted_ltv |
| `StartTrial` | Trial | currency, value, content_ids |
| `Contact` | Contato | description |
| `Download` | Download asset | content_id |
| `SubmitForm` | Form enviado | content_id, form_id |
| `CompleteRegistration` | Sign-up | content_id, status |
| `CustomizeProduct` | – | content_id |
| `FindLocation` | – | content_id |
| `Schedule` | – | content_id |
| `SubmitApplication` | – | content_id |
| `ApplicationApproval` | – | content_id |

### 1.3 Exemplo de uso (ViewContent + Purchase)

```js
// PDP
ttq.track('ViewContent', {
  content_type: 'product',
  content_id: 'SKU-12345',
  content_name: 'Tênis Air Brasil',
  content_category: 'Calçados',
  currency: 'BRL',
  value: 299.90,
  quantity: 1,
  contents: [{ content_id: 'SKU-12345', content_type: 'product', content_name: 'Tênis Air Brasil', price: 299.90, quantity: 1 }]
});

// Purchase (com event_id para dedupe com CAPI)
ttq.track('PlaceAnOrder', {
  content_type: 'product', currency: 'BRL', value: 599.80,
  contents: [{ content_id: 'SKU-12345', price: 299.90, quantity: 2 }]
}, { event_id: 'order_' + orderId });
```

### 1.4 Identify (Advanced Matching client-side)

Chamar ANTES de qualquer `track`. SDK faz SHA-256 automático em PII em plaintext.

```js
ttq.identify({
  email: 'user-000044@account.example.invalid',
  phone_number: '${USER_RESOURCE_000045}',
  external_id: 'user_42'
});
```

### 1.5 Instalação por plataforma
- **Manual** no `<head>`.
- **GTM client** — template "TikTok Pixel" comunitário.
- **Shopify** — TikTok Sales Channel + Advanced Data Sharing (ativa CAPI automático com event_id consistente).
- **WooCommerce** — TikTok for Business plugin oficial, ou Conversios/PixelYourSite.
- **VTEX** — App TikTok for Business no App Store (LATAM/BRL only).
- **Magento/Adobe Commerce** — módulo Apptrian ou Launch + extension TikTok.
- **Tray/Nuvemshop/Yampi** — via GTM ou PixelYourSite/Conversios.

### 1.6 Debug
- **TikTok Pixel Helper** (Chrome): eventos, parâmetros, EMQ por evento, erros de schema.
- **Events Manager → Test Events**: usar `test_event_code` em CAPI antes de produção.
- **Diagnostics**: warnings de duplicação, ausência de event_id, EMQ baixo.

---

## 2. Events API (CAPI) — server-side

### 2.1 Endpoint
- **POST** `https://business-api.tiktok.com/open_api/v1.3/event/track/`
- Headers: `Access-Token: <token>`, `Content-Type: application/json`.
- Batch: até **50 eventos**/request; payload ≤ **1 MB**.

### 2.2 Payload schema

```json
{
  "event_source": "web",
  "event_source_id": "C8E2OS3C77UABCDXYZ",
  "partner_name": "Agencia XPTO",
  "test_event_code": "TEST12345",
  "data": [{
    "event": "PlaceAnOrder",
    "event_time": 1735689600,
    "event_id": "order_2025-12-31_98765",
    "user": {
      "ttclid": "E.C.P.v3fQ2RHacdkf...",
      "ttp": "94e2a4j9-h3ss-...",
      "external_id": "9a5e8...sha256",
      "email": "0c69d...sha256",
      "phone": "f1abe...sha256",
      "first_name": "1d4e8...sha256",
      "last_name":  "ab53c...sha256",
      "city":  "f99d2...sha256",
      "state": "9e2a0...sha256",
      "country": "br",
      "zip_code": "01001...sha256",
      "ip": "192.0.2.1",
      "user_agent": "Mozilla/5.0 ...",
      "locale": "pt_BR"
    },
    "properties": {
      "currency": "BRL", "value": 599.80,
      "content_type": "product", "content_id": "SKU-12345",
      "contents": [{ "content_id": "SKU-12345", "price": 299.90, "quantity": 2 }],
      "order_id": "98765"
    },
    "page": { "url": "https://service.example.invalid", "referrer": "https://service.example.invalid" },
    "limited_data_use": false
  }]
}
```

### Campos hashed (SHA-256) vs claro
- **Hashear**: email, phone, external_id, first_name, last_name, city, state, zip_code.
- **NÃO hashear**: ttclid, ttp, ip, user_agent, country (ISO-2 minúsculo), locale.

### 2.3 Exemplo Node.js

```js
import axios from 'axios';
import crypto from 'crypto';

const sha256 = v => crypto.createHash('sha256').update(String(v).trim().toLowerCase()).digest('hex');

await axios.post('https://business-api.tiktok.com/open_api/v1.3/event/track/', {
  event_source: 'web',
  event_source_id: process.env.TT_PIXEL_ID,
  partner_name: 'AgenciaXPTO',
  data: [{
    event: 'PlaceAnOrder',
    event_time: Math.floor(Date.now()/1000),
    event_id: `order_${order.id}`,
    user: {
      ttclid: req.cookies.ttclid,
      ttp:    req.cookies._ttp,
      email:  sha256(order.email),
      phone:  sha256(order.phoneE164),
      external_id: sha256(order.userId),
      ip:     req.headers['x-forwarded-for']?.split(',')[0],
      user_agent: req.headers['user-agent']
    },
    properties: {
      currency: 'BRL', value: order.total,
      contents: order.items.map(i => ({ content_id: i.sku, price: i.price, quantity: i.qty })),
      order_id: order.id
    },
    page: { url: order.successUrl, referrer: order.referrer }
  }]
}, { headers: { 'Access-Token': secret_placeholder, 'Content-Type': 'application/json' } });
```

### 2.4 Exemplo Python

```python
import hashlib, time, requests, os
def sha(v): return hashlib.sha256(str(v).strip().lower().encode()).hexdigest()

payload = {
  "event_source": "web",
  "event_source_id": os.environ["TT_PIXEL_ID"],
  "partner_name": "AgenciaXPTO",
  "data": [{
    "event": "PlaceAnOrder",
    "event_time": int(time.time()),
    "event_id": f"order_{order_id}",
    "user": {
      "email": sha(email), "phone": sha(phone_e164),
      "external_id": sha(user_id),
      "ttclid": ttclid, "ttp": ttp,
      "ip": client_ip, "user_agent": ua
    },
    "properties": {"currency":"BRL","value": total, "order_id": order_id,
                   "contents":[{"content_id": sku, "price": price, "quantity": qty}]}
  }]
}
r = requests.post("https://business-api.tiktok.com/open_api/v1.3/event/track/",
                  headers={"Access-Token": os.environ["TT_ACCESS_TOKEN"]},
                  json=payload, timeout=10)
```

### 2.5 Deduplicação
- Dedupe por par **(`event`, `event_id`)** no `event_source_id`.
- **Pixel↔Pixel** ou **API↔API**: dedupe em janela 48h.
- **Pixel↔API**: dedupe/merge após 5 min, dentro de 48h.
- Sem `event_id` → CPA inflado, algoritmo aprende em sinal falso.
- Convenção: `event_id = "{event}_{order_id}"` ou `"{event}_{timestamp_ms}_{uuid}"`.

### 2.6 Partner integrations
- **Stape / sGTM** (template `stape-io/tiktok-tag`) — Shopify/Woo/Magento; SHA-256 automático.
- **GTM Server-side (sGTM)** — Tag oficial comunidade.
- **Segment** — destination "TikTok Conversions".
- **RudderStack** — destination TikTok Ads/Conversions.
- **mParticle** — mapping nativo dos standard events.
- **Hightouch (Reverse ETL)** — eventos a partir de Snowflake/BigQuery.
- **Tealium server-side** — 50/batch, queue 5 min, 1 MB.
- **Adobe Launch / Web SDK** — extensão oficial.
- **Customer.io, AppsFlyer, Adjust, Branch** — App events.

### 2.7 Offline/CRM upload
- Mesmo endpoint, `event_source: "offline"` ou `"crm"`.
- Cada registro: mínimo email OU phone (plaintext convertido localmente em hash) para match.

### 2.8 App events
- `event_source: "app"`; via SDK ou MMP (AppsFlyer/Adjust/Branch/Singular).

---

## 3. EMQ — Event Match Quality

Score 0–10 (Below Average / Good / Great).

### Faixas e impacto
| Faixa | Score | Impacto |
|---|---|---|
| Below Average | 0–5 | Algoritmo não otimiza; CPA infla 30–60%; learning travado |
| Good | 5–7 | Atribuição parcial, depende de ttclid |
| Great | 8–10 | Match probabilístico + determinístico; learning rápido |

### Sinais (ordem de importância)
1. **ttclid** (click ID) — determinístico, peso máximo.
2. **ttp** (cookie first-party) — match cross-session.
3. **email + phone** hashed.
4. **external_id** hashed.
5. **IP + UA** — probabilístico.
6. **first/last name, city, state, zip** — adicional.

### Receita para EMQ ≥ 8
- Capturar `ttclid` da URL e persistir em cookie próprio 7d.
- Persistir `_ttp` (gerado pelo pixel) e enviar no CAPI.
- Capturar email + phone E.164 no checkout/login, hashear, enviar em `ttq.identify` + CAPI.
- Enviar `external_id` em **todo** evento.
- sGTM em Stape: IP do usuário (não do servidor de tag), UA original.
- Phone E.164 com `+55...` antes do hash.

### Impacto financeiro
- TikTok internal: click-only sem CAPI+EMQ subestima conversões em **~73% para app advertisers**.
- LATAM e-commerce: 30–50%.
- Ganho típico: **+15–35% ROAS reportado** quando EMQ médio sobe de 4 → 8.

---

## 4. `ttclid` e `_ttp`

### `ttclid` (TikTok Click ID)
- Param URL ao clicar ad TikTok (`?ttclid=E.C.P.v3fQ2...`).
- Lifetime útil: **7 dias**.
- Propagar cross-subdomain: cookie `Domain=.dominio.com.br; Max-Age=604800`.
- Em Next.js/Express middleware:

```js
app.use((req, res, next) => {
  const ttclid = req.query.ttclid;
  if (ttclid) {
    res.cookie('ttclid', ttclid, {
      domain: '.minhaloja.com.br',
      maxAge: 7 * 24 * 60 * 60 * 1000,
      sameSite: 'lax', secure: true
    });
  }
  next();
});
```

- No CAPI: `user.ttclid` sem hash.
- GA4 audit: sessões com `ttclid` que aparecem como "direct" → falta UTM (`utm_source=tiktok`).

### `_ttp` (Pixel cookie)
- Cookie first-party criado pela `events.js`.
- Identificador estável do browser (cobre orgânico TikTok, view-through).
- No CAPI: `user.ttp` sem hash.

---

## 5. Server-side stacks recomendados

| Stack | Custo mensal | Trade-off |
|---|---|---|
| **GTM Server-Side (Cloud Run)** | ~US$30–80 infra | Mais barato, requer time técnico, sem suporte; bom EMQ |
| **Stape.io** | US$20–500+ | sGTM gerenciado, templates prontos, suporte BR |
| **Segment** | US$120/mês start (10k MTUs) | Robusto, multi-destino, escala caro |
| **RudderStack** | Free <1M events/mo | Open-source, warehouse-first |
| **Snowplow** | Self-host US$ infra; cloud US$1k+/mês | Schema rigoroso, atomic table; não afetado por ITP |
| **mParticle** | Enterprise | Mobile-first, MMP, expensive |
| **Tealium iQ + EventStream** | Enterprise | Forte governança |
| **AppsFlyer / Adjust / Branch** | Per install | Obrigatório para apps; integra TikTok Events App API |

**Recomendação agência BR DTC:** **Stape + sGTM** é sweet-spot para Shopify/VTEX (R$ <USER_AMOUNT>–500/mês, EMQ 8+, deploy <1 dia). DTC grande (>R$ <USER_AMOUNT>/mês ad spend): Segment ou Snowplow + warehouse-first.

---

## 6. Custom Audiences upload (SHA-256)

### Formatos
- CSV/TXT, ≤ **1 GB**, vírgula ou newline.
- Header: `Email`, `Phone`, `MAID`, `IDFA`, `GAID`.
- UTF-8.

### Hashing
- **SHA-256** preferido (MD5 aceito).
- Normalizar ANTES de hash:
  - Email: lowercase, trim.
  - Phone: E.164 (`${USER_RESOURCE_000045}`), sem espaços/hífens.
  - external_id: lowercase do CRM ID.
- Conteúdo raw todo upper OU todo lower (consistente).

### Segmentos para Shop BR
| Audiência | Tamanho | Refresh | Uso |
|---|---|---|---|
| High-LTV top 10% por GMV 12m | 5–20k | Mensal | Seed LAL 1% |
| Repeat buyers ≥2 ordens | 10–50k | Semanal | Retargeting upsell |
| AOV > R$ <USER_AMOUNT>| 10–30k | Semanal | Exclusão de aquisição low-ticket |
| Lapsed 90–180d | 20–100k | Quinzenal | Win-back |
| Cart abandoners 7d | 5–30k | Diário | Retargeting dinâmico |
| PDP viewers no purchase 14d | 50–200k | Diário | Retargeting cold-warm |
| Refunders / chargebacks | 1–5k | Mensal | **EXCLUSÃO** em todas |
| Email subscribers active 30d | 50–200k | Semanal | Nurture |

### Endpoint Marketing API
```bash
# Create
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/create/" \
  -H "Access-Token: $AT" -H "Content-Type: application/json" \
  -d '{"advertiser_id":"'$AID'","custom_audience_name":"BR_HighLTV_Top10pct","calculate_type":"EMAIL_SHA256"}'

# Upload file
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/file/upload/" \
  -H "Access-Token: $AT" \
  -F "advertiser_id=$AID" -F "calculate_type=EMAIL_SHA256" \
  -F "file=@audience_emails_hashed.csv"

# Apply
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/dmp/custom_audience/file/apply/" \
  -H "Access-Token: $AT" -H "Content-Type: application/json" \
  -d '{"advertiser_id":"'$AID'","custom_audience_id":"'$CAID'","file_paths":["FILE_PATH"],"calculate_type":"EMAIL_SHA256"}'
```

---

## 7. LGPD / ANPD / Consent

### Bases legais
- LGPD (Lei 13.709/2018) exige opt-in informado, livre e específico para tracking não essencial.
- **Cookies estritamente necessários** (carrinho, sessão): dispensam consentimento.
- **Cookies de marketing/tracking** (TikTok Pixel, ttclid, _ttp): exigem opt-in prévio.
- Hashed PII no CAPI: ainda é dado pessoal se re-identificável. Use "consentimento" (Art. 7º I) ou "legítimo interesse" (Art. 7º IX) com balancing test documentado.

### Cookie banner
- **1º nível**: Aceitar / Rejeitar / Preferências — sem dark patterns.
- **2º nível**: categorias (essencial / funcional / analytics / marketing) com toggle.
- Retenção do consentimento: 6–12 meses.
- Log: timestamp + IP + texto da política versão X em DB.

### Consent Mode para TikTok
- Se rejeita marketing → **não carregar pixel + não enviar CAPI com PII**.
- Se aceita → pixel completo + CAPI com EMQ.
- Implementação:
  ```js
  ttq.holdConsent();      // antes do load
  ttq.grantConsent();     // quando user aceita
  ttq.revokeConsent();    // quando rejeita
  ```

### Penalidades ANPD
- Até **2% do faturamento BR**, **R$ <USER_AMOUNT>i por infração**.

### Retention
- Event analytics raw: máx 90–180d; agregar depois.
- Hashed PII em audiências: refresh trimestral, deletar quando perder finalidade.
- Direito ao esquecimento: pipeline `DELETE FROM` por external_id + delete em TikTok via CA update.

---

## 8. Custom Conversions

Quando evento não bate com Standard:

1. Events Manager → Pixel → **Custom Events** → Create.
2. Regra: URL contém `/lead/sucesso` OU `ttq.track('CustomName', {...})`.
3. Source of quality: mínimo **50 conversões/semana** por ad set para sair de learning.
4. Mapear custom para "Optimization Event" no ad group.

**Heurística**: Standard tem melhor performance (TikTok já sabe o que é Purchase). Custom é para nichos ("WhatsAppClick", "VirtualAppointmentBooked"). Usar Custom como **secundário**.

---

## 9. Checklist de implementação (DTC BR novo)

1. **Dia 1**: Pixel base + `ttq.identify` + `Purchase` com `event_id=order_{id}`.
2. **Dia 2–3**: `ttclid` capture + cookie `.dominio.com.br` 7d.
3. **Dia 4–7**: Stape sGTM (ou GTM SS Cloud Run) + tag TikTok Events API com mesmo `event_id`.
4. **Semana 2**: Validar EMQ ≥ 7 em Events Manager → Diagnostics; dedupe 0 warnings.
5. **Semana 2**: Marketing API token + Reporting sync diário → BigQuery via Fivetran/Airbyte.
6. **Semana 3**: TikTok Shop OAuth + webhooks (ORDER_STATUS_CHANGE / PACKAGE_UPDATE / REFUND_STATUS_CHANGE) → `fact_shop_order`.
7. **Semana 4**: Dashboard MER + CAC + ROAS + creative-level + contribution margin.
8. **Mês 2**: 1ª Conversion Lift Study (se spend ≥ USD 30k/mês) ou GeoLift DIY.
9. **Mês 3+**: Custom Audiences upload mensal.
10. **Trimestral**: Robyn MMM rerun calibrado com CLS.

---

## Skills relacionadas
- **tiktok-ads-fundamentals** — onde os eventos otimizam.
- **tiktok-bi-metrics** — schemas, SQL, dashboards.
- **tiktok-shop-fundamentals** — Shop Open API e webhooks.

## Fontes
Lista em `./references/sources.md`.
