---
name: cfo-dash-sim
description: "Procedimento especializado de cfo-dash-sim; consultar requisitos e evidencias antes de executar."
---

Skill de LEITURA financeira da DASH SIM MASTER: transforma os números exibidos em uma leitura reconciliada de rentabilidade, com a base de cada valor declarada e as lacunas sinalizadas.

## O que é a DASH SIM MASTER (e o que NÃO é)

- **MASTER (a verdade):** `service.example.invalid`, repo `dashboard-master-sim` (branch `sim-dash-bigdata`), Next.js 14.2 + Prisma + shadcn/ui + NextAuth, container `sim-dash` em `${HAOS_PRIVATE_ROOT}` no Hetzner. O app só LÊ (`prisma.$queryRaw` em `lib/bigdata-*.ts`).
- **Fonte da verdade real:** Big Data SIM no Supabase gerenciado, schemas `raw` / `stg` / `dwh` / `app`. Tabela-fato central: `dwh.fct_venda`. Taxas e regras vivem em SQL versionado (`dwh.dim_payment_rate`, `app.rate_config`), NUNCA hardcoded. Credenciais por nome no MASTER.env (ex.: `SUPABASE_BIGDATA_SIM_DB_URL`, `SUPABASE_BIGDATA_SIM_*`), nunca colar valor.
- **NÃO confundir:** `service.example.invalid` (container `dados-view`) é a dash ESTÁTICA de apresentação. Puxa API crua, SEM reconciliação. Bom para mostrar, NÃO é base de decisão. Se divergir da MASTER, a MASTER ganha.
- **Maturidade auditada:** 58/100. Resumo honesto: "banco confiável, número exibido nem sempre". Por isso esta skill existe, ler sem reconciliar gera erro.

## A regra de ouro do número

`fct_venda.valor` = **BRUTO**. É o KPI oficial de topo HOJE. O líquido ainda NÃO é oficial.

As colunas de decomposição (`valor_bruto`, `taxa_plataforma`, `taxa_gateway`, `imposto_venda`, `valor_liquido` GENERATED) e de proveniência (`valor_kind`, `taxa_*_origem`) estão em **SHADOW RUN**: existem e são calculadas, mas só viram KPI oficial após o **gate G6** (shadow run de 30 dias com erro <= 2%). Então, ao ler a dash hoje, o número de topo é BRUTO. **Declare sempre a base.** Líquido só entra rotulado como "(shadow, não oficial)".

## Fluxo de leitura (siga em ordem; adapte a profundidade à pergunta)

### 1. Fixar fonte da verdade e período
- Confirme que está lendo a MASTER (reconciliada), não a `dados-view`.
- Fixe a janela: D-1, MTD, mês fechado, intervalo. Todo número sai junto com o período.
- Se a pergunta for "quanto faturou", a fonte é `dwh.fct_venda` no Big Data, não o card da tela isolado.

### 2. Declarar a base de cada número
- Topo da dash = **bruto** (`valor`). Diga isso explicitamente.
- Cada plataforma vem numa base diferente. NUNCA some sem normalizar:
  - Assiny e Asaas = **líquido**
  - Yampi e Bling = **bruto**
  - Lia = **caixa ou competência** (ambíguo, confirmar antes)
  - TikTok = **bruto + comissão real** à parte
- Se mostrar líquido, marque "(shadow run, pré-G6, não oficial)".

### 3. Reconciliar e aplicar expurgos
Antes de declarar qualquer total como definitivo, aplique:
- **Yampi:** status pago = `[4, 6]`. Outro status não é receita.
- **Assiny:** já houve expurgo de **R$ 765k de receita falsa**. Confirme que segue expurgado; pico anômalo = suspeitar de reintrodução.
- **PIX gerado contado como pago:** PIX só conta quando liquidado. PIX gerado/aguardando infla Purchase, não é caixa.
- **Dedupe:** Bling espelha Yampi (dedupe remove Yampi cru); Asaas pode ser o gateway por trás de outra plataforma (dedupe por `externalReference`). Some só linha reconciliada (não duplicada).
- **Data Quality:** rode `dwh.fn_dq_checks()` e leia `dwh.dq_log`. Qualquer FAIL que toque receita bloqueia "número definitivo", vira provisório com o check citado.

(Queries prontas de leitura por plataforma/base/expurgo em `references/queries.md`.)

### 4. Ler tela a tela com lente financeira
Use a tabela abaixo. Para cada tela: qual é a leitura de CFO e qual a armadilha.

| Tela (`/dashboard/*`) | O que olhar como CFO | Armadilha |
|---|---|---|
| **Visão Geral** | Receita Bruta D-1/MTD (KPI oficial). Líquida só como sinal. | A "Receita Líquida" é shadow run, pré-G6. NÃO reportar como oficial. |
| **Tráfego** | Investimento, ROAS geral x pago, CPA, CPM, CPC, CTR. | ROAS usa receita bruta no numerador; margem real é menor. TikTok Ads bloqueado e Google parcial: investimento total subestimado. |
| **Campanhas** | ROAS real por campanha Meta. | Selo de cobertura de atribuição ~21% em 30d: ROAS por campanha cobre só uma fração das vendas. Não extrapole para o todo. |
| **Funil** | 5 camadas (Visitantes, Lead, stages Clint, Checkout, Compra). Conversão entre etapas. | Checkout pode inflar por PIX gerado. Compare a base de "Compra" com receita reconciliada, não com Purchase cru. |
| **Cobranças** | Aging 30/60/90, inadimplência, forward book (~R$ 1,08M em 7.954 parcelas até 2030). | Recebível não é caixa realizado. LIA vs Asaas têm bases diferentes; não some forward book com receita reconhecida. |
| **Leads/CRM** | Volume (~319k leads), custo por lead. | Lead não é receita. Métrica de topo de funil, não entra em rentabilidade. |
| **Lead Score** | RFM-E normalizado 0-100 (`mv_lead_score_v2`), concentração de valor. | É score relativo (normalizado), não R$. Não confundir score alto com receita garantida. |
| **Leads de Site** | GA4 generate_lead, origem orgânica. | Base GA4 (eventos), não casa 1:1 com lead do CRM nem com venda. |
| **Presença/Sorteio** | Tags `LP_*` de lives, engajamento. | Presença em live não é conversão; não atribuir receita direto. |
| **Bling** | Estoque, Kits/BOM, NF-e. Catálogo ~92 produtos, valor em estoque ~R$ 89,5k. | Alertas de estoque negativo/baixo/fantasma distorcem o valor em estoque. Trate o fantasma antes de valorizar. |
| **BI** | Gateway (pix 0,79% vs boleto 6,24%, ~7,9x), LTV pago vs orgânico. | Mix de gateway move a margem real; boleto come ~7,9x mais que pix. LTV pago x orgânico muda a leitura de CAC. |

### 5. Entregar a leitura com lacunas sinalizadas
Formato de saída esperado:
- **Período** e **fonte** (MASTER reconciliada).
- **Número de topo** com a **base** ("bruto, KPI oficial").
- **Líquido**, se pedido, sempre como "(shadow, pré-G6, não oficial)".
- **Expurgos aplicados** (Yampi status, Assiny 765k, PIX, dedupe) e o que ficou de fora.
- **Por plataforma**, com a base de cada uma (não somar bases mistas sem normalizar).
- **Lacunas e ressalvas:** DQ em FAIL, cobertura de atribuição ~21%, TikTok Ads bloqueado, Lia ambígua, estoque fantasma, maturidade 58/100.
- Conclusão de rentabilidade com o nível de confiança explícito. Nunca apresentar número reconciliado como certeza se um check relevante falhou.

## Princípios inegociáveis
1. **Declare a base sempre.** Bruto x líquido shadow x caixa x recebível são coisas diferentes. Misturar é o erro número um.
2. **Bruto é o oficial hoje.** Líquido só com selo de shadow até G6.
3. **Reconcilie antes de afirmar.** Expurgos e dedupe antes de qualquer total definitivo.
4. **A MASTER ganha da dados-view.** Snapshot de apresentação não é base de decisão.
5. **Não fabricar.** Sem o dado reconciliado, diga que é provisório e cite a lacuna. Maturidade 58/100 é motivo para humildade no número.
6. **Taxa vem da dimensão**, nunca hardcoded. Origem da taxa (`taxa_*_origem`) separa medido de estimado.

## Referências do repo (citar quando relevante)
- `${USER_PROJECT_ROOT}/docs/AUDITORIA-BIGDATA-2026-06-09.md` (maturidade 58/100, achados)
- `REAVALIACAO-FINANCEIRO-AUTOMATICO.md` (decomposição bruto, taxas, plano G1-G6)
- `references/queries.md` (catálogo de queries de leitura por plataforma/base/expurgo)

## Skills irmãs (usar junto)
- `margem-sim-multiplataforma`: margem real por plataforma normalizando as bases.
- `receita-sim-reconhecimento`: caixa vs competência, quando a receita conta.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
