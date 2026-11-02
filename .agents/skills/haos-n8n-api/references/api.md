# n8n Public API (`/api/v1`), detalhes

Base: `$N8N_API_URL` = `https://service.example.invalid`
Auth: header `X-N8N-API-KEY: $N8N_API_KEY` (MASTER.env). Sempre `accept: application/json`.

> Public API = `/api/v1`. NÃO confundir com a API interna do editor (`/rest/...`, cookie de sessão). Automação usa só `/api/v1`.

## Paginação (cursor)

A Public API pagina por **cursor**, não por `page`:

```json
{ "data": [ ... ], "nextCursor": "abc123" }
```

- Pedir próxima página: `?cursor=<nextCursor>`. Acabou quando `nextCursor` é `null`/ausente.
- `limit` (default 100, máx 250 conforme versão).

```bash
cursor=""
while :; do
  resp=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_API_URL/api/v1/workflows?limit=100${cursor:+&cursor=$cursor}")
  echo "$resp" | jq -r '.data[] | "\(.id)\t\(.active)\t\(.name)"'
  cursor=$(echo "$resp" | jq -r '.nextCursor // empty')
  [ -z "$cursor" ] && break
done
```

## WORKFLOWS

### `GET /api/v1/workflows`
Params: `active=true|false`, `tags=`, `name=`, `limit=`, `cursor=`, `excludePinnedData=true`.
Resposta `data[]`: `id`, `name`, `active`, `nodes`, `connections`, `settings`, `createdAt`, `updatedAt`, `versionId`, `triggerCount`, `tags`.

### `GET /api/v1/workflows/{id}`
JSON completo (nodes + connections + settings + staticData). É o que se edita.

### `POST /api/v1/workflows`
Cria. Body aceita `name`, `nodes`, `connections`, `settings`. `active` NÃO entra aqui (ativar é endpoint próprio).

### `PUT /api/v1/workflows/{id}`, substitui o workflow
⚠️ **Rejeita campos read-only.** Mandar SÓ: `name`, `nodes`, `connections`, `settings` (`staticData` opcional).

Remover antes do PUT:
- top-level: `id`, `active`, `createdAt`, `updatedAt`, `tags`, `versionId`, `triggerCount`, `shared`, `meta`, `pinData` (se a versão recusar)
- `settings`: às vezes `binaryMode`, `availableInMCP` (remover se o erro citar)
- **manter** `settings.executionOrder: "v1"`

Erro `request/body must NOT have additional properties` = sobrou campo read-only → tirar o campo citado e repetir. Use `${USER_PROJECT_ROOT}/scripts/wf_edit.py`.

### Ativar / desativar
`POST /api/v1/workflows/{id}/activate` · `POST /api/v1/workflows/{id}/deactivate`.
`active:true` dentro do PUT é ignorado/recusado, ativar é sempre por este endpoint.

### `DELETE /api/v1/workflows/{id}`
Apaga. Backup do JSON antes.

## EXECUTIONS

### `GET /api/v1/executions`
Params: `status=success|error|waiting`, `workflowId=`, `includeData=true|false`, `limit=`, `cursor=`.
- `status=waiting`/execuções `running` que acumulam = **fila travada** (ver SKILL → Timeouts).

### `GET /api/v1/executions/{id}`
Detalhe (com `includeData=true` traz a saída de cada node, útil pra debug).

### `POST /api/v1/executions/{id}/stop`
Cancela no DB. ⚠️ Pode **não matar** um processo já pendurado no worker, pra esse caso, `docker restart n8n-worker`.

### `DELETE /api/v1/executions/{id}`
Apaga registro de execução.

## CREDENTIALS

### `GET /api/v1/credentials`
Lista credenciais, **NÃO retorna o segredo** (só metadados: id, name, type).

### `GET /api/v1/credentials/schema/{credentialTypeName}`
Schema dos campos de um tipo de credencial (ex.: `httpHeaderAuth`, `${RESOURCE_ID}`).

### `POST /api/v1/credentials`
Cria credencial. Body conforme o schema do tipo. O valor é criptografado com `N8N_ENCRYPTION_KEY`.
⚠️ Credencial OAuth Google **não** dá pra autorizar 100% por API (o consentimento é interativo no browser), criar/reconectar pelo painel.

## TAGS
`GET/POST /api/v1/tags`, `GET/PUT/DELETE /api/v1/tags/{id}`, tags de organização dos workflows.

## Webhooks
- Webhook de **produção**: `$N8N_API_URL/webhook/<path>` (fluxo ATIVO).
- Webhook de **teste**: `$N8N_API_URL/webhook-test/<path>` (só dispara com o editor em "Listen for test event").
- Disparar produção com payload mock pra testar (ver SKILL → Padrão de teste). Limpar dados de teste no destino depois.

## Erros comuns
| Sintoma | Causa | Fix |
|---|---|---|
| 401 | header errado/key inválida | `X-N8N-API-KEY` (não Bearer), key do MASTER.env |
| 404 em `/api/v1/...` | Public API desabilitada ou path errado | conferir `N8N_PUBLIC_API_DISABLED` no container; usar `/api/v1` |
| `must NOT have additional properties` no PUT | campo read-only no body | sanitizar (ver wf_edit.py) |
| execução fica `running` pra sempre | HTTP node sem timeout | `options.timeout=30000` + `docker restart n8n-worker` |

