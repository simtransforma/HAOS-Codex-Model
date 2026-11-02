# Clint API, Troubleshooting

<!-- synthetic-client-examples -->
Exemplos sinteticos: nomes de campanha, contatos, IDs, valores e configuracoes abaixo sao ficticios, nao um inventario de cliente nem evidencia de producao. Adaptar IDs e slugs ao contrato autorizado; conferir a versao da API e o resultado antes de qualquer efeito externo.


Bugs/pegadinhas conhecidos da API do Clint + soluções validadas em produção.

Quando aparecer problema novo, **registre aqui** pra próxima vez não perder tempo.

---

## 1. `?search=` em /tags retorna 100 tags aleatórias (não filtra)

**Sintoma:** chamada `GET /tags?search=${RESOURCE_ID}` retorna 100 tags totalmente não relacionadas ao termo buscado.

**Causa-raiz:** o parâmetro `search` está implementado errado (provavelmente faz nada e retorna `?page=1&limit=100`). Não é bug de tipo/case, é bug funcional.

**Cenario de teste:** colocar uma tag sintetica em pagina posterior da listagem e comparar a busca direta com a paginacao completa. Nao presumir que a primeira pagina contenha o resultado.

**Solução:**

```python
# Errado (pode não achar):
r = client.get("/tags", params={"search": "example-search"})

# Certo (paginação completa + filtro client-side):
tag = client.find_tag_by_name("example-tag")
```

A `ClintClient.find_tag_by_name()` já implementa: tenta search primeiro (rápido se rolar a sorte), depois pagina tudo.

**Impacto em workflow n8n:** se você usar HTTP Node em vez do client Python, **NÃO confie em search**. Pagine.

---

## 2. PII espalhada, `c.cep`, `c.doc`, `c.cidade` vêm `None`

**Sintoma:** ao processar contatos, campos como `c.get("cep")`, `c.get("doc")`, `c.get("cidade")`, `c.get("sobrenome")` retornam `None` mesmo pra contatos que claramente têm esses dados (visíveis na UI).

**Causa-raiz:** Clint não coloca PII no raiz do objeto Contact, coloca em `c["fields"]["..."]`.

**Solução:**

```python
# Errado:
cep = c.get("cep")          # → None
doc = c.get("doc")          # → None
cidade = c.get("cidade")    # → None

# Certo (prioridade fields, fallback raiz):
fields = c.get("fields") or {}
cep = fields.get("cep") or c.get("cep")
doc = fields.get("doc") or c.get("doc")
cidade = fields.get("cidade") or c.get("cidade")
sobrenome = fields.get("sobrenome") or c.get("sobrenome")
```

A `normalize_contact()` do client já faz isso.

---

## 3. Telefone canônico é `fullPhone`, não `phone`

**Sintoma:** `c.get("phone")` retorna telefone vazio, com máscara variada, ou inválido. `c.get("complete_phone")` também.

**Causa-raiz:** o campo `fullPhone` é o único que vem sempre populado e em formato consistente (E.164 com 55 prefix pra BR).

**Solução:**

```python
phone = (
    c.get("fullPhone")
    or c.get("complete_phone")  # fallback legado
    or c.get("phone")           # último recurso
    or ""
)
```

Validar com `c.get("valid_phone")` se disponível, se for `False`, Clint já flaggou como inválido.

---

## 4. Estado vem como "São Paulo" e quebra match Meta Ads

**Sintoma:** ao hashear estado pra Meta Custom Audience, match rate fica baixo. Cidade/estado deveriam normalizar mas não normalizam.

**Causa-raiz:** Clint armazena estado às vezes como UF ("SP"), às vezes como nome completo ("São Paulo", com acento). Meta espera SEMPRE em UF de 2 letras minúsculas (`"sp"`).

**Cenario de teste:** comparar o valor de exibicao de `fields.estado` com a representacao aceita pela API da versao usada, usando contatos sinteticos e sem inferir resultado em producao.

**Solução:**

Use o `STATE_MAP` em `clint_client.py` (27 UFs + variantes acento/lowercase):

```python
from clint_client import STATE_MAP

estado_raw = (
    fields.get("estado") or c.get("estado") or ""
).strip().lower()
estado = STATE_MAP.get(estado_raw, "")  # "sp" ou "" se desconhecido
```

Em SQL/n8n similar: criar map equivalente.

---

## 5. Loop de paginação infinito

**Sintoma:** script roda pra sempre puxando páginas vazias ou repetindo a mesma página.

**Causa-raiz:** `hasNext` não é confiável em todos os endpoints (às vezes retorna `true` mesmo na última página).

**Solução:**

```python
while True:
    r = client.get(path, params={**params, "page": page, "limit": 100})
    items = r.get("data") or []
    if not items:
        break                       # vazio = última
    yield from items
    if len(items) < 100:
        break                       # menos que limit = última
    has_next = bool(r.get("hasNext"))
    if not has_next:
        break
    page += 1
    time.sleep(0.15)                # rate-limit gentle
```

A `ClintClient.paginate()` já implementa essa lógica.

---

## 6. 401 Unauthorized mesmo com token correto

**Sintoma:** todas as chamadas retornam 401, mesmo confirmando que o token está válido (testado em outra ferramenta).

**Causas possíveis:**

1. **Header errado.** Use `api-token: <token>` (NÃO `Authorization: Bearer <token>`).
2. **Header `accept` faltando.** Algumas vezes Clint exige `accept: application/json`.
3. **Token revogado.** Confirmar em Clint UI → Settings → API Keys.
4. **Token de workspace errado.** Cada workspace do Clint tem token próprio.

**Diagnóstico rápido:**

```bash
# Deve retornar JSON com lista de tags
curl -v -H "api-token: $CLINT_API_TOKEN" \
        -H "accept: application/json" \
        "https://api.clint.digital/v1/tags?limit=1"
```

Se 401 aqui = token problema. Se 200 aqui mas 401 nos outros = problema no código.

---

## 7. 429 Too Many Requests

**Sintoma:** após várias chamadas seguidas, retorna 429.

**Causa-raiz:** rate limit não documentado.

**Solução:**

- 200ms entre páginas em loops longos (já no client)
- Backoff exponencial em 429: `time.sleep(2 ** attempt)`, `ClintClient` faz pra 5xx, adicionar pra 429:

```python
except urllib.error.HTTPError as e:
    if e.code == 429 and attempt < MAX_RETRIES - 1:
        time.sleep(2 ** attempt)
        continue
    raise
```

- Considerar dividir trabalho em janelas (não rodar 10 sincs paralelos)

---

## 8. Não tem `created_after` em /contacts

**Sintoma:** quer puxar só contatos criados depois de X timestamp pra sync incremental, mas o param não funciona/não existe.

**Causa-raiz:** API não tem filtro temporal nativo em `/contacts`.

**Solução: walk reverso**

```python
def fetch_since(client, tag_id: str, since_iso: str) -> list[dict]:
    """Pega contatos da tag criados após since_iso (paginação reversa)."""
    since = parse_iso(since_iso)
    new = []
    page = 1
    while True:
        r = client.get("/contacts", params={
            "tag_ids": tag_id, "page": page, "limit": 100,
        })
        items = r.get("data") or []
        if not items:
            break
        # Clint ordena ASC por created_at. Pega só os > since.
        stop = False
        for it in items:
            if parse_iso(it["created_at"]) > since:
                new.append(it)
            else:
                stop = True
                break
        if stop or len(items) < 100:
            break
        page += 1
    return new
```

⚠️ Em volumes altos, isso ainda é custoso. O workflow n8n `${RESOURCE_ID}` tem implementação otimizada (janela de páginas adaptativa baseada em downtime).

---

## 9. POST /contacts cria duplicata em vez de atualizar

**Sintoma:** chamar `POST /contacts` com email já existente cria contato novo (duplicata) em vez de atualizar o existente.

**Causa-raiz:** `POST /contacts` (sem id) não faz upsert. (Já `POST /deals` faz upsert de contato embutido, ver pegadinha #19.)

**Solução:**

```python
# 1. Achar o contato existente (id)
existing = client.list_contacts(email=email)
if existing:
    # 2. Update = POST /contacts/{id} (NÃO PUT, ver #20), faz MERGE de fields
    return client.update_contact_fields(existing[0]["id"], payload["fields"])
else:
    return client.create_contact(payload)
```

Cuidado: `list_contacts(email=...)` filtra, mas não é confiável p/ lookup em massa (dedupe por telefone), ver #21.

---

## 10. Webhook não dispara em high-load

**Sintoma:** configurou webhook pra `contact.tag.added` mas eventos não chegam de forma confiável.

**Causa-raiz:** Clint não garante delivery de webhooks em alta carga. Sem retry, sem queue durável.

**Solução:** NÃO use webhook como mecanismo único. Polling + diff é mais robusto. Webhook serve como "complemento" (reduz latência da percepção mas não é fonte da verdade).

Modelo condicional: se o webhook nao atender ao contrato de entrega, usar polling/diff com intervalo configurado e teste de opt-out; nao presumir workflow existente.

---

## 11. Verificar suporte a criacao de webhook na API instalada

**Sintoma:** ao tentar `POST /v1/webhooks` retorna 404 ou método não existe.

**Causa-raiz:** Clint não expõe gerenciamento de webhooks pela API REST. Webhook só pode ser configurado **manualmente no painel** (UI) do Clint.

**Solução:**

1. Para uma integracao autorizada, escolher agenda, zona de horario, paginacao e limite de carga; medir o universo e reconciliar totais sem copiar cron ou volumes de outro cliente.
2. Se o caso exigir menor latencia, definir intervalo de polling/diff e validar carga, cotas e entrega no ambiente do usuario.

⚠️ Mesmo com webhook do painel, validar entrega, Clint não tem retry confiável.

---

## 12. Endpoint singular `/contact` retorna erro

**Sintoma:** tentou `GET /v1/contact/{id}` (singular) por engano e recebeu erro.

**Causa-raiz:** Convenção REST do Clint usa SEMPRE plural pra recursos coleção.

**Solução:** sempre `/v1/contacts/{id}` (plural). Mesmo regra pra `/tags`, `/deals`, `/pipelines`, `/organizations`.

---

## 13. Base URL sem `/v1` retorna 404

**Sintoma:** chamadas pra `https://api.clint.digital/contacts` (sem `/v1`) retornam 404.

**Solução:** SEMPRE incluir `/v1` no path. Base canônica:

```
https://api.clint.digital/v1
```

Não tente `/v2`, `/api/v1`, ou outras variantes, só `/v1` está ativo.

---

## 14. IP do lead/contato NÃO está disponível via API

**Sintoma:** quer filtrar leads por país/região via IP, ou montar antifraude usando IP.

**Diagnostico condicional:** se o IP nao estiver no esquema e nas respostas de `/contacts`, `/deals` ou campos customizados da versao usada, nao inferir nem fabricar esse dado; verificar uma origem de coleta autorizada.

**Solução:**

- Pra geo: usar `fields.cidade` / `fields.estado` (preenchidos via form/import)
- Pra antifraude: usar `valid_phone` + `duplicate_phone` (flags nativos do Clint)
- Se precisa IP de verdade, captar no form da landing e mandar via API pro `fields.utm_source` ou campo custom (perde o conceito original mas resolve)

---

## 15. Variável de ambiente confusa (`CLINT_API_KEY` vs `CLINT_API_TOKEN`)

**Sintoma:** script nao encontra a variavel de autenticacao na configuracao local autorizada.

**Hipotese a verificar:** cliente e configuracao podem usar nomes diferentes:
- **`CLINT_API_KEY`**, nome de exemplo a confirmar no contrato do cliente
- `CLINT_API_TOKEN`, usada em alguns scripts antigos
- `CLINT_TOKEN`, fallback raro

**Solucao condicional:** conferir a ordem de resolucao implementada pelo cliente e alinhar os nomes na configuracao autorizada. Um metodo como `ClintClient.from_master_env()` depende da implementacao fornecida pelo usuario; este documento nao fornece nem autoriza acesso a um cofre.

---

## 16. Query pontual por adaptador local sem expor token

**Cenario condicional:** se o ambiente autorizado oferecer um broker local, realizar consultas limitadas sem entregar a credencial ao operador.

**Modelo de solucao:** fornecer e revisar um comando local com allowlist de rotas, leitura segura da credencial e logs sem segredos. O adaptador nao e embarcado nem presumido instalado. Confirmar interface, permissoes e autorizacao antes de qualquer consulta dependente.

Exemplo de interface, somente apos configurar e verificar `USER_BROKER_COMMAND`:

```bash
"$USER_BROKER_COMMAND" '/v1/tags?page=1&limit=100'
```

Validar o adaptador para o sistema operacional usado, incluindo Windows quando aplicavel. Sem adaptador disponivel, manter a consulta dependente bloqueada; nao abrir um cofre ou usar conta pessoal como fallback automatico.

---

## 17. `GET /contacts?email=` não acha contato com `+` no email (n8n / URL crua)

**Sintoma:** `GET /contacts?email=contact@example.invalid` retorna `totalCount: 0`, mas o contato existe (Python com `urlencode` acha com `totalCount: 1`).

**Causa-raiz:** o `+` em query string é interpretado como **espaço** pelo servidor (`application/x-www-form-urlencoded`). Sem encoding, o Clint busca por `"test contact@example.invalid"` → não acha. Pega quem monta a URL como string crua (n8n HTTP node com `?email={{...}}` na URL, curl sem `--data-urlencode`).

**Solução:**
- **n8n:** conferir na versao usada `sendQuery: true` + `queryParameters` estruturados e testar com endereco sintetico a preservacao de `+` como `%2B`, sem presumir resultado de workflow externo.
- **Python:** `urllib.parse.urlencode({"email": email})` já resolve.
- **curl:** `--data-urlencode "email=$EMAIL" -G`.

⚠️ Vale pra QUALQUER param com `+`, espaço ou char especial. O `?email=` em si FILTRA de verdade (match exato), o bug é só de encoding.

## 18. Eventual consistency: contato/deal recém-criado não aparece em GET por ~segundos

**Sintoma:** logo após `POST /deals` (que faz upsert de contato), um `GET /contacts?email=` ou `GET /deals?contact_id=` imediato pode retornar vazio por alguns segundos.

**Impacto:** dedupe best-effort baseado em GET falha em re-disparos quase-simultâneos (ex: webhook reentregue em <10s). Em reentregas reais (segundos/minutos depois) já funciona.

**Solução:** aceitar como best-effort, ou (se dedupe rígido for crítico) usar uma camada de idempotência própria (ex: dedupe key por transação no n8n/DB antes de chamar a API).

## 19. `POST /deals` ignora o objeto `fields` silenciosamente (CRÍTICO)

**Sintoma:** você cria o deal via `POST /deals` mandando `fields: {utm_source, doc, cidade, ...}` e os custom fields **nunca aparecem** no contato/deal do CRM. Status 201 normal, sem erro.

**Causa-raiz:** o `POST /deals` **descarta o objeto `fields` inteiro** (volta `{}` na resposta). Custom field NÃO é gravável pela rota de deal, só pela rota de contato. Bug que fazia os campos nunca chegarem.

**Solução (fluxo de 2 passos):**

```python
# 1. Cria o deal (faz upsert do contato; retorna contact_id)
deal = c.create_deal(origin_id, email=email, name=name, phone=phone, value=100.00)
contact_id = deal["data"]["contact_id"]

# 2. Grava os custom fields NO CONTATO (única rota que persiste fields)
c.update_contact_fields(contact_id, {"utm_source": "example-utm-source", "doc": cpf, "ip_1": ip})
```

⚠️ E ainda assim só persistem slugs JÁ registrados no painel (silent-drop, ver `endpoints.md` seção CUSTOM FIELDS).

---

## 20. Update de contato/deal é `POST /{recurso}/{id}`, PUT e PATCH dão 404

**Sintoma:** `PUT /contacts/{id}` ou `PATCH /contacts/{id}` → **404** "Cannot PUT/PATCH". Mesmo pra deals.

**Causa-raiz:** o Clint não usa PUT/PATCH pra update. O verbo de update é **POST no recurso com id**.

**Solução:**

```python
# Update de campos do contato (MERGE, não sobrescreve preenchido):
c.update_contact_fields(contact_id, {"utm_source": "example-utm-source"})   # POST /contacts/{id}

# Marcar deal como ganho:
c.mark_deal_won(deal_id)                                       # POST /deals/{id} {"status":"WON"}
```

⚠️ O `ClintClient.update_contact()` legado usava `self.put(...)` → quebrava (404). Foi mantido por compat mas **redireciona pra POST** agora. Use `update_contact_fields()` pra clareza. DELETE de contato/deal = **204** (funciona).

---

## 21. `?email=` filtra, mas não é confiável p/ lookup em massa

**Sintoma:** `GET /contacts?email=contact@example.invalid` retorna `totalCount: 0` pra um comprador que existe e tem deal aprovado.

**Causa-raiz:** o Clint deduplica contatos por **telefone** no upsert. Um evento pode ter sido anexado a um contato cujo email canônico é OUTRO (ex: o contato foi criado antes com email diferente, e o telefone bateu). O `?email=` faz match exato no email canônico, se o evento ligou ao contato por telefone, o email não bate.

**Cenario de teste:** se a busca direta por email retornar vazio, comparar email e telefone normalizados em um subconjunto autorizado de tag sintetica, com denominador e criterios de correspondencia explicitos; nao inferir compra ou identidade real a partir de um unico campo.

**Solução (match robusto em massa):**
1. Restringir o universo por tag autorizada (`list_contacts_by_tag`) e registrar o denominador medido, sem assumir volume de cliente.
2. Indexar esse subconjunto por `email` **e** por telefone normalizado (`only_digits(fullPhone)`).
3. Casar o evento por email OU telefone (qualquer um que bata).

Evitar lookup individual em toda a base: paginar o subconjunto autorizado e comparar email e telefone normalizados, sem inferir identidade a partir de um unico campo.

---

## 22. `POST /deals` não é idempotente (2 POST = 2 deals)

**Sintoma:** webhook reentregue / re-disparo cria deal duplicado na mesma origin pro mesmo contato.

**Causa-raiz:** `POST /deals` faz upsert do **contato** (match email/telefone), mas **não** do **deal**, cada POST cria um deal novo.

**Solução (dedupe best-effort):**

```python
existing = c.find_deal_by_contact(contact_id, origin_id=origin_id)
if not existing:
    c.create_deal(origin_id, email=email, ...)
```

⚠️ `find_deal_by_contact` usa `GET /deals?contact_id=` (filtra de verdade) e filtra `origin_id` no código (`?origin=` NÃO filtra). Sujeito a eventual consistency (#18), em re-disparos quase-simultâneos pode escapar; pra dedupe rígido, camada de idempotência própria (dedupe key no n8n/DB).

---

## Estratégias gerais de debug

### 1. Sempre logar URL completa e response status

```python
try:
    r = client.get(path, params=params)
except ClintAPIError as e:
    print(f"Falhou: {e.url} status={e.status}")
    print(f"Body: {e.body[:500]}")
    raise
```

### 2. Mascarar PII em logs

```python
from clint_client import mask_pii
print(f"Contato: name={c['name']}, email={mask_pii(c['email'])}, "
      f"phone={mask_pii(c['fullPhone'])}")
```

### 3. Smoke test antes de operação grande

```python
c = ClintClient.from_master_env()
print(f"Tags total: {len(c.list_tags())}")  # confirma auth + paginação
```

### 4. Salvar 1 contato em arquivo pra inspecionar estrutura

```python
import json
contacts = client.list_contacts_by_tag(tag_id, limit_per_page=2)
with open("/tmp/sample_contact.json", "w") as f:
    json.dump(contacts[0], f, indent=2, ensure_ascii=False)
# Abre o arquivo e confere onde os campos REALMENTE estão
```

