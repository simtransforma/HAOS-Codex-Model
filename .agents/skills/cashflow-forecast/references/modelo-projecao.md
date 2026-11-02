# Modelo de projecao de caixa (com exemplo numerico)

Use este modelo para montar a projecao da skill `cashflow-forecast`. Primeiro o modelo de tabela em branco, depois um exemplo numerico completo de ponta a ponta. Numeros sao ilustrativos e neutros (negocio generico), so para demonstrar o metodo.

---

## 1. Modelo de tabela (projecao mensal, horizonte 90 dias)

| Linha | Mes 1 | Mes 2 | Mes 3 |
|---|---:|---:|---:|
| **(A) Saldo inicial** | saldo de hoje | = (E) do Mes 1 | = (E) do Mes 2 |
| Entradas: recebiveis ja vendidos (forward book) | | | |
| Entradas: vendas novas (deslocadas pelo lag) | | | |
| Entradas: nao operacionais (aporte, emprestimo) | | | |
| **(B) Total de entradas** | soma | soma | soma |
| Saidas fixas (folha, aluguel, SaaS, infra) | | | |
| Saidas variaveis (midia, gateway, CMV, frete) | | | |
| Saidas: impostos | | | |
| **(C) Total de saidas** | soma | soma | soma |
| **(D) Burn liquido do mes = C - B** | | | |
| **(E) Saldo projetado = A + B - C** | | | |

Apos a tabela:
- **Burn liquido mensal medio** = media de (D) nos meses em que ha queima.
- **Runway** = saldo de hoje / burn medio (em meses).
- **Vale do caixa** = menor valor da linha (E) no horizonte, e em que mes ocorre. Se (E) ficar negativo, esse e o mes do estouro.

Para caixa apertado, troque os 3 meses por 8 a 12 semanas com a mesma estrutura.

---

## 2. Exemplo numerico completo

### Premissas (cenario base)

- Saldo de caixa hoje: R$ 120.000.
- Recebiveis ja vendidos (forward book): vendas dos ultimos meses, parte em cartao parcelado e parte em gateway D+30, que vao liquidar assim: R$ 60.000 no Mes 1, R$ 45.000 no Mes 2, R$ 30.000 no Mes 3.
- Vendas novas reconhecidas: R$ 80.000/mes. Metade liquida em D+30 (entra no mes seguinte) e metade e parcelada em 3x (entra 1/3 por mes a partir do mes seguinte). Resultado ja deslocado pelo lag: entrada de caixa de vendas novas estimada em R$ 25.000 no Mes 1, R$ 52.000 no Mes 2 e R$ 66.000 no Mes 3 (a esteira vai enchendo conforme as vendas antigas comecam a liquidar).
- Saidas fixas: R$ 70.000/mes (folha, encargos, aluguel, SaaS, infra).
- Saidas variaveis: R$ 35.000/mes (midia R$ 20.000 + taxa de gateway, CMV, frete R$ 15.000).
- Impostos: R$ 12.000/mes, vencendo no mes seguinte ao faturamento.

### Tabela base

| Linha | Mes 1 | Mes 2 | Mes 3 |
|---|---:|---:|---:|
| **(A) Saldo inicial** | 120.000 | 88.000 | 76.000 |
| Recebiveis ja vendidos (forward book) | 60.000 | 45.000 | 30.000 |
| Vendas novas (deslocadas pelo lag) | 25.000 | 52.000 | 66.000 |
| **(B) Total de entradas** | 85.000 | 97.000 | 96.000 |
| Saidas fixas | 70.000 | 70.000 | 70.000 |
| Saidas variaveis | 35.000 | 35.000 | 35.000 |
| Impostos | 12.000 | 12.000 | 12.000 |
| **(C) Total de saidas** | 117.000 | 117.000 | 117.000 |
| **(D) Burn liquido do mes (C - B)** | 32.000 | 20.000 | 21.000 |
| **(E) Saldo projetado (A + B - C)** | 88.000 | 76.000 | 55.000 |

### Leitura do cenario base

- O caixa cai de R$ 120.000 para R$ 55.000 em 90 dias: queima mesmo com o forward book entrando, porque as saidas (R$ 117k) ainda superam as entradas (R$ 85k a 97k).
- **Burn liquido mensal medio** = (32.000 + 20.000 + 21.000) / 3 = R$ 24.300.
- **Runway** = 120.000 / 24.300 = **cerca de 4,9 meses**. Faixa de **alerta** (3 a 6 meses): pede plano de correcao, ainda nao e critico.
- **Vale do caixa:** menor saldo no horizonte e R$ 55.000 no fim do Mes 3, e a curva segue descendo. Nao cruza zero nos 90 dias, mas cruzaria por volta do quinto mes mantido o ritmo.
- Observacao do metodo: o burn diminui de R$ 32k para ~R$ 20k porque a esteira de recebiveis enche conforme as vendas novas comecam a liquidar. E o efeito do lag, e exatamente o que a projecao por data de liquidacao captura.

---

## 3. Os tres cenarios (mesmas premissas, viradas)

Mudancas aplicadas em relacao ao base:

| Premissa | Pessimista | Base | Otimista |
|---|---|---|---|
| Vendas novas / volume | -25% | esperado | +20% |
| Prazo de recebimento | mais lento (parte escorrega 1 mes) | contratual | mais rapido (antecipa recebivel) |
| Inadimplencia / churn | +5 p.p. | historico | estavel |
| Custo variavel (midia) | mantem | mantem | corta R$ 10.000/mes |

Resultado em saldo final (Mes 3) e runway:

| Cenario | Saldo final Mes 3 | Burn medio mensal | Runway | Vale do caixa |
|---|---:|---:|---:|---|
| **Pessimista** | ~18.000 | ~34.000 | **~3,5 meses** | cruza zero por volta do Mes 4 |
| **Base** | 55.000 | 24.300 | ~4,9 meses | R$ 55.000 no Mes 3 |
| **Otimista** | ~98.000 | ~7.000 | **>12 meses** | nao queima, caixa estabiliza |

### Sensibilidade

A premissa que mais move o saldo final aqui e o **prazo de recebimento** combinado com **volume de vendas novas**: no pessimista, atrasar parte dos recebiveis em um mes e perder 25% de volume joga o caixa para o vermelho ja no Mes 4; no otimista, antecipar recebivel mais cortar R$ 10k de midia estabiliza o caixa. A faixa de runway (3,5 a >12 meses) mostra que a incerteza e grande e a decisao deve ser tomada olhando o **pessimista**.

---

## 4. Recomendacao derivada do exemplo

- **Postura:** defensiva-moderada. Runway base de ~4,9 meses esta na faixa de alerta, e o pessimista cruza zero no Mes 4. Nao e hora de aumentar verba sem retorno provado.
- **Acoes prioritarias (as 3 que mais movem o vale do caixa):**
  1. Antecipar parte do forward book (negociar antecipacao de recebivel) para elevar o vale do caixa nos meses 2 e 3.
  2. Cortar ou condicionar R$ 10.000/mes de midia ate o runway voltar para >6 meses, liberando so com ROI provado por dado.
  3. Acelerar a conversao de vendas que liquidam mais rapido (a vista / D+menor) para encurtar o lag medio.
- **Risco em dinheiro:** no pessimista, o caixa fica negativo em ~R$ 15.000 no Mes 4 se nada for feito.
- **Nivel de confianca:** medio. Depende da confirmacao do forward book e da taxa real de conversao do pipeline. Premissas de volume e prazo sao as fontes de erro.
- **Lacunas:** confirmar a data exata de liquidacao de cada lote do forward book e a taxa de gateway efetiva por meio de pagamento. Enquanto nao confirmado, tratar como premissa, nao como caixa garantido.

---

## 5. Checklist do modelo

- [ ] Toda entrada datada pela liquidacao, nao pela venda.
- [ ] Parcelas e D+X abertos mes a mes (nada de venda parcelada lancada inteira na origem).
- [ ] Saidas fixas, variaveis e impostos separados, imposto com vencimento defasado.
- [ ] Saldo encadeado: (E) de um mes = (A) do seguinte.
- [ ] Burn e runway calculados e classificados no semaforo.
- [ ] Tres cenarios com runway de cada e a premissa mais sensivel apontada.
- [ ] Premissas listadas e lacunas sinalizadas (nada fabricado).
- [ ] Texto sem travessao (em-dash); so virgula, ponto, dois-pontos, parenteses ou hifen normal.

