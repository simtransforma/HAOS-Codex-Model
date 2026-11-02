---
name: cloudflare
description: "Operar a conta Cloudflare do grupo (${USER_BRAND}): autenticar token, listar zonas, ler/criar/editar registro DNS, pegar Zone ID, configurar Bot Fight Mode, Access e Tunnel. Use SEMPRE que o usuário pedir \"mexer no DNS\", \"criar/editar registro CNAME ou A\", \"pegar o zone id de um domínio\", \"validar o token Cloudflare\", \"extrair os DNS de um domínio\", \"ligar o Bot Fight Mode\", \"apontar subdomínio pro Hetzner/Lovable/Stape\", \"configurar rota de Worker\", \"quem tem acesso pelo Cloudflare Access\". Também aciona implicitamente quando a tarefa de tracking, migração de site, túnel ou deploy depende de um registro DNS ou de um Zone ID do grupo, mesmo sem citar \"Cloudflare\". NÃO pule esta skill quando for tocar em qualquer DNS dos domínios do grupo: o token e os escopos têm pegadinhas que já custaram tempo (ver §1 e §2).\n"
---

# Cloudflare (conta do grupo)

Operação da conta Cloudflare do grupo ${USER_BRAND} via API v4: validar token, listar zonas, ler/criar/editar DNS, Bot Fight Mode, Access e Tunnel. Esta skill é INTERNA: cita Zone IDs e domínios, mas NUNCA o valor de token (refira sempre por nome de variável do MASTER.env).

Pegadinhas críticas estão em §1 (token `cfat_`) e §2 (escopos). Não improvise: elas já custaram tempo.

---

## Conta e credenciais

- Conta principal (login `contact@example.invalid`): account ID em `CLOUDFLARE_ACCOUNT_ID` = `${RESOURCE_ID}`. Tem **5 zonas** e cerca de **167 web hosts** (registros A/AAAA/CNAME).
- Token da API na variável `CLOUDFLARE_API_TOKEN` (token all-zones do HAOS, escopo de zona). Há também `CLOUDFLARE_API_TOKEN_HAU` para o outro login.
- `service.example.invalid` NÃO está nesta conta: vive em OUTRO login Cloudflare (subdomínios tipo `conhecer.`, `nike-wk.` apontam pra lá). Não procurar nas 5 zonas abaixo; usar o token/login do HAU.
- Carregar o MASTER.env antes de qualquer chamada (caminho em `project_credentials.md`):
  ```bash
  set -a && source "${HAOS_PRIVATE_ROOT}" && set +a
  ```

### Tabela de Zone IDs (conta principal)

| Domínio | Zone ID | Variável MASTER.env |
|---|---|---|
| ${USER_BRAND}.com.br | `${RESOURCE_ID}` | `CLOUDFLARE_<dominio>_ZONE_ID` |
| service.example.invalid | `${RESOURCE_ID}` | idem |
| editoramindset.com.br | `${RESOURCE_ID}` | idem |
| service.example.invalid | `${RESOURCE_ID}` | idem |
| sociedadeinternacionaldomindset.com | (puxar via `GET /zones?name=...`) | idem |

> Os Zone IDs ficam no MASTER.env como `CLOUDFLARE_<dominio>_ZONE_ID` (ex: `CLOUDFLARE_${USER_BRAND}_ZONE_ID`). Se em dúvida, listar via API (§2) em vez de chutar.

---

## 1. Autenticar e validar o token (PEGADINHA)

Tokens novos do Cloudflare têm prefixo **`cfat_`** (cerca de 53 chars). Eles **retornam `code 1000 Invalid API Token` no endpoint `/user/tokens/verify` mesmo quando são válidos.** NÃO declarar um token inválido só porque o `/verify` reclamou.

Validação correta: bater num recurso real e checar `success: true`.

```bash
# ERRADO pra cfat_ (dá falso negativo):
# curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"

# CERTO: bater em /zones
curl -s "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" | python -c "import sys,json;d=json.load(sys.stdin);print('OK' if d.get('success') else d.get('errors'))"
```

Autenticação em toda chamada: header `Authorization: Bearer $CLOUDFLARE_API_TOKEN`. Base da API pública: `https://api.cloudflare.com/client/v4`.

---

## 2. Escopos: `Zone:Read` NÃO é `DNS:Read` (PEGADINHA)

- Listar zonas (`GET /zones`) e ler detalhe da zona (`GET /zones/{id}`) = permissão **`Zone Read`**.
- Listar/editar **DNS records** (`/zones/{id}/dns_records`) = permissão **`DNS`** na seção **Zone**. Faltando ela, o erro é `10000 Authentication error`.
- A categoria "DNS & Zones" da UI nova de token (Account DNS Settings, DNS Firewall, DNS View, Registrar) NÃO inclui o `DNS Records`. A permissão certa chama-se só **`DNS`** (seção Zone).
- À prova de erro ao criar token novo: template **"Read all resources"** (já vem com DNS Read + todas as zonas). No Cloudflare, **`Edit` inclui `Read`** pra mesma permissão.

### Listar zonas e achar o Zone ID

```bash
# Todas as zonas (id + nome + status):
curl -s "https://api.cloudflare.com/client/v4/zones?per_page=50" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  | python -c "import sys,json;[print(z['id'],z['name'],z['status']) for z in json.load(sys.stdin)['result']]"

# Zone ID de um domínio específico:
curl -s "https://service.example.invalid" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  | python -c "import sys,json;print(json.load(sys.stdin)['result'][0]['id'])"
```

---

## 3. Ler registros DNS

```bash
ZONE=${RESOURCE_ID}   # ${USER_BRAND}.com.br
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records?per_page=100" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  | python -c "import sys,json;[print(r['type'],r['name'],'->',r['content'],'proxied' if r['proxied'] else 'dns-only') for r in json.load(sys.stdin)['result']]"
```

Paginar com `&page=N` quando a zona tiver mais de 100 records (${USER_BRAND} tem cerca de 188). Filtrar por tipo com `&type=A` ou por nome com `&name=sub.dominio.com.br`.

IPs de referência do grupo (para reconhecer destinos ao ler DNS): Lovable `example.invalid`, Stape `sad.stape.io`, Hetzner `example.invalid`, hosting-legacy/cPanel `example.invalid`, Abacus `sites.abacusai-cdn.net`, túnel CF `*.cfargotunnel.com`, Railway `*.up.railway.app`.

---

## 4. Criar registro DNS

`POST /zones/{id}/dns_records`. Campos: `type`, `name` (subdomínio ou `@` pra raiz), `content`, `ttl` (1 = automático), `proxied` (true = laranja/CDN, false = cinza/dns-only).

```bash
ZONE=${RESOURCE_ID}
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"CNAME","name":"novo","content":"alvo.exemplo.com","ttl":1,"proxied":true}'
```

Regra de proxy: páginas/sites que querem CDN+WAF da Cloudflare = `proxied:true`. Túnel, validação de SSL externo, Stape/sGTM e qualquer destino que exija IP/origem direta = `proxied:false` (cinza). Na dúvida em registro de tracking, manter `dns-only`.


---

## 5. Editar e apagar registro DNS

Precisa do `record_id`. Pegar listando (§3, cada item tem `id`) ou filtrando por `&name=`.

```bash
ZONE=${RESOURCE_ID}
REC=<record_id>

# Editar (PATCH atualiza só os campos enviados; PUT exige o objeto inteiro):
curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records/$REC" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"content":"example.invalid","proxied":true}'

# Apagar:
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records/$REC" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

Preferir `PATCH` a `PUT` pra não zerar campos por engano.

---

## 6. Truque: extrair DNS SEM token, pela sessão logada do Chrome


`https://dash.cloudflare.com/api/v4/zones/{zone_id}/dns_records?per_page=100&page=N`

Via Chrome MCP (`javascript_tool`), rodar um `fetch` same-origin (a aba PRECISA estar em `dash.cloudflare.com`). O REPL do `javascript_tool` NÃO aceita top-level await e não devolve payload grande. Padrão que funciona:

1. Num call: `(async () => { const r = await fetch('https://dash.cloudflare.com/api/v4/zones/'+ZID+'/dns_records?per_page=100'); window.__x = await r.json(); })()` (sem `return`, sem await no topo).
2. No call seguinte: ler `window.__x`.
3. Pra payload grande: escrever em `document.body` e ler com `get_page_text` (aguenta mais que o retorno do `javascript_tool`).

Isso varre todas as zonas/páginas sem depender de token. Bom como fallback ou auditoria.

---

## 7. Bot Fight Mode (PENDENTE nos 4 domínios)

Pendência aberta: ligar o Bot Fight Mode nos 4 domínios principais (${USER_BRAND}.com.br, service.example.invalid, editoramindset.com.br, service.example.invalid).

```bash
# Ler estado:
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE/bot_management" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```


---

## 8. Tunnel e Access (contexto)

- **Tunnel:** `claw.${USER_BRAND}.com.br` aponta para `localhost:18789` (painel OpenClaw via Cloudflare Tunnel). Registros de túnel aparecem como CNAME pra `*.cfargotunnel.com`.
- **Worker routes:** tocar em rota de Worker (ex: `${USER_BRAND}-router`) exige token com permissão de ZONA (DNS + Workers Routes), não basta account-level. O token all-zones do HAOS (`CLOUDFLARE_API_TOKEN`) resolve.

---

## 9. Codex + MCP oficial da Cloudflare (OAuth)

Quando a operação ocorrer pelo Codex, preferir o MCP oficial autenticado por OAuth. Instalar ou habilitar o plugin da Cloudflare **não prova** que a conexão MCP está autenticada nem que as ferramentas remotas foram carregadas.

Fluxo seguro:

1. Confirmar que a conexão aponta para `https://mcp.cloudflare.com/mcp`.
2. Executar o login OAuth pelo CLI atual do Codex.
3. Se uma versão antiga do CLI falhar no callback com erro de emissor (`missing required issuer`), não insistir no mesmo binário: repetir com uma versão atual e compatível do CLI.
4. Reiniciar o aplicativo ou a tarefa do Codex após autenticar, pois o catálogo de ferramentas MCP é carregado no início da sessão.
5. Confirmar que as ferramentas da API Cloudflare aparecem antes de concluir que a integração está pronta.

Para mutações DNS, aplicar sempre o ciclo idempotente:

1. Descobrir no MCP o endpoint exato da operação.
2. Ler a zona e consultar o hostname exato antes de alterar.
3. Bloquear a execução se houver registro conflitante ou mais de uma correspondência inesperada.
4. Criar somente quando não existir; atualizar somente quando a identidade do registro estiver confirmada.
5. Exigir `success: true` e fazer nova leitura do registro.
6. Verificar externamente resolução DNS e HTTPS, sem tratar a resposta da API como prova suficiente do serviço final.

OAuth evita manipular o token bruto durante a operação. Nunca registrar em memória, relatório, log ou commit valores de token, senha, record ID, Zone ID, IP de origem ou inventário de hosts.

Playbook detalhado: `references/codex-mcp-dns-playbook.md`.

---

## Saída esperada

Conforme o pedido:
- **Validação de token:** dizer válido/inválido + por qual endpoint testou (`/zones`, nunca `/verify` pra `cfat_`).
- **Zone ID / listagem:** o(s) ID(s) + nome + status, em tabela.
- **Leitura de DNS:** lista `tipo | nome | conteúdo | proxied/dns-only`, paginada se preciso.
- **Criação/edição/remoção:** mostrar o JSON da mudança ANTES, esperar OK, executar, confirmar com a resposta `success:true` da API.

Nunca imprimir o valor do token nem de qualquer segredo: referir só pelo nome da variável do MASTER.env.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
