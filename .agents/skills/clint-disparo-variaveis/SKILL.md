---
name: clint-disparo-variaveis
description: "Procedimento especializado de clint-disparo-variaveis; consultar requisitos e evidencias antes de executar."
---

# clint-disparo-variaveis

Prepara contatos do Clint pra disparo em massa de WhatsApp com template de
variaveis, gravando os custom fields `v1..v5` direto via API. Skill PRIVADA
(operacao interna da Clint); NAO vai pro HAOS_CC publico.

## O problema que resolve

puxam dos custom fields do contato: `CONTACT.V1 .. CONTACT.V4`. O jeito manual e
montar um CSV, importar pela tela do Clint (mapeando coluna->campo) e so entao
telefones (ou IDs) + as copies, e a skill:

1. acha cada contato na Clint,
2. grava as copies nos campos `v1..v5` via API,
3. aplica uma tag (opcional) pro disparo mirar so nesses contatos.

## Os slugs (confirmados por print da tela)

Os campos do template no painel do Clint tem slug MINUSCULO (tipo Texto, ativos):

| Slug | Variavel no template | Uso |
|---|---|---|
| `v1` | `{{1}}` | em uso |
| `v2` | `{{2}}` | em uso |
| `v3` | `{{3}}` | em uso |
| `v4` | `{{4}}` | em uso |
| `v5` | (nenhuma) | existe, template atual NAO usa |

⚠️ O slug e case-sensitive na gravacao. Tem que ser `v1`, nao `V1`. Slug que
nao existe no painel e descartado silenciosamente pela API (silent-drop).

## Como rodar

```
python scripts/injetar_vars_clint.py [ENTRADA | --tag-origem NOME]
       [--tag NOME] [--v1 TXT ... --v5 TXT] [--criar-tag] [--criar] [--dry-run]
       [--workers N] [--limit N] [--fone COL] [--id-col COL]
```

### Dois modos de entrada (escolha UM)

- **Modo ARQUIVO** (`ENTRADA` posicional): le CSV/xlsx e resolve cada linha por
  ID ou telefone. Comportamento historico, intacto.
- **Modo TAG-ORIGEM** (`--tag-origem NOME`): busca os contatos DIRETO pela tag
  (`find_tag_by_name` + `list_contacts_by_tag`), sem arquivo. A coleta e ROBUSTA
  (paga a tag inteira, nao so a 1a fatia). Se a tag nao existir OU vier 0
  contatos, PARA e reporta (nao grava nada). As copies vem so das flags `--vN`
  (nao ha planilha). **E o caminho recomendado pro disparo em massa** (evita
  montar/limpar planilha): use pra gravar copies em TODOS os leads de uma tag
  (ex: evento ao vivo). Validado em producao no 1o disparo real (11/07/2026):
  498 leads em ~40s.
  - **ATUALIZADO 11/07/2026: a coleta por tag agora e robusta**
    (`list_contacts_by_tag` corrigido no `clint_client.py` pra retentar paginas
    vazias intermitentes da API). Seguro pra tags grandes (validado em 17.688 e
    em 498). Antes desta data, tag grande truncava em ~1500. A API do Clint
    devolve PAGINAS VAZIAS TRANSIENTES no meio da paginacao (mesmo com
    `hasNext=true` e faltando paginas): o `paginate` antigo parava na 1a vazia; o
    novo pagina de 1 ate `totalPages`, RETENTA cada pagina vazia com backoff
    (ate 8 tentativas) e so entao segue, deduplicando por `id`. Resultado:
    paginas vazias persistentes = zero, coleta completa. NAO use paginacao
    ingenua (parar na 1a pagina vazia) pra tag grande.
  - **Allowlist client-side**: cada contato do Clint traz sua propria lista
    `tags`. Depois de coletar, a skill so mantem quem REALMENTE carrega a tag de
    origem. Se o filtro `?tag_ids=` do servidor algum dia regredir e devolver a
    base inteira (varios filtros da API ja sao documentados como frouxos), a
    skill descarta quem nao tem a tag e nunca grava fora do alvo. Se a API parar
    de devolver `tags` (fail-open), nao filtra pra nao quebrar o caminho.
  - Se `--tag-origem` for usada sem nenhuma copy (`--vN`) e sem `--tag` pra
    aplicar, PARA (nao ha nada a gravar). A `--tag` a aplicar so e criada
    DEPOIS de validar a origem (nunca cria tag vazia se a origem falhar).

### Gravacao paralela + verificacao (sincrono)

- As gravacoes (`update_contact_fields` = `POST /contacts/{id}`) rodam num
  `ThreadPoolExecutor` com `--workers` (default 8). SEMPRE **sincrono no proprio
  processo** — nunca background/nohup, que morria junto com o ciclo da
  ferramenta e travava em ~90/498 no sequencial. Foi exatamente essa mudanca
  (sincrono + paralelo) que destravou o disparo.
- **Retry/backoff sem duplicacao**: o `ClintClient` ja retenta 5xx e erro de
  rede por dentro; esta skill so cobre o que ele NAO cobre — `429` (throttle) e
  resposta truncada — com backoff exponencial + **jitter** (evita thundering
  herd de N workers). Sem retry aninhado 3x3. Contato que falha e registrado e o
  processo segue.
- **Verificacao final X/N**: apos gravar, rele os contatos e conta quantos
  ficaram com o valor esperado.
  - No modo TAG-ORIGEM rele a tag INTEIRA de uma vez (paginacao robusta, com a
    mesma retentativa de pagina vazia da coleta) e confere em memoria: em tag
    pequena sao poucas requisicoes (ex: ~5 pra 498 leads) em vez de 1 GET por
    contato. Em tag grande a releitura tambem cobre todas as paginas.
  - No modo ARQUIVO sem tag, cai pro `get_contact` individual (com retry).
  - O endpoint de listagem por tag tem **read-after-write lag** (a escrita
    persiste na hora, mas a listagem so reflete alguns segundos depois). Por
    isso a verificacao **converge**: rele algumas vezes com um settle curto
    ANTES de concluir que faltou. So o que continuar faltando depois de a
    leitura convergir dispara uma rodada extra de gravacao (evita reescrever o
    lote inteiro por leitura defasada). Comparacao tolerante a espacos.

### ENTRADA (CSV ou xlsx) — modo arquivo

Precisa de UMA forma de achar o contato por linha:

- **coluna de ID do Clint** (`id`, `contact_id`, `clint_id`, ...) -> match exato,
  mais seguro. Se existir, tem prioridade.
- **coluna de telefone** (`telefone`, `numero`, `phone`, `celular`, `whatsapp`,
  `fone`, `tel`, ...). `--fone` forca o nome da coluna.

Pode ter tambem colunas `v1..v5` (copies por linha) e/ou uma coluna de nome.

> Perf: no modo ARQUIVO a resolucao de cada linha (lookup por ID ou telefone) e
> SEQUENCIAL no thread principal (so a gravacao/verificacao sao paralelas). Pra
> LOTE GRANDE prefira o modo `--tag-origem` (leitura em bloco paginada) ou traga
> uma coluna de ID (match direto, 1 GET/linha) em vez de telefone (1-2 GETs +
> variacao do 9o digito por linha).

### Copies: fixas (flag) x por linha (planilha)

- `--v1..--v5`: copy FIXA aplicada a TODAS as linhas (modo disparo em massa).
  Sobrepoe a coluna `vN` da planilha quando as duas existem.
- Coluna `vN` na planilha: copy especifica daquela linha.
- So grava campo com valor. String vazia a API do Clint IGNORA (nao limpa campo).

### Tag

- `--tag NOME`: aplica a tag em cada contato. Por padrao EXIGE que a tag ja
  exista (se nao existir, avisa e segue SEM tag; nao inventa tag).
- `--criar-tag`: se a tag nao existir, cria (use so quando for intencional).

### Exemplos

```bash
# 1) Simular (nao grava): copies fixas pra todos, mirando por telefone
python scripts/injetar_vars_clint.py lista.csv --tag ${RESOURCE_ID} \
  --v1 "Convite especial" --v4 "Aperte o botao" --dry-run

# 2) Gravar de verdade, copies por linha vindas da planilha
python scripts/injetar_vars_clint.py lista.xlsx --tag ${RESOURCE_ID}

# 3) Por ID do Clint (mais seguro), gravando
python scripts/injetar_vars_clint.py ids_e_copies.csv

# 4) TAG-ORIGEM: pega TODOS os contatos da tag e injeta as copies (8 workers)
python scripts/injetar_vars_clint.py --tag-origem Evento_AoVivo \
  --v1 "Comecou!" --v4 "Entrar agora" --workers 8
```

No Windows, rodar com `${RESOURCE_ID}=1` na frente garante emoji/acento no console
(o script ja forca UTF-8 na saida, mas o env var ajuda no PowerShell/Bash).

## Como acha o contato por telefone

Normaliza o telefone (reusa `normaliza_fone` da skill `limpar-lista-contatos`) ->
tenta `?phone=` com o numero normalizado -> se nao achar, gera a variacao com/sem
o 9o digito (logica da `chave_canonica`) e tenta de novo. SEMPRE confere no
cliente (chave canonica do `fullPhone`) antes de aceitar o match, entao nunca
escreve num contato que so voltou por filtro frouxo. Se mais de um contato casar,
pula e reporta (nao adivinha).

## Fatos da API que a skill depende (validados)

- **Gravar custom field = `POST /contacts/{id}` com `{"fields":{...}}`** (metodo
  `update_contact_fields` do `ClintClient`). E a UNICA rota que persiste custom
  field. `POST /deals` IGNORA `fields`.
- **Overwrite FUNCIONA.** Campo `vN` ja preenchido E sobrescrito por um novo
  valor nao vazio (validado 10/07/2026: escrevi PROBE_A, depois PROBE_B, leu
  PROBE_B). Isso contradiz a nota antiga da skill `clint-api` ("merge nao
  sobrescreve preenchido"); na pratica sobrescreve. Essencial pra re-disparo com
  copies novas.
- **String vazia / null sao IGNORADOS** (nao limpam o campo). Pra "limpar" de
  verdade, so pelo painel. Por isso a skill so envia valores nao vazios.
- **Emoji e acento sobrevivem** ao round-trip da API (UTF-8, urllib json). Vide
  `👉` e `Indesistível` gravados e lidos identicos.
- **Tag = array de strings** no `POST /contacts/{id}/tags` (`add_tags_to_contact`).
- **`get_contact` volta `{"status":..,"data":{...}}`**; os campos ficam em
  `data.fields`.
- **Listagem por tag tem read-after-write lag.** `list_contacts_by_tag` (=
  `GET /contacts?tag_ids=`) so reflete uma gravacao recente alguns segundos
  depois; `get_contact` individual e fresco. Confirmado 11/07/2026 (logo apos
  gravar, a listagem mostrou o valor antigo; segundos depois, o novo). Por isso
  a verificacao converge com settle antes de reescrever.
- **Cada contato traz sua lista `tags`** (`[{id,name,color}, ...]`) — permite a
  allowlist client-side no modo `--tag-origem`.
- **`GET /contacts?tag_ids=` devolve paginas VAZIAS TRANSIENTES no meio da
  paginacao** (mesmo com `hasNext=true` e `page < totalPages`). Descoberto e
  provado em producao 11/07/2026: a tag `${RESOURCE_ID}` tem
  `totalCount=17688` / 177 paginas, mas a coleta ingenua (parar na 1a vazia)
  trazia so ~1500. A resposta expoe os metadados canonicos (`status`,
  `totalCount`, `page`, `totalPages`, `hasNext`, `hasPrevious`, `data`). Por isso
  `list_contacts_by_tag` no `clint_client.py` foi corrigido pra paginar de 1 ate
  `totalPages`, RETENTAR a pagina vazia com backoff (ate 8 tentativas, a vazia e
  transiente) e so entao seguir, deduplicando por `id`. Com isso a coleta traz a
  tag inteira (paginas vazias persistentes = zero).

## Seguranca

- Nunca expoe o token (o `ClintClient` le do `MASTER.env` e nunca imprime).
- Mascara PII nos logs: telefone/email (`mask_pii`) e **nome** (primeiro nome +
  (sem query nem corpo cru, que podem carregar PII do contato).
- `--dry-run` nao grava nada; mostra exatamente o que faria (contato, id, campos).
- Escreve so custom field + tag em contato EXISTENTE. Nao deleta, nao dispara
  mensagem, nao mexe em deal — **salvo `--criar`/`--origin`** (modo arquivo),
  caminho conservador e NAO validado que cria contato/deal FORA da lista alvo e
  imprime um AVISO alto ao ser usado. Na duvida, nao use essas flags.

## Dependencias

- stdlib + `pandas` + `openpyxl`.
- `ClintClient` da skill `clint-api`
  (`~/.Codex/skills/clint-api/scripts/clint_client.py`), carregado por caminho
  absoluto. Nao duplica auth/paginacao.
- `normaliza_fone` / `chave_canonica` da skill `limpar-lista-contatos`
  (`~/.Codex/skills/limpar-lista-contatos/scripts/limpar_lista.py`).

## Fluxo recomendado (disparo real)

1. Rodar com `--dry-run` primeiro e conferir: achou todos? campos certos?
2. Rodar de verdade com a `--tag` do disparo (criar a tag antes no painel, ou
   usar `--criar-tag` de forma intencional).
3. Conferir alguns contatos no painel (ou via `get_contact`) antes de disparar.
4. Disparar pelo Clint mirando a tag.

Pra SEPARAR uma tag em lotes de N (ex: 5000) com uma tag por lote, use a skill
`clint-split-lotes` (complementar; roda ANTES do disparo/injecao). Ela usa a
mesma coleta robusta e aplica uma tag `..._Lote1..N` por fatia; depois voce roda
esta skill (ou o `/disparo-clint`) por lote.

## Validacao

${USER_BRAND}, Layra): dry-run localizou os 3 por ID; gravacao real gravou
`v1..v4` com acento e o emoji `👉`; leitura de volta provou persistencia exata
dos 4 campos nos 3 contatos e a tag `HAOS_teste_disparo` aplicada. Nenhum
contato fora dos 3 foi tocado.

**11/07/2026 (1o disparo real, modo TAG-ORIGEM):** disparo de 498 leads de uma
tag; o modo sequencial 1-a-1 travava em ~90/498; a virada pra sincrono +
`ThreadPoolExecutor` (8 workers) fechou os 498 em ~40s.

**11/07/2026 (teste do modo TAG-ORIGEM na tag `Teste_Disparo`, 3 contatos):**
`--tag-origem Teste_Disparo --v1 "TESTE tag-mode ok" --v2 "linha 2" --v3
"linha 3" --workers 4`: allowlist manteve os 3, gravou e verificou 3/3 (leitura
de volta por `get_contact` e por listagem de tag bateram identico). A verificacao
convergente absorveu o read-after-write lag da listagem sem disparar rodada extra
inutil.

**11/07/2026 (coleta robusta em escala + overwrite):** com o `list_contacts_by_tag`
corrigido pra retentar paginas vazias:
- Overwrite de `v1/v2/v3` em 498 leads da tag `${RESOURCE_ID}`: 498/498
  gravados e verificados.
- Injecao em 4 lotes da `${RESOURCE_ID}` (base ~17.688 fatiada em lotes
  de 5000 pela `clint-split-lotes`): Lote1 4999/5000 (1 registro corrompido no
  lado do Clint, nao no coletor), Lote2/3/4 100 por cento. Prova de que a coleta
  por tag deixou de truncar em ~1500 e passou a pegar a tag inteira.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
