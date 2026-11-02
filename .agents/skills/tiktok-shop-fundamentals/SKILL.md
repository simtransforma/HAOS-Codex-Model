---
name: tiktok-shop-fundamentals
description: "Conhecimento operacional sobre TikTok Shop \u2014 cadastro de seller (US/UK/BR/MX), modelos de fulfillment (FBT/FBM/Affiliate), estrutura de taxas e comiss\u00f5es por categoria, catalog/listing, promo\u00e7\u00f5es, programa de afiliados, LIVE Shopping, Shop Ads (GMV Max), Open API, compliance e penalty points. Use sempre que precisar planejar entrada no TikTok Shop, estimar take-rate real, montar opera\u00e7\u00e3o de seller, configurar afilia\u00e7\u00e3o com creators, escolher fulfillment, integrar via API, ou auditar compliance de loja. Cobre 2025\u20132026 com foco em Brasil + EUA."
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

# TikTok Shop — Skill Operacional

Use esta skill sempre que estiver planejando, auditando ou operando uma loja TikTok Shop. Cobre seller setup, fulfillment, comissões reais, catalog, promoções, affiliate, LIVE shopping, Shop Ads (GMV Max), Open API e compliance — com foco em Brasil + EUA (2026).

> **Fontes oficiais que valem ler antes de qualquer decisão:** `seller-us.tiktok.com/university`, `seller-br.tiktok.com`, `partner.tiktokshop.com/docv2`, `developers.tiktok.com/doc/shop-management`, `business.tiktokshop.com`. Lista completa em references/sources.md.

## Mapa rápido — quando usar o quê

| Pergunta do usuário | Vá direto para |
|---|---|
| "Posso vender no TikTok Shop BR?" | §2 Cadastro de seller |
| "Quanto a TikTok vai me cobrar de fato?" | §4 Taxas e comissões |
| "Como cuido de envio?" | §3 Fulfillment |
| "Como funciona o programa de afiliados?" | §7 Affiliate |
| "Quero rodar live commerce" | §8 LIVE Shopping |
| "Quero rodar ads dentro da Shop" | §9 Shop Ads / GMV Max |
| "Quero integrar via API para BI/ERP" | §10 Open API |
| "Esse produto pode ser vendido?" | §11 Compliance |
| "Que números públicos posso citar?" | §12 Benchmarks |

---

## 1. Países e Status 2026

- **Mercados ativos (mai/2026):** EUA, Reino Unido, Alemanha, França, Itália, Espanha, Irlanda, Japão (lançado 2025), Singapura, Indonésia (via Tokopedia — ByteDance comprou 75%), Malásia, Tailândia, Vietnã, Filipinas, **México** (fev/2025) e **Brasil** (operacional mai/2025).
- **GMV global TikTok Shop 2025:** ~US$ 64,3–66 bi (≈2× 2024). Projeção 2026: **US$ 87–112 bi (+50–70% YoY)**.
- **GMV EUA 2025:** US$ 15,1 bi (+68% YoY, Momentum Works).
- **Brasil:** lançou em mai/2025; GMV no 1º mês ~US$ 1 mi → 3 meses depois ~US$ 50 mi/mês (25× crescimento). Brasil é o **2º maior mercado mundial em live shopping** (~111 mi usuários TikTok). **Não tem FBT no Brasil** ainda em 2026. MEI aceito desde mai/2026 (teto R$ <USER_AMOUNT>il/ano).
- **Roadmap:** Coreia do Sul em estudo, expansão LATAM (Colômbia, Chile, Argentina indicados).

---

## 2. Cadastro de Seller

### 2.1 EUA
- **PF:** ≥18 anos, residente US, RG/Passport/Driver License/State ID, SSN/ITIN, conta bancária US, W-9. Aprovação 24–48h.
- **PJ (LLC/Corp):** EIN, registro estadual, conta bancária da empresa, endereço US.
- **Cross-border (CB) US/UK:** desde 2024 só empresas licenciadas. Indivíduos foram banidos do CB US/UK.

### 2.2 Brasil
- **CNPJ ativo obrigatório**, cartão CNPJ emitido há ≤90 dias.
- **MEI aceito** desde mai/2026 (atenção ao teto R$ <USER_AMOUNT>il/ano ≈ R$ <USER_AMOUNT>/mês).
- Conta bancária PJ, documento do representante, comprovante de endereço.
- Cruzamento automático com Receita Federal — divergência bloqueia.
- Sellers com histórico em ML/Shopee são aprovados mais rápido.
- **Categorias proibidas BR:** produtos adultos, álcool, tabaco, vapes, animais, balões, fogos, armas/munição.
- **Categorias restritas (precisa aprovação):** automotivos, eletrônicos sensíveis (TVs grandes, drones), acessórios de moda com IP.

### 2.3 Local vs Cross-border
- **Local seller** = entidade no país do shop, fulfillment local, payout em moeda local. Padrão em US/UK/BR/MX.
- **CB seller** = entidade fora do país, exige licença CB + acordo com 3PL local.
- **US→MX:** TikTok recruta sellers americanos para vender ao México sem entidade local (CB regional).

---

## 3. Modelos de Fulfillment

### 3.1 FBT (Fulfilled by TikTok) — só onde existe
- 14+ DCs nos EUA; dispatch em 24h; **82,7% das entregas em 3 dias** quando uso ≥30%.
- **US$ 2,86–3,58/unidade** (pick+pack+ship) para single-unit — até 40% mais barato que TikTok Shipping discount.
- Pedidos FBT são **excluídos de OTDR e VTR** (não impactam SPS por logística).
- "3-Day Delivery" badge: **+15–20% conversão**, **+30% visualizações diárias**.
- **Independent shipping encerrou 31/mar/2026 nos EUA**: sellers US devem usar FBT, Upgraded TikTok Shipping ou Collections.
- Perde controle sobre packaging/unboxing.

### 3.2 FBM / Seller-Fulfilled (padrão BR)
- SLA dispatch: **3 dias úteis**; entrega prevista em 6 dias úteis.
- Seller controla packaging/frete/transportadora.
- Atraso/cancelamento conta direto no SPS.

### 3.3 Shoppable Live
- Métrica-chave: **GPM** = GMV por 1.000 viewers (unificador entre lives de tamanhos diferentes).
- Cadência: sessões ≥3h; 8h+ vê salto exponencial.

### 3.4 Shoppable Video
- Vídeos curtos 15–60s com tag de produto; algoritmo redistribui por semanas.

### 3.5 TikTok Shop Affiliate
- Vendas atribuídas a creators via link; live + affiliate são >50% do GMV em algumas categorias (beauty, fashion).

---

## 4. Taxas, Comissões e Payouts

### 4.1 EUA (2026)
- **Referral fee padrão:** 6% para a maioria das categorias.
- Por categoria: Fashion 8% / Beauty 5% / Electronics 3% / Home 5% / Health 6% / Food 2% / Sports 5% / Jewelry 5%.
- **Promo new seller:** 3% nos primeiros 90 dias (confirmar no onboarding).
- **Payment processing:** 1,02–3,78% (em cima da referral). **True take-rate ≈ 7%** antes de fulfillment e afiliado.
- **FBT fulfillment:** US$ 2,86–3,58/unidade.
- **Creator commissions médias:** Beauty 15–30%, Fashion 10–15%, Home 12–18%, Tech 5–10%.

### 4.2 Brasil (2026)
- **Comissão padrão:** 6% sobre o pedido.
- **Taxa por item:** **R$ <USER_AMOUNT>** por item vendido por menos de **R$ <USER_AMOUNT>** (similar à "regra da blusinha" ML/Shopee).
- **Promo onboarding:** 90 dias sem comissão + frete grátis ao cumprir missões.
- **Payment fees:** ~2,99% + R$ <USER_AMOUNT>em cartão; **~1,99% no PIX** (preferido por margem).
- **Subsídio de frete:** TikTok subsidia até **R$ <USER_AMOUNT>/pedido** em programas promocionais.
- **Comparativo (efetivo):** TikTok Shop BR 5–10% / Shopee 0–15% / ML 10–20% / Amazon BR 7–45% + assinatura + FBA.

### 4.3 Payout / Settlement
- 5 tiers: Introductory, Standard, Accelerated, Express, Deferred.
- Período padrão: começa **quando carrier marca entregue** + 8 dias.
- **Reserva:** parte retida 30 dias para cobrir devoluções.
- Saque diário / semanal / mensal.
- US: payout mínimo US$ 1 settled; US$ 2 para saque externo.

### 4.4 Cálculo de margem real (use sempre)
```
Margem líquida = Preço de venda
                − COGS
                − Referral fee (3–8%)
                − Payment fee (~2% PIX BR / ~3% cartão BR / 1–3,78% US)
                − Fulfillment (FBT US$ 2,86–3,58 OU custo de frete-out BR)
                − Comissão de afiliado (10–30% se aplicável)
                − Custo de ad (CAC)
                − Reserva 30 dias (impacta caixa, não P&L)
```
**Regra prática:** assuma take-rate plataforma de **≈ 7% US** ou **8–10% BR** (com R$ <USER_AMOUNT>/item em produtos baratos).

---

## 5. Catalog & Listing

### 5.1 Imagens
- **5 mínimas, 9 máximas** por produto (até 3 por variante).
- Mínimo 600×600px; recomendado **800×800+ em 1:1**.
- Formato **.PNG ou .JPG** apenas.
- Imagem principal: fundo branco/neutro, sem logos/texto/sticker.
- Secundárias: estilo "lifestyle" elevam CTR.

### 5.2 Variantes e SKUs
- Até **100 SKUs por produto**.
- Variant style 1 obrigatório; style 2 opcional (cor + tamanho).
- Bulk upload: **Seller Center → Products → Bulk Listing** (template Excel/CSV).

### 5.3 Integrações ERP/Plataforma
- **Shopify** — canal nativo "TikTok" (mais robusto).
- **WooCommerce** — plugin oficial + M2E Cloud para multi-store.
- **VTEX** — app oficial "TikTok on VTEX" no App Center (sincroniza catálogo + pixels).
- **Magento, BigCommerce, Wix** — apps via TikTok App Store.
- **Brasil — Bling, Tiny, Olist** — não há app oficial direto. Usar middleware (**Anymarket, Skyhub, Hub2b**) para conectar ERP ao TikTok Shop API.
- **Enterprise:** Pipe17, CedCommerce, ChannelEngine, Salesforce Commerce Cloud.

---

## 6. Promoções, Cupons e Mega Sales

- **Flash Sales:** até 60–85% off, countdown, drop diário.
- **Free Shipping:** cupons plataforma (subsidiados) + seller; combinable.
- **Vouchers stackable:** Platform + Shop + Live podem ser usados juntos.
- **Smart Promotion Program:** TikTok co-financia descontos / frete / bônus.
- **Calendar 2026:** 6.6, 7.7, 8.8, 9.9, 10.10, 11.11, 12.12.
- **Brand Day** dedicado pode gerar resultados absurdos (Crocs Croctober 2024: **US$ 1 mi em vendas, +28.300% em live sales**).
- BR: subsídio de frete até **R$ <USER_AMOUNT>/pedido**, cupons de boas-vindas a novos compradores.

---

## 7. TikTok Shop Affiliate

### 7.1 Modelos
- **Open Plan:** todos creators aprovados; comissão **10–15%** (10–12% para testar fit). CVR médio 2–4%.
- **Target Plan:** convite específico; comissão **18–30%** (até 50% para top performers). CVR 8–12%.

### 7.2 Ferramentas para creators
- Elegibilidade típica: ≥1.000 seguidores + idade legal + país habilitado.
- **Product Marketplace** dentro do Creator Tools (lista Open/Target).
- **Showcase tab** (vitrine no perfil — sacolinha azul).
- **Storefront** (vitrine do seller na Shop Tab).
- **TAP (TikTok Affiliate Partner) / Affiliate Plaza:** programa para agências gerenciarem dezenas/centenas de creators em escala (talent, sampling, payout tracking). Docs em `partner.tiktokshop.com`.

### 7.3 Métricas a monitorar
- Sample request rate, Creator activation rate, GMV per creator, CPA por afiliado, Halo organic.
- Comissão efetiva média 2026 (creator + boost): ~26,6% (Dashboardly).

### 7.4 Setup recomendado para agência
- Open Plan 10–12% para volume.
- Target Plan 18–25% para top 20–30 creators de nicho.
- Mínimo **50 creators ativos no mês 3** para o flywheel arrancar.

---

## 8. LIVE Shopping

### 8.1 Métricas-chave
- **GPM (GMV per Mille)** = GMV / (viewers/1000).
- **GMV/min**, **viewer retention curve**, CTR sacolinha, ATC rate, checkout CVR, AOV ao vivo.

### 8.2 Operacional
- Duração ≥ 3h; **8h+ vê salto exponencial** (TikTok Ads docs).
- Cadência diária no mesmo horário cria audiência fiel.
- Roteiro em blocos de 15–20 min: intro → drop oferta → demo → CTA → repete.
- Co-host: brand host (expertise) + creator (credibilidade).
- 30–80 SKUs por live (evita sold-out e mantém dinâmica).
- Cupons exclusivos com timer 60–120s elevam GPM em **30–50%**.
- Setup baseline: iluminação 5500K + áudio profissional + 2 câmeras.

### 8.3 Programas
- "Live Hosting Agency" em US/UK/BR.
- Creator Match dentro do Seller Center.

### 8.4 Live Shop assistida por IA

Para prototipar ativos de live com IA, aplicar `./references/live-shop-ia-controlado.md`. O playbook exige validacao de produto, direitos, politica vigente e ambiente de pratica antes de qualquer publicacao.

---

## 9. TikTok Shop Ads (GMV Max)

### 9.1 Migração
- **Antes (até jul/2025):** VSA, PSA, LSA separados.
- **Desde jul/2025:** consolidado em **GMV Max** — único campaign type para Shop Ads novos (em mercados ativos).

### 9.2 GMV Max
- **Product GMV Max:** automatiza criativos (orgânicos + ads + affiliate), placements (For You, Search, Shop Tab, Pangle) e bidding. Mede GMV total (pago + orgânico) incremental.
- **LIVE GMV Max:** otimiza tráfego de live room para maximizar GMV da sessão.
- **Disponibilidade:** US + sudeste asiático; UK/Europa em rollout; Brasil ainda em modelo legacy em 2026.
- **Auto-creative** via Symphony + assets do seller.
- **Mensuração:** TikTok roda lift studies internos.

### 9.3 Best practices
- ≥ 50–70 criativos no pool.
- 5–10 novos vídeos/dia.
- Min daily budget: **3–5× CPA-alvo** para acelerar learning.
- Target ROAS mínimo evita cauda de spend sem retorno.
- Catálogo: ≥ 50% dos SKUs com 4+ estrelas e 5+ reviews.

### 9.4 Legacy (ainda relevante em BR)
- VSA — vídeo + tag de produto.
- PSA — card de produto puro (sem vídeo).
- LSA — booster de live ativa.

---

## 10. TikTok Shop Open API

### 10.1 Auth
- OAuth 2.0:
  1. Seller autoriza app em URL com `app_key` + `scopes`.
  2. Troca `auth_code` → `access_token` (≈7 dias) + `refresh_token` (30 dias) + `shop_cipher`.
  3. Requests subsequentes enviam `access_token` no header + `shop_cipher` em param.

### 10.2 Endpoint families
- **Product API** — CRUD produtos, variantes, preço, estoque.
- **Order API** — listar, detalhe, atualizar status, filtros.
- **Logistics/Fulfillment API** — shipment, label, tracking, cancel.
- **Finance API** — statement, transactions, payouts, reservas.
- **Customer Service API** — mensagens, response stats, tickets.
- **Promotion API** — flash sales, coupons, vouchers via API.
- **Affiliate API** — collaborations, comissões pagas, performance por creator.
- **Webhooks** — order_status_change, product_change, settlement, return/refund (real-time).

### 10.3 Limites
- Rate limit: até **10 QPS** em endpoints sensíveis; **600 reqs/min** comum; alguns **1.000 reqs/dia**.
- HTTP 429 quando excede (sliding 1 min).
- SDKs oficiais: Python e Node.js.
- Sandbox disponível.

### 10.4 Casos de uso BI (recomendados)
- Pull orders → BigQuery/Snowflake → dashboard GMV/AOV/take-rate **real**.
- Finance API → reconcilia orders × payouts × ad spend; expõe fees não óbvias.
- Affiliate API → dashboard de contribuição por creator.
- Webhook product_change → alerta de stock-out.
- Multichannel: TikTok Shop + Shopify + ML + Shopee em camada única.

---

## 11. Compliance

### 11.1 Proibidos (resumo)
Armas/munição/réplicas, drogas, esteroides, fat burners/detox, conteúdo adulto, animais vivos, tabaco, vape, álcool (varia país), CITES, moeda física, NFTs/cripto, conteúdo político.

### 11.2 Restricted (precisa aprovação)
Suplementos, vitaminas, cosméticos sensíveis, drones, lasers, scooters, automotivos, fashion com IP, produtos infantis (CPSIA).

### 11.3 IP / Anti-counterfeit
Política rigorosa. Brand Registry interno dispara takedowns. Não usar logo/marca/imagem de terceiros em listing, live, vídeo ou shop name sem autorização.

### 11.4 Returns/Refunds
Janela padrão 30 dias após entrega. Refund-only auto-aprovado se shop foi desativado. Buyer protection pode reembolsar buyer e deduzir do seller mesmo após payout (reserva existe para isso).

### 11.5 Shop Performance Score (SPS) 0–5
6 métricas compõem o SPS:
- 12-Hour Response Rate (virou principal a partir de 15/ago/2025; antes era 24h).
- IM Dissatisfaction Rate.
- Non-Buyer Fault Return Rate.
- Seller Fault Cancellation Rate.
- On-Time Delivery Rate (OTDR).
- After-Sales Handling Time.
- Negative Review Rate.

### 11.6 Penalty Points
Acumulativo, **reset a cada 90 dias** se não estourar threshold:
- 12 pts → suspensão de novos listings 7 dias.
- 24 pts → 14 dias.
- 36 pts → 28 dias.
- 48 pts → **suspensão permanente**.
- Violações graves (contrafação, IP) podem dar 48 pts em uma única ocorrência.
- 2 appeals por violação; primeiro em até 30 dias.

---

## 12. Benchmarks Públicos Citáveis

- **Conversion rate:** TikTok Shop **4,7%** > Instagram Shopping 2,1% > Facebook Shops 1,8% > média global 1,9%.
- **Crescimento US H1/2025:** +120% YoY. Sellers com GMV anual >US$ 30 mi cresceram **+95% YoY**.
- **Beleza é #1 nos EUA:** US$ 2,49 bi em 2025 (22,5% do GMV total US).
- **Virtual Try-On (lançado out/2025):** −31% return rate apparel, +27% conversion.
- **Live commerce sessions H1/2026:** +340% YoY (eMarketer).
- **Symphony Creative Studio:** American Eagle +60% ROAS com Showcase Products; redução média de 70% no tempo de produção criativa.

---

## 13. Diferença vs Concorrentes (BR)

| Dimensão | TikTok Shop | Shopee | ML | Amazon BR | Instagram |
|---|---|---|---|---|---|
| Comissão base BR | 5–10% | 0–15% | 10–20% | 7–45% + assinatura + FBA | Sem comissão (checkout fora) |
| Descoberta | Feed algorítmico (push) | Search + recomm. | Search + ad | Search | Follower-driven |
| CVR | **4,7%** | 2–3% | 2–3% | 10–15% (high intent) | 2,1% |
| Live commerce | **Nativo e principal** | Forte | Em expansão | ~0 | Limitado |
| Checkout in-app | **Sim** | Sim | Sim | Sim | Não desde ago/2025 |
| Fulfillment próprio | FBT (US/UK) | Shopee Express | Mercado Envios | FBA | — |

**Tese estratégica:** TikTok Shop captura **demanda gerada** (discovery + impulse). ML/Amazon retêm **demanda capturada** (consideration + repeat). São canais complementares.

---

## 14. Recomendações operacionais para agência

1. **Auditoria pré-cadastro:** validar CNPJ + categoria do cliente vs lista de proibidos/restritos antes de prometer entrada.
2. **Stack BI mínima:** TikTok Shop Open API → ETL (Airbyte/Fivetran/middleware) → DW (BigQuery/Snowflake) → Looker/Metabase. Finance API expõe take-rate real.
3. **Affiliate setup padrão:** Open 10–12% (volume) + Target 18–25% (top 20–30 creators de nicho). Meta: 50 creators ativos no mês 3.
4. **Live cadence (mês 1):** 4–6 lives/semana de 3h+; depois consolidar 2 horários "anchor" diários.
5. **Ad budget split inicial:** 60% GMV Max + 40% TopView/Spark Ads; migrar para 80%+ GMV Max conforme ROAS estabiliza.
6. **Compliance mensal:** monitorar SPS, response <12h, late dispatch, penalty pts. Documentar autorizações de IP/marca de tudo revendido.
7. **Para B2C nacional:** TikTok Shop BR **complementa** ML/Shopee, não substitui.

---

## 15. Recursos relacionados
- **tiktok-ads-fundamentals** — para campanhas dentro e fora da Shop.
- **tiktok-creative-playbook** — para vídeos que vendem.
- **tiktok-bi-metrics** — para dashboards e attribution.
- **tiktok-tracking-setup** — para Pixel/CAPI.
- **references/live-shop-ia-controlado.md** — prototipagem controlada de Live Shop assistida por IA.

## Fontes
Lista detalhada em `./references/sources.md`.
