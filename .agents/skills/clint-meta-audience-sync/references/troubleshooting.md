# Troubleshooting — clint-meta-audience-sync

Pegadinhas técnicas mapeadas em produção (06/06/2026 e antes). Se algo falhar, procura aqui primeiro.

## Erros Meta API

### `2654 / 1870053` — "Parâmetro 'subtipo' não é aceito"

A API recente da Meta **rejeita `subtype=WEBSITE` explícito** em POST de Custom Audience.

**Solução:**
- Pra audience FILE (CUSTOM): use `subtype=CUSTOM` + `customer_file_source=USER_PROVIDED_ONLY` (continua aceitando)
- Pra audience WEBSITE (pixel-based): **omitir totalmente o `subtype`**. Meta detecta automaticamente pela presença de `rule`.

Esta skill só faz FILE, então o erro não deve ocorrer. Se ocorrer, conferir versão da Graph API (deve ser `v21.0` ou superior).

### `100 / 1487079` — "Hash inválido"

Algum campo foi enviado em texto puro em vez de SHA-256. Conferir `to_hash_row()`.

### `2650` — "Audience temporarily unavailable"

Audience criada está em estado transitório. Esperar 30-60s e retentar upload.

### `num_invalid_entries` alto

**Normal** — Meta marca como "invalid" qualquer hash de string vazia (ex: CPF/CEP/city ausentes). Os campos preenchidos do mesmo lead ainda contam pra matching.

Só preocupar se `num_invalid_entries > num_received` ou se `num_received = 0`.

## Erros Clint API

### Tag não encontrada

`GET /v1/tags?search=...` retornou vazio ou nenhum match exato.

**Causas:**
- Case incorreto (Clint é case-sensitive)
- Tag escrita errada
- Token sem permissão de ler tags

**Verificação:** rode `GET /v1/tags?limit=100` e procure a tag manualmente.

### Paginação infinita

Loop sem fim no `while True`.

**Solução já implementada no script:** quebra se `len(items) < 100` (última página). Se a Clint mudar o limite default, ajustar.

### Clint não tem filtro `created_after`

Confirmado em produção. Pra auto-sync no workflow n8n, a solução é **walk reverso da última página** com early-stop quando `created_at < last_synced_at`. O workflow base já implementa isso.

Esta skill (upload inicial) puxa tudo da tag de uma vez — não precisa de filtro temporal.

## Erros n8n

### `require('crypto')` blocked


**Não tentar substituir** por `node-forge` ou outras libs — vão dar problema similar.

### Workflow duplicado mas Init State não atualiza

Verificar se o node `Init State` é tipo Set ou Code. O script tenta os dois caminhos. Se a estrutura mudar no workflow base, atualizar `n8n_duplicate_workflow()`.

### Workflow não ativa

`POST /api/v1/workflows/{id}/activate` precisa que o workflow tenha ao menos 1 trigger (Cron, no caso). Se a duplicação não copiou triggers, o ativar falha.

## Erros de auth

### `Authentication failed` Clint

Var no MASTER.env esperada: `CLINT_API_TOKEN` (ou `CLINT_TOKEN` ou `CLINT_API_KEY` — script tenta em ordem).

Header correto: `api-token: <valor>` (não `Authorization: Bearer ...`).

### `OAuthException` Meta

Var: `META_TOKEN_BM01` (ou BM02, BM11, etc).

System User do BM precisa ter role na Página + Ad Account.

App Mode deve estar Live (validado em 23/05/2026).

### `N8N_API_URL` não definida

Conferir MASTER.env. Padrão: `https://service.example.invalid`.

Header: `X-N8N-API-KEY: <key>`.

## Audience criada com tamanho `<1.000`

**Normal** durante as primeiras 1-6h. Meta processa match em background. Aguardar.

Se após 24h continuar `<1.000`, verificar:
- Match rate baixo (qualidade da base) — ver `num_invalid_entries` / `num_received`
- Audience com `delivery_status.code != 200` — abrir Ads Manager pra detalhes

## Workflow não roda no cron

1. Conferir se está **ATIVO** (toggle no canto superior do editor)
2. Conferir trigger cron está com timezone `America/Sao_Paulo`
3. Ver execuções em `/workflow/{id}/executions` — erros aparecem com stack trace
4. Se `staticData.last_synced_at` parece travado, editar manualmente e forçar próxima execução

## Tokens vazaram

Se algum log/commit/screenshot expôs token:

1. Revogar token na origem (Clint, Meta, n8n)
2. Gerar novo
3. Atualizar MASTER.env
4. Atualizar Credentials no n8n
5. Reiniciar workflow

**Esta skill NÃO loga tokens** — qualquer aparição em log é bug a reportar.

