# Receita detalhada do workflow n8n (node a node)

Detalhe da estrutura validada (FPV369 / Lia Practitioner). Os params de cada tipo de node, os porques e os bugs estao na `haos-n8n-api`; aqui esta a MONTAGEM especifica do funil. NAO redescobrir auth/PUT/encoding aqui.

## Topologia

```
Webhook (POST, path proprio)
  -> Normalize <Plataforma> (Code)        # 1 ponto unico de leitura do payload
  -> IF produto-alvo?                       # descarta produto fora do funil E parcelas (produto generico)
       (false) -> NoOp / fim
       (true)  -> Switch Evento            # 1 saida por status/evento da plataforma
                    |-- branch: Gerou Pagamento
                    |-- branch: Compra Aprovada
                    |-- branch: Compra Negada
                    |-- branch: Carrinho Abandonado (so se a plataforma emitir)
```

Cada branch repete o mesmo sub-fluxo (abaixo), mudando so o `origin_id`, o `stage_id` da plataforma, a lista de "suborigens anteriores" pra dar ganho e se aplica tag.

## Node 0 - Webhook

- Method POST, path proprio (ex.: `clint-<plataforma>-<produto>`). URL prod fica `https://service.example.invalid<path>`.
- Responde 200 rapido (responde imediato; o processamento segue async).

## Node 1 - Normalize <Plataforma> (Code)

Le o payload UMA vez e devolve um objeto plano com tudo que as branches usam. Evita repetir `$json.data.offer...` em 20 nodes. Saida tipica:

```
{
  event,            // evento/status normalizado
  product_id,       // como a plataforma identifica o produto (ex.: data.offer.product.id na Lia)
  email, name, phone,
  doc, address, utm_source,   // podem vir vazios (ex.: Lia so manda no order)
  value,            // ja dividido por 100 se a plataforma manda em centavos
  tx_id             // id da transacao, util pra log/dedupe
}
```

> O mapa de campo de CADA plataforma (caminhos e fallbacks) esta na skill da plataforma (`lia-api` tem o mapa completo). Aqui so se consome o normalizado.

## Node 2 - IF produto-alvo?

- Condicao: `product_id` esta na lista de product_ids do funil.
- Isto descarta de uma vez: produto de outro funil E (em plataforma com financiamento) a PARCELA, que carrega produto generico. So o produto real passa.

## Node 3 - Switch Evento

- 1 saida por evento/status. Mapeia pro evento -> suborigem (ver tabela da Fase 3 e `example-ids.md`).

## Sub-fluxo por branch (o miolo)

### a) Busca Contato - HTTP GET
- `GET https://api.clint.digital/v1/contacts` com `sendQuery: true` + `queryParameters` `[{name:"email", value: <email>}]`.
- NAO montar `?email=...` na URL (o `+` no email vira espaco e quebra o match).
- Auth: credencial `httpHeaderAuth` (header `api-token`). timeout 30000. onError continueRegularOutput.

### b) Busca Deals - HTTP GET
- `GET .../v1/deals` com queryParameters `[{name:"contact_id", value: <id do contato achado>}]`.
- So roda se achou contato. So `?contact_id=` filtra de verdade (origin/search nao filtram).

### c) Decide - Code
- Recebe contato + deals + o `origin_id` desta branch. Emite `jaExiste`, `deal_id`, `deal_status`, `should_move`, `contact_id`. Esqueleto em `decide-node.js`.
- `contact_id` sai daqui e e a fonte estavel pro Atualiza Contato (vale tanto no caminho create quanto move).

### d) IF novo? (`jaExiste === false`)

**SIM, novo -> Cria Deal - HTTP POST**
- `POST .../v1/deals`, body json:
```json
{
  "origin_id": "<origin desta branch>",
  "stage_id": "<stage da PLATAFORMA nesta suborigem>",
  "name": "<nome>",
  "email": "<email>",
  "phone": "<telefone>"
}
```
- `POST /deals` faz upsert do contato embutido E respeita o `stage_id`. NAO mandar `fields` aqui (e ignorado). Pegar `contact_id` da resposta como fallback.

**NAO, ja existe -> IF mover? (`should_move === true`)**
- **OPEN -> Move Deal - HTTP POST** `POST .../v1/deals/{deal_id}` body `{ "stage_id": "<stage da plataforma do evento>" }`. Move o card pra coluna da plataforma.
- **WON -> para.** Nao move (deixa ganho).

### e) Atualiza Contato - HTTP POST
- `POST .../v1/contacts/{contact_id}` body `{ "fields": { ...campos disponiveis... } }`.
- `contact_id` vem do node **Decide** (estavel). MERGE: so completa o vazio, nao sobrescreve. Unica rota pra custom field.

### f) Marca Ganhos + Da Ganho - HTTP POST (loop)
- Pras suborigens ANTERIORES a esta: `POST .../v1/deals/{id_do_deal_naquela_suborigem}` body `{ "status": "WON" }`.
- Achar o deal de cada suborigem anterior filtrando os deals do contato por `origin_id` (no Decide ou num Code dedicado). Cadeia: Gerou/Negada -> ganha(Carrinho); Aprovada -> ganha(Carrinho + Gerou + Negada).

### g) Tag - HTTP POST (so no evento de pago)
- `POST .../v1/contacts/{contact_id}/tags` body = **array** `["<tag_id de pago>"]`. NAO objeto.

## Regras de node (resumo, detalhe na haos-n8n-api)
- Todo HTTP node: `typeVersion` 4.4+, `options.timeout = 30000`, `onError: continueRegularOutput`, auth `httpHeaderAuth` (NUNCA token hardcoded).
- URL nunca comeca com `=`. Query/body/headers sempre estruturados (toggles sendQuery/sendBody), nao string concatenada.

## PUT seguro do workflow (ao salvar via API)
1. GET o workflow -> backup do JSON em `_secrets/backups/wf_<slug>_<id>_<AAAA-MM-DD_HHMM>.json`.
2. Remover read-only top-level: `id, active, createdAt, updatedAt, tags, versionId, triggerCount, shared, meta` (e `binaryMode`/`availableInMCP` dentro de settings se reclamar). Manter `settings.executionOrder: "v1"`.
3. PUT so com `name, nodes, connections, settings`.
4. Ativar e endpoint separado `/activate` (active:true no PUT e ignorado).
- Helper: `${USER_PROJECT_ROOT}/scripts/wf_edit.py` da `haos-n8n-api` (GET+backup+sanitiza+PUT).

## Teste (cenarios que validamos)
1. Gerou pagamento -> deal em "Gerou Pagamento", stage da plataforma. OK
2. Aprovado -> deal em "Compra Aprovada" + tag de pago + ganho em "Gerou". OK
3. Negado/cancelado -> deal em "Compra Negada". OK
4. (financiamento) parcela com produto generico -> IGNORADA pelo IF produto-alvo. OK
5. Reenvio do "aprovado" 2x -> 1 deal so (idempotencia). OK
6. evento de etapa intermediaria nao mapeada (ex.: in_progress) -> ignorado. OK
7. variante/oferta alternativa -> cai no mesmo funil, aprovado + tag. OK
8. cross-plataforma: deal OPEN existente + evento de outra plataforma -> MOVE o card (nao duplica). OK
9. deal ja WON + reenvio -> NAO move. OK
-> No fim, DELETAR todos os dados de teste no Clint (DELETE = 204).

