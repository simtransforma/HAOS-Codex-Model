# Conexão e queries, Supabase do grupo

Detalhe operacional da skill `supabase`. Tudo aqui lê a connection string por NOME de variável do ${USER_SECRET_FILE}, nunca o valor. Carregue o ${USER_SECRET_FILE} antes (caminho em `<USER_PROJECT_CONTEXT>.md`).

---

## 1. Os 3 modos de conexão e quando usar

Host do pooler do Big Data SIM (região correta `aws-1-sa-east-1`, NÃO `aws-0`):

- **Pooler de TRANSAÇÃO, porta 6543** -> PADRÃO. Webhook, ETL, cron de import, edge, qualquer script efêmero e concorrente.
- **Pooler de SESSION, porta 5432** -> só pool de app de longa vida (Prisma da dash). Max ~15 clients: satura.
- **Direto (`db.<ref>.supabase.co:5432`)** -> evite. No Big Data SIM é só IPv6, falha em container.

O usuário do pooler tem o formato `postgres.<<USER_PROJECT_CONTEXT>>` (ex.: `postgres.myrxujdvbjjxhpqmtsnx`). O `<<USER_PROJECT_CONTEXT>>` é o ref do §1 da skill.

### Selecionar o pooler nos importadores Python da dash
Os importadores escolhem a chave por env:

```bash
# força o pooler de transação (6543) no import/ETL
SIM_DB_URL_KEY=POOLER_TRANSACTION python importador_api.py --plataforma all --days 3
```

Há fallback regex no `capi_assiny.py`/wrappers que troca `5432`->`6543` quando a string vier em session. A regra durável: carga concorrente = 6543.

---

## 2. psql (read-only)

```bash
# carregue a string por NOME de variável (exemplo de nome; confirme no ${USER_SECRET_FILE})
#   SUPABASE_DATABASE_URL  -> string com :6543
psql "$SUPABASE_DATABASE_URL" -c '\d dwh.fct_venda'

# leitura simples
psql "$SUPABASE_DATABASE_URL" \
  -c "SELECT count(*), sum(valor) FROM dwh.fct_venda WHERE data_venda >= date '2026-06-01';"
```

Se só existir a string de session no ${USER_SECRET_FILE}, troque a porta na hora (`:5432` -> `:6543`) para a inspeção concorrente. Confirme o nome exato da variável com `grep -i supabase` no ${USER_SECRET_FILE} (TODO ao vivo).

---

## 3. Python (psycopg) com keepalive e timeout

Lições do incidente (12/06): conexão sem `connect_timeout`/keepalive fica pendurada em `idle in transaction` quando o load balancer mata o socket em silêncio, segurando um slot do pool. Padrão seguro:

```python
import os, psycopg

# nome de variável, nunca o valor literal
dsn = os.environ["SUPABASE_DATABASE_URL"]  # string :6543

conn = psycopg.connect(
    dsn,
    autocommit=True,            # não abrir transação durante I/O externo (ex.: POST Meta)
    connect_timeout=15,
    keepalives=1, keepalives_idle=30, keepalives_interval=10, keepalives_count=3,
    prepare_threshold=None,     # transaction pooler não guarda prepared de sessão
)
with conn.cursor() as cur:
    cur.execute("SELECT sum(valor) FROM dwh.fct_venda WHERE data_venda >= %s", ("2026-06-01",))
    print(cur.fetchone())
conn.close()
```

Regra: nunca segure transação aberta enquanto faz chamada HTTP externa. Marque o estado em tabela com transação curta (batch + `executemany`), feche.

---

## 4. Client SDK / edge (apps Lovable)

Leitura do browser usa a **anon key** (RLS aplica). Escrita server-side usa **service_role** (ignora RLS, só na edge/script):

```ts
// no app (browser): anon key embutida no build, RLS protege
import { createClient } from "@supabase/supabase-js";
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY); // nomes de var
const { data } = await supabase.from("purchases").select("name,city,uf").order("created_at", { ascending: false }).limit(20);
```

```ts
// na edge function (Deno): service_role, ignora RLS, NUNCA exposto ao browser
const admin = createClient(SUPABASE_URL, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
await admin.from("purchases").insert({ name, city, uf });
```

Deploy de edge (projeto Supabase puro):
```bash
supabase functions deploy purchases-ingest --project-ref woodkkvkrxscmnomfitc
```
Para projeto Lovable, preferir o agente Lovable (MCP `lovable`), não a UI.

---

## 5. Data Quality antes de confiar no número (warehouse)

```sql
SELECT dwh.fn_dq_checks();
SELECT check_name, status, qtd_falhas, detalhe, criado_em
FROM dwh.dq_log
ORDER BY criado_em DESC
LIMIT 50;
```
Qualquer FAIL que toque receita bloqueia "número definitivo". Para a leitura financeira reconciliada (bases mistas por plataforma, expurgos Yampi/Assiny/PIX, dedupe), use a skill `cfo-dash-sim`.

---

## 6. Checklist rápido

1. Carregar ${USER_SECRET_FILE}. Confirmar o REF do projeto certo (tabela §1 da skill).
2. Conexão concorrente/efêmera -> pooler de TRANSAÇÃO 6543. App de longa vida -> session 5432.
3. Ler a string por NOME de variável. Nunca colar o valor.
4. Warehouse = read-only por padrão (`SELECT`). Escrita só por importador versionado + backup.
5. App Lovable = RLS habilitada; anon no browser, service_role só na edge.
6. Dado não confirmado ao vivo = TODO, não fabricar.

---

## TODOs a confirmar ao vivo
- Nomes EXATOS das variáveis do ${USER_SECRET_FILE} (`grep -i supabase` + por cada ref).
- Refs dos demais projetos Lovable (edbcom; e qualquer projeto novo) via MCP `lovable list_projects` ou painel da org.
- Plano de cada projeto (Pro x Free) e limite de pool por projeto.
- Se edbcom tem Supabase próprio ou só n8n -> Clint.
- Nomes de coluna de filtro em `dwh.fct_venda` (`status_origem`, `is_duplicado`, `metodo_pagamento`) podem variar entre `stg` e `dwh`; conferir com `\d`.

