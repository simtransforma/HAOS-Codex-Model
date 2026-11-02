---
name: tiktok-ads-fundamentals
description: "TikTok Ads Manager 2026 \u2014 Business Center + Ad Account, hierarquia Campaign/AdGroup/Ad, budget m\u00ednimos, partner access e roles. Objetivos (Reach, Traffic, Video Views, Community, Lead, App, Sales, Smart+, GMV Max), bidding (Max Delivery, Cost Cap, Bid Cap, VBO/Min ROAS), targeting (interests, behaviors, custom audiences, lookalikes), Marketing API, attribution, SKAN 4.0, Spark Ads, TTCM, pol\u00edticas BR (CONAR/ANVISA/SPA/MF/BCB/CVM/SUSEP), benchmarks BR e global, comparativo com Meta. Use sempre que precisar estruturar conta, escolher objetivo/bidding, planejar or\u00e7amento, montar split test, integrar via API ou interpretar pol\u00edtica BR."
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

# TikTok Ads Fundamentals — Skill Operacional

Use ao estruturar conta TikTok, escolher objetivo/bidding, planejar orçamento, montar split test, integrar Marketing API ou interpretar política BR.

---

## 1. Estrutura de conta

### 1.1 Hierarquia
- **Business Center (BC)** — control tower; gerencia múltiplos Ad Accounts, pixels, catálogos, audiências, Partner Access, finanças. **Não compra mídia direto.**
- **Ad Account** — moeda, fuso e país **FIXOS** na criação (atenção ao abrir conta BR em BRL).
- Dentro do Ad Account: **Campaign → Ad Group → Ad**.
  - Campaign: objetivo + CBO opcional.
  - Ad Group: audiência, placements, schedule, optimization event, bidding, ABO.
  - Ad: criativo (vídeo/imagem/Spark post), copy, CTA, display name, LP/Deeplink, pixel.

### 1.2 Budget mínimos (2026)
- Campanha: **USD 50/dia** (equivalente local).
- Ad Group: **USD 20/dia** ou **USD 700 lifetime**.
- Em BRL: conversão pela tabela TikTok no momento; abaixo do piso trava entrega.

### 1.3 Múltiplos BCs e Partner Access
- Agência opera vários BCs (1 por cliente, ou BC central + Partner Access).
- **Partner Access** é o caminho preferido: cliente adiciona BC da agência como parceiro e atribui assets. Time da agência herda acesso, sem invite individual.

### 1.4 Roles
**BC-level**: Admin · Standard Member · Finance Manager · Finance Analyst.

**Asset-level (Ad Account)**: Admin · Operator · Analyst.

**Business Account (perfil orgânico)**: Admin · Operator.

Práticas: **Operator** → time de tráfego; **Analyst** → stakeholders read-only; **Admin** apenas 1–2 leads.

---

## 2. Objetivos de campanha 2026

Três blocos: **Awareness → Consideration → Conversion** + variantes automatizadas (Smart+ / GMV Max).

### 2.1 Awareness
- **Reach** — maximizar usuários únicos a menor CPM. Topo de funil + brand awareness.

### 2.2 Consideration
- **Traffic** — cliques / LPV / IC. E-commerce BR early-stage usar **LPV** para limpar tráfego.
- **Video Views** — 2s, 6s, 15s/100%. CPM cai forte. Audiência de re-engajamento.
- **Community Interaction** — seguidores, visitas, **LIVE viewers**.

### 2.3 Conversion
- **Lead Generation** — Instant Form (in-app) ou Website Form.
- **App Promotion** — install (AIO) ou App Event Optimization (AEO). iOS: MMP + SKAN 4.0.
- **Sales** (consolidado 2025–2026; absorveu Website Conversions e Product Sales). Fontes: Website (pixel + CAPI), App (MMP), Website+App, **TikTok Shop = GMV Max apenas** desde jul/2025.

### 2.4 Eventos de otimização
Prioridade alta (sinal forte): **Purchase / CompleteRegistration / Lead**.
Mid-funnel (fallback): AddToCart, InitiateCheckout, ViewContent, AddPaymentInfo, ClickButton, Subscribe.

### 2.5 Learning Phase
- Aplicada **no Ad Group**.
- Termina em **50 eventos de otimização em 7 dias**.
- Edições estruturais resetam.
- Volatilidade CPA cai por volta de 25 conv.; estabiliza em 50.
- TikTok recomenda budget diário **≥ 20× CPA-alvo**.

---

## 3. Smart+ (campanhas automatizadas)

Resposta TikTok ao Advantage+ do Meta. Pacote ponta-a-ponta — targeting, criativos, lance, placement.

### 3.1 Como funciona
- Você dá KPI (evento + custo/ROAS-alvo), criativos, geo, idioma. Algoritmo cuida do resto.
- Cobre **Sales (Web/App/Catalog), Lead Generation, App Promotion, Traffic**.
- Limites: **30 ad groups/campanha · 30 asset groups/ad group · 50 criativos/asset group**.

### 3.2 Ativos esperados
- **Mín. 6 criativos**; diversidade > volume bruto (hooks/ângulos/formatos variados).
- Vertical 9:16, 1080×1920; durações variadas (15s impacto, 30–60s storytelling).
- Audiências amplas; segmentação estreita desencorajada.
- Pixel + CAPI verificados; target CPA/ROAS realista.

### 3.3 Smart+ Web Campaign
- Conversão em site (não-Shop).
- Pixel + CAPI + Events Manager bem cabeçados.
- Catalog dentro de Smart+ exige **≥ 4 SKUs aprovados in-stock**.
- Pode pinar até **20 produtos**; adicionar até **30 vídeos/imagens** suplementares ao feed.

### 3.4 Smart+ App Campaign
- Install OU App Event.
- iOS via SKAN + MMP modeled; Android via SDK.
- Budget diário **≥ 20× CPA-alvo histórico**.

### 3.5 Quando NÃO usar
- Volume <50 conv./semana (algoritmo não calibra).
- Restrição forte de público (B2B nichado, geo hipersegmentado).
- Early-stage de creative testing (split manual é mais limpo).
- Verticais regulados (saúde/finance) com risco de algoritmo achar audiência fora do compliance.
- CPA-alvo agressivo + budget < 20× target (entrega volume inflado com CPA descalibrado).

### 3.6 Smart+ Upgraded Experience (2026)
- Dial entre "Max Conversions" e "Max Value", asset groups com signals criativos, auto-selected creatives a partir do feed orgânico/UGC autorizado.

---

## 4. GMV Max (TikTok Shop) — único Sales-objective para Shop desde jul/2025

### 4.1 O que é
Automação total para sellers de TikTok Shop. Roda **paid + orgânico do seller + posts de afiliados + lives** num pool único otimizado para **GMV incremental total**.

### 4.2 Variantes
- **Product GMV Max** — SKUs (catálogo).
- **Live GMV Max** — boost de live em real-time.

### 4.3 Setup
1. Sales com source=TikTok Shop.
2. Products ou LIVE.
3. SKUs ou live ativa.
4. **ROI-alvo (target ROAS)** + budget diário (recomendado USD 50–100/dia para testar).
5. Anexar todos os assets (orgânicos, UGC, posts afiliados via TTCM).
6. Rodar **2–3 semanas** antes de adicionar constraints.

### 4.4 ROAS / GPM
- **Break-even ROAS** = 1 / margem após referral (6% padrão BR).
- Target ROAS 10–15% acima do break-even nas 2 primeiras semanas; depois apertar.
- Após 50+ conversões: 3:1 ROAS é guideline geral.

### 4.5 Attribution GMV Max
- Conta vendas atribuídas a **qualquer** vídeo orgânico, paid ou afiliado dentro da janela.
- **Infla ROAS reportado vs last-click puro** — esperado, mas cuidado ao comparar com outras plataformas.
- Internal TikTok: **+20–30% uplift em GMV** em testes iniciais. SMB documentado: USD 6K spend → USD 45K vendas (7.5×).

### 4.6 Troubleshooting
- Baixa entrega → ROI-alvo agressivo demais; relaxar 20–30%, 72h.
- GMV alto + margem negativa → break-even mal calculado.
- Criativos não rotacionam → falta de assets; 6–10 vídeos novos/semana.
- Affiliate posts não aparecem → checar TikTok Shop Affiliate Center.

---

## 5. Bidding strategies

| Estratégia | Input | Quando usar |
|---|---|---|
| **Max Delivery** (Lowest Cost) | Só budget | Scale, prospecting, learning inicial |
| **Cost Cap** | Target CPA | Manter eficiência pós-learning |
| **Bid Cap** | Bid máximo | Travar custo absoluto |
| **VBO Highest Value** | – | E-commerce alto AOV; após 50+ purchases |
| **VBO Min ROAS** | Target ROAS | E-commerce maduro |

### Notas
- Bid Cap travado demais = sem entrega.
- VBO exige `value` em todos os eventos via pixel + CAPI.
- Migrar Max Delivery → Cost Cap após 50 conv.; VBO/Min ROAS após 100+ purchases.

---

## 6. Targeting

### 6.1 Demographics
- Idade: **13-17, 18-24, 25-34, 35-44, 45-54, 55+** (6 brackets).
- Gênero: Male / Female / Aberto.
- Localização: país/estado/cidade/DMA. No BR, granularidade estadual + algumas capitais.
- Idioma do app.
- Household income / spending power: **apenas US**.

### 6.2 Interest & Behavior
1. **Interest Categories** — afinidade longo prazo.
2. **Purchase Intention** — usuários considerando categoria.
3. **Video Interactions** — interações nos **últimos 7 ou 15 dias**.
4. **Creator Interactions** — followers / visits.
5. **Hashtag Interactions** — interagiram com hashtag nos **últimos 7 dias**.

### 6.3 Custom Audiences (CA)
Tipos: Customer File · Engagement · App Activity · Website Traffic · Lead Gen · Shop Activity · Business Account · Challenge · Premium Audience.

**Requisitos**:
- Mínimo **1.000 usuários matched** para ativar.
- Limite **400 CAs por Ad Account**.

### 6.4 Lookalike
- Seed mínima 1.000 usuários.
- 1% (semelhante) a 10% (amplo).
- Rodar **1%, 5% e 10% em ad groups separados**.

### 6.5 Exclusions + Automated Targeting
- Excluir compradores recentes, leads fechados.
- Automated Targeting: algoritmo escolhe o público — default em Smart+, opcional em manual. Bom para cold-start.

---

## 7. Pixel / Events API / Events Manager

Detalhes operacionais completos em **tiktok-tracking-setup**. Resumo:

- Pixel client-side: `events.js` carrega `window.ttq`; `ttq.page()` no head; `ttq.track(eventName, params, {event_id})`.
- CAPI: `POST https://business-api.tiktok.com/open_api/v1.3/event/track/` — batch até 50 eventos, payload até 1 MB. Header `Access-Token`.
- **Rodar Pixel + CAPI em paralelo** com mesmo `event_id` → dedupe.
- Eventos prioritários: **Purchase / Lead / CompleteRegistration** (sinal forte).
- Advanced Matching automático + manual.
- **EMQ ≥ 8** = match excelente; correlaciona com melhor atribuição.

---

## 8. Attribution

### 8.1 Janelas
- **Default**: 7d click + 1d view (CTR/Sales/Conv).
- Custom Click: 1, 7, 14, 28d.
- Custom View: 1, 7d.
- **LIVE Shopping Ads**: 7d click + 1d view + **30-min click**.

### 8.2 Click-only undervalues TikTok
- Pesquisa TikTok interna: **79% das conversões somem em last-click**.
- TransUnion 2024: TikTok gera **iROAS 2.35× maior** que o reportado.
- **52% das conversões incrementais TikTok são exclusivas**.

### 8.3 Reported vs Modeled
- iOS app: parte modelada via SKAN.
- TikTok reporta modeled separado.

### 8.4 Attribution Manager / Performance Comparison
- Compara janelas (1d/7d/14d/28d click) sem refazer campanhas.
- Use para escolher janela de relatório a stakeholders.

### 8.5 Conversion Lift Study (CLS) — nativo
- Test/control aleatorizado em **nível de usuário**.
- iROAS, CPIC, relative lift %, incremental conversions.
- Requer spend ~USD 30k+/mês na vertical, duração 14–30d.
- Solicitar via account manager.

---

## 9. Formatos & specs

| Formato | Aspect | Resolução | Duração ideal | Outras |
|---|---|---|---|---|
| **In-Feed** | 9:16 (rec.) | 1080×1920 (mín 540×960) | 9–15s sweet spot; até 10 min | .mp4/.mov/.mpeg/.3gp/.avi; ≤500 MB; ≥516 kbps; caption até 2.200 chars |
| **Spark Ads** | herda do original | herda | até 10 min | Boost de orgânico; **CTR 2.4× / CVR 1.4× vs in-feed** |
| **TopView** | 9:16 obrigatório | – | 5–60s (9–15s rec.) | Som ON nativo; **CTR ~16,4%**; via rep TikTok |
| **Brand Takeover** | 9:16/1:1/16:9 | – | 3–5s sem skip | 1 brand takeover/usuário/dia |
| **Branded Hashtag Challenge** | 9:16 | 720×1280 rec. | até 60s (21–34s rec.) | Campanha 6d padrão; eng. rate médio 8,5% |
| **Branded Effects** | – | logo 150×130 / cover 800×800 / hint ≤48 chars | – | AR filter / sticker / 3D |
| **Carousel** | 1:1 | 1080×1080 .jpg/.png | – | 2–35 imagens swipeable |
| **VSA (legado)** | 9:16 pref. | 720×1280 mín | 5–16s rec. | Substituído por GMV Max em mercados Shop |
| **LIVE Shopping Ads** | – | – | – | 7d/1d/**30-min click**; migrado para Live GMV Max |

**Branded Content Tag** obrigatória em conteúdo orgânico promocional.

---

## 10. Spark Ads — operação

### Por quê
- Mantém likes/comments/shares/follows.
- Clicar no @ leva ao **perfil real**.
- Aproveita UGC e creators.
- TikTok promove melhor.
- **2.4× CTR · 1.4× CVR · +132% completion rate** vs padrão.

### Autorização por Spark Code (creator → brand)
1. Vídeo → ⋯ → Ad Settings → toggle Ad authorization.
2. Duração: 30 / 60 / 365 dias.
3. **Generate code** → Copy → enviar ao advertiser.

### Importar no Ads Manager
- Criação de ad → aba "TikTok Posts" → "Authorize new post" → cola o code.
- **Batch authorization até 20 codes** de uma vez.
- Posts da própria conta business: autorização direta sem code.

### Best practices
- Code via canal escrito.
- 365d se "evergreen".
- Não editar o vídeo orgânico enquanto ad ativo (invalida code).

---

## 11. TikTok Creator Marketplace (TTCM) / TikTok One

### Discovery
Filtros: localização, categoria, faixa de followers, views médias, eng. rate, demographics da audiência. Brasil tem ampla base ativa.

### Brief & contratação
Brief estruturado: objetivos, deliverables, prazos, talking points, do's/don'ts. Creator aceita/recusa/contrapropõe.

### Pagamento
**TTCM Pay** escrow — brand funda saldo, TikTok segura até aprovação, libera ao creator. Reduz fraude em parcerias first-time.

### Boost para ad
Conteúdo entregue pode ser convertido em Spark Ad **diretamente no TTCM**, sem precisar Spark Code manual.

---

## 12. Testing framework

### Split Testing nativo
- Tools → Split Testing.
- Confidence default **90%** (algumas versões 95%).
- Variáveis: Audience · Creative · Placement · Optimization Goal · Bidding · Bid Amount.

### Cadência iterativa
1. **Hook test** primeiro (3s define 71% da continuidade).
2. Lock hook → **CTA/copy test**.
3. Lock CTA → **audience test**.
4. Repete trimestralmente.

Case documentado: DTC com essa cadência por 3 meses → **+47% ROAS**.

### Duração e budget
- 7–14 dias mínimos.
- USD 50–200/dia por variante.
- ≥ 50 conv./variante para fechar.
- Não pausar/editar variantes durante o teste.

### Asset volume
- 5–10 vídeos novos/semana.
- "Creative wheel" 3×3×2 = 18 combinações.
- Aproveitar UGC + Spark Ads para diversidade.

---

## 13. iOS 14+ / SKAN 4.0

- 3 janelas: **0–2d, 3–7d, 8–35d**.
- 3 postbacks por install com conversion values distintos.
- Coarse (low/medium/high) + fine (0–63).
- Postback delay: até 24h–4d.

### Campanhas iOS Dedicated
- Mais de 1 ad group → conversions SKAN são **modeled no nível do ad group**.
- Limite histórico: **9 campanhas iOS dedicadas** simultâneas (SKAN 3.0); SKAN 4.0 relaxa parcialmente.

### MMP real-time
- Adjust, AppsFlyer, Branch, Kochava entregam modeled conversions muito mais cedo que SKAN puro.
- Branch: **PAM capta 26% das conversões iOS** vs <1% via SKAN puro = **+2.900%** mensurável.

### Recomendações
- AEO só após VO/Install maduros (50+ conv./semana).
- Não fragmentar muito ad groups em iOS Dedicated.
- CAPI server-side via MMP.
- Pixel web complementar (cross-device modeling).

---

## 14. Reporting

### Métricas-chave
Impressions · Reach · CPM · CPC · CTR · CVR · CPA/CPL/CPI · ROAS · Video Views (2s/6s/15s/100%) · VVR · **6s Focused View (Hold Rate)** · Engagement Rate · Avg Watch Time · **GMV** · **GPM**.

### Breakdowns
Age · Gender · Country/Region · Placement · Device · OS · Network · Time-of-day · Day-of-week · Creative.

### Custom Reports
- Reporting → Custom Reports.
- Salvar templates, agendar email diário/semanal/mensal.
- Export CSV/XLSX.

### Reports API
- `POST /open_api/v1.3/reports/integrated/get/` — sync (até 100K rows) ou async.
- Granularidade até hora; janela retroativa varia por métrica.

---

## 15. Marketing API

### Overview
Replica Ads Manager em escala. Famílias:
- Identity & Auth (OAuth, BC, advertiser).
- Campaign Management (CRUD Campaign/AdGroup/Ad, status, budgets).
- Audience Management (CRUD CAs, LAL, file upload SHA-256).
- Creative Asset (upload vídeos/imagens, dynamic creative).
- Pixel & Events (CAPI inclusive).
- Catalog (CRUD, feeds).
- Reporting (Sync/Async).
- Tools (Bid Recommendation, Audience Reach, Asset Library).

### Auth
- App em `business-api.tiktok.com/portal`.
- `/oauth2/auth/` → `/oauth2/access_token/`.
- Access token TTL geralmente **24h**; refresh longer.

### Sandbox vs Production
- Sandbox: `https://sandbox-ads.tiktok.com/open_api`.
- Production: `https://business-api.tiktok.com/open_api`.
- Sandbox tokens NÃO funcionam em produção.

### Rate limits
- Sliding window 1 min.
- HTTP 429 → `rate_limit_exceeded`.
- Reporting mais restritivo. Contatar TikTok p/ upgrade.

### SDKs oficiais
Python, Java, Go: github.com/tiktok/tiktok-business-api-sdk. PyPI: `TikTok-Business-API`.

### Versão atual: **v1.3**.

### App review
Após dev em sandbox: 7–14 dias típicos. Functional + data-security + use-case + business verification.

---

## 16. Políticas BR

### Proibido em ads BR
- **Política / political ads**.
- Tabaco, vape, e-cigarettes, drogas ilícitas.
- Armas, munição, explosivos.
- Conteúdo adulto/porn.
- Pirâmide / MLM agressivo.
- Cripto altamente especulativa sem licença local.

### Restritos (whitelist/aprovação)
- **Apostas esportivas**: via TikTok rep + verificação SPA/MF (Lei 14.790/2023 regulou em BR).
- **Social casino / F2P**: sem cash-out real.
- **Saúde/farmacêutico**:
  - OTC: permitido seguindo ANVISA.
  - **Prescrição: proibido**.
  - Suplementos: claims permitidos ("supports healthy metabolism" OK; "queima gordura em 7 dias" → rejeição).
  - Estética: restrições altas; before/after geralmente proibido.
- **Financeiro**:
  - Bancos/fintechs licenciados BCB, corretoras CVM, seguradoras SUSEP: permitidos com verificação.
  - Crédito consignado/predatório/negativados: claims agressivos vetados.
  - Educação financeira: sem garantia de retorno.
- **Bebidas alcoólicas**: 21+ (gate obrigatório), sem incentivo a consumo excessivo, sem dirigir.

### Branded Content Policy
Toggle "Branded Content" obrigatório em conteúdo pago. Spark herda.

### Appeals
- Hover no status → View more → **Appeal**.
- Texto até 2.000 chars, anexar até 5 arquivos (10 MB cada).
- Review típico 24–48h; regulados 2–3 dias úteis.
- **One Click Appeal** por ad group; depois é "Contact Customer Service".

### Disclaimers BR
- Age gate para álcool e apostas.
- Health claims com disclaimer ANVISA.
- Promoções: CNPJ promotor + SUSEP/Caixa se sorteio aleatório (Lei 5.768/71).

---

## 17. Benchmarks 2026

### Global cross-industry (médias)
| Métrica | Valor |
|---|---|
| CPM In-feed | USD 4,80–9,16 |
| CPM TopView | USD 14,20 |
| CPM Spark | USD 11,85 |
| CPC In-feed | USD 1,02 |
| CTR In-feed | 1,0% |
| CTR Spark | 2,4% |
| CTR TopView | 16,4% |
| CTR Branded Hashtag | 8,5% |
| CVR In-feed | 1,8% |
| CVR Spark | 2,6% |
| CVR TikTok Shop product ads | 3,7% |

### Por vertical (global)
| Vertical | CPM | CPC | CTR | CVR |
|---|---|---|---|---|
| Retail/e-commerce | 4–6 | 0,60–0,90 | 0,8–1,0% | 1,8–2,4% |
| Apparel | 4,24 | – | 0,69% | 2,37% |
| Home & Garden | – | – | 0,68% | **2,42%** |
| Toys/Art | – | – | – | 2,38% |
| Electronics | – | – | **0,73%** | – |
| Beauty | – | 0,74 | – | – |
| Finance/SaaS | 11+ | 1,50–3,00 | 0,4–0,7% | 0,8–1,5% |
| Lead Gen B2B | 5–12 | 1,50–3,00 | – | – |
| Sports/Outdoors | 3,79 | – | – | – |

### Brasil (Tier 3 LATAM)
- TikTok BR: ~**100M MAU**.
- CPM BR: **USD 1,00–3,00** típicos; algumas leituras Meta ~USD 4,20 como referência.
- CPC BR e-commerce: **R$ <USER_AMOUNT>–1,50**.
- CPA BR:
  - E-commerce DTC: **R$ <USER_AMOUNT>–80** (depende ticket).
  - Lead B2C (educação/finance/saúde): **R$ <USER_AMOUNT>–35**.
  - Lead B2B/SaaS: **R$ <USER_AMOUNT>–200**.
  - App install: **R$ <USER_AMOUNT>–15** (vertical-dependente).
- Bot traffic Tier 3: **20–30% low-quality**; mitigar com filtros placement, pixel validation, exclude low-quality network audiences.

### Sazonalidade
- Q4 (BFCM, Natal): CPM **+40–60%**.
- Jan-Fev: menor custo do ano.
- Carnaval: queda regional de atenção.
- Dia das Mães/Crianças/Pais/Black Friday BR: spikes regionais.
- Q1 2026 ad spend global TikTok: **+32% YoY** (USD 5,8 bi/trimestre).

---

## 18. TikTok vs Meta (BR/Global)

| Métrica | TikTok | Meta |
|---|---|---|
| CPM | USD 3–10 | USD 6–15 |
| CPC | USD 0,50–1,50 | USD 3–5 |
| CTR | 1,0–2,4% | 0,9–1,5% |
| CVR | 1,8–3,7% | 1,5–3% |
| iROAS reportado | 2,35× last-click (TransUnion) | subreportado ~94% |

**TikTok entrega CPM ~47% menor que Meta** em média global; Meta tem signals mais densos e attribution mais madura no BR.

### Onde TikTok ganha
- CPM/CPC menor.
- Gen Z + Millennials jovens.
- Creative virality / UGC autêntico.
- "Demand creation" topo-funil.
- TikTok Shop / live commerce.
- CTR superior + **2.4× CTR Spark Ads**.

### Onde Meta ganha
- Attribution mais madura (CAPI consolidada, MMM robusto).
- Audiência 35+ com poder de compra.
- Buyer intent capture (LAL mais precisos, dataset maior).
- B2B/SaaS.
- Catalog/DABA mais maduros para retargeting.

### Mix recomendado BR
- DTC e-commerce ticket baixo-médio: **60% TT + 40% Meta** se há creator content forte.
- DTC ticket alto/luxury: **70% Meta + 30% TT**.
- Lead Gen B2C jovem: **50/50** (TT prospect, Meta retarget).
- B2B/SaaS BR: **10–20% TT** apenas; resto Meta + LinkedIn + Google.
- App install jogos/social/finance: **40–60% TT**.

### Sinergia operacional
- TT cria demanda → Meta retargeta engajados.
- Vídeos winners TT funcionam no Instagram Reels.
- Pixel paralelo: TikTok + Meta + GA4 + MMP.
- **Não usar last-click para split de orçamento** — usar MMM ou CLS.

---

## 19. Checklist onboarding cliente

1. BC da agência + Partner Access do cliente.
2. Ad Account moeda BRL + fuso BRT.
3. Pixel + CAPI (dedupe via `event_id`).
4. 6+ standard events priorizando Purchase/Lead.
5. Advanced Matching automático + manual.
6. **EMQ > 7** antes de escalar.
7. Catálogo (≥4 SKUs) se Shop/e-commerce.
8. Seed CAs: Customer File + All Visitors 180d + Engagement 365d.
9. LALs 1%/5%/10% para cold prospecting.
10. Estrutura inicial: 1 Smart+ scale + 1 manual para hook test.
11. Bidding: Max Delivery → Cost Cap (50 conv.) → VBO/Min ROAS (100+ purchases).
12. Attribution 7d-click/1d-view; comparar com 28d-click via Performance Comparison.
13. 5–10 vídeos novos/semana.
14. Reporting agendado (CSV + dashboard).
15. Revisar policies BR da vertical ANTES de subir criativo.

---

## Skills relacionadas
- **tiktok-shop-fundamentals** — Shop Ads e GMV Max em contexto Shop.
- **tiktok-creative-playbook** — anatomia + hook + testing.
- **tiktok-tracking-setup** — Pixel/CAPI/EMQ/ttclid.
- **tiktok-bi-metrics** — KPIs, dashboards, MMM.

## Fontes
Lista completa em `./references/sources.md`.
