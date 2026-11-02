---
name: google-cloud
description: "Procedimento especializado de google-cloud; consultar requisitos e evidencias antes de executar."
---

# Google Cloud (guarda-chuva HAOS)

O hub de autenticacao e servicos Google do grupo. Quando a tarefa toca Google e NAO
e Ads, GTM ou GA4, comeca por aqui: decide a conta certa, o modo de auth certo e o
servico certo, sem nunca expor segredo.

## Guardrails (ler antes de agir)

- Segredo so por NOME de variavel. Nunca imprima, cole, mascare ou commite client
  secret, refresh token, access token, SA JSON, senha ou cookie.
- Fonte unica de segredo = `MASTER.env`:
  `${HAOS_PRIVATE_ROOT}`
- Leitura (Drive/Sheets) = executar direto. Escrita externa irreversivel (criar/mover/
- Skill INTERNA (`~/.Codex/skills`). Nunca vai pro repo publico HAOS_CC.

## Mapa das contas Google do grupo

| Conta | Dono / uso | Observacao |
|---|---|---|
| `contact@example.invalid` | Conta SIM. Dona do projeto GCP `${USER_BRAND}`, do Drive de operacao, do OAuth `GOOGLE_GTM_*` | **Sem o "s"** em "transforma" - e assim mesmo, nao corrigir |
| `contact@example.invalid` | Conta Edson (marca pessoal) | NAO criar recurso de operacao aqui - ver pegadinha cross-account |

Regra pratica: para operacao (Drive de revisao, planilhas, backup) a conta padrao e

## Os 2 modos de autenticacao (e quando usar cada um)

### A) OAuth 2.0 (client id + secret + refresh token)
Age **como um usuario humano** (a conta dona). Use quando o recurso precisa pertencer
a uma conta de pessoa: criar/ler arquivo no **Drive pessoal** da simtranforma, mandar
**Gmail**, formatar **Docs**. Service account NAO consegue escrever no Drive/Gmail de
conta pessoal (Gmail comum nao tem domain-wide delegation) - por isso operacao de Drive
da simtranforma e sempre OAuth.

Variaveis no MASTER.env (conta simtranforma):
- `GOOGLE_GTM_CLIENT_ID`
- `GOOGLE_GTM_CLIENT_SECRET`
- `GOOGLE_GTM_REFRESH_TOKEN`

> Nota de nome: a familia chama `GOOGLE_GTM_*` por origem historica (foi criada no
> contexto GTM), mas o **escopo e `drive` completo** (nao so `drive.file`), entao serve
> de credencial OAuth geral de Drive/Docs/Sheets da simtranforma. TODO: confirmar ao
> vivo se existe uma familia `GOOGLE_OAUTH_*` separada ou se `GOOGLE_GTM_*` e a unica.

Trocar refresh token por access token:
```
POST https://oauth2.googleapis.com/token
client_id=$GOOGLE_GTM_CLIENT_ID
client_secret=$GOOGLE_GTM_CLIENT_SECRET
refresh_token=$GOOGLE_GTM_REFRESH_TOKEN
grant_type=refresh_token
```
Resposta tem `access_token` (vale ~1h). Use no header `Authorization: Bearer <token>`.

O consent screen do OAuth do projeto `${USER_BRAND}` esta **"Em producao"** (nao aplica a
expiracao de 7 dias do modo Testing). Isso nao torna o refresh token eterno: senha
trocada, revogacao manual, inatividade, limite de tokens e politicas de sessao ainda
podem invalida-lo.

**Regra de isolamento de escopos:** refresh token operacional de Drive/Docs/Sheets/
GTM/GA4/Search Console nao deve incluir `cloud-platform`. Esse escopo sujeita o token
ao controle de duracao de sessao do Google Cloud/Workspace e pode produzir
`invalid_grant` com `invalid_rapt`. Infraestrutura GCP deve usar credencial separada,
preferencialmente service account/ADC com menor privilegio. O procedimento completo
esta em `references/google-oauth-refresh-lifecycle-playbook.md`.

### B) Service Account (JSON key)
Age **como uma identidade de robo**, sem humano no loop. Use para automacao
server-to-server e para acessar recursos que a SA possui ou que foram **compartilhados
com o email da SA**: jobs no Hetzner, rclone de backup, escrita em Shared Drive, leitura
de planilha compartilhada com a SA.

Service account conhecida (projeto `${USER_BRAND}`, usada no backup/rclone de Drive):
- `GCP_SIM_MAKE_PROJECT` - id do projeto GCP
- `GCP_SIM_MAKE_CLIENT_EMAIL` - email da SA (e o que voce compartilha na planilha/pasta)
- `GCP_SIM_MAKE_SA_JSON` - chave JSON inteira (NUNCA imprimir)

Limite importante (aprendido no backup): a SA **nao escreve** no Drive/Gmail pessoal da
simtranforma. Por isso o remote `gdrive_sa:` foi descartado e o backup ficou no
`gdrive_oauth:` (OAuth). Para SA escrever, o destino tem que ser um Shared Drive ou
pasta explicitamente compartilhada com `GCP_SIM_MAKE_CLIENT_EMAIL`.

### Qual escolher (regra de 1 linha)
- Recurso e de conta de pessoa (Drive/Gmail/Docs da simtranforma)? -> **OAuth**.
- Automacao headless / Shared Drive / recurso compartilhado com a SA? -> **Service Account**.

## Servicos Google e ponteiros

| Servico | Como acessar | Skill dedicada |
|---|---|---|
| **Drive** | OAuth (conta pessoal) ou SA (Shared Drive) | esta skill |
| **Sheets** | Sheets API v4 (mesmo token) | esta skill |
| **Docs** | Docs API v1 (`batchUpdate`) | esta skill (ver fluxo de revisao) |
| **Gmail** | OAuth da conta (SA nao serve em Gmail pessoal) | esta skill (auth) |
| Google Ads | API de Ads + developer token (MCC) | `haos-google-ads-gtm-api` |
| Google Tag Manager | GTM API | `haos-google-ads-gtm-api` |
| GA4 / Analytics Data API | GA4 Data API | `ga4` |

Para Ads/GTM/GA4, **NAO** reimplemente aqui - carregue a skill dedicada. Esta skill so
resolve a camada de auth comum e os servicos genericos (Drive/Sheets/Docs/Gmail).

> No Codex.ai / MCP: pode existir conector de Drive/Sheets/Docs ja plugado (ver comando
> `/ler-drive`). Quando o conector MCP estiver disponivel, prefira ele a montar a chamada
> REST na mao. A auth via MASTER.env e o caminho para Codex / scripts.

## Drive e Sheets na pratica

### Ler uma planilha (Sheets API v4)
```
GET https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}
Authorization: Bearer <access_token>
```
`range` ex: `A1:Z100` ou `'Nome da Aba'!A:D`. Para descobrir as abas:
`GET https://sheets.googleapis.com/v4/spreadsheets/{id}?fields=sheets.properties`.

### Ler/baixar um arquivo do Drive
```
GET https://www.googleapis.com/drive/v3/files/{fileId}?fields=id,name,mimeType
GET https://www.googleapis.com/drive/v3/files/{fileId}?alt=media        (binario)
```
Google Doc/Sheet nativo nao baixa com `alt=media` - exporta:
`GET https://www.googleapis.com/drive/v3/files/{fileId}/export?mimeType=...`.

### Criar pasta / arquivo no Drive
```
POST https://www.googleapis.com/drive/v3/files?supportsAllDrives=true
{ "name": "...", "mimeType": "application/vnd.google-apps.folder", "parents": ["<parentId>"] }
```
Para upload com conteudo use `POST https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true` (metadata + corpo).

### Setar permissao (link)
```
POST https://www.googleapis.com/drive/v3/files/{id}/permissions?supportsAllDrives=true
{ "role": "commenter", "type": "anyone" }
```

## Pasta Drive padrao de revisao (regra GLOBAL)

Toda copy de disparo / doc aguardando revisao vai para:
- **Pasta:** `${RESOURCE_ID}` ("Revisão")
- **Conta:** `contact@example.invalid` (criar DIRETO nela, ver pegadinha abaixo)
- **Permissao:** `anyone with link = commenter`
- **Auth:** OAuth `GOOGLE_GTM_*`
- **Titulo:** `[Tipo], [Descricao], DD-MM-AAAA`
- **Conteudo:** abrir com bloco "Instrucoes pro revisor" + criterios

Fluxo completo (token -> criar doc -> formatar -> permissao) esta documentado e usa
Docs API `batchUpdate` para negrito/titulos. Esse e o caminho canonico de "manda pra
revisao".

## PEGADINHA CRITICA: cross-account da 404

NUNCA crie um arquivo na conta `contact@example.invalid` (Edson) e tente mover via
API para a pasta da simtranforma. Mesmo com as contas compartilhadas, o GET no arquivo
movido retorna **404** (cross-account). **Sempre criar direto na conta destino**
(simtranforma) com o token dela. Vale para qualquer recurso de operacao, nao so a pasta
de revisao.

## LICAO CRITICA: trocar a senha Google revoga TODOS os tokens OAuth

refresh tokens OAuth daquela conta**. Ja aconteceu 2x com `contact@example.invalid`:
quebrou o rclone do backup off-site e a credencial Gmail do n8n (a quebra so apareceu
quando o fluxo precisou enviar, semanas depois).

Sintomas de credencial morta: `invalid_grant`, `401`, "Token has been expired or revoked",
backup off-site parou, Gmail/Drive do n8n falhando. Se a descricao trouxer
`invalid_rapt`, investigar primeiro controle de sessao e presenca de `cloud-platform`;
nao presumir modo Testing nem mandar publicar o app sem verificar o tipo de audiencia.

Acao proativa **toda vez que uma senha Google for trocada**:
1. Reconectar no n8n TODAS as credenciais Google daquela conta (Gmail/Drive/Slides/Sheets).
2. Reautorizar o rclone do backup (ver skill/memoria de backup).
3. Regerar o `GOOGLE_GTM_REFRESH_TOKEN` (re-consent OAuth) e atualizar o MASTER.env -> rodar o sync-secrets.

producao" + alerta WhatsApp para detectar a quebra cedo.

### n8n + Google OAuth (HTTP Request node)
Se um node HTTP Request der "This credential is configured to prevent use within an HTTP
Request node" ou `401 CREDENTIALS_MISSING` ao chamar API Google:
1. Node HTTP: `authentication: predefinedCredentialType` + `nodeCredentialType:
   ${RESOURCE_ID}` (escopo `auth/drive` cobre Drive/Sheets/Slides) apontando para
   credencial Google ja autorizada.
2. Atualizar o node de `typeVersion 1` (legado, nao anexa o token - bug n8n) para `4.2`.
3. Node nativo (`googleDrive`) nao sofre esse bug, so o HTTP Request.

## Saida esperada

- **Auth:** access token obtido (em memoria/var, nunca impresso) ou diagnostico claro da
  credencial quebrada com o passo de reconexao.
- **Leitura Drive/Sheets:** o dado pedido, em tabela/resumo.
  certa (simtranforma) + permissao aplicada.
- **Sempre:** zero segredo no output; so nome de variavel.

## TODOs (confirmar ao vivo no MASTER.env)

- [ ] Nomes EXATOS das variaveis OAuth gerais: `GOOGLE_GTM_CLIENT_ID/SECRET/REFRESH_TOKEN`
      e se existe familia `GOOGLE_OAUTH_*` ou `GOOGLE_CLOUD_*` separada.
- [ ] Nomes EXATOS da service account: `GCP_SIM_MAKE_PROJECT / _CLIENT_EMAIL / _SA_JSON`.
- [ ] ID/nome canonico do projeto GCP (`${USER_BRAND}`) e se ha outro projeto alem dele.
- [ ] Escopos OAuth realmente concedidos no client `${USER_BRAND}` (confirmado `drive`; checar
      `spreadsheets`, `gmail`, `docs`).
- [ ] Se ha conector MCP de Drive/Sheets ativo na sessao (alternativa ao REST).

## Playbooks

- `references/google-oauth-refresh-lifecycle-playbook.md` — diagnostico de
  `invalid_grant`/`invalid_rapt`, separacao de escopos, rotacao segura, propagacao no
  n8n e validacao sem expor segredos.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
