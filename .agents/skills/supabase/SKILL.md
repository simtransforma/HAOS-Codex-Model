---
name: supabase
description: "Operar os projetos Supabase do grupo (HAU/SIM/EdsonBurger/Editora): o Big Data SIM (warehouse, schemas raw/stg/dwh/app, fato dwh.fct_venda) e os Supabase dos apps Lovable (PMX26/usuario, PNL usuario, edbcom, HAU Tasks). Use SEMPRE que a tarefa envolver Supabase em qualquer forma: \"conecta no supabase\", \"roda uma query no big data\", \"consulta o fct_venda\", \"qual o ref do projeto supabase\", \"cria uma edge function\", \"pooler de transa\u00e7\u00e3o\", \"porta 6543 ou 5432\", \"RLS desse projeto\", \"service_role key\", \"supabase do lovable\", \"qual o connection string do warehouse\", \"l\u00ea a tabela X no supabase\", \"psql no banco SIM\". Tamb\u00e9m aciona implicitamente quando ETL, webhook n8n, dash, app Lovable ou tarefa financeira do grupo precisa ler/escrever no Postgres gerenciado de qualquer um desses projetos, mesmo sem citar \"Supabase\". N\u00c3O improvise a conex\u00e3o: o grupo J\u00c1 teve incidente de esgotar conex\u00f5es (EMAXCONNSESSION) por usar o pooler errado. Siga a PEGADINHA do pooler de transa\u00e7\u00e3o (porta 6543) daqui. N\u00c3O use para construir a dash (sim-dash) nem para a leitura financeira dela (cfo-dash-sim).\n"
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

# Supabase (projetos do grupo)

Operação dos projetos Supabase (Postgres gerenciado) do grupo HAU/SIM/EdsonBurger/Editora. São VÁRIOS projetos: um warehouse (Big Data SIM) e os bancos dos apps Lovable. Esta skill é INTERNA: cita refs de projeto e schemas, mas NUNCA o valor de connection string ou key (refira sempre por nome de variável do ${USER_SECRET_FILE}).

A pegadinha mais cara está em "Conexão" (pooler de TRANSAÇÃO, porta 6543). Não improvise: ela já custou um incidente de produção (EMAXCONNSESSION, max clients).

---

## 1. Mapa dos projetos Supabase

Cada app/sistema do grupo tem o seu projeto. Confirme o ref antes de conectar; o ref errado lê o banco errado.

| Projeto | Ref (<USER_PROJECT_CONTEXT>) | Plano | Uso | Schemas / tabelas-chave |
|---|---|---|---|---|
| **Big Data SIM** (warehouse) | `myrxujdvbjjxhpqmtsnx` | Pro (org SIM, "coração da empresa") | Data warehouse da dash SIM MASTER. Fonte da verdade event-grain de vendas/leads/tráfego. | `raw` / `stg` / `dwh` / `app`. Fato central `dwh.fct_venda`. Dimensões `dwh.dim_*`. Config `app.rate_config`, `dwh.dim_payment_rate`. |
| **PMX26 / usuario** (Lovable) | `hrkyajfzabietrwaqwhu` | (confirmar ao vivo) | App upsell usuario Experience. Gate de acesso por ingresso (Assiny) via tag no Clint. | Edge function `check-ticket` (consulta Clint por tag). |
| **PNL usuario** (Lovable) | `woodkkvkrxscmnomfitc` | (confirmar ao vivo) | Landing PNL usuario com feed de compras ao vivo. | Tabela `purchases` (id, name, city, uf, created_at). Edge function `purchases-ingest` (Deno). RLS "Public can read purchases". |
| **HAU Tasks** (app interno) | `xeqeuzlqqjjrvflbcwbk` | (confirmar ao vivo) | Gerenciador de tarefas interno (containers hau-tasks). | Tabela `tasks` com RLS. Senha em `PASSWORD_DATABASE_HAU_TASK`. |
| **edbcom** (landings EdsonBurger) | TODO confirmar ao vivo | (confirmar) | Captura de leads das landings Lovable do EdsonBurger. Hoje o lead vai pro Clint via webhook n8n (não necessariamente persiste em Supabase). | TODO mapear ao vivo. |

> **TODO (confirmar ao vivo):** refs exatos de cada projeto Lovable (listar via MCP `lovable` `list_projects` / `get_project`, ou no painel Supabase da org), plano de cada um, e se edbcom tem projeto Supabase próprio ou só usa n8n -> Clint. Cada projeto Lovable mapeia para 1 projeto Supabase; o ref aparece na URL `https://<ref>.supabase.co`.

**Big Data SIM, detalhe da região:** o pooler correto é `aws-1-sa-east-1` (NÃO `aws-0`). A conexão DIRETA (sem pooler) é só IPv6, falha em container/ambiente sem IPv6: use SEMPRE o pooler.

---

## 2. Conexão (LEIA antes de conectar): pooler de TRANSAÇÃO obrigatório

Supabase expõe 3 formas de conectar. A escolha errada esgota o pool e derruba gravação em produção.

| Forma | Porta | Quando usar | Risco |
|---|---|---|---|
| Conexão direta | 5432 (host `db.<ref>.supabase.co`) | Quase nunca aqui. Só IPv6 no Big Data SIM. | Falha em container sem IPv6. |
| Pooler **SESSION** (Supavisor) | **5432** (host pooler `aws-1-sa-east-1...pooler.supabase.com`) | Conexão longa, prepared statements, migrations. | **Max ~15 clients.** Satura fácil. Foi a causa do incidente. |
| Pooler **TRANSAÇÃO** (Supavisor) | **6543** | **PADRÃO para webhook, ETL, script, serverless, edge.** Conexão curta por transação. | Não suporta prepared statements de sessão; ok para o nosso uso. |

### Como o nome da variável aparece (por NOME, nunca o valor)

As connection strings vivem no ${USER_SECRET_FILE} por nome de variável. Carregue o ${USER_SECRET_FILE} antes de qualquer chamada (caminho em `<USER_PROJECT_CONTEXT>.md`). Convenção observada/esperada:

- `SUPABASE_DATABASE_URL` (connection string do Big Data SIM). Variantes prováveis por pooler: `SUPABASE_DATABASE_URL` (6543) e `..._POOLER_SESSION` (5432).
- Nos importadores Python da dash, a chave do pooler é selecionada por env `SIM_DB_URL_KEY` (ex.: `POOLER_TRANSACTION`); há fallback regex que troca `5432`->`6543`.
- Keys de API por projeto: `SUPABASE_<PROJETO>_ANON_KEY` (cliente/browser, RLS aplica) e `SUPABASE_<PROJETO>_SERVICE_ROLE_KEY` (server, ignora RLS, **nunca no browser nem em repo público**). HAU Tasks usa `PASSWORD_DATABASE_HAU_TASK`.

> **TODO (confirmar ao vivo):** os nomes exatos das variáveis no ${USER_SECRET_FILE} (grep por `SUPABASE` e por cada ref). NÃO assuma o nome; confira. Detalhes de conexão e exemplos psql/Python em `./references/conexao-e-queries.md`.

---

## 3. Query read-only no warehouse (Big Data SIM)

Padrão para inspecionar o warehouse sem risco. O app NUNCA escreve no `dwh`; aqui também é só `SELECT`.

- Conecte pelo pooler de **transação (6543)**, lendo a string por nome de variável.
- Schemas: `raw` (cru por plataforma) -> `stg` (limpo/tipado) -> `dwh` (modelado, fato/dimensão) -> `app` (config e views servidas).
- Fato central: `dwh.fct_venda` (`valor` = BRUTO oficial; colunas de decomposição `valor_liquido` etc. estão em shadow run, NÃO oficiais). Para LEITURA FINANCEIRA reconciliada (bases mistas, expurgos, qual número reportar) use a skill `cfo-dash-sim`, não improvise aqui.
- Antes de confiar num número, rode `SELECT dwh.fn_dq_checks();` e leia `dwh.dq_log`.

```sql
-- exemplo de leitura: receita bruta de um período
SELECT count(*) AS qtd, sum(valor) AS receita_bruta
FROM dwh.fct_venda
WHERE data_venda >= date '2026-06-01'
  AND data_venda <  date '2026-07-01';
```

Catálogo de queries de leitura (por plataforma, base, expurgo, DQ) em `./references/conexao-e-queries.md` e, para a leitura financeira, na skill `cfo-dash-sim`.

**Escrita no warehouse** (DDL/backfill): só os importadores versionados em `bigdata-etl/` (idempotentes, `ON CONFLICT`, backups `dwh._bkp_*`). NÃO rode DDL ad-hoc em produção; é tarefa de @dev-backend/@data-engineer com backup e gate. Bling tem gate fiscal do contador (zero escrita no Bling pela dash).

---

## 4. Edge functions dos apps Lovable

Os apps Lovable usam Supabase Edge Functions (Deno) para lógica server-side, porque o **custom domain do Lovable serve SÓ o frontend estático** (as server routes `/api/*` do TanStack NÃO rodam no domínio publicado). Por isso feed, gate e ingest viram edge function + leitura via client SDK.

Padrões já em produção:

- **`check-ticket`** (projeto PMX26 `hrkyajfzabietrwaqwhu`): recebe email, consulta o Clint CRM por tag (`PMX26_Prata_Pago` / `_Ouro_Pago` / `_Diamante_Pago`, prioridade Diamante > Ouro > Prata) e libera a tela do tier. URL absoluta da edge function, funciona em qualquer domínio.
- **`purchases-ingest`** (projeto usuario `woodkkvkrxscmnomfitc`): recebe `{Nome, Cidade, Estado}`, header `Authorization: Bearer <segredo>` (auth errada = 401), extrai primeiro nome + UF, insere na tabela `purchases` via **service_role**. n8n (`[Assiny] Todos Eventos`) chama essa edge no evento de compra aprovada; o feed lê direto da tabela por client SDK (anon key, RLS `read true`, polling ~15s).

Como operar edge functions:

- Deploy/edição preferencialmente via o agente Lovable (MCP `lovable`), NÃO pela UI do navegador do usuario (regra `feedback_lovable_via_api`). Para o projeto puro Supabase, `supabase functions deploy <nome> --project-ref <ref>` (CLI) é o caminho; confirme login/token antes.
- O segredo de auth da função e a service_role key vivem nos Secrets do projeto (Supabase Dashboard > Edge Functions > Secrets) e/ou no ${USER_SECRET_FILE} por nome. NUNCA hardcode no código que vai pro git (o `usuario-api/server.js` legado tinha token Clint hardcoded e por isso NÃO entrou no backup do repo, ver `<USER_PROJECT_CONTEXT>`).

---

## 5. RLS (Row Level Security)

- Os apps Lovable expõem a **anon key no build** (vai pro browser). Por isso RLS é o que de fato protege a tabela. Ex.: usuario tem policy `Public can read purchases` (`USING true`) para o feed; a escrita só via **service_role** na edge (que ignora RLS).
- **service_role ignora RLS** e nunca pode aparecer no browser, no client SDK ou em repo público. É só server-side (edge function, script, n8n).
- HAU Tasks: tabela `tasks` com RLS, 21 usuários. O classifier BLOQUEIA query SQL direta na produção mesmo com permissão verbal: precisa autorização nas settings OU access_token da API. NÃO contornar (ver `<USER_PROJECT_CONTEXT>`, bloco HAU-Task).
- Ao criar tabela nova num app Lovable: habilitar RLS e escrever a policy explícita (read público só onde o dado é público; escrita só service_role). Sem policy, ou trava tudo ou (pior) vaza.

---

## 6. Regras de segurança e operação

1. **Nunca colar segredo.** Connection string, service_role e tokens só por NOME de variável do ${USER_SECRET_FILE}. Esta skill é interna (pode citar ref e schema), mas valor de segredo nunca.
2. **Pooler de transação (6543) para carga concorrente.** Webhook/ETL/edge/script. Session (5432) só para o pool de app de longa vida. (Incidente EMAXCONNSESSION, §2.)
3. **Read-only por padrão no warehouse.** Inspeção = `SELECT`. Escrita só por importador versionado, idempotente, com backup; nunca DDL ad-hoc em produção sem gate.
4. **RLS sempre que a anon key for pública.** É a única barreira no app Lovable.
5. **Edge/Lovable via API/MCP, não pela UI.** Validação visual é do usuario.
6. **Confirmar o ref antes de conectar.** Ref errado = banco errado. A tabela do §1 é o índice; quando houver dúvida, confirme ao vivo.

---

## 7. Saída esperada desta skill

Ao acionar esta skill, a entrega é uma das abaixo, sempre declarando o projeto (ref) e o método de conexão:

- **Conectar / rodar query:** o resultado da query (read-only), citando projeto + ref + que usou o pooler de transação (6543) lendo a string por nome de variável. Nunca o valor da string.
- **Mapear projeto:** o ref, o uso, os schemas/tabelas e o estado de RLS do projeto pedido, com os TODOs marcados quando o dado não foi confirmado ao vivo.
- **Criar/editar edge function:** o nome da função, o projeto, o contrato (input/output, header de auth por nome) e como foi deployada (MCP Lovable ou CLI), sem segredo embutido.
- **Diagnóstico de conexão:** identificar pooler errado (5432 em carga concorrente) como causa de EMAXCONNSESSION/max clients e a correção (6543), com evidência.

Em qualquer caso: se um dado (ref, nome de variável, plano) não foi confirmado ao vivo, marque como TODO e diga que é a confirmar, não fabrique.

## Skills e memórias relacionadas
- `cfo-dash-sim` / `sim-dash`: leitura financeira e construção da dash que LÊ o Big Data SIM.
- `cloudflare`: DNS dos apps Lovable (custom domain -> IP anycast Lovable).
- Memórias: `<USER_PROJECT_CONTEXT>` (warehouse + incidente pooler), `<USER_PROJECT_CONTEXT>` (check-ticket), `<USER_PROJECT_CONTEXT>` (purchases-ingest), `<USER_PROJECT_CONTEXT>`, `feedback_lovable_via_api`.

