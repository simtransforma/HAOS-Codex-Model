---
name: tiktok-shop-sim
description: "Integracao COMPLETA do TikTok Shop da loja \"Editora Mindset - usuario\" (grupo SIM), ja em producao no Big Data SIM-Dash. Use SEMPRE que a tarefa envolver TikTok Shop em qualquer forma - vendas/pedidos do TikTok, comissao ou taxa do TikTok, liquidacoes/settlements/repasses, token ou autorizacao da loja, importador ou sync do TikTok, webhook do TikTok, pixel/eventos TikTok, ou perguntas tipo \"quanto o tiktok vendeu\", \"comissao do tiktok\", \"renova o token do tiktok\", \"roda o sync do tiktok\", \"o tiktok ta atualizando?\". Tambem quando alguem for mexer na fct_venda plataforma tiktok_shop, em raw.tiktok_orders/raw.tiktok_settlements, no Bling canal tiktok, ou estender a API do TikTok Shop. Esta skill tem os caminhos prontos (scripts, credenciais por nome, tabelas, crons) - NAO reinvente nada do zero, NAO re-investigue a API, siga os caminhos daqui."
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

# TikTok Shop SIM (loja Editora Mindset - usuario)

Integracao em PRODUCAO desde 11/06/2026. Loja BR, seller LOCAL, shop_id final 9929, 20 escopos.
Tudo roda sozinho (crons + webhook). Esta skill da os caminhos pra consultar, operar e estender.

## Regras inegociaveis

1. NUNCA imprimir/logar valor de token ou segredo (os scripts ja mascaram; mantenha).
2. PII so mascarada ou hasheada em logs/relatorios.
3. Idempotencia: tudo aqui e UPSERT/ON CONFLICT; re-rodar nao duplica. Mantenha esse padrao em extensoes.
4. Esta skill e INTERNA (contem infra). NUNCA copiar pro repo publico HAOS_CC.
5. A API Finance so mostra pedido JA LIQUIDADO (TikTok liquida 1 a 2 semanas POS-ENTREGA).
   Venda recente sem taxa nao e bug, e lag estrutural; o cron preenche sozinho.

## Credenciais (${USER_SECRET_FILE}, ler por nome, nunca expor valor)

Arquivo: `${USER_WORKSPACE_ROOT}`

| Variavel | O que e |
|---|---|
| TIKTOK_SHOP_API_KEY / API_SECRET | app key/secret do app no Partner Center |
| TIKTOK_SHOP_ACCESS_TOKEN (+_EXPIRES_AT) | access token, vale ~7 dias, renova SOZINHO |
| TIKTOK_SHOP_REFRESH_TOKEN (+_EXPIRES_AT) | refresh token, vale ~99 ANOS (loja nunca re-autoriza) |
| TIKTOK_SHOP_LINK_AUTORIZATION | link de autorizacao da loja (so se precisar re-autorizar) |

## Ferramentas prontas (pasta dos scripts)

Pasta: `%OneDrive%\Documentos\Projetos\Agencia HAU - Soluções Digitais\2. Clientes\1.Ativos\usuario\[BigData] Banco de Dados\_schema\`
Rodar os scripts DESSA pasta (dependem de `prep_ga4.py` pra ler MASTER e conectar no Supabase).
Suprimir stderr do dotenv (`2>/dev/null` no bash): warnings das linhas 308+ do MASTER sao conhecidos e inofensivos.

### tiktok_auth.py (token)
- `python tiktok_auth.py --status` ve presenca/expiracao dos tokens (sem expor valores).
- `python tiktok_auth.py --refresh` forca refresh agora (normalmente desnecessario).
- `python tiktok_auth.py --auth-code <code>` troca auth_code novo por tokens (so em re-autorizacao).
- `ensure_fresh_token(margin_s)` e importavel: renova se faltar < 24h e PERSISTE a rotacao no
  MASTER com backup (.bak_tiktok) + verificacao de integridade. O importador ja usa.

### importador_tiktok_shop.py (orders + finance + enrich)
Flags: `--probe` (testa token+shop, nao grava) | `--verify-only` (relatorio do banco) |
`--days N` ou `--since/--until AAAA-MM-DD` | `--orders-only` | `--finance-only` | `--no-detail` |
`--enrich-fct` (aplica comissao real na fct_venda) | `--selftest-sign` | `--apply-ddl` | `--print-ddl`.

Operacao padrao (igual ao cron): `python importador_tiktok_shop.py --days 7 --enrich-fct`

### Cron (ja registrado, nao recriar)
Tarefa agendada Windows local **"SIM-Dash TikTok Diario"**, diaria 05:45, roda `tiktok_daily.ps1`
(mesma pasta), log em `_logs\tiktok.log`. LICAO: o caminho tem `[BigData]`, entao NUNCA usar
redirect `*>>` em PowerShell com esse path (trata como wildcard e falha silencioso);
o script ja usa `2>&1 | Add-Content -LiteralPath`.

## Onde os dados vivem (Supabase Big Data SIM)

Conexao: `import prep_ga4 as g; psycopg.connect(g._cfg().get("SUPABASE_DATABASE_URL"))`

| Tabela | Conteudo |
|---|---|
| `raw.tiktok_orders` | 1 linha por pedido (PK order_id, 18 digitos), status, datas, valor, payload PII-mascarada |
| `raw.tiktok_settlements` | 1 linha por (order_id, statement_id): receita liquidada, fees ASSINADOS (negativos), repasse liquido |
| `dwh.fct_venda` plataforma='tiktok_shop' | vendas na dash; `order_number` = order id TikTok; `transaction_ext_id` = 'bling:<id>' |
| `raw.webhook_events` source='tiktok_shop' | eventos do webhook em tempo real |
| `raw.bling_pedidos` canal='tiktok_shop' | espelho via Bling (loja_id 205985320; `numero_loja` = order id TikTok) |

JOIN GARANTIDO (validado): `raw.tiktok_orders.order_id = fct_venda.order_number = raw.bling_pedidos.numero_loja`.

Enrich da comissao: `--enrich-fct` faz UPDATE em fct_venda tiktok_shop com
`taxa_plataforma = abs(sum(fee_total))` e `taxa_plataforma_origem = 'real_tiktok'`;
`valor_liquido` e coluna GENERATED (recalcula sozinha). So onde existe settlement.
Sem settlement = origem 'pendente' (lag normal, cron resolve).

## Receitas prontas

### "Quanto o TikTok vendeu / qual a comissao real?"
SQL direto (nao precisa da API):
```sql
SELECT date_trunc('month', data_id) mes, count(*) vendas,
       round(sum(valor_bruto)::numeric,2) bruto,
       round(sum(taxa_plataforma)::numeric,2) taxa_real,
       round(sum(valor_liquido)::numeric,2) liquido
FROM dwh.fct_venda
WHERE plataforma='tiktok_shop' AND status='paid'
GROUP BY 1 ORDER BY 1;
```
Ou por canal na `dwh.mv_daily_financeiro` (canal='tiktok_shop').
Fatos de referencia: take rate REAL ~23,6% do bruto liquidado (~16,7% do bruto cheio).
Composicao do fee: fee_per_item_sold (maior fatia) + sfp_service_fee (frete loja) +
gmv_max_ad_fee (Ads GMV Max) + platform_commission (pequena) + affiliate_*.

### "Roda o sync / atualiza o TikTok agora"
```bash
cd <pasta _schema> && python importador_tiktok_shop.py --days 7 --enrich-fct 2>/dev/null
```

### "O token ta valido? / problema de auth"
1. `python tiktok_auth.py --status` (expiracoes). 2. Se access vencido: `--refresh` (raro; o cron ja renova).
3. So se a LOJA revogou a autorizacao (refresh morto): seguir o guia de 3 passos com o usuario:
   `...\[BigData] Banco de Dados\Dash\SIM-Dash\GUIA_TIKTOK_3_PASSOS.md` (abrir LINK_AUTORIZATION
   logado na conta da loja, copiar `code=` da URL de redirect, validade 30 min, uso unico) e
   entao `python tiktok_auth.py --auth-code <code>`.

### "O TikTok ta atualizando? / health check"
```bash
python importador_tiktok_shop.py --verify-only 2>/dev/null   # estado do banco
python importador_tiktok_shop.py --probe 2>/dev/null         # token + shop ao vivo
```
+ checar a tarefa: `schtasks /query /tn "SIM-Dash TikTok Diario"` e o log `_logs\tiktok.log`.
+ webhook: `SELECT count(*), max(received_at) FROM raw.webhook_events WHERE source='tiktok_shop'`.

PEGADINHA 1 (incidente real 12/06): `LastTaskResult=0` no schtasks NAO prova sucesso; o wrapper
nao propaga o exit code do Python. A fonte da verdade e o `_logs\tiktok.log` (procure
"BLOQUEADO"/"exit"). Sempre leia o log, nunca confie so no Task Scheduler.

PEGADINHA 2 (incidente real 12/06): edicao manual do ${USER_SECRET_FILE} pode APAGAR ou RENOMEAR as
linhas TIKTOK_SHOP_* sem querer (aconteceu: viraram APP_KEY/APP_SECRET e os 4 tokens sumiram).
Sintoma: log "BLOQUEADO (sem token)". Recuperacao SEM re-autorizar a loja: os backups
`${USER_SECRET_FILE}.bak_*` (bak_bling, bak_tiktok...) na mesma pasta guardam as linhas; restaurar
CIRURGICAMENTE so as linhas TIKTOK_SHOP_* faltantes (backup do atual antes + verificar ancoras
de outras chaves depois + nunca imprimir valores), entao validar com --probe.

PEGADINHA 3 (RESOLVIDA 12/06/2026): o no Postgres dos webhooks n8n usava o pooler SESSION do
Supabase; sob saturacao (erro EMAXCONNSESSION, pool 15/15) gravacoes do webhook FALHAVAM.
FIX APLICADO 12/06/2026: credencial nova `simbigdata-tx-pooler` (id ${USER_RESOURCE_000043}ZC5wRAUf2Ar9RM4, pooler de
TRANSACAO porta 6543) no node "Gravar Supabase BigData" dos 11 workflows *Dash-SIM (piloto
TikTok validado e2e antes da frota). As ~265 execucoes perdidas por pool (7d) foram re-executadas
via POST /api/v1/executions/{id}/retry com {"loadWorkflow": true}. Se o erro voltar: conferir se
algum node novo voltou pra credencial session antiga (simbigdata00001) e quem esta comendo o pool
session (pg_stat_activity; historico: capi_assiny.py pendurado em idle in transaction).

### Webhook (tempo real, ja ativo)
n8n workflow `[TikTok] Dash-SIM`, URL registrada no Partner Center:
`https://service.example.invalid/webhook/${USER_RESOURCE_000042}`
Grava raw.webhook_events source='tiktok_shop' (dedup type+order_id, payload cru, skipOnConflict).

## Pixel / eventos web (lado Ads, nao confundir com a API da loja)

Pixel TikTok: `D115FU3C77U61SUD7RV0`. Vive no GTM (web ${USER_RESOURCE_000005}, checkout ${USER_RESOURCE_000040},
server ${USER_RESOURCE_000041} com tag CompletePayment EAPI, dedup event_id `yampi_<order.id>`).
PENDENTE (do usuario): token do Events API do TikTok (Events Manager > pixel D115 > Settings >
Generate Access Token) pra ligar o lado servidor; ate la o EAPI falha silencioso e o browser cobre.
TikTok ADS (gasto de midia): NAO integrado (sem credencial de Marketing API; gasto TikTok nao
esta em fct_ads_spend).

## Estender a API (novos endpoints)

Leia `./references/api.md` ANTES (assinatura HMAC exata, hosts, versoes, paginacao, pegadinhas).
Reuse o signer e o `ensure_fresh_token` do importador. Nao escreva auth/assinatura do zero.

## Relacao com o Bling (nao duplicar!)

Os pedidos TikTok chegam por 2 caminhos que CONVIVEM: Bling (cria a venda na fct_venda via
`importador_bling.py --project-tiktok`, cron local 05:30 "SIM-Dash Bling Diario") e API direta
(enriquece com a comissao real). REGRA: o Bling e dono da CRIACAO da venda; a API TikTok e dona
da TAXA/liquidacao. Nunca criar venda pela API TikTok (duplicaria com o Bling).

