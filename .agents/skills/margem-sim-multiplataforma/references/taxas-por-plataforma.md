# Taxas, bases e pendências por plataforma

Referência detalhada para a skill `margem-sim-multiplataforma`. Carregar quando for calcular margem que dependa da taxa real de uma plataforma específica.

Credenciais sempre por nome de variável do ${USER_SECRET_FILE}. As taxas em produção vivem em SQL versionado no projeto do usuario (`dim_payment_rate`, `app.rate_config`), nunca hardcoded no código do app.

---

## Tabela mestra

| Plataforma | Base reportada | Taxa de plataforma | Taxa de gateway | Status |
|---|---|---|---|---|
| Assiny | Líquido do produtor | já embutida na origem | PagSeguro / PagBank, percentual a confirmar | Pendente: % do gateway. Não redescontar a taxa de plataforma (já veio líquido) |
| Yampi + Bling | Bruto | n/a (loja própria) | gateway da Yampi, a medir | Descontar gateway + imposto + CMV + frete |
| Eduzz | Conforme retorno | comissão Eduzz | embutida | Confirmar split por produto |
| Hotmart | Conforme retorno | comissão Hotmart | embutida | Confirmar split por produto |
| Lia EdTech | Caixa ou competência | cláusula <USER_RATE_PERCENT> na recorrência | gateway de financiamento | Pendente: aplicar <USER_RATE_PERCENT>; resolver regime (ver `receita-sim-reconhecimento`) |
| Asaas | Líquido recebido | n/a | já líquido | Não redescontar |
| TikTok Shop | Bruto + comissão real | comissão TikTok medida | embutida | Única com taxa real extraída (raw.tiktok_settlements) |

---

## Pendências do usuario (lacunas que travam a margem real)

1. **Percentual do gateway Assiny (PagSeguro/PagBank):** não confirmado. Como Assiny é cerca de <USER_RATE_PERCENT> da receita, essa lacuna domina o erro da margem do grupo. Prioridade alta.
2. **Imposto de <USER_RATE_PERCENT>:** ainda não aplicado nos KPIs da dash. Enquanto não entrar, a receita líquida exibida está superestimada nesse ponto.
3. **Cláusula Lia <USER_RATE_PERCENT> na recorrência:** a confirmar e aplicar.
4. **CMV dos produtos físicos:** zero produtos com preço de custo no Bling. O valor de estoque usa preço de venda. Sem isso, não há margem real por SKU físico. Ação: cadastrar `preço_custo` por produto e por componente do BOM.
5. **Frete real por pedido:** Correios faixa manual ou fulfillment via CD. Custo por pedido a consolidar.

---

## Imposto por NCM (produto físico)

A carga tributária muda conforme o NCM do item. Em discussão (gate: parecer do contador):

| Item | NCM em estudo | Natureza |
|---|---|---|
| Livro | 4901.99.00 | Imunidade tributária do livro |
| Impresso / papelaria | 4817.30.00 | Tributado |
| Caneta (brinde) | 9608.10.00 | Tributado |

Quando a nota lista os componentes (ex: kit explode em livro + carta), o imposto é por componente, não pelo preço cheio do kit. Por isso a mudança de NCM altera o imposto de cada pedido. Ver skill `bling` para BOM e desmembramento na NF-e.

---

## Como calcular quando a taxa é desconhecida

Apresente a margem em faixa, não em ponto:
- **Margem teto:** sem o custo desconhecido (ex: sem o gateway Assiny).
- **Margem conservadora:** com uma estimativa do custo, rotulada explicitamente como estimativa, citando a premissa (ex: gateway estimado em X% por analogia com PagSeguro padrão).

Nunca apresentar a margem teto como se fosse a margem real. A diferença entre teto e conservadora é a medida do quanto a lacuna importa, e isso vira pendência acionável.

