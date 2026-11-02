---
name: haos-n8n-api
description: "Referência interna pra operar o n8n da HAOS (Hetzner, n8n.${USER_BRAND}.com.br) via API REST e editar workflows programaticamente, endpoints, pegadinhas do PUT, HTTP Request node + OAuth/header auth, bugs de expressão, timeouts/estabilidade, infra Docker e backup/export. Use SEMPRE que a tarefa envolver n8n em qualquer forma, \"mexer no n8n\", \"editar/criar workflow\", \"adicionar node\", \"ativar/desativar fluxo\", \"webhook do n8n\", \"automação n8n\", \"o n8n travou\", \"credencial no n8n\", \"HTTP Request node não anexa o token\", \"listar execuções\", \"exportar workflows\", \"API do n8n\", \"PUT no workflow deu erro\", \"integrar X com n8n\". Padrões validados em produção (FPV369, Yampi, gerador de certificado) 05-18/06/2026."
---

# n8n (HAOS / Hetzner), API + edição de workflows

Como operar o n8n da casa via API REST e editar workflows sem redescobrir as pegadinhas (PUT read-only, HTTP node + OAuth, travamentos por timeout, encoding de URL). INTERNA, contém IDs/URLs internos, NÃO vai pro repo público HAOS_CC.

## Quando usar

Triggers do user:
- "editar/criar/duplicar workflow", "adicionar/trocar node", "ativar/desativar fluxo"
- "webhook do n8n", "automação n8n", "integrar [X] com n8n"
- "o n8n travou / está pendurado / não processa", "fila parada"
- "credencial no n8n", "HTTP Request não anexa token / credential prevent use"
- "listar/parar execuções", "exportar/backup dos workflows", "API do n8n"
- "PUT no workflow deu erro / campo read-only"

## Acesso

- **Base API:** `https://service.example.invalid` (env `N8N_API_URL`)
- **Auth:** header `X-N8N-API-KEY: <N8N_API_KEY>` (do MASTER.env, NUNCA hardcode)
- **UI:** mesmo host, login no painel
- **Infra:** Hetzner `root@example.invalid` (chave `_secrets/ssh/hetzner_ed25519`, SSH instável → comandos curtos e individuais)

```bash
# Smoke test (lista workflows)
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
     "$N8N_API_URL/api/v1/workflows?limit=5" | jq '.data[] | {id,name,active}'
```

> ⚠️ A API REST do n8n é a **Public API** (prefixo `/api/v1`). É diferente da API interna do editor (`/rest/...`, autenticada por cookie de sessão). Pra automação use SEMPRE `/api/v1` + `X-N8N-API-KEY`.

## Endpoints principais (Public API `/api/v1`)

| Método | Endpoint | Uso |
|---|---|---|
| `GET` | `/api/v1/workflows?limit=&active=` | listar workflows (paginado por `cursor`) |
| `GET` | `/api/v1/workflows/{id}` | pegar o JSON completo (nodes+connections+settings) |
| `POST` | `/api/v1/workflows` | criar workflow novo |
| `PUT` | `/api/v1/workflows/{id}` | **substituir** o workflow (ver pegadinhas) |
| `POST` | `/api/v1/workflows/{id}/activate` | ativar |
| `POST` | `/api/v1/workflows/{id}/deactivate` | desativar |
| `DELETE` | `/api/v1/workflows/{id}` | apagar |
| `GET` | `/api/v1/executions?status=&workflowId=&limit=` | listar execuções (`status`= success/error/waiting) |
| `GET` | `/api/v1/executions/{id}` | detalhe da execução (dados de cada node) |
| `POST` | `/api/v1/executions/{id}/stop` | cancela no DB (⚠️ pode não matar processo pendurado) |
| `GET` | `/api/v1/credentials` / `/credentials/schema/{type}` | credenciais (lista NÃO retorna o segredo) |
| `GET` | `/api/v1/tags` | tags de workflow |

Detalhes, paginação por cursor e exemplos em `references/api.md`.

## ⚠️ Editar workflow via PUT, pegadinhas (CRÍTICO)

A Public API **rejeita campos read-only** no `PUT /workflows/{id}`. O fluxo seguro:

1. **GET** o workflow → salvar **backup do JSON** antes de qualquer coisa:
   `_secrets\backups\wf_<slug>_<id>_<AAAA-MM-DD_HHMM>.json`
2. **Remover os campos read-only** do objeto antes do PUT:
   - top-level: `id`, `active`, `createdAt`, `updatedAt`, `tags`, `versionId`, `triggerCount`, `shared`, `meta`
   - dentro de `settings`: às vezes `binaryMode` / `availableInMCP` precisam sair
   - manter `settings.executionOrder: "v1"` (não remover, define ordem de execução)
3. PUT só com `name`, `nodes`, `connections`, `settings` (`staticData` opcional).
4. Mexer **só nos nodes necessários**, NÃO reescrever lógica/URL/método de nodes que não estão no escopo.
5. Ativar é endpoint separado (`/activate`), `active:true` no PUT é ignorado/rejeitado.

Erros típicos: `request/body must NOT have additional properties` (sobrou campo read-only) → tirar o campo citado e repetir. Helper pronto: `${USER_PROJECT_ROOT}/scripts/wf_edit.py` (GET+backup+sanitiza+PUT).

```bash
# Backup rápido de UM workflow antes de editar
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_URL/api/v1/workflows/${RESOURCE_ID}" \
  > "_secrets/backups/${RESOURCE_ID}$(date +%Y-%m-%d_%H%M).json"
```

## HTTP Request node, auth de credencial (a pegadinha mais comum)

**Erro "This credential is configured to prevent use within an HTTP Request node"** (ou 401 `CREDENTIALS_MISSING`):

- **Causa:** (a) credencial OAuth2 genérica marcada pra não permitir uso em HTTP Request; **e/ou** (b) HTTP Request node em `typeVersion 1` (legado), a v1 **NÃO anexa o token OAuth** mesmo com `predefinedCredentialType` (bug n8n #14020/#12230).
- **Fix (validado no `${RESOURCE_ID}`):**
  1. `authentication: "predefinedCredentialType"` + `nodeCredentialType: "<tipo>"` apontando pra uma credencial já autorizada. Ex.: Google → `${RESOURCE_ID}` (escopo `auth/drive` cobre Slides batchUpdate + Drive export). **NÃO** usar OAuth2 genérico.
  2. Subir o node de `typeVersion 1` → **`4.2`+**, migrando params legados (`requestMethod/jsonParameters/bodyParametersJson` → `method/sendBody/specifyBody:json/jsonBody`). NÃO alterar URL/método/lógica.
  3. Node **nativo** (ex.: `googleDrive` "Copiar Modelo") NÃO sofre esse erro, só HTTP Request.
- **API com header** (ex.: Clint `api-token`, qualquer Bearer): credencial tipo **`httpHeaderAuth`** (`authentication: "predefinedCredentialType"` + `nodeCredentialType: "httpHeaderAuth"`). **NUNCA** hardcode o token no node/expressão.

## Bugs comuns de expressão / encoding

Para integrações de voz, validar o parser da versão instalada e a persistência
do identificador de chamada antes de diagnosticar tools como problema de prompt.
Procedimento: validação n8n/voz (dependency not bundled: ../../../playbooks/n8n-voice-runtime-validation.md).

- **URL começando com `=https://...`**: o `=` extra faz o n8n tratar a string inteira como **expressão** e quebra. **Remover o `=`** do começo da URL (ou da string que vira a URL).
- **Email/strings com `+` ou char especial em query string**: `?email=test+x@dominio` → o `+` vira espaço no servidor (form-urlencoded) e o match falha. **Usar `sendQuery: true` + `queryParameters` estruturado** (o n8n encoda `+`→`%2B`) em vez de concatenar na URL. Validado 17/06 no `${RESOURCE_ID}` (lookup Clint por email). Vale pra QUALQUER param com `+`/espaço/char especial.
- Em geral: prefira params/headers/body **estruturados** (toggles `sendQuery`/`sendHeaders`/`sendBody`) a montar strings na mão.

## Timeouts & estabilidade (causa nº 1 de travamento)

Travamento clássico: HTTP node **sem timeout** pendura o worker → a execução fica `running` pra sempre → bloqueia a fila (Bull/Redis) → o fluxo (e às vezes o n8n inteiro) "para".

- **Por node:** setar `options.timeout = 30000` (30s) em TODO HTTP Request node. (Resolveu o `[Yampi] Todos Eventos`, 42 HTTP nodes.)
- **Global (env do container):** `EXECUTIONS_TIMEOUT=600` + `EXECUTIONS_TIMEOUT_MAX=3600`. Healthcheck no `n8n-worker`.
- **Destravar fila travada:** `docker restart n8n-worker` (mata o processo pendurado e libera a fila). `POST /executions/{id}/stop` marca cancelado no DB mas **pode não matar** o processo já pendurado.
- Diagnóstico: `GET /executions?status=running` (ou `waiting`) → se acumula, fila travada.

## Infra (Hetzner)

- Containers: **`n8n`** (UI + main) + **`n8n-worker`** (executor da fila). Stack em **`${HAOS_PRIVATE_ROOT}`** (docker-compose).
- Banco: container **`postgres`** (user `admin`, db `n8n`). Fila: **Redis** (Bull). Roteado pelo **Traefik** (n8n via Traefik direto, NÃO via tunnel).
- `N8N_ENCRYPTION_KEY` (criptografa as credenciais) está no MASTER.env + cofre Bitwarden, **fora do pacote de backup**. Trocar a key = perder todas as credenciais.
- SSH instável → comandos curtos e individuais (ver `project_hetzner_server_map` / skill `haos-hetzner-map` antes de mexer no servidor).

## Backup / export de workflows

```bash
# Exporta TODOS os workflows (1 arquivo por workflow, nomeado por id)
docker exec n8n n8n export:workflow --backup --output=/tmp/wf_backup
# Exporta UM workflow
docker exec n8n n8n export:workflow --id=${RESOURCE_ID} --output=/tmp/wf.json
# Credenciais (vêm CRIPTOGRAFADAS, precisam da N8N_ENCRYPTION_KEY pra restaurar)
docker exec n8n n8n export:credentials --backup --output=/tmp/cred_backup
```

- Backup automatizado: `${HAOS_PRIVATE_ROOT}` (cron semanal dom 03:30 BRT) → 29 wf JSON + 14 cred + dump banco → Drive pasta **N8N**. DR testado (RTO ~10min). Runbook `${HAOS_PRIVATE_ROOT}`. Detalhes na memória `project_backup_system.md`.
- Antes de editar via API, sempre salvar o JSON local (ver seção PUT).

## Padrão de teste (não disparar produção real)

1. Disparar o webhook de **produção** com **payload mock** (email/telefone fake, ex.: `contact@example.invalid`).
2. Conferir o resultado no **destino** (CRM/planilha/DB), não confiar só no "200 OK" do n8n.
3. **Limpar os dados de teste** no destino (DELETE do contato/deal/linha criados).

## Regra: troca de senha Google revoga TODOS os tokens OAuth

Trocar a senha de uma conta Google **revoga todos os refresh tokens** dela → quebram **todas** as credenciais OAuth no n8n (Gmail / Drive / Sheets / Slides) **e** o rclone do backup off-site. Já aconteceu 2x com `contact@example.invalid`.

**Ação proativa após qualquer troca de senha Google:**
- Reconectar no n8n cada credencial Google da conta (Credentials → abrir → "Reconnect"/"Connect my account" → login → Permitir → Save) e re-disparar o fluxo.
- Reautorizar o rclone do backup (ver `project_backup_system.md`).

Refs cruzadas: memórias `learning_n8n_google_oauth` e `project_backup_system`.

## Workflows-chave conhecidos

| Workflow | ID | Notas |
|---|---|---|
| `[Assiny] Todos Eventos` | `${RESOURCE_ID}` | Switch por produto; branch FPV369 → Clint via API REST direta |
| `[Yampi] Todos Eventos` | (ver painel) | 42 HTTP nodes; timeout 30s aplicado (anti-travamento) |
| Gerador de Certificado Practitioner PNL | `${RESOURCE_ID}` | HTTP node Google Slides/Drive (fix OAuth predefinedCredentialType + v4.2) |
| `[PDM] Lia Order Finished -> ActiveCampaign` | `${RESOURCE_ID}` | webhook Lia → AC lista Alunos + tag |
| Polling Clint → Meta Custom Audience | `${RESOURCE_ID}` | base de duplicação p/ `clint-meta-audience-sync` (cron 30min) |
| `[Whatsapp] Bloquear/Voltou Contato` | (ver painel) | automação WhatsApp/Evolution |

(IDs internos, usar como ponto de partida; confirmar nome/estado atual no painel antes de editar.)

## Restrições/segurança

- **NUNCA** hardcode token/segredo em node, expressão, log ou screenshot, sempre credencial do n8n (`httpHeaderAuth`/OAuth) ou env.
- `N8N_API_KEY` e `N8N_ENCRYPTION_KEY` só do MASTER.env (referenciar por nome).
- Sempre backup do JSON antes de PUT/DELETE.

## Skills/refs relacionadas

- `clint-api`, quando o workflow fala com o Clint (cliente Python + pegadinhas da API).
- `haos-hetzner-map` (carregar antes de mexer no servidor).
- Memórias: `learning_n8n_google_oauth`, `project_backup_system`, `project_assiny_clint_fpv369`, `project_hetzner_server_map`.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
