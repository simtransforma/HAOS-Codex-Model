---
name: clint-funnel-playbook
description: "Playbook ponta-a-ponta pra montar uma integracao \"plataforma de venda -> funil no Clint\" via n8n, do levantamento ao teste e fechamento. E o \"como fazer\" que ORQUESTRA as 3 skills de API (clint-api, lia-api, haos-n8n-api); nao duplica nenhuma delas. Use SEMPRE que a tarefa for replicar o padrao \"eventos de uma plataforma de venda (Assiny, Lia, Yampi, Hotmart, Eduzz, Asaas, TikTok Shop, etc.) criam/movem deals num funil/grupo do Clint\" pra um PRODUTO NOVO. Triggers do user, \"integrar [plataforma] com Clint\", \"criar funil no Clint pra produto X\", \"replicar a integracao da FPV369 / da Lia pra outro produto\", \"novo produto no Clint via n8n\", \"webhook de venda pro Clint\", \"criar grupo/suborigem no Clint e ligar na plataforma\", \"monta o fluxo de venda -> CRM pro [produto]\", \"joga as vendas do [plataforma] no funil do Clint\". Tambem aciona implicitamente quando o objetivo e que venda de uma plataforma vire card no funil do Clint. NAO use pra mexer numa integracao Clint que JA existe (va direto na clint-api/haos-n8n-api), nem pra Meta Audience a partir de tag (= clint-meta-audience-sync)."
---

# Clint Funnel Playbook, plataforma de venda -> funil no Clint (n8n)

O processo completo, do jeito que vivemos (FPV369 -> Lia -> regra de upsert-move -> cross-plataforma), pra repetir em qualquer produto/plataforma novos SEM redescobrir as pegadinhas. Esta skill e o roteiro de ponta a ponta. As 3 skills de API fazem o trabalho pesado, esta aqui so amarra a ordem, as decisoes e as regras de negocio.

INTERNA: contem IDs/infra (workflow ids, origin/stage ids, grupos). NAO vai pro repo publico HAOS_CC.

## Skills que esta playbook orquestra (referenciar, nao copiar)

| Skill | Papel nesta playbook |
|---|---|
| `clint-api` | Cliente Python + pegadinhas do Clint (deals, contatos, tags, origins/stages). DESTINO da integracao. |
| `lia-api` | Padrao de uma skill de API de plataforma de venda (eventos, payload, webhooks). Modelo pra mapear plataforma NOVA. |
| `haos-n8n-api` | Operar/editar o workflow, PUT seguro, HTTP node + auth, timeouts, encoding, backup/export. |

Outras skills de plataforma ja prontas: `yampi`, `tiktok-shop-sim`, `bling`. Se a plataforma ja tem skill, USE-A; se nao, crie uma skill de API dela no padrao da `lia-api` (Fase 1).

## Quando usar

Replicar o padrao "eventos de uma plataforma de venda criam/movem deals num funil do Clint" pra um PRODUTO NOVO. Gatilhos:
- "integrar [plataforma] com Clint", "criar funil no Clint pra produto X"
- "replicar a integracao da FPV369 / da Lia pra outro produto"
- "novo produto no Clint via n8n", "webhook de venda pro Clint"
- "joga as vendas do [plataforma] no funil do Clint", "monta o fluxo de venda -> CRM pro [produto]"

NAO use pra: mexer numa integracao que ja existe (va direto em `clint-api` + `haos-n8n-api`); criar publico Meta a partir de tag (`clint-meta-audience-sync`).


**Jornada de cards — obrigatorio, atualizado em 2026-09-24:** seguir
Clint Global: jornada e pagamento (dependency not bundled: ../clint-global/references/jornada-card-pagamento.md).
Na mesma origem, atualizar o mesmo card de abandono a gerada e aprovada;
pagamento confirmado exige Fechado/Ganho (`WON`) no card aprovado e tag paga.
Em origens separadas, dar ganho na anterior e criar ou atualizar o card da
proxima, sem duplicar. As receitas abaixo com suborigens por evento se aplicam
somente a esse segundo modelo; nao criar novas origens ou cards por evento
quando a campanha usa etapas dentro de uma origem.

**NAO mexer no que ja existe. CRIAR tudo novo.** Workflow novo, webhook novo, branch isolada. Fluxos/webhooks existentes ficam intactos. (Foi o que fizemos na Lia: workflow 100% novo, 3 webhooks aditivos, zero toque nos 30 existentes.) Acao externa irreversivel (criar webhook em producao, ativar fluxo que grava no CRM real) -> mostrar plano e pedir OK.

---

## FASE 1 - Investigar (antes de construir)

Levantar TUDO antes de tocar no n8n. Checklist:

**Plataforma de venda**
- [ ] id(s) do produto/variantes que entram (ex.: principal + ofertas alternativas + bolsa social).
- [ ] modelo de eventos: quais eventos disparam, shape do payload, COMO o payload identifica o produto, e quais campos do comprador vem em cada evento (nome/email/telefone/doc/endereco/UTM).
- [ ] como registrar o webhook (endpoint, body, e se e ADITIVO ou substitui).
- [ ] Se a plataforma JA tem skill (`lia-api`, `yampi`, `tiktok-shop-sim`, `bling`): use-a. Se NAO: criar skill de API dela seguindo o padrao da `lia-api` (acesso, endpoints, mapa de eventos, payload, pegadinhas, cliente Python).

**Clint (destino)**
- [ ] o grupo/funil (origem-mae) onde os deals vivem.
- [ ] as suborigens (origins) do funil e os `origin_id` de cada uma (`GET /origins`).
- [ ] os STAGES de cada suborigem e seus `stage_id` (modelo do tenant Edson = origin + stage, NAO pipeline). Existe um stage POR plataforma (ex.: "Assiny", "Lia")? Pegar o `stage_id` da coluna da plataforma em cada suborigem.
- [ ] a TAG de "pago"/conversao a aplicar (pegar o tag_id por nome).

> Como buscar tudo isso esta na `clint-api` (`GET /origins`, paginacao, find_tag_by_name) e na skill da plataforma. NAO redescobrir auth/paginacao aqui.

---

## FASE 2 - Decisoes (as 6 que sempre aparecem)


1. **Quais produtos/variantes** entram no mesmo funil? (Lia: 3 product_ids -> 1 funil.)
2. **Reusar grupo existente** gravando no STAGE da plataforma, ou grupo novo? (Padrao recente: reusar o grupo, gravar no stage da plataforma. Foi assim na Lia, que entrou no G369 no stage "Lia".)
3. **Eventos sem fonte na plataforma** (ex.: Lia nao tem carrinho abandonado): a etapa fica orfa (so recebe "ganho", nunca entrada). Confirmar que e aceitavel.
5. **Tag:** mesma tag por produto (ex.: `Practitioner_pago` serve Assiny e Lia), ou uma por plataforma? Em geral a tag e por PRODUTO/oferta, nao por plataforma.

---

## FASE 3 - Mapear evento -> suborigem -> stage

Montar a tabela-modelo (e o coracao da integracao). Uma linha por evento da plataforma:

| Evento da plataforma | -> Suborigem (origin_id) | -> Stage da plataforma (stage_id) | Tag? |
|---|---|---|---|
| pagamento gerado (pix/boleto/pending) | Gerou Pagamento | stage da plataforma | nao |
| compra aprovada (paid/finished/approved) | Compra Aprovada | stage da plataforma | SIM (tag de pago) |
| compra negada/cancelada/vencida | Compra Negada | stage da plataforma | nao |
| carrinho abandonado (se a plataforma emitir) | Carrinho Abandonado | stage da plataforma | nao |

- Se a plataforma NAO emite um evento (ex.: abandono na Lia), a suborigem correspondente fica sem fonte: so recebe "ganho" quando o lead avanca, nunca entrada direta.
- Exemplo trabalhado, com ids reais (Assiny e Lia, grupo G369), em `references/example-ids.md`.

---

## FASE 4 - Receita do workflow n8n (estrutura validada)

Workflow NOVO, nome `[Clint][<Plataforma>][<Produto>]`, com webhook proprio. Esqueleto:

```
Webhook -> Normalize <Plataforma> (Code) -> IF produto-alvo -> Switch Evento -> (1 sub-branch por evento)
```

Cada sub-branch de evento (a parte que se repete):

1. **Busca Contato** - `GET /contacts?email=` (use queryParameters estruturado, NAO concatenar na URL, por causa do `+`).
2. **Busca Deals** - `GET /deals?contact_id=` (so `?contact_id=` filtra de verdade).
3. **Decide (Code)** - emite: `jaExiste`, `deal_id`, `deal_status`, `should_move` (= existe && status OPEN), `contact_id`. Esqueleto JS reutilizavel em `references/decide-node.js`.
4. **IF novo?**
   - SIM (novo) -> **Cria Deal** - `POST /deals` com `origin_id` + **`stage_id` da plataforma** + contato (email/nome/telefone). (`POST /deals` RESPEITA stage_id; sem ele cai no default/BASE.)
   - NAO (ja existe) -> **IF mover?** (`should_move`)
     - status OPEN -> **Atualiza Deal** - atualizar etapa e valor do evento; no pagamento confirmado, incluir `status: WON` no proprio card aprovado. Gerada permanece OPEN ate confirmar pagamento.
     - status WON -> **para** (nao move, deixa ganho).
5. **Atualiza Contato** - `POST /contacts/{id}` com os campos (POST /deals IGNORA `fields`). Resolver o `contact_id` a partir do node **Decide** (e estavel nos 2 caminhos: criar e mover; o id sai do create OU do lookup).
6. **Marca Ganhos + Da Ganho** - em origens separadas, fechar os cards anteriores existentes da cadeia mapeada como `WON`; no pagamento confirmado, o card de Compra Aprovada tambem deve ficar `WON`. Na mesma origem, atualizar somente o card canonico, sem criar outro.
7. **Tag** (so no evento de pago) - `POST /contacts/{id}/tags` com body = **ARRAY de strings** `["tag_id"]`.

Regras tecnicas dos nodes (detalhe e por que na `haos-n8n-api`):
- HTTP Request node `typeVersion 4.4+` (a v1 nao anexa OAuth; bug conhecido).
- `options.timeout = 30000` (30s) em TODO HTTP node (anti-travamento da fila).
- `onError: continueRegularOutput` nos HTTP nodes (uma falha pontual nao mata a execucao).
- Auth = credencial `httpHeaderAuth` (`authentication: predefinedCredentialType` + `nodeCredentialType: httpHeaderAuth`). **NUNCA** hardcode o token. (Clint reusa a credencial header `api-token`.)
- URL nunca comeca com `=https://` (o `=` faz o n8n tratar como expressao e quebra).

Receita detalhada (node a node, com params) em `references/workflow-recipe.md`.

---

## FASE 5 - Regras de comportamento (decisoes de negocio que viraram regra)

- **1 deal por contato por suborigem.** Nada de duplicar: por isso Busca Deals + Decide ANTES de criar (`POST /deals` NAO e idempotente, 2 POST = 2 deals).
- **Upsert-move.** Se existe OPEN, atualizar o mesmo ID para a etapa e valor atuais. Pagamento confirmado tambem define `WON` no card aprovado e aplica tag paga. Se WON, evento antigo nao reabre nem regride; uma nova notificacao nao cria outro card.
- **Dar ganho.** Ao avancar, marca WON nos deals das suborigens ANTERIORES (filtra por origin_id). Cruza plataformas de proposito: o lead converteu, fecha os dois funis (ex.: aprovou na Lia -> da ganho tambem no que entrou pela Assiny). Cadeia tipica: Gerou/Negada -> ganha(Carrinho); Aprovada -> ganha(Carrinho + Gerou + Negada).
- **Campos via `POST /contacts/{id}`** (POST /deals ignora `fields`). E **MERGE**, nao sobrescreve o ja preenchido. Util quando o PII chega depois (ex.: doc/endereco/UTM da Lia so vem no `order`).
- **Match de contato por email** (+ telefone como reforco). `?email=` sozinho pode falhar (dedupe interno por telefone); em lookup em massa, casar email + telefone restrito por tag.

---

## FASE 6 - Protocolo de teste


1. Disparar o webhook de PRODUCAO com **payload mock** (contato fake, ex.: `test+<produto>@haos.test`, telefone fake).
2. Conferir o deal **na suborigem + stage certos** no painel do Clint (nao confiar so no "200 OK").
3. **Cross-plataforma:** com um contato que ja tem deal OPEN, disparar evento de outra plataforma -> o card deve MOVER de coluna, NAO duplicar.
4. **WON-nao-move:** com um deal ja WON, disparar de novo -> NAO move, fica ganho.
5. **Dar-ganho:** ao avancar de etapa, conferir que os deals anteriores viraram WON (`won_at` setado).
6. **Idempotencia/anti-parcela:** reenviar o mesmo "aprovado" 2x -> 1 deal so. Se a plataforma tem financiamento (Lia), confirmar que a PARCELA (produto generico) e descartada pelo IF de produto-alvo.
7. **LIMPAR** todos os dados de teste no Clint (DELETE de contato/deal/tag criados; DELETE = 204).

Checklist de teste por cenario validado: `references/workflow-recipe.md` (secao Teste).

---

## FASE 7 - Fechamento

- **Backup** do workflow (GET + JSON) ANTES de qualquer PUT, e o backup final apos ativar: `_secrets/backups/wf_<slug>_<id>_<AAAA-MM-DD_HHMM>.json`. Se mexeu em webhooks da plataforma, backup da lista ANTES (`_secrets/backups/<plataforma>_webhooks_BEFORE_<data>.json`).
- **Doc no Obsidian:** resumo tecnico em `Codex-Vault/03-Resumos-Tecnicos/AAAA-MM-DD_titulo.md`.
- **Memoria:** registrar a integracao (workflow id, product ids, origin/stage ids, tag) seguindo o padrao das memorias `project_assiny_clint_fpv369` / `project_lia_clint_practitioner`.
- **Atualizar skills:** se descobriu pegadinha nova de API, atualizar a skill da API (clint-api / skill da plataforma / haos-n8n-api), NAO esta playbook. Esta playbook so muda se o PROCESSO mudar.
- Rodar `finish_task.ps1` (AGENTS.md secao 22): commit+push do repo da sessao + backup da memoria eterna.

---

## PEGADINHAS (resumo + skill certa pra cada uma)

**Clint** (detalhe -> `clint-api`)
- `fields` IGNORADO no `POST /deals` -> gravar custom field via `POST /contacts/{id}` (MERGE).
- Tag = body **array de strings** `["uuid"]`, NAO `{"tag_id":...}` (objeto da 400).
- Ganho = `POST /deals/{id}` `{"status":"WON"}` (seta `won_at`). Update e POST no recurso com id (PUT/PATCH = 404).
- `?origin=` / `?search=` NAO filtram; so `?contact_id=` filtra deals; `?email=` filtra exato em /contacts (mas pode falhar por dedupe de telefone).
- `POST /deals` RESPEITA `stage_id` explicito; sem ele cai no default/BASE.

**Lia** (e plataformas com financiamento; detalhe -> `lia-api`)
- Sem evento de carrinho abandonado (a etapa fica orfa).
- doc/endereco/UTM so vem no evento `order`; em bill/billing vem vazio (o MERGE do Clint completa quando o order chega).
- Parcela de financiamento (`bill_type: installment`) carrega produto GENERICO -> filtrar pelos product_ids reais descarta a parcela e evita deal duplicado.

**n8n** (detalhe -> `haos-n8n-api`)
- HTTP node `typeVersion 4.4+` (v1 nao anexa OAuth, bug #14020/#12230).
- URL com `=https://` no comeco quebra (remover o `=`).
- `+` na query vira espaco -> usar `sendQuery` + `queryParameters` estruturado.
- PUT rejeita campos read-only (remover id/active/createdAt/updatedAt/tags/versionId/etc.); backup do JSON ANTES.

**Risco recorrente (o que ja nos mordeu)**
- Node de telemetria/Supabase (ex.: "USO DA HAOS") SEM `onError` ANTES da branch Clint: se ele falhar, ABORTA a execucao e o evento nunca chega no CRM (tag/deal nao aplicados). **Mitigar:** por a branch Clint PRIMEIRO, ou `onError: continueRegularOutput` no node de telemetria.

---

## Implementacoes de referencia (exemplo trabalhado, com ids)

| Integracao | Workflow | Plataforma -> produto | Grupo Clint | Stage |
|---|---|---|---|---|
| **Assiny FPV369** | `${RESOURCE_ID}` (branch FPV369) | Assiny, product id `${RESOURCE_ID}` | G369 | "Assiny" |
| **Lia Practitioner** | `${RESOURCE_ID}` (workflow novo) | Lia, 3 product ids | G369 (mesmo) | "Lia" |

Tabela completa de origin_ids, stage_ids (Assiny e Lia), tag e mapeamento de evento -> `references/example-ids.md`.
(IDs internos como ponto de partida; confirmar no painel antes de editar.)

## Restricoes / seguranca

- INTERNA. NAO publicar no HAOS_CC. Sem tokens reais: referenciar vars do MASTER.env (`CLINT_API_TOKEN`, `N8N_API_KEY`, `LIA_API_KEY`, etc.) por NOME.
- Em logs, mascarar email/telefone/CPF.
- Backup do JSON ANTES de todo PUT; backup da lista de webhooks ANTES de criar webhook novo.

## Skills / refs relacionadas

- `clint-api`, `lia-api`, `haos-n8n-api` (as 3 que esta playbook orquestra).
- `yampi`, `tiktok-shop-sim`, `bling` (outras plataformas de venda ja mapeadas).
- `clint-meta-audience-sync` (tag do Clint -> publico Meta; NAO e funil).
- `haos-hetzner-map` (carregar antes de mexer no servidor).
- Memorias: `project_assiny_clint_fpv369`, `project_lia_clint_practitioner`, `learning_n8n_google_oauth`.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
