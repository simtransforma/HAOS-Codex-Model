---
name: cashflow-forecast
description: "Projeta o fluxo de caixa de um negocio (entradas, saidas, saldo, runway, burn) e roda cenarios base, otimista e pessimista. Use SEMPRE que o usuario pedir \"projecao de caixa\", \"forecast de caixa\", \"quanto caixa sobra\", \"qual o runway\", \"fluxo de caixa dos proximos 90 dias\", \"quanto tempo o dinheiro dura\", \"burn mensal\", \"vou ficar sem caixa?\", \"cenario otimista e pessimista de caixa\", ou qualquer variacao disso. Tambem aciona quando o usuario fala de saude financeira ao longo do tempo sem usar a palavra caixa: \"ate quando consigo pagar a folha\", \"posso aumentar o budget sem quebrar\", \"tenho dinheiro pra esse investimento\", \"as parcelas/recebiveis cobrem as contas\", ou quando confunde lucro com dinheiro disponivel. Use tambem antes de aprovar um gasto recorrente ou uma contratacao, porque a pergunta real e se o caixa aguenta. NAO pule esta skill quando a decisao depende de QUANDO o dinheiro entra ou sai, e nao apenas de quanto: forecast e sempre de caixa, nao de competencia.\n"
---

# Cashflow Forecast

Monta a projecao de caixa de um negocio (saldo inicial, entradas e saidas por prazo real de liquidacao, saldo projetado mes a mes), calcula runway e burn, e estressa o resultado em tres cenarios.

Leia `references/modelo-projecao.md` antes de montar a tabela: tem o modelo pronto e um exemplo numerico completo (saldo, entradas por D+X, parcelas, saidas, runway e os tres cenarios).

---

## Quando usar

Sempre que a decisao depender de QUANDO o dinheiro entra ou sai, nao so de quanto. Aprovar gasto recorrente, contratar, dimensionar verba de midia, responder "ate quando o caixa dura", checar se os recebiveis futuros cobrem as contas fixas: tudo isso e forecast de caixa. Lucro no papel nao paga salario, caixa paga.

---

## Principio que rege tudo: caixa, nao competencia

Antes de projetar qualquer numero, separe os dois regimes. Errar isso e o erro financeiro mais caro do forecast.

- **Competencia (regime de resultado):** a receita e reconhecida quando a venda acontece. Serve para medir lucro e margem. NAO diz quando o dinheiro chega.
- **Caixa (regime financeiro):** o dinheiro so existe quando entra na conta. Forecast de caixa trabalha SO com isso.

Converter receita reconhecida em entrada de caixa exige tratar dois atrasos:

1. **Lag de liquidacao (D+X).** O gateway/adquirente paga em D+X (ex.: cartao liquida em D+2, D+14 ou D+30 conforme o contrato; e-commerce que so libera apos a entrega confirmada empurra o caixa mais para frente). Uma venda de hoje vira caixa daqui a X dias. Na projecao, a entrada cai no periodo da LIQUIDACAO, nao no da venda.
2. **Receita parcelada / financiamento.** Venda parcelada (cartao em N vezes, carne, financiamento estudantil/consorcio) entra como caixa ao longo de varios meses, nao de uma vez na assinatura do contrato. Tratar parcela futura como caixa imediato e a forma classica de fabricar um saldo que nao existe. Cada parcela cai no mes em que efetivamente liquida.

Regra pratica: **toda entrada da projecao e datada pela liquidacao, nunca pela venda.**

---

## Anatomia da projecao

A identidade que se repete em cada periodo (mes a mes, ou semana a semana se o caixa for apertado):

```
saldo inicial do periodo
  + entradas previstas (ja liquidadas no periodo)
  - saidas previstas (que vencem no periodo)
  = saldo projetado (vira o saldo inicial do periodo seguinte)
```

Horizonte tipico: **90 dias** (3 meses). Caixa muito apertado ou runway curto pede granularidade semanal nas primeiras 4 a 8 semanas.

**Entradas a mapear (sempre pela data de liquidacao):**
- Vendas novas projetadas no horizonte, ja deslocadas pelo lag de liquidacao e por parcelamento.
- Entradas nao operacionais: aporte, emprestimo, devolucao de imposto.

**Saidas a mapear (pela data de vencimento):**
- Fixas: folha e encargos, assinaturas/SaaS, aluguel, infra, contratos recorrentes. Saem todo mes independentemente de venda.
- Variaveis: investimento em midia, taxa de gateway/adquirente, comissoes, custo de produto/CMV, frete, embalagem. Variam com o volume.
- Impostos: faturamento gera tributo com vencimento proprio (muitas vezes no mes seguinte). Esquecer imposto e otimismo embutido.

---

## Runway e burn

- **Burn liquido mensal = saidas do mes - entradas do mes.** Se positivo, o caixa esta encolhendo (queima); se negativo, o negocio gera caixa (nao ha runway a calcular, o caixa cresce).
- **Runway = caixa atual / burn liquido mensal medio.** E o numero de meses ate o caixa zerar mantido o ritmo atual.

Interpretacao (use como semaforo, ajuste ao risco do negocio):

| Runway | Leitura | Acao |
|---|---|---|
| < 3 meses | Critico | Caixa e a prioridade unica. Cortar saida e antecipar recebivel agora. |
| 3 a 6 meses | Alerta | Plano de correcao ja, antes que vire critico. |
| 6 a 12 meses | Saudavel | Espaco para operar e investir com disciplina. |
| > 12 meses | Confortavel | Da para ser agressivo onde o retorno justifica. |

Use o burn dos ultimos meses reais como base; se houver sazonalidade forte, use a media do ciclo, nao o melhor mes.

---

## Cenarios (base, otimista, pessimista)

Uma projecao de numero unico mente, porque o futuro tem faixa. Rode tres cenarios mexendo nas MESMAS premissas, em direcoes opostas:

| Premissa | Pessimista | Base | Otimista |
|---|---|---|---|
| Receita nova / volume de vendas | abaixo do realista | esperado realista | acima do realista |
| Conversao do pipeline em caixa | conservadora | historica | favoravel |
| Prazo de recebimento (lag) | mais lento (atrasa caixa) | contratual | mais rapido |
| Churn / cancelamento / inadimplencia | mais alto | historico | mais baixo |
| Custo (corte ou aumento) | sem corte / custo sobe | plano atual | corte ja contratado |

**Sensibilidade:** identifique a premissa que mais move o saldo final (geralmente receita nova ou prazo de recebimento). E nela que vale concentrar atencao e plano de contingencia. A diferenca de runway entre pessimista e otimista mostra o tamanho real da incerteza.

Regra de prudencia: **planeje o caixa pelo cenario pessimista, mire o base, comemore o otimista.** Pessimista nao e catastrofe, e o realista com as premissas viradas contra voce.

---

## Armadilhas (checar antes de entregar)

- **Confundir lucro com caixa.** DRE positiva com caixa negativo e comum (vendeu, ainda nao recebeu). Forecast e de caixa, ponto.
- **Tratar receita parcelada como caixa imediato.** A venda de hoje em 12x nao e caixa hoje, e 1/12 por mes (menos a taxa). Lancar tudo na venda infla o saldo.
- **Esquecer o lag de liquidacao.** Venda de hoje que so liquida em D+30 nao paga a conta de amanha.
- **Otimismo na conversao do pipeline.** Pipeline ponderado por probabilidade realista, nao pelo valor cheio nem pela melhor hipotese.
- **Ignorar sazonalidade.** Projetar dezembro com a media de um mes fraco (ou o contrario) quebra o forecast. Use o padrao do ciclo.
- **Esquecer impostos.** Tributo tem vencimento proprio, quase sempre defasado do faturamento. Sempre na linha de saida.
- **Custo fixo subestimado.** Folha, encargos, SaaS e infra saem chova ou faca sol. Levantar a base fixa real, nao a otimista.

---

## Processo

### 1. Levantar saldo e recebiveis
Saldo de caixa atual (todas as contas) e o forward book: parcelas e vendas em D+X ja contratadas que vao liquidar no horizonte. Esse e o caixa mais firme.

### 2. Mapear entradas pelo prazo real de liquidacao
Cada entrada cai no periodo em que o dinheiro chega, nao em que a venda ocorre. Aplicar lag (D+X) e abrir parcelamento mes a mes. Somar vendas novas projetadas, ja deslocadas.

### 3. Mapear saidas fixas e variaveis
Fixas (folha, aluguel, SaaS, infra), variaveis (midia, gateway, CMV, frete, comissao) e impostos, cada uma na data de vencimento.

### 4. Montar a projecao de 90 dias
Preencher a tabela de `references/modelo-projecao.md`: saldo inicial + entradas - saidas = saldo projetado, encadeando os periodos. Granularidade semanal se o caixa for apertado.

### 5. Calcular runway e burn
Burn liquido mensal medio e runway = caixa atual / burn. Classificar no semaforo. Apontar o periodo em que o saldo fica mais baixo (vale do caixa) e se ele cruza zero.

### 6. Rodar cenarios
Refazer a projecao em pessimista e otimista mexendo as premissas da tabela de cenarios. Reportar runway nos tres. Apontar a premissa mais sensivel.

### 7. Recomendar acao
- Caixa apertado (runway curto, pessimista cruza zero) -> postura **defensiva**: cortar/adiar saida, antecipar recebivel, segurar contratacao e verba.
- Caixa confortavel nos tres cenarios -> postura **agressiva**: ha folga para investir onde o retorno justifica.
Toda recomendacao com o risco em dinheiro e o nivel de confianca. Acao que gasta dinheiro: recomendar, nao executar sem OK.

---

## Saida esperada

Uma projecao de caixa cobrindo:

1. **Tabela de projecao de 90 dias** (mes a mes ou semana a semana): saldo inicial, entradas, saidas, saldo projetado por periodo, no cenario base.
2. **Runway e burn:** burn liquido mensal e runway em meses, com o semaforo, mais o vale do caixa (menor saldo e quando).
3. **Os tres cenarios** (base, otimista, pessimista) com o saldo final e o runway de cada, e a premissa mais sensivel.
4. **Recomendacao:** postura (defensiva ou agressiva), as 2 a 3 acoes prioritarias, o risco em dinheiro e o nivel de confianca.
5. **Premissas e lacunas explicitas:** que premissas foram usadas e que dado faltou (custo ou recebivel nao confirmado). Premissa nao some no texto, vai listada. Nunca fabricar numero ausente, sinalizar a lacuna.

Formato: `.md` estruturado, valores datados pela liquidacao, base de cada valor declarada (bruto, liquido ou caixa). Texto sem travessao (em-dash), use virgula, ponto, dois-pontos, parenteses ou hifen normal.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
