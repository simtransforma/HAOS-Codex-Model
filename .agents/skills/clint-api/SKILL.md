---
name: clint-api
description: "Reference completa da API REST do Clint CRM (api.clint.digital/v1), endpoints, schemas, autenticação, pegadinhas conhecidas + biblioteca Python reutilizável `ClintClient`. Use SEMPRE que precisar interagir com Clint via API: buscar/listar/criar/atualizar contatos, consultar/aplicar/remover tags, gerenciar deals (negócios), pipelines, stages, organizations, custom fields. Triggers típicos do user, \"puxar contatos do Clint\", \"buscar leads no Clint\", \"exportar tag X do Clint\", \"integrar Clint com [outra plataforma]\", \"Clint API\", \"extrair dados do CRM\", \"listar deals do Clint\", \"adicionar tag no contato Clint\", \"criar contato no Clint via API\", \"sincronizar Clint com Y\". Padrão contrato de exemplo a verificar 06/06/2026."
---

<!-- synthetic-client-examples -->
Exemplos sinteticos: nomes de campanha, contatos, IDs, valores e configuracoes abaixo sao ficticios, nao um inventario de cliente nem evidencia de producao. Adaptar IDs e slugs ao contrato autorizado; conferir a versao da API e o resultado antes de qualquer efeito externo.



# Clint CRM API: Reference completa

Biblioteca + docs pra usar a API do Clint sem precisar redescobrir pegadinhas toda vez.

## Regra obrigatoria de negocios

Antes de criar ou atualizar cards, aplicar
a regra de jornada da Clint Global (dependency not bundled: ../clint-global/references/jornada-card-pagamento.md):
reutilizar o card por contato/origem; pagamento confirmado atualiza etapa,
valor, status `WON` (Fechado/Ganho) e tag paga. Em origens separadas, dar ganho
na anterior e criar ou atualizar na seguinte, sem duplicar. Ganho de etapa
anterior nao substitui comprovacao financeira.

## Quando usar

Triggers do user:
- "puxar/buscar/listar contatos do Clint"
- "exportar leads da tag X"
- "criar/atualizar contato no Clint"
- "consultar/aplicar/remover tag"
- "listar deals/negócios"
- "integrar Clint com [outra plataforma]"
- "Clint API"
- "extrair dados do CRM"

Use também quando outra skill (ex: `clint-meta-audience-sync`) precisar de cliente Clint, `import` a `${USER_PROJECT_ROOT}/scripts/clint_client.py`.

## Endpoint base

```
https://api.clint.digital/v1
```

## Autenticação

Header **`api-token`** (NÃO `Authorization: Bearer`):

```python
headers = {"api-token": "example-api-token", "accept": "example-accept"}
```

Configurar a autenticacao local aprovada e conferir os aliases de ambiente aceitos pelo cliente. Nenhum cofre ou configuracao de cliente e fornecido.

## Como usar (3 caminhos)

### A) Use a biblioteca pronta (mais simples)

```python
from clint_client import ClintClient

c = ClintClient.from_master_env()  # depende da configuracao local autorizada do usuario

# Achar tag por nome
tag = c.find_tag_by_name("example-tag")
print(tag["id"], tag["name"])

# Listar contatos de uma tag (paginado automaticamente)
contacts = c.list_contacts_by_tag(tag["id"])
print(f"{len(contacts)} contatos")

# Listar todas as tags
tags = c.list_tags()

# Get contato individual
contact = c.get_contact(contact_id)

# Exemplo sintetico: deals e custom fields; validar contrato antes de executar.

# Criar deal numa suborigem (upsert de contato embutido) + gravar custom fields
# (create_deal faz os 2 passos: POST /deals e DEPOIS POST /contacts/{id} c/ fields,
#  porque POST /deals ignora `fields`)
deal = c.create_deal(
    origin_id="example-origin_id",  # Compra Aprovada
    email="contact@example.invalid", name="example-name", phone="example-phone",
    value=100.00,
    fields={"utm_source": "example-utm-source", "doc": "<EXAMPLE_DOC>", "ip_1": "example-ip-1"},
)
contact_id = deal["data"]["contact_id"]

# Dedupe antes de criar (POST /deals NÃO é idempotente)
if not c.find_deal_by_contact(contact_id, origin_id=ORIGIN_ID):
    c.create_deal(ORIGIN_ID, email=email, ...)

# Marcar deal como ganho (seta won_at)
c.mark_deal_won(deal_id)

# Adicionar tag(s), body é ARRAY de strings
c.add_tags_to_contact(contact_id, ["${RESOURCE_ID}"])

# Atualizar só custom fields (MERGE, não sobrescreve preenchido)
c.update_contact_fields(contact_id, {"utm_source": "example-utm-source"})
```


### B) HTTP direto (urllib/requests)

Ver `references/endpoints.md` pra exemplos de cada endpoint.

### C) Curl (debug)

```bash
curl -H "api-token: $CLINT_API_TOKEN" \
     -H "accept: application/json" \
     "https://api.clint.digital/v1/tags?page=1&limit=100"
```

## Pegadinhas críticas (mapeadas em produção)

⚠️ **Leia `references/troubleshooting.md` antes de invocar endpoint novo.**

Pegadinhas resumidas:

| # | Sintoma | Causa-raiz | Solução |
|---|---|---|---|
| 1 | `?search=name` retorna 100 tags aleatórias | Param `search` da API **não filtra de fato** | Use paginação completa + filtro client-side |
| 2 | `contact.cep`, `.doc`, `.cidade` vêm `None` mesmo com dados | PII fica em `contact["fields"]["cep"|"doc"|...]`, não no raiz | Sempre acessar via `fields.*` com fallback no raiz |
| 3 | `contact.phone` está vazio | Telefone canônico é `fullPhone` (não `phone` nem `complete_phone`) | Prioridade: `fullPhone` → `complete_phone` → `phone` |
| 4 | `estado` vem como "São Paulo" e quebra match Meta | Não normaliza pra UF de 2 letras | Usar `STATE_MAP` da skill `clint-meta-audience-sync` |
| 5 | Loop de paginação infinito | API pode não ter `hasNext` confiável | Break se `len(items) < limit` |
| 6 🔴 | Custom fields somem ao criar deal | **`POST /deals` IGNORA `fields` silenciosamente** | Gravar fields via `POST /contacts/{id}` (use `create_deal(...)` que faz os 2 passos) |
| 7 | Tag não aplica, 400 "Body must be an array of strings" | `POST /contacts/{id}/tags` quer **ARRAY** de tag_id, não objeto | `["uuid1","uuid2"]` (use `add_tags_to_contact`) |
| 8 | `PUT/PATCH /contacts/{id}` ou `/deals/{id}` → 404 | Update é **POST no recurso com id** | `POST /contacts/{id}` (MERGE de fields) / `POST /deals/{id}` |
| 9 | `?email=` retorna 0 p/ comprador real | Dedupe interno por **telefone** liga evento a outro email | Match em massa = email **+** telefone, restrito por **tag** |
| 10 | `?origin=` / `?search=` em /deals não filtram | Só `?contact_id=` filtra de verdade | Filtrar origin no código (`find_deal_by_contact`) |

## Endpoints mapeados

Resumo (detalhes em `references/endpoints.md`):

| Recurso | Endpoint | Observações |
|---|---|---|
| Tags | `GET /tags?page=N&limit=100` | search bugado |
| Contatos por tag | `GET /contacts?tag_ids={uuid}&page=N&limit=100` | paginado |
| Contato individual | `GET /contacts/{id}` | retorna `fields` aninhado |
| Criar contato | `POST /contacts` | sem upsert; cria duplicata se email existe |
| **Update contato** | `POST /contacts/{id}` | ⚠️ POST (não PUT/PATCH=404); `{"fields":{...}}` = **MERGE**; ÚNICA rota p/ custom field |
| Add tag(s) | `POST /contacts/{id}/tags` | body = **array de strings** `["uuid"]` |
| Origins (suborigens) | `GET /origins?page=N&limit=100` | modelo real = origin + stage (não pipeline) |
| Deals/Negócios | `GET /deals?page=N&limit=100` | só `?contact_id=` filtra |
| **Criar deal** | `POST /deals` | upsert de contato embutido; ⚠️ **`fields` IGNORADO**; não-idempotente |
| **Marcar ganho** | `POST /deals/{id}` `{"status":"WON"}` | seta `won_at` |
| Pipelines | `GET /pipelines` | conferir pipeline ou origin/stage no contrato da versao usada |
| Stages | `GET /pipelines/{id}/stages` | |
| Organizations | `GET /organizations?page=N&limit=100` | empresas dos contatos |
| Deletar | `DELETE /contacts/{id}` / `DELETE /deals/{id}` | 204 no sucesso |

⚠️ **Outros 20+ endpoints existem** mas não foram validados ainda. Quando explorar um novo, atualize `references/endpoints.md` com schema + pegadinhas.

## Schema dos objetos principais

Ver `references/schema.md` pra estrutura completa de Contact, Tag, Deal, etc.

Resumo crítico (Contact):

```python
{
  "id": "example-id",
  "name": "Exemplo sintetico",
  "email": "contact@example.invalid",
  "fullPhone": "<EXAMPLE_FULLPHONE>",  # ← canônico
  "phone": "<EXAMPLE_PHONE>",                # ← raw, pode estar diferente
  "complete_phone": "example-complete-phone",       # ← legado
  "tags": [{"id": "example-id", "name": "Exemplo sintetico"}],
  "fields": {                    # ← PII aqui dentro
    "cep": "<EXAMPLE_CEP>",
    "doc": "<EXAMPLE_DOC>",        # CPF
    "sobrenome": "example-sobrenome",
    "cidade": "example-cidade",
    "estado": "SP" ou "São Paulo",
    "bairro": "example-bairro",
    "endereco": "example-endereco",
  },
  "organization": {
    "fields": {"state": "example-state"},  # ← às vezes estado vem aqui
  },
  "created_at": "2000-01-01T00:00:00Z",
  "updated_at": "2000-01-01T00:00:00Z",
}
```

## Restrições/segurança

- **NUNCA** persistir token em arquivos da vault, logs ou screenshots
- Headers `api-token`, **não** `Authorization` (erro silencioso 401)
- Rate limit não documentado, usar backoff de 200ms entre paginas em loops longos
- Hash PII (SHA-256) ANTES de enviar pra qualquer destino externo
- Em logs, mascarar email/phone/CPF (`mail.priv@***`, `5511***8888`)

## Convenção de uso em outras skills

Outras skills que precisem de Clint devem **importar** `ClintClient`:

```python
sys.path.insert(0, str(Path.home() / ".Codex" / "skills" / "clint-api" / "scripts"))
from clint_client import ClintClient
```

Não duplicar lógica de auth/paginação/normalização. Quando descobrir pegadinha nova, **atualize esta skill**, não a skill consumidora.

## Limites conhecidos

- Sem endpoint nativo `created_after` em `/contacts` → polling diff é `walk reverso` (ver workflow base n8n `${RESOURCE_ID}`)
- Webhook nativo só pra alguns events, não confiável pra "tag added" em alta carga
- Bulk operations (criar 1000 contatos de uma vez) não documentado, usar loop 1-a-1

## Modelos condicionais de integracao

- **BI e tags:** se houver integracao autorizada, importar contatos e tags com paginacao completa, reconciliar totais e registrar descartes sem email. Definir conexao, limites e eventual uso de pooler para o ambiente do usuario; nenhuma contagem, cron ou banco e presumido instalado.
- **Audiencias:** se houver workflow n8n autorizado, comparar snapshots de tags por polling/diff e definir a agenda, a zona de horario e o destino de audiencia. Verificar consentimento, cotas e opt-out antes de qualquer efeito externo; nenhum workflow e apresentado como ativo.
- **Webhooks de venda:** se o provedor e o CRM suportarem a integracao, configurar o mapeamento autorizado de eventos para contatos, validando autenticacao, idempotencia e tratamento de falhas. Exigir teste controlado e readback antes de declarar entrega.
- **Broker local:** se o usuario fornecer um adaptador, revisar allowlist de rotas e leitura segura da credencial, testar sua interface e manter logs sem segredos. Nao presumir sandbox, comando ou infraestrutura pessoal de terceiros.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
