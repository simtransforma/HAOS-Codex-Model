---
name: yampi
description: "Integracao com a API da Yampi (loja/checkout, plataforma Dooki). Use SEMPRE que a tarefa envolver a Yampi: listar/consultar catalogo de produtos e SKUs, ver o metodo de envio (shipment_service) de um pedido, ativar/desativar produto, mapear SKU de funil pro produto canonico, conferir se uma oferta esta viva, variacoes/ofertas, ou perguntas tipo \"qual o metodo de envio desse pedido na Yampi\", \"lista os produtos da Yampi\", \"desativa esse produto na loja\", \"esse SKU vende direto?\", \"puxa as ofertas\". Credenciais no ${USER_SECRET_FILE} (YAMPI_ALIAS / YAMPI_TOKEN / YAMPI_SECRET_KEY). Auth por headers User-Token + User-Secret-Key. Complementa a skill `bling` (Yampi = venda, Bling = ERP/estoque/nota)."
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

# Yampi (Dooki) API , Integracao HAOS

Loja/checkout das marcas (SIM / Editora Mindset / EdsonBurger). E a fonte da
**venda**; o **Bling** e o ERP (estoque + nota fiscal). A integracao Yampi->Bling
cria/mapeia 1 produto no Bling por SKU da Yampi (campo `erp_id`).

## Auth + base

- Base: `https://service.example.invalid`
- Headers: `User-Token`, `User-Secret-Key`, `Accept: application/json` (+ `Content-Type: application/json` em POST/PUT).
- Credenciais no `${USER_SECRET_FILE}`: **`YAMPI_ALIAS`**, **`YAMPI_TOKEN`**, **`YAMPI_SECRET_KEY`**.
- Resposta em `{ "data": ..., "meta": { "pagination": {...} } }`.

```python
import urllib.request, json
H={'User-Token':TOK,'User-Secret-Key':SEC,'Accept':'application/json','Content-Type':'application/json'}
def req(method, path, body=None):
    data=json.dumps(body).encode() if body is not None else None
    r=urllib.request.Request(f'https://service.example.invalid', data=data, method=method, headers=H)
    with urllib.request.urlopen(r,timeout=60) as resp: return json.loads(resp.read())
```

## Endpoints usados

| Metodo | Path | Para que |
|---|---|---|
| GET | `catalog/products?include=skus&limit=100&page=N` | Lista produtos + SKUs. Paginar via `meta.pagination.total_pages`. `limit` max 100 (default ~3/pagina). |
| GET | `catalog/products/{id}?include=skus` | Detalhe do produto. |
| PUT | `catalog/products/{id}` | Edita. **Desativar = `{ "active": false }`** (reversivel). |
| GET | `orders/{numeroLoja}` | Detalhe do pedido. Campo-chave: **`shipment_service`** (metodo de envio: Padrao / PAC / SEDEX) que o Bling NAO expoe. |

## Estrutura do produto / SKU

- Produto: `id, name, active, simple, has_variations, ncm, erp_id, sku, skus{data:[...]}`.
- SKU (em `skus.data[]`): `id, product_id, sku` (= o codigo, bate com o `codigo` do produto no Bling), `title, erp_id, blocked_sale, availability, barcode`.
- **`active`** = produto visivel/vendavel na loja. **`blocked_sale`** = venda bloqueada naquele SKU. (Um livro pode estar `active=true` + `blocked_sale=true` = no ar mas sem vender.)
- **`erp_id`** liga o SKU ao produto no Bling.

## Fatos importantes (descobertos em producao, jun/2026)

1. **TODOS os produtos sao `simple` (`has_variations=False`).** A Yampi **nao usa variacao** , cada cor / oferta / funil / orderbump / frete-gratis e um **SKU/produto proprio e separado**. Ex: kit+caneta = **2 SKUs** (um azul, um preto), NAO 1 com variacao de cor; "O Novo Codigo" = **7 SKUs** de funis diferentes.
2. **E a raiz da "salada de SKU"**: o mesmo item fisico vira N produtos no Bling (1 por SKU), com estoque fragmentado. Convencao pra arrumar: mesmo item fisico = mesmo SKU, muda so preco/link da campanha (nao criar produto novo por funil).
3. **Metodo de envio so existe aqui** (`orders/{numeroLoja}.shipment_service`), nunca no Bling , usado pra decidir logistica (ex: SEDEX vs PAC Correios Log por corredor).
4. **Frete-gratis / so-paga-frete**: a "gratuidade" esta na config da OFERTA (preco), NAO no nome (so 1 produto tinha "FRETE" no nome). Mesma BOM/componentes do pago; muda so o VALOR na nota (ponto do contador).
5. **Sync de estoque Yampi<->Bling esta OFF** (jun/2026) , mexer no estoque do Bling NAO afeta a venda na Yampi. Religar o sync = fase 2 (depois de arrumar o catalogo).
6. **Desativar produto morto**: `PUT catalog/products/{id} {"active": false}`. Usado p/ limpar SKUs antigos (ex: KNCM kit-com-livro, Kit da Riqueza).

## Pegadinhas

- `numeroLoja` do pedido Yampi e **curto**; origens tipo TikTok tem id longo (logistica propria, filtrar fora).
- Paginar sempre ate `meta.pagination.total_pages`.
- A integracao cria produto no Bling por SKU automaticamente. **SKU novo na Yampi vira produto no Bling SEM estrutura** (vende sem desmembrar a BOM na nota) -> por isso precisa do "guard" (n8n retem pedido com SKU sem estrutura) + governanca de SKU.
- O preco no Bling costuma vir `0` nos produtos sincronizados (quem manda no preco e a Yampi).

## Ver tambem

Skill **`bling`** , o outro lado (ERP): produto canonico, estrutura/composicao
(BOM), estoque, NF-e com desmembramento, modelo de catalogo de 2 niveis.

