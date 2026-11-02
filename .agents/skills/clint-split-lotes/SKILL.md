---
name: clint-split-lotes
description: "Separa TODOS os contatos de uma tag do Clint em LOTES de tamanho fixo (ex 5000) e aplica uma tag nova por lote (<prefixo>_Lote1, <prefixo>_Lote2, ...), pra quebrar uma base grande em pedacos disparaveis. Coleta robusta (retenta as paginas vazias transientes da API do Clint, entao traz a base COMPLETA, nao uma fracao). Use SEMPRE que a tarefa for \"separa a tag X em lotes de 5000\", \"quebra a base em lotes\", \"cria Lote1/Lote2 a partir da tag\", \"split de tag em lotes pro disparo\", \"divide os leads dessa tag em blocos de N\", \"fatia a tag em lotes\", \"separa os 17 mil da tag em lotes\", \"gera as tags de lote pra disparar aos poucos\", ou variacoes. Complementa clint-api (usa o ClintClient dela) e clint-disparo-variaveis (a injecao das copies v1..v5 e feita DEPOIS, POR LOTE). NAO dispara mensagem: so coleta e etiqueta. Preserva a tag origem (so ADICIONA tags de lote). Idempotente. Validado em producao 11/07/2026 (17.688 leads da tag ${RESOURCE_ID} em 4 lotes)."
---

# clint-split-lotes

Separa TODOS os contatos de uma tag do Clint em LOTES de tamanho fixo, etiquetando
cada lote com uma tag nova (`<prefixo>_Lote1`, `<prefixo>_Lote2`, ...). Skill PRIVADA
(operacao interna do grupo); NAO vai pro HAOS_CC publico.

E a automacao do que foi feito na mao em 11/07/2026 pros 17.688 leads da tag
`${RESOURCE_ID}`: quebrar uma base grande em pedacos de tamanho gerenciavel
pra disparar aos poucos (respeitando limite/janela de envio, aquecimento de numero,
etc.).

## O que faz e o que NAO faz

- FAZ: acha a tag origem, coleta TODOS os contatos dela (robusto), divide em lotes de
  N e aplica uma tag por lote. So ADICIONA tag; a tag origem fica intacta.
- NAO FAZ: nao dispara mensagem, nao grava as copies `v1..v5`, nao remove a origem.
  A injecao das copies e o disparo vem DEPOIS, por lote, via a skill
  `clint-disparo-variaveis` (ex: `--tag-origem <prefixo>_Lote1`).

## Onde entra no fluxo

```
clint-split-lotes  (esta skill)      -> quebra a tag grande em <prefixo>_Lote1..k
        v
clint-disparo-variaveis (por lote)   -> injeta v1..v5 nos contatos de cada lote
        v
disparo do template WhatsApp (Clint) -> mira UM lote por vez
```

Usa o `ClintClient` da skill **clint-api** (auth via MASTER.env + paginacao robusta).
NAO reimplementa auth nem token.

## A pegadinha da paginacao (JA RESOLVIDA no client)

Descoberta e provada em producao 11/07/2026: `GET /contacts?tag_ids=...` devolve
**paginas VAZIAS transientes** no meio da paginacao, mesmo com `hasNext=true` e mesmo
faltando paginas (`page < totalPages`). O `paginate()` antigo tinha `if not items:
return`, entao PARAVA na 1a pagina vazia e trazia so uma fracao (a tag
`${RESOURCE_ID}` tem `totalCount=17688` / 177 paginas, mas o coletor antigo
trazia so ~1500).

A correcao vive no **ClintClient** (`clint-api/scripts/clint_client.py`): quando a
resposta traz o metadado canonico `totalPages`, ele pagina de 1..totalPages e, quando
uma pagina vem vazia e ainda faltam paginas, RETENTA a MESMA pagina com backoff (ate
8x) antes de seguir; dedup por `id`. Assim a coleta traz os 17.688 completos.

Esta skill so REUSA esse coletor robusto (`list_contacts_by_tag`). Como defesa extra,
o `split_lotes.py` tambem carrega um `robust_collect_local` identico (flag
`--coleta-local`) pro caso improvavel do metodo do client regredir.

## Como rodar

```
python scripts/split_lotes.py --tag-origem NOME [--batch N] [--prefixo NOME]
       [--workers N] [--dry-run] [--limpar-lotes] [--coleta-local]
```

### Argumentos

| Flag | Default | O que faz |
|---|---|---|
| `--tag-origem` | (obrigatorio) | Nome da tag cuja base sera separada. |
| `--batch` | `5000` | Tamanho de cada lote. |
| `--prefixo` | = nome da tag origem | Prefixo das tags de lote. Viram `<prefixo>_Lote1..k`. |
| `--workers` | `8` | Threads paralelas pra aplicar a tag. |
| `--dry-run` | off | So mostra o plano (contatos, numero de lotes, tamanho de cada). Nada e criado/aplicado. |
| `--limpar-lotes` | off | Antes de aplicar, remove as tags `<prefixo>_LoteX` pre-existentes dos contatos que as tenham (reaplicar limpo). NAO toca na origem. |
| `--coleta-local` | off | Usa o coletor robusto LOCAL (defesa extra) em vez do metodo do client. So se o client regredir. |

### Exemplos

```bash
# 1) Planejar (read-only): quantos contatos, quantos lotes, tamanho de cada
python scripts/split_lotes.py --tag-origem "${RESOURCE_ID}" --dry-run

# 2) Executar: 4 lotes de 5000 (tags ${RESOURCE_ID}..4)
python scripts/split_lotes.py --tag-origem "${RESOURCE_ID}" --batch 5000

# 3) Prefixo custom (tags viram ${RESOURCE_ID}, ${RESOURCE_ID}, ...)
python scripts/split_lotes.py --tag-origem "${RESOURCE_ID}" --prefixo "Janela1" --batch 5000

# 4) Reaplicar limpo (havia um Lote1 provisorio): tira os lotes antigos antes
python scripts/split_lotes.py --tag-origem "${RESOURCE_ID}" --batch 5000 --limpar-lotes
```

## Fluxo interno

1. **Achar a tag origem** (`find_tag_by_name`). Se nao existe, PARA (nao cria nada).
2. **Coletar contatos** (robusto, dedup por `id`) via `list_contacts_by_tag`. Reporta
   `coletados`, `totalCount` da API e as paginas vazias persistentes. Se
   `abs(coletados - totalCount) > 50`, avisa pra revisar.
3. **Plano dos lotes**: `ceil(n / batch)` lotes; imprime o tamanho de cada
   (`<prefixo>_LoteK`). Com `--dry-run` para aqui.
4. **(opcional) `--limpar-lotes`**: acha as tags `^<prefixo>_Lote\d+$`, coleta os
   contatos de cada (robusto) e remove a tag deles, em paralelo com retry.
5. **Aplicar lotes**: pra cada bloco de `batch`, cria/reusa a tag `<prefixo>_LoteK`
   (`POST /tags`, reusa se ja existe) e aplica em paralelo (`ThreadPoolExecutor` +
   retry/backoff). So ADICIONA tag; a origem nunca e removida.
6. **Verificar**: releitura robusta de cada lote e reporta `alvo | aplicado | falhas |
   conferido`.

## Garantias

- **Preserva a origem**: a skill so faz `add_tags_to_contact`; nunca remove a tag
  origem. (`--limpar-lotes` remove APENAS tags `<prefixo>_LoteX`, nunca a origem.)
- **Idempotente**: rerun reusa as tags de lote (nao duplica) e reaplicar uma tag num
  contato que ja a tem e inocuo.
- **Read-only ate mutar**: `--dry-run` e toda a fase de coleta nao alteram nada.
- **Nao expoe token**: o `ClintClient` le do MASTER.env sozinho; nada sensivel e
  impresso. Saida em UTF-8.

## Validacao 11/07/2026 (producao)

Tag `${RESOURCE_ID}` (id `${RESOURCE_ID}`,
`totalCount=17688`) separada em **4 lotes de 5000**: `5000, 5000, 5000, 2688`. A coleta
robusta trouxe os 17.688 completos (paginas vazias persistentes = zero), contra os
~1500 que o coletor antigo (parava na 1a pagina vazia) trazia. Um `Lote1` provisorio
anterior foi removido com o equivalente do `--limpar-lotes` antes da reaplicacao
definitiva.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
