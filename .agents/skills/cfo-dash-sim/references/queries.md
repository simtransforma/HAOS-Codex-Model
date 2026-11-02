# Catálogo de queries de leitura, DASH SIM MASTER (Big Data SIM)

Queries de LEITURA da fonte da verdade. O app NUNCA escreve; aqui também é só leitura (`SELECT`). Use `prisma db execute` ou cliente psql apontando para `SUPABASE_BIGDATA_SIM_DB_URL` (nome de variável do MASTER.env, nunca cole o valor). Schemas: `raw` (cru por plataforma), `stg` (limpo/tipado), `dwh` (modelado, fato/dimensão), `app` (config e views servidas).

Convenção: tudo abaixo é exemplo de leitura. Ajuste o filtro de período (`data_venda`) à pergunta. Os nomes de coluna seguem a tabela-fato `dwh.fct_venda`.

---

## 1. Base do número: BRUTO oficial vs decomposição em shadow run

`fct_venda.valor` = BRUTO. É o KPI de topo HOJE. As colunas de decomposição (`valor_bruto`, `taxa_plataforma`, `taxa_gateway`, `imposto_venda`, `valor_liquido`) estão em SHADOW RUN: existem, são calculadas, mas NÃO são o número oficial até o gate G6 (30 dias de shadow com erro <= 2%). Sempre que mostrar líquido, rotular "(shadow, não oficial)".

```sql
-- KPI oficial de topo (BRUTO) de um período
SELECT
  count(*)                         AS qtd_vendas,
  sum(valor)                       AS receita_bruta_oficial
FROM dwh.fct_venda
WHERE data_venda >= date '2026-06-01'
  AND data_venda <  date '2026-07-01';
```

```sql
-- Bruto oficial x decomposição shadow lado a lado (para inspecionar o gap)
SELECT
  sum(valor)            AS bruto_oficial,      -- KPI de hoje
  sum(valor_bruto)      AS bruto_decomposto,   -- shadow, deveria bater com 'valor'
  sum(taxa_plataforma)  AS taxa_plataforma,    -- shadow
  sum(taxa_gateway)     AS taxa_gateway,       -- shadow
  sum(imposto_venda)    AS imposto_venda,      -- shadow
  sum(valor_liquido)    AS liquido_shadow      -- shadow, GENERATED, NÃO oficial
FROM dwh.fct_venda
WHERE data_venda >= date '2026-06-01'
  AND data_venda <  date '2026-07-01';
```

Leitura de CFO: se `bruto_oficial` <> `bruto_decomposto`, a decomposição ainda tem furo, NÃO use o líquido shadow para decisão. O `valor_liquido` é coluna GENERATED (derivada das outras), não some manualmente as taxas em cima dela.

---

## 2. Proveniência do valor (de onde veio cada taxa)

As colunas de origem dizem se o número é medido na fonte ou estimado por regra. Sem isso, líquido vira chute.

```sql
-- Distribuição da proveniência: quanto do líquido é medido vs estimado
SELECT
  taxa_plataforma_origem,   -- ex.: 'plataforma' (medido) vs 'dim_payment_rate' (estimado)
  taxa_gateway_origem,
  valor_kind,               -- natureza do 'valor' na fonte: bruto | liquido
  count(*)                  AS linhas,
  sum(valor)                AS bruto
FROM dwh.fct_venda
WHERE data_venda >= date '2026-06-01'
GROUP BY 1, 2, 3
ORDER BY bruto DESC;
```

Leitura de CFO: linha com `taxa_*_origem` = regra/dimensão é estimativa (vem de `dim_payment_rate` / `app.rate_config`), não de extrato. Reporte como "estimado", separado do medido.

---

## 3. Base por plataforma (o ponto mais perigoso da reconciliação)

Cada plataforma entrega o `valor` numa base diferente. NUNCA some sem normalizar.

| Plataforma | `valor_kind` esperado | Base |
|---|---|---|
| Assiny | liquido | já vem líquido |
| Asaas | liquido | já vem líquido (pode ser gateway por trás de outra plataforma) |
| Yampi | bruto | bruto |
| Bling | bruto | bruto (espelha Yampi, dedupe remove Yampi cru) |
| Lia | ambíguo | caixa OU competência, confirmar antes |
| TikTok Shop | bruto | bruto + comissão real à parte |

```sql
-- Bruto x natureza da base, por plataforma
SELECT
  plataforma,
  valor_kind,                      -- bruto | liquido | (null = não classificado)
  count(*)                         AS qtd,
  sum(valor)                       AS valor_na_base_da_plataforma
FROM dwh.fct_venda
WHERE data_venda >= date '2026-06-01'
GROUP BY plataforma, valor_kind
ORDER BY valor_na_base_da_plataforma DESC;
```

Leitura de CFO: se você somar Assiny (líquido) com Yampi (bruto) sem normalizar, o total mistura bases e não significa nada. Para um total comparável, traga tudo para bruto (preferido hoje) ou tudo para líquido shadow (só para inspeção, com selo).

---

## 4. Expurgos e armadilhas conhecidas

Aplique sempre antes de fechar um número.

```sql
-- Yampi: só status pago é [4, 6]. Qualquer outro status NÃO conta como receita.
SELECT plataforma, status_origem, count(*), sum(valor)
FROM dwh.fct_venda
WHERE plataforma = 'yampi'
  AND data_venda >= date '2026-06-01'
GROUP BY plataforma, status_origem
ORDER BY 4 DESC;
-- Receita Yampi válida = somar só onde status_origem IN (4, 6).
```

```sql
-- Assiny: já houve expurgo de R$ 765k de receita falsa. Confirmar que o expurgo
-- está aplicado (flag de qualidade / exclusão na stg). Se aparecer pico anômalo
-- em Assiny, suspeitar de receita falsa reintroduzida.
SELECT date_trunc('day', data_venda) AS dia, sum(valor) AS bruto_assiny
FROM dwh.fct_venda
WHERE plataforma = 'assiny'
  AND data_venda >= date '2026-06-01'
GROUP BY 1
ORDER BY 1;
```

```sql
-- PIX gerado contado como pago (Purchase inflado): inspecionar método x status.
-- PIX 'gerado'/'aguardando' não é caixa. Só PIX liquidado conta.
SELECT metodo_pagamento, status_origem, count(*), sum(valor)
FROM dwh.fct_venda
WHERE data_venda >= date '2026-06-01'
GROUP BY 1, 2
ORDER BY 4 DESC;
```

```sql
-- Dedupe cross-plataforma: Asaas pode ser o gateway por trás de outra venda.
-- A dedupe usa externalReference. Cheque se há linha marcada como duplicada
-- que ainda esteja somando.
SELECT is_duplicado, plataforma, count(*), sum(valor)
FROM dwh.fct_venda
WHERE data_venda >= date '2026-06-01'
GROUP BY 1, 2
ORDER BY 4 DESC;
-- Receita reconciliada = somar só is_duplicado = false.
```

---

## 5. Data Quality (rodar antes de confiar no número)

```sql
-- Roda a bateria de checks e lê o log mais recente
SELECT dwh.fn_dq_checks();

SELECT check_name, status, qtd_falhas, detalhe, criado_em
FROM dwh.dq_log
ORDER BY criado_em DESC
LIMIT 50;
```

Leitura de CFO: qualquer check em `FAIL` que toque receita (status, dedupe, base por plataforma) bloqueia a leitura como definitiva. Reporte o número como provisório e cite o check que falhou.

---

## 6. Recebíveis (forward book) para a tela Cobranças

```sql
-- Forward book: parcelas a receber por ano, fonte (LIA vs Asaas) e aging
SELECT
  extract(year FROM data_vencimento)      AS ano,
  fonte_cobranca,                          -- lia | asaas
  count(*)                                 AS parcelas,
  sum(valor_parcela)                       AS a_receber
FROM dwh.fct_recebivel
WHERE status = 'aberto'
GROUP BY 1, 2
ORDER BY 1, 2;
-- Esperado na ordem de R$ 1,08M em ~7.954 parcelas até 2030 (confira contra a tela).
```

```sql
-- Aging de inadimplência (30/60/90+)
SELECT
  CASE
    WHEN dias_atraso BETWEEN 1 AND 30  THEN '01-30'
    WHEN dias_atraso BETWEEN 31 AND 60 THEN '31-60'
    WHEN dias_atraso BETWEEN 61 AND 90 THEN '61-90'
    WHEN dias_atraso > 90              THEN '90+'
    ELSE 'em_dia'
  END AS faixa_aging,
  count(*) AS parcelas,
  sum(valor_parcela) AS valor
FROM dwh.fct_recebivel
WHERE status IN ('aberto', 'atrasado')
GROUP BY 1
ORDER BY 1;
```

---

## 7. Sanidade contra a dash estática (dados-view)

A `service.example.invalid` puxa API crua, SEM reconciliação. Serve só de apresentação. Se o número dela divergir da MASTER, a MASTER (reconciliada) é a verdade. Use a query do item 1 para confrontar.

```sql
-- Total bruto reconciliado do dia, para confrontar com o snapshot estático
SELECT sum(valor) AS bruto_reconciliado_dia
FROM dwh.fct_venda
WHERE data_venda = current_date - 1   -- D-1
  AND is_duplicado = false
  AND NOT (plataforma = 'yampi' AND status_origem NOT IN (4, 6));
```

---

## Notas de uso

- Os nomes exatos de coluna de filtro (`status_origem`, `is_duplicado`, `metodo_pagamento`, `fonte_cobranca`) podem variar entre `stg` e `dwh`; confirme no schema antes de rodar (`\d dwh.fct_venda`). O que NÃO muda: `valor` = bruto oficial, e a base por plataforma é mista.
- Taxas e regras vivem em `dwh.dim_payment_rate` e `app.rate_config`, versionadas. NUNCA hardcode taxa na query; leia da dimensão.
- Para margem por plataforma e reconhecimento de receita (caixa vs competência), use as skills irmãs `margem-sim-multiplataforma` e `receita-sim-reconhecimento`.

