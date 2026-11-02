---
name: margem-sim-multiplataforma
description: "Calcula a MARGEM DE CONTRIBUI\u00c7\u00c3O REAL por venda e por produto do grupo SIM, EdsonBurger e projeto do usuario, descontando da receita as taxas reais de plataforma e gateway, imposto, CMV (custo do produto) e frete, lidando com as bases de valor diferentes de cada plataforma. Use SEMPRE que a tarefa for \"qual a margem real\", \"quanto sobra dessa venda\", \"qual o lucro por produto\", \"desconta as taxas\", \"quanto a Assiny fica\", \"qual a margem do livro X\", ou comparar rentabilidade entre produtos ou plataformas. Tamb\u00e9m aciona quando algu\u00e9m mostra um faturamento bruto e quer saber o que sobra de verdade, ou quando se vai decidir pre\u00e7o, kit ou desconto sem saber a margem. N\u00c3O confunda receita com lucro: sem descontar custo n\u00e3o h\u00e1 margem.\n"
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

# margem-sim-multiplataforma

Leva uma venda do grupo da receita bruta até a margem de contribuição real, descontando taxa de plataforma, taxa de gateway, imposto, CMV e frete, e sinalizando todo custo que ainda não existe em vez de chutar.

Skills irmãs (o dado vem delas): `cfo-dash-sim` (onde o número vive), `receita-sim-reconhecimento` (qual venda contar), `bling` (BOM e estoque), `tiktok-shop-sim` (settlements). Tabela de taxas e pendências detalhadas em `./references/taxas-por-plataforma.md`.

---

## Conceito: a hierarquia do valor

Nunca pare na receita. Desça a escada toda:

```
Receita bruta (o que o cliente pagou)
  − taxa de plataforma        (comissão do infoprodutor / marketplace)
  − taxa de gateway           (PagSeguro, Pagar.me, etc.)
  − imposto sobre a venda     (alíquota por NCM / regime)
  = Receita líquida
  − CMV                       (custo do produto: impressão, componentes, brinde)
  − frete                     (Correios, quando bonificado é custo nosso)
  = Margem de contribuição    (o que sobra pra cobrir custo fixo e gerar lucro)
```

Regra dura: **nunca somar bases de valor diferentes sem normalizar.** Cada plataforma reporta em base diferente (bruto, líquido ou caixa). Saber a base é o passo 1, não o último.

---

## Fluxo

### 1. Identificar a plataforma e a base do valor
Antes de qualquer conta, descubra de qual plataforma veio a venda e em que base o valor está (bruto, líquido do produtor, ou caixa). Ver tabela abaixo. Se o número já vem líquido (Assiny, Asaas), não desconte taxa de novo: você contaria duas vezes.

### 2. Descontar taxa de plataforma e de gateway
Aplique a taxa real da plataforma e do gateway. Use a tabela de `./references/taxas-por-plataforma.md`. Onde a taxa é desconhecida (ex: percentual do gateway Assiny), **marque como lacuna** e mostre a margem com e sem ela (faixa), nunca um número falso de precisão.

### 3. Aplicar imposto
Desconte a alíquota de imposto sobre a venda. Para produto físico, a alíquota depende do NCM (livro imune, papelaria, caneta têm cargas diferentes). Atenção: a alíquota de <USER_RATE_PERCENT> ainda não está aplicada nos KPIs da dash (pendência), então ao ler a dash o imposto provavelmente ainda não foi descontado.

### 4. Descontar CMV (só produto físico)
Infoproduto não tem CMV. Produto físico tem: impressão do livro, componentes do kit (BOM no Bling), brinde (caneta). Problema central: hoje há cadastro de custos a verificar no catalogo do usuario, então o CMV em geral é uma lacuna. Quando faltar, calcule a margem pós-taxa e deixe o CMV explícito como "a obter", nunca zero implícito.

### 5. Descontar frete
Frete Correios. Frete grátis ao cliente é custo nosso (bonificação), não desconto zero. Se o custo real do frete por pedido não estiver disponível, sinalize a lacuna.

### 6. Consolidar margem e lacunas
Entregue a margem de contribuição por venda ou por produto, com a base declarada e a lista de cada custo que faltou. Onde houver lacuna, apresente uma faixa (margem otimista sem o custo faltante, margem conservadora com estimativa marcada como estimativa).

---

## Base do valor por plataforma (resumo)

| Plataforma | Base do valor reportado | Tem taxa real medida? | Tipo |
|---|---|---|---|
| Assiny (participacao a medir) | Líquido do produtor | Gateway PagSeguro a confirmar (lacuna) | Infoproduto |
| Yampi + Bling | Bruto (pago pelo cliente) | Não, descontar gateway | Físico |
| Eduzz | Conforme retorno do gateway | Parcial | Infoproduto |
| Hotmart | Conforme retorno do gateway | Parcial | Infoproduto |
| Lia EdTech | Caixa ou competência (ambíguo) | Cláusula <USER_RATE_PERCENT> recorrência a aplicar | Financiamento |
| Asaas | Líquido recebido | Sim (já líquido) | Gateway transversal |
| TikTok Shop | Bruto + comissão real | Sim, em raw.tiktok_settlements | E-commerce |

Detalhe completo (percentuais, pendências, NCM por produto) em `./references/taxas-por-plataforma.md`.

---

## Produto físico vs infoproduto

- **Infoproduto** (projeto do usuario, usuario, projeto do usuario, ofertas usuario): sem CMV. Margem = receita líquida (pós taxa e imposto). O grosso da margem some na taxa de plataforma e no imposto.
- **Produto físico** (livros, kits da projeto do usuario): tem CMV (impressão, componentes, brinde via BOM no Bling) e frete. A margem real depende de dados de custo que hoje faltam. Sem CMV, a margem de produto físico é uma estimativa de teto, e tem que ser rotulada como tal.

---

## Regra de lacuna (inegociável)

Quando um custo não existe no sistema (CMV sem cadastro, taxa de gateway não confirmada, frete real não medido), **sinalize a lacuna explicitamente**. Nunca preencha com zero implícito nem com chute apresentado como fato. Uma margem com lacuna honesta vale mais que uma margem precisa e falsa. Liste as lacunas como pendências acionáveis (ex: cadastrar preço de custo dos N produtos no Bling, confirmar percentual do gateway Assiny).

---

## Saída esperada

Uma leitura de margem de contribuição por venda ou por produto, contendo:
- valor bruto e base declarada
- cada desconto aplicado (taxa plataforma, gateway, imposto, CMV, frete) com a fonte
- margem de contribuição em reais e em percentual
- faixa otimista vs conservadora quando há lacuna
- lista de lacunas como pendências acionáveis

Refira credenciais de banco e API somente por nome de variável do ${USER_SECRET_FILE}. Zero em-dash no texto.

