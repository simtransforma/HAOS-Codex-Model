---
name: waid-curseduca-api
description: "Playbook operacional da API do Waid (ex-CursoEduca), plataforma que roda o 369Flix, matricular aluno, criar membro, adicionar/remover de grupo de acesso, inativar, matr\u00edcula em massa idempotente. Use SEMPRE que a tarefa envolver acesso de aluno na plataforma de curso, \"matricula fulano no 369Flix\", \"libera o acesso na plataforma\", \"cadastra os compradores no curso\", \"o pessoal n\u00e3o recebeu o acesso\", \"matr\u00edcula em massa\", \"grupo do Evolu\u00e7\u00e3o 369\", \"Waid\", \"CursoEduca\", \"369Flix\", \"tira o acesso de fulano\", \"termo de aceite do curso\". Tem os paths assim\u00e9tricos, a exig\u00eancia de token ADMIN e as pegadinhas que j\u00e1 custaram tempo. Validado em produ\u00e7\u00e3o 16 a 19/07/2026 (600 compradores matriculados). Autoria, usuario Marco Menegussi Scaglianti."
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

# Waid / CursoEduca (369Flix), playbook de matrícula via API

Waid é o novo nome do CursoEduca. O tenant do grupo é o **369Flix**.
Doc oficial, help.waid.io. Specs, `prof.curseduca.pro/docs-json` (Members) e `clas.curseduca.pro/docs-json` (Contents).

Autoria e manutenção, usuario Marco Menegussi Scaglianti.

## a. Quando usar

Gatilhos na linguagem real do usuario:
- "matricula fulano no 369Flix"
- "libera o acesso na plataforma"
- "cadastra os compradores no curso"
- "o pessoal não recebeu o acesso"
- "matrícula em massa"
- "grupo do Evolução 369"
- "Waid", "CursoEduca", "369Flix"

Também aciona implicitamente quando o resultado esperado for um comprador conseguir entrar na área de membros do curso.

## b. Pré-requisitos

**Credenciais (nomes das variáveis no ${USER_SECRET_FILE}, nunca os valores):**
- `CURSOEDUCA_API_KEY`
- `CURSOEDUCA_ACCESS_TOKEN`

**O token PRECISA ser de usuário ADMIN.** `user.roles` no JWT deve conter `ADMIN` (aceita `ADMIN` sozinho ou `ADMIN` e `SUPPORT`). Token de **INSTRUCTOR autentica** (200 em `/groups`) mas dá **403 "Forbidden resource"** em criar membro, buscar por email e inativar. As flags `is_curseduca_admin` e `admin_permissions` são de staff da plataforma, não do tenant, e vêm false ou vazias mesmo no token bom, não use elas como critério.

**O JWT não tem claim `exp`**, então não dá pra prever expiração. Se der 401 ou 403 global, o token foi revogado ou é de papel errado.

**Pegadinha real:** token copiado da UI selecionando o texto vem **ABREVIADO com reticências no meio** e dá 403. Usar o botão de copiar da interface.

Checagem rápida do papel do token (sem imprimir o token):

```bash
python -c "import os,base64,json; t=os.environ['CURSOEDUCA_ACCESS_TOKEN']; p=t.split('.')[1]; p+='='*(-len(p)%4); print(json.loads(base64.urlsafe_b64decode(p)).get('user',{}).get('roles'))"
```

## c. Passo a passo

**Base:** `https://service.example.invalid` (Members API).

**Headers SEMPRE os DOIS juntos.** Um sozinho dá 403, mesmo nos endpoints que a spec diz serem api_key-only:

```
api_key: $CURSOEDUCA_API_KEY
Authorization: Bearer $CURSOEDUCA_ACCESS_TOKEN
Content-Type: application/json
```

### 1. Buscar aluno por email

```bash
curl -s "https://service.example.invalid" \
  -H "api_key: $CURSOEDUCA_API_KEY" \
  -H "Authorization: Bearer $CURSOEDUCA_ACCESS_TOKEN"
```

- **404** = não existe, siga para criar.
- **200** = existe, devolve `{id, uuid, groups, ...}`.

⚠️ **`GET /members?search=` NÃO FILTRA.** Ignora o parâmetro e devolve membros aleatórios de uma base de 32 mil. Nunca usar pra buscar aluno. Só `/api/v1/members/by?email=`.

### 2. Criar aluno já dentro do grupo

```bash
curl -s -X POST "https://service.example.invalid" \
  -H "api_key: $CURSOEDUCA_API_KEY" \
  -H "Authorization: Bearer $CURSOEDUCA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fulano de Tal",
    "email": "user-000047@account.example.invalid",
    "password": "<senha forte aleatória gerada na hora>",
    "group": {"id": 124},
    "sendMemberRegisteredEmail": true,
    "phones": {"mobile": {"countryCode": "55", "areaCode": "11", "number": "999998888"}}
  }'
```

- `sendMemberRegisteredEmail: true` dispara o email de criação de senha.
- **409** = já existe, cai no fluxo do passo 3.
- Quem JÁ tinha cadastro **não recebe email**, entra com a senha que já tem. Isso é esperado, não é falha.
- A senha deve ser forte e aleatória por aluno, gerada em memória, nunca fixa e nunca logada.

### 3. Adicionar ao grupo (aluno que já existe)

⚠️ **Path assimétrico de propósito, SEM o prefixo `/api/v1`.** Com o prefixo dá 404.

```bash
curl -s -X POST "https://service.example.invalid" \
  -H "api_key: $CURSOEDUCA_API_KEY" \
  -H "Authorization: Bearer $CURSOEDUCA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"member": {"id": 12345, "uuid": "<uuid do membro>", "role": "STUDENT"}, "group": {"id": 124}}'
```

Exige os TRÊS campos do member (`id`, `uuid`, `role`). É **IDEMPOTENTE**, re-adicionar quem já está devolve 201 sem erro.

### 4. Remover do grupo

```bash
curl -s -X DELETE "https://service.example.invalid" \
  -H "api_key: $CURSOEDUCA_API_KEY" -H "Authorization: Bearer $CURSOEDUCA_ACCESS_TOKEN"
```

### 5. Inativar membro

⚠️ O path `/members/{id}/inactivate-member` dá **404**. O correto é a raiz:

```bash
curl -s -X PATCH "https://service.example.invalid" \
  -H "api_key: $CURSOEDUCA_API_KEY" \
  -H "Authorization: Bearer $CURSOEDUCA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"member": {"id": 12345}}'
```

**NÃO EXISTE delete de membro na API.** Inativar é o máximo.

### 6. Matrícula em massa

Padrão obrigatório do script:
- **Idempotente:** sempre `members/by?email=` antes; 409 no create cai em `members/groups`; `members/groups` é idempotente por natureza. Re-rodar é seguro.
- **Concorrência baixa** (2 a 3) e pausa entre chamadas.
- **Estado salvo em arquivo** (jsonl com email e status) pra re-rodar só o que faltou.
- **CSV de resultado** ao fim, com email, member_id, ação tomada (criado, adicionado, já estava) e erro.
- Nunca gravar senha nem token no arquivo de estado ou no CSV.

**Referência real de throughput:** 600 compradores processados em ~34 minutos, sem falha (19/07/2026).

## d. Verificação (como provar que deu certo)

1. `GET /api/v1/members/by?email=` do aluno e conferir que o grupo alvo aparece no array `groups` do payload.
2. `GET /groups/{id}/members` para contar o total do grupo antes e depois do lote. O delta tem que bater com os "criado" mais "adicionado" do CSV.

Não declarar conclusão sem esses dois números na mão.

## e. Pegadinhas e anti-padrões

| # | Pegadinha | O que fazer |
|---|---|---|
| 1 | Um header só dá 403 | Mandar `api_key` **e** `Authorization: Bearer` sempre juntos |
| 2 | Paths assimétricos | Busca com `/api/v1`, vínculo de grupo **sem** `/api/v1`. Não "padronize" |
| 3 | `GET /members?search=` não filtra | Usar só `/api/v1/members/by?email=` |
| 4 | Token INSTRUCTOR | Autentica mas dá 403 em criar/buscar/inativar. Exigir role ADMIN |
| 5 | Token copiado da UI truncado com reticências | Usar o botão de copiar |
| 6 | Sem delete de membro | Só remover do grupo e inativar |
| 7 | Inativar no path errado | `PATCH /inactivate-member` na raiz, body `{"member":{"id":N}}` |
| 8 | Termo de aceite | **Não existe campo nem endpoint na API.** Membro criado por API nasce com termo PENDING e a plataforma cobra o aceite no primeiro login na UI, gerando auditoria com IP, navegador e geolocalização. Isso é **melhor juridicamente** do que aceitar pelo aluno. Nada a fazer no código. O termo é configurável por grupo de acesso no painel |

## f. Rollback

O máximo que a API permite:
1. `DELETE /members/{id}/groups/{groupId}`, tira o acesso ao conteúdo.
2. `PATCH /inactivate-member`, desativa o login.

O **registro do membro persiste** (não há delete). Rollback de lote deve usar o CSV de resultado, revertendo só as linhas com ação "criado" ou "adicionado".

## g. Dados do ambiente atual

| Item | Valor |
|---|---|
| Tenant | 369Flix |
| Grupo Evolução 369 | id **124**, uuid `${USER_RESOURCE_000048}` |
| Conteúdo "POWER MIND EXPERIENCE \| EVOLUÇÃO 369" | uuid `${USER_RESOURCE_000049}` |
| Base Members | `https://service.example.invalid` |
| Base Contents | `https://service.example.invalid` |

## Histórico

- **16/07/2026:** API mapeada ao vivo no projeto de pesquisa de recuperação P369. 8 pegadinhas documentadas.
- **19/07/2026:** matrícula em massa de 600 compradores PMX26 no grupo Evolução 369, ~34 min, sem falha. Playbook promovido a skill.

Créditos: **usuario Marco Menegussi Scaglianti**.


## Adaptacao Codex HAOS

- Carregar `${USER_WORKSPACE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nao executar push, deploy, publicacao, mensagem, gasto, servidor ou infraestrutura externa sem OK explicito do usuario.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.
