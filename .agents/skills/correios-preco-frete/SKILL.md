---
name: correios-preco-frete
description: "Custear o frete REAL pago aos Correios via a API de PRECO de contrato (Correios Log+), autenticando pelo cartao de postagem. Use SEMPRE que a tarefa for descobrir \"quanto pagamos de frete aos Correios\", \"custo real de frete\", \"valida o frete na API dos Correios\", \"quanto sai o SEDEX/PAC de contrato pra esse CEP\", \"compara custo SEDEX x PAC no corredor\", \"o frete do relatorio esta certo?\", ou quando for calcular custo de envio de um lote a partir de peso + CEP destino. Traz o fluxo de token (cartao de postagem), o endpoint /preco, os coProduto exclusivos de contrato (39888 SEDEX Log+, 39870 PAC Log+), qual campo e o preco de contrato (pcFinal), o throttle seguro, a origem do CD e a PEGADINHA de que a /preco so cobre a perna de postagem (nao inclui o fee de fulfillment do CD). INTERNA, fica so em ${HAOS_PRIVATE_ROOT} - GPT-Codex/HAOS/your-private-project/.agents/skills (nao vai pro HAOS_CC)."
---

# Custo real de frete via API de preco dos Correios (contrato Log+)

Skill de dominio fiscal/operacional. Responde UMA pergunta que ja causou erro de
relatorio: **quanto a operacao REALMENTE paga de frete aos Correios por um
pedido** - o custo de contrato, nao a receita de frete que o cliente pagou no
checkout.

Nasceu de 23/07/2026: um relatorio de fulfillment estava tratando a RECEITA de
frete (o `vFrete` que o cliente pagou) como se fosse o CUSTO. Sao coisas
diferentes. O custo real so sai autenticado, na API de preco de contrato.

---

## 1. Quando usar (gatilhos)

- "quanto pagamos aos Correios por esse frete", "custo real de frete".
- "valida o frete na API dos Correios", "confere o preco de contrato".
- "quanto sai o SEDEX/PAC Log+ pra esse CEP com esse peso".
- "compara SEDEX x PAC dentro/fora do corredor" (leitura economica do corredor
  vive em [[project_automacao_fulfillment_v2]]; o NUMERO de cada rota sai daqui).
- fechar custo de frete de um lote a partir de (peso em gramas + CEP destino).

NAO use pra receita de frete (isso e o `transporte.frete`/`vFrete` do pedido no
Bling); pra receita nao se chama a API. Ver a distincao dura em
[[feedback_correcao_frete_api_correios]].

---

## 2. Pre-requisitos (credenciais, so por nome de variavel)

Todas no MASTER.env (nunca imprimir o valor):

| Variavel | O que e |
|---|---|
| `CORREIOS_CNPJ_SIM` | CNPJ da SIM, usuario da autenticacao Basic |
| `CORREIOS_CHAVE_API` | chave de acesso da API (o "password" do Basic) |
| `CORREIOS_CARTAO_POSTAGEM` | numero do cartao de postagem que resolve o contrato |

O cartao de postagem e a peca central: e ele que amarra o contrato. Com o cartao
certo no corpo da autenticacao, os campos `nuContrato`/`nuDR` ficam **redundantes**
nas chamadas seguintes (o cartao ja resolve o contrato).

---

## 3. Passo a passo

### 3.1 Autenticar (pega o bearer, dura ~24h)

`POST https://api.correios.com.br/token/v1/autentica/cartaopostagem`

- Header `Authorization: Basic base64(CORREIOS_CNPJ_SIM:CORREIOS_CHAVE_API)`
- Body JSON `{"numero": "<CORREIOS_CARTAO_POSTAGEM>"}`
- Resposta: `token` (bearer, validade ~24h) + dados do contrato.

Montar o Basic sem vazar o segredo (le do MASTER.env, nao ecoa):

```bash
set -a; . ${HAOS_PRIVATE_ROOT} 2>/dev/null || . "$HAOS_MASTER_ENV"; set +a
BASIC=$(printf '%s:%s' "$CORREIOS_CNPJ_SIM" "$CORREIOS_CHAVE_API" | base64 -w0)
TOKEN=$(curl -s -X POST 'https://api.correios.com.br/token/v1/autentica/cartaopostagem' \
  -H "Authorization: Basic $BASIC" -H 'Content-Type: application/json' \
  -d "{\"numero\":\"$CORREIOS_CARTAO_POSTAGEM\"}" | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')
```

Cacheie o token; nao reautentique a cada objeto (limite de conta compartilhada).

### 3.2 Precificar (o custo de contrato)

`GET https://api.correios.com.br/preco/v1/nacional/{coProduto}`

Query params:

| Param | Valor / significado |
|---|---|
| `cepOrigem` | `${RESOURCE_ID}` (CD Indaiatuba; qualquer CEP de Indaiatuba da a MESMA tarifa) |
| `cepDestino` | 8 digitos do destino |
| `psObjeto` | peso em GRAMAS |
| `tpObjeto` | `2` (pacote) |
| `comprimento` / `largura` / `altura` | dimensoes em cm (padrao usado: 23 / 16 / 4) |

Header `Authorization: Bearer <token>`.

```bash
curl -s "https://api.correios.com.br/preco/v1/nacional/39888?cepOrigem=${RESOURCE_ID}&cepDestino=${RESOURCE_ID}&psObjeto=545&tpObjeto=2&comprimento=23&largura=16&altura=4" \
  -H "Authorization: Bearer $TOKEN"
```

### 3.3 Ler o preco

O campo do custo de contrato e **`pcFinal`** (preco final ja com o desconto do
contrato). NAO usar `pcBase`/valores de tabela varejo. `pcFinal` vem como string
com virgula decimal (ex: `"8,45"`).

---

## 4. Os coProduto que importam (exclusivos de contrato)

| coProduto | Servico |
|---|---|
| `39888` | SEDEX CORREIOS LOG + |
| `39870` | PAC CORREIOS LOG + |

Sao **codigos proprios dos Correios** (o Bling so os espelha, nao os inventa) e
sao **exclusivos de contrato**: so retornam preco quando a chamada esta
autenticada com o cartao/contrato. E exatamente por isso que servem de prova de
contrato (secao 6).

---

## 5. Throttle e origem

- **Throttle: <= 2,5 req/s** (teto oficial 3 req/s; a conta e COMPARTILHADA, entao
  fica abaixo do teto; cota diaria ~120.000 chamadas). Para lote grande, serialize
  com pausa e cacheie por (coProduto, faixa de CEP, faixa de peso).
- **Origem = CD de Indaiatuba, `cepOrigem=${RESOURCE_ID}`.** Qualquer CEP de Indaiatuba
  devolve a mesma tarifa (a tarifa e por regiao de origem, nao por logradouro).

---

## 6. PEGADINHA OBRIGATORIA (nao pular)

**A `/preco` entrega SO a perna de POSTAGEM.** Ela NAO inclui o fee de
fulfillment / armazenagem / separacao do CD (a "montagem" que o Correios Log faz
antes de despachar). Esse fee e faturado a parte, FORA dessa API.

Consequencia direta: **`pcFinal` NAO e o "custo total pousado" do pedido.** E o
custo da postagem. Chamar `pcFinal` de "custo total" subestima o gasto real (falta
o fee do CD). Em relatorio, rotular sempre como "custo de postagem (contrato)",
nunca "custo total de frete".

---

## 7. Verificacao (como saber que o preco e mesmo de contrato)

Dois sinais, juntos:

1. **`pcFinal` bem abaixo do varejo** para o mesmo peso/rota (o desconto de
   contrato e grande). Se vier no valor de balcao, a autenticacao/cartao nao
   pegou o contrato.
2. **Sensivel a peso e a rota** - muda com `psObjeto` e com `cepDestino`. Preco
   chapado = resposta errada/cacheada.

Se os dois batem, e preco de contrato de verdade.

---

## 8. NUNCA

- Nunca confundir `pcFinal` (custo que PAGAMOS) com `vFrete`/`transporte.frete`
  do pedido (receita que o cliente PAGOU). Ver [[feedback_correcao_frete_api_correios]].
- Nunca chamar `pcFinal` de "custo total pousado": falta o fee de fulfillment do CD.
- Nunca imprimir/logar `CORREIOS_CHAVE_API` nem o `CORREIOS_CARTAO_POSTAGEM`.
- Nunca reautenticar por objeto num lote (estoura a cota da conta compartilhada);
  reusa o bearer de ~24h.
- Nunca usar coProduto de varejo esperando preco de contrato: os de contrato sao
  39888 (SEDEX Log+) e 39870 (PAC Log+); so precificam autenticado.

---

## 9. Onde se encaixa

- Leitura economica do corredor (SEDEX x PAC dentro/fora do corredor SP, media,
  paradoxo de mix, premio por honrar SEDEX): [[project_automacao_fulfillment_v2]].
- Distincao custo x receita como regra duravel: [[feedback_correcao_frete_api_correios]].
- Contexto do dominio de fulfillment: [[index_fulfillment]] e `bling_fiscal/GUIA_MESTRE_FULFILLMENT.md`.



## Adaptacao Codex HAOS

- Carregar `${HAOS_PRIVATE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
