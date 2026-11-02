---
name: bling
description: "Integracao completa com a API do Bling V3 (ERP) — autenticacao OAuth 2.0 com auto-refresh, pedidos de venda, produtos, contatos, situacoes, logistica e objetos de postagem. Use SEMPRE que a tarefa envolver o Bling em qualquer forma: puxar/criar/alterar pedidos de venda, listar ou filtrar por situacao, mexer em produtos (NCM/origem/CEST/tributacao, estrutura/composicao de kit/BOM, saldo de estoque), montar produto que desmembra os componentes na NF-e, conciliar/lancar estoque, cadastrar/enriquecer contatos, gerar objeto de rastreio (Correios Log), trocar situacao de pedido, renovar token do Bling, ou perguntas tipo \"puxa os pedidos em aberto do Bling\", \"muda a situacao pra atendido\", \"cria objeto de postagem\", \"o token do Bling expirou\", \"lista os produtos sem NCM\". Tem cliente Python pronto (BlingClient) com refresh automatico, backoff em 429 e o mapa das duas APIs (publica OAuth + interna por cookie). NAO reinvente o fluxo OAuth nem o rate-limit do zero — siga os caminhos daqui."
---

# Bling API V3 — Integracao HAOS

Skill de referencia + cliente pronto pra operar o ERP Bling via API V3. Cobre o
fluxo OAuth 2.0 (com a pegadinha dos dois hosts), pedidos de venda, produtos,
contatos, situacoes e logistica, alem do conhecimento avancado descoberto em
producao (API interna `vendasinternal`, objeto de postagem nativo, whitelist de
edicao, truque do servidor local CORS).

## Quando usar

Ative esta skill quando a tarefa for:

- **Pedidos de venda**: listar (com filtro por situacao/periodo/contato), detalhar,
  criar, alterar, trocar situacao, lancar estoque/contas, excluir.
- **Produtos**: listar, detalhar, criar/editar, ajustar tributacao
  (NCM / origem / CEST / dados adicionais), saldos de estoque.
- **Contatos**: cadastrar ou enriquecer (CPF/CNPJ, endereco, telefone).
- **Situacoes**: descobrir os ids corretos por conta antes de filtrar ou patchear.
- **Logistica / postagem**: listar integracoes Correios Log, servicos PAC/SEDEX,
  gerar objeto de rastreio.
- **Token**: renovar `access_token`, refazer o fluxo `authorization_code`,
  diagnosticar `401`/`403`/`invalid_grant`.

Nao usar pra notas fiscais de servico de terceiros nem pra coisas que nao sao Bling.

## Autenticacao (OAuth 2.0)

### A pegadinha dos dois hosts (erro mais comum)

| Operacao | Host | Path |
|---|---|---|
| **OAuth** (authorize / token / revoke) | `www.bling.com.br` | `/Api/v3/oauth/...` |
| **Dados** (produtos, pedidos, contatos...) | `api.bling.com.br` | `/Api/v3/...` |

Misturar os hosts e o erro numero 1. O `bling_client.py` ja separa:
`BASE_URL = https://api.bling.com.br/Api/v3` e
`TOKEN_URL = https://www.bling.com.br/Api/v3/oauth/token`.

### Fluxo Authorization Code

1. **`GET www.bling.com.br/Api/v3/oauth/authorize`** — abre a tela de consentimento.
   Params: `response_type=code` (obrigatorio), `client_id` (obrigatorio),
   `state` (use sempre, anti-CSRF, o setup local usa `state=hau-fiscal-001`).
   `redirect_uri` e `scope` opcionais (herda os do cadastro do app). O usuario
   autoriza e o Bling redireciona pra `redirect_uri?code=...&state=...`.
2. **`POST www.bling.com.br/Api/v3/oauth/token`** — troca o `code` por tokens.
   - Header: `Authorization: Basic base64(client_id:client_secret)` +
     `Content-Type: application/x-www-form-urlencoded` + `Accept: 1.0`.
   - Body: `grant_type=authorization_code`, `code`, `redirect_uri`.
   - Retorna: `access_token`, `token_type=Bearer`, `expires_in=21600` (6h),
     `scope`, `refresh_token`.

### Refresh (renovacao)

Mesmo endpoint `/oauth/token`, Basic auth, body
`grant_type=refresh_token` + `refresh_token`. O `BlingClient._refresh()` ja faz
isso automaticamente em `401` (auto-retry 1x) e renova ao iniciar se nao tem
`access_token` em cache.

### Validades e rotacao

- `access_token`: **6h** (`expires_in=21600`).
- `refresh_token`: **~30 dias**. Se ninguem renovar por 30 dias, ele **morre** e e
  obrigatorio refazer o fluxo `authorization_code` no navegador (rodar
  `bling_oauth_setup.py`). Mantenha um job dentro da janela.
- **Rotacao**: a cada refresh o Bling **pode** devolver um `refresh_token` NOVO. E
  obrigatorio persistir o novo (o `bling_client.py` grava em `BLING_REFRESH_TOKEN`
  no `MASTER.env`). Continuar com o antigo faz o proximo refresh falhar com
  `invalid_grant`.

### Escopos

Definidos no app em **Central de Extensoes > Area do Integrador**. Informe so os
necessarios. Chamada sem escopo do recurso volta **`403 FORBIDDEN`** ("token nao
possui permissao para operar"), **nao** `401`. **Mudar escopo no cadastro do app
REVOGA todas as autorizacoes** — precisa reautorizar (novo `authorization_code`)
pro token carregar o escopo novo.

### Cloudflare no endpoint de token

`www.bling.com.br/Api/v3/oauth/token` fica atras do Cloudflare e **bloqueia o IP
por flood** (devolve uma **pagina HTML 429**, nao JSON). Contorno: trocar o `code`
a partir de outro IP (ex.: rodar no servidor Hetzner) ou esperar o cooldown. Os
scripts `hetzner_exchange.py` / `exchange_code.py` existem pra esse cenario.

## Endpoints por dominio

Base de dados: `https://api.bling.com.br/Api/v3`. Toda resposta vem em `{"data": ...}`.

### Pedidos de Venda (`/pedidos/vendas`)

| Metodo | Path | Para que |
|---|---|---|
| GET | `/pedidos/vendas` | Lista paginada (so cabecalho: id, numero, data, total, contato, situacao, loja). |
| GET | `/pedidos/vendas/{id}` | Detalhe completo: so aqui vem `itens[]`, `parcelas[]`, `transporte{}`, tributacao, desconto. |
| POST | `/pedidos/vendas` | Cria. Body minimo: `contato.id` + `itens[]`. |
| PUT | `/pedidos/vendas/{id}` | Altera (**substituicao TOTAL**, nao merge — reenvie tudo). |
| PATCH | `/pedidos/vendas/{id}/situacoes/{idSituacao}` | Muda a situacao (caminho correto, NAO via PUT). |
| PATCH | `/pedidos/vendas/{id}/lancar-estoque` | Baixa de estoque (body opcional com deposito). |
| PATCH | `/pedidos/vendas/{id}/lancar-contas` | Lanca contas a receber (parcelas) no financeiro. |
| DELETE | `/pedidos/vendas/{id}` | Exclui. |

Filtros do GET list: `pagina`, `limite` (max 100), `idContato`,
`idsSituacoes[]` (array, repetir a chave), `dataInicial`/`dataFinal`
(`YYYY-MM-DD`, intervalo <= 1 ano), `dataAlteracaoInicial`/`dataAlteracaoFinal`
(`YYYY-MM-DD HH:MM:SS`), `numerosLojas[]`, `idsVendedores[]`, `numero`.

### Produtos (`/produtos`)

| Metodo | Path | Para que |
|---|---|---|
| GET | `/produtos` | Lista (resumido). Filtros: `pagina`, `limite`, `criterio` (2=so ativos), `tipo` (P/S), `codigo`, `nome`, `idCategoria`. |
| GET | `/produtos/{id}` | Detalhe completo (tributacao, variacoes). |
| POST | `/produtos` | Cria. |
| PUT | `/produtos/{id}` | Edita. Aceita `tributacao{ncm, origem, cest, dadosAdicionais}`. |

Tambem cobre variacoes, saldos de estoque, categorias, depositos, estruturas,
fornecedores e lojas sob o mesmo prefixo.

### Situacoes (pre-requisito pratico)

| Metodo | Path | Para que |
|---|---|---|
| GET | `/situacoes/modulos` | Lista modulos (Vendas = id **98310**). |
| GET | `/situacoes/modulos/{id}` | Lista as situacoes do modulo (os ids reais). |

**Ids de Vendas confirmados nesta conta** (variam por conta, conferir antes):

| Id | Situacao |
|---|---|
| 6 | Em aberto |
| 9 | Atendido |
| 12 | Cancelado |
| 15 | Em andamento |
| 462581 | Entregue |
| 462583 | Em Transporte |
| 785500 | Aguardando Coleta |

### Logistica (`/logisticas`)

| Metodo | Path | Para que |
|---|---|---|
| GET | `/logisticas` | Lista integracoes (Correios Log = id **1002679**, tipo `CorreiosLog` nativa). |
| GET | `/logisticas/servicos/{id}` | Servicos de uma logistica. |
| GET | `/logisticas/objetos/{id}` | Objetos de postagem. |
| POST | `/logisticas/objetos` | **So funciona em logistica PERSONALIZADA** (nativa retorna erro, ver pegadinhas). |

Servicos Correios Log nesta conta: **PAC** id `${RESOURCE_ID}` (cod 39870),
**SEDEX** id `${RESOURCE_ID}` (cod 39888).

## Pegadinhas e Conhecimento Avancado

> Esta secao concentra o que **NAO esta na doc publica** — descoberto em producao.
> Leia antes de qualquer tarefa nao-trivial de pedido/postagem.

### 1. Existem DUAS APIs

- **Publica** — `api.bling.com.br/Api/v3`, auth OAuth Bearer. E a desta skill.
- **Interna** — `www.bling.com.br/Api/v3/vendasinternal/{id}`, autenticada por
  **cookie de sessao HttpOnly** (a que a propria tela do Bling usa). **NAO aceita
  o token OAuth.** Usada so quando a publica nao expoe o recurso (ex.: criar objeto
  de postagem em integracao nativa).

### 2. Objeto de postagem em integracao NATIVA (Correios Log)

`POST /logisticas/objetos` da publica **so funciona pra logistica
PERSONALIZADA** — em nativa (Correios Log) retorna *"O servico nao e de uma
logistica personalizada"*. E o `PUT /pedidos/vendas` publico **IGNORA**
`transporte.volumes` (nao cria objeto).

**Solucao**: criar o objeto via **PUT INTERNO** (`vendasinternal`) setando
`transporte.volumes = [{ id: 0, idServico: "<id servico>", tracking: "" }]`.

### 3. Whitelist do PUT vendasinternal + unidadeNegocio

O `PUT vendasinternal` exige o corpo do pedido, mas:

- Envie **so a whitelist de chaves da UI**: `numero, numeroLoja, tipoIntegracao,
  idCategoria, idListaPreco, contato, loja, cnpj, tipoPessoa, data, dataSaida,
  dataPrevista, outrasDespesas, desconto, numeroDaOrdemDeCompra, observacoes,
  observacaoInterna, idControleCaixa, transporte, itens, estruturas, parcelas,
  totalICMS, totalIPI, numeroManual, quoteByProduct, intermediador, idOrigem,
  primeiraCompra, taxas, troco, mesa, idMagento, vendedor, id`.
- **DELETE `loja.unidadeNegocio` quando o id dele = 0**, senao erro
  *"Ao informar unidade de negocio o id e obrigatorio"*.
- URL de edicao da SPA: `vendas.php#edit/{id}` (id = id da API V3).

### 4. Truque do servidor local CORS (rodar a API interna em lote)

O cookie HttpOnly **nao e legivel via JS** (`document.cookie`). Pra rodar a API
interna em lote, faca `fetch` **no contexto da pagina logada** (mesma origem).
Truque util: uma pagina HTTPS do Bling consegue fazer `fetch` de
`http://localhost` (loopback e **isento de mixed-content**) — da pra servir dados
de um servidor local CORS pro browser. O `cors_server.py` faz exatamente isso:
`HTTPServer(("example.invalid", 9999))` com `Access-Control-Allow-Origin: *`, expondo
`/batch` e `/plano` pro JS injetado na pagina do Bling consumir.

### 5. Tributacao do PRODUTO nao tem CST

`PUT /produtos/{id}` aceita `tributacao{ ncm, origem, cest, dadosAdicionais }`,
mas **NAO aceita CST**. CST e aliquotas ficam na **Natureza de Operacao**, fora da
API de produto.

### 6. `idsSituacoes` e param de ARRAY

Repetir a chave com colchetes: `idsSituacoes[]=6&idsSituacoes[]=9`. **NAO** mandar
CSV (a doc do conector Floui confunde, mas a V3 espera `[]`). No Python:
`params={"idsSituacoes[]": sid}` (chave literal com colchetes funciona no
`urlencode`).

### 7. Outras pegadinhas duras

- **`authorization_code` expira em 1 MINUTO e e de USO UNICO.** Reutilizar revoga o
  acesso do usuario (refazer todo o fluxo). Troque por token imediatamente.
- **PUT e substituicao TOTAL** (nao patch parcial). Reenviar sem `itens`/`parcelas`
  **zera** esses dados. Sempre reenvie o objeto completo.
- **Trocar situacao NAO e via PUT** com campo `situacao` (e ignorado/erro). Use o
  PATCH dedicado `/situacoes/{id}`.
- **`numero` != `id` interno.** O filtro `numero` e o numero visivel no ERP; todos
  os paths `/{id}` usam o id interno do list/POST.
- **Ids de situacao variam por conta/modulo** — nunca hardcodar sem checar
  `/situacoes/modulos`.
- **Periodo > 1 ano no filtro retorna 400.** Fatiar em janelas <= 12 meses.
- **List nao traz itens/parcelas/transporte** — exige um `GET /{id}` por pedido
  (multiplica requests, cuidado com rate limit).
- **`contato.id` deve ser contato JA cadastrado** no Bling (id interno). Item
  avulso (sem `produto.id`) exige `descricao` + `valor` + `quantidade`.
  `desconto.unidade` = `REAL` ou `PERCENTUAL`.
- **Empresa/conta inativa** (ou plano sem API) bloqueia gerar novo `access_token`
  mesmo com `refresh_token` valido.

### Rate limit

**Global da conta** (nao por endpoint nem por token): **~3 req/s e 120.000 req/dia**.
Estourou = **429**. O `BlingClient` faz backoff exponencial (`2^n` ate 5 retries).
Em varredura, throttle ~`0.35-0.4s` entre paginas e no maximo `max_workers=4` em
paralelo. Nao paralelizar agressivo.

### Formato de erro

Body JSON: `{ error: { type, message, description, fields[] } }`. `type` =
`VALIDATION_ERROR` / `MISSING_REQUIRED_FIELD_ERROR`, e `fields[]` aponta o campo.
**Sempre logar o body** — a mensagem diz o campo exato.

| Codigo | Significado | Fix |
|---|---|---|
| 400 `invalid_grant` | code/refresh invalido, expirado, ja usado, ou `redirect_uri` divergente | conferir code/refresh; `redirect_uri` identico byte a byte ao cadastrado e ao do `/authorize` |
| 400 `VALIDATION_ERROR` | campo invalido | ler `fields[]` |
| 401 `invalid_client` | Basic auth errado / client_id invalido | conferir `base64(client_id:client_secret)` no header (NAO no body) |
| 401 (access_token) | token expirado | renovar via refresh e repetir (o client faz auto-retry 1x) |
| 403 FORBIDDEN | escopo OAuth faltando | incluir o escopo no app + reautorizar |
| 404 | id inexistente | conferir id interno |
| 429 | rate limit | backoff exponencial |

## Produtos com estrutura / composicao (kit / BOM)

Produto tem `formato`: **`S`** (simples) ou **`E`** (estrutura/composicao = kit). O campo:

```
"estrutura": {
  "tipoEstoque": "V",       // V=Virtual (saldo vem dos componentes) | F=Fisico (saldo proprio). So aceita V ou F.
  "lancamentoEstoque": "",   // fica vazio p/ Virtual
  "componentes": [ { "produto": { "id": <id> }, "quantidade": 1 } ]
}
```

- **Converter simples -> estrutura**: `GET /produtos/{id}` -> setar `formato='E'` + `estrutura` -> `PUT` (substituicao TOTAL, sempre **read-modify-write**, senao zera a tributacao ja aplicada).
- **`tipoEstoque` so aceita `V` ou `F`** (descoberto por erro de validacao: *"Tipo de estoque invalido. Os valores aceitos sao V (Virtual) e F (Fisico)"*). Pra vendavel que baixa os componentes ao vender = **`V`**.
- **BOM plana** (componentes-folha direto no vendavel), NAO aninhada, pra desmembrar certo na nota.
- **Estrutura nao referencia a si mesma como componente.** Se o SKU vendavel for tambem a peca fisica (mesmo SKU), precisa de um SKU "peca fisica" separado (o vendavel = estrutura [peca + carta/outros]).
- **A lista (`GET /produtos` / `get_all_produtos`) NAO traz `estrutura.componentes`** (vem `[]` mesmo com `formato=E`), igual a lista de pedidos nao traz itens. Pra conferir a BOM, SEMPRE `GET /produtos/{id}` (detalhe). Nao concluir "perdeu os componentes" pela lista.

## Desmembramento de componentes na NF-e

Faz a nota sair com **cada componente em sua linha** (NCM/CST proprio) em vez do produto-pai , exigencia pra fulfillment (o CD usa a nota pra montar) e legal (revenda de kit discrimina cada item). Liga em **Config > Vendas > Vendas**, chave **"emissao da nota"**, **para o tipo de estoque VIRTUAL** (a chave e separada por tipo; ligar Fisico com kit Virtual NAO desmembra). Ha chave separada pra desmembrar no checkout do pedido. Na venda o produto permanece unico; so na nota ele explode.

## Estoque (/estoques, /depositos)

- **Depositos**: `GET /depositos`. Conta SIM tem **1 so**: "Geral" id **${RESOURCE_ID}** (padrao).
- **`saldoVirtualTotal`** (em `produto.estoque`) = saldo total. **`10000` = saldo fantasma** (controle real nao ligado) -> bomba de oversell, conferir/zerar.
- **Lancar saldo**: `POST /estoques` `{ produto:{id}, deposito:{id}, operacao, quantidade, observacoes }`.
  - `operacao`: **`B`** = Balanco (define valor **ABSOLUTO**), `E` = Entrada (soma), `S` = Saida (subtrai). Pra setar valor exato use `B`; pra zerar, `B` com `quantidade:0`.
- Estrutura Virtual: saldo do vendavel = computado dos componentes (o menor). **Conciliar os componentes ANTES de montar estruturas**, senao o vendavel mostra 0.

## Notas fiscais (/nfe)

- `GET /nfe` = lista (id, numero, serie, `tipo` [1=saida / 0=entrada], `naturezaOperacao{id}`, `situacao` [6=autorizada], `dataEmissao`).
- `GET /nfe/{id}` = detalhe com **`itens[]`** (codigo, descricao, quantidade, valor) , fonte do saldo real do que foi enviado.
- Nota de remessa fulfillment = **CFOP 5.949**. Pode sair **dividida em varias notas** (limite de itens) -> somar os itens pra ter o total por SKU.

## Modelo de catalogo de 2 niveis (fulfillment Correios)

- **NIVEL 0 , COMPONENTES** (`formato S`, estoque real): livros, cartas, cheque, selo, envelope, canetas, garrafas, canecas. E o que o **Correios rastreia** (SKU da remessa).
- **NIVEL 1 , VENDAVEIS** (`formato E`, `tipoEstoque V`): cada SKU de funil/oferta = estrutura que **explode a BOM na nota** pro Correios montar.
- **Regra de ouro**: 1 item fisico = 1 componente; N vendaveis apontam pra ele (acaba a salada de SKU).
- Ex: vendavel "O Novo Codigo" -> nota com **Livro (4901.99.00, imune) + Carta (4817.30.00)**, cada um sua linha.

## Tributacao por categoria (matriz do contador SIM)

| Categoria | NCM | CEST |
|---|---|---|
| Livro | 4901.99.00 (imune) | , |
| Carta / impressos / kit | 4817.30.00 | 19.019.00 (kit) |
| Caneta | 9608.10.00 | 19.001.00 |
| Caneca porcelana | 6911.10.90 | 14.008.00 |
| Garrafa | 9617.00.10 | , |

CST/CFOP ficam na **Natureza de Operacao**, nunca no produto (so NCM/origem/CEST). Remessa fulfillment: CFOP 5.949, CST ICMS 41, PIS/COFINS 08, IPI 53, aliquotas 0.

## Exemplos praticos

Pre-requisitos: `BLING_CLIENT_ID`, `BLING_CLIENT_SECRET`, `BLING_REFRESH_TOKEN` no
`MASTER.env`. O `bling_client.py` ja le tudo e auto-renova.

### Primeira autorizacao (gera o refresh_token)

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
