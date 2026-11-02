---
name: receita-sim-reconhecimento
description: "Politica contabil pratica do CFO sobre QUANDO uma venda do grupo SIM/usuario/HAU/Editora vira receita reconhecida e COMO evitar dupla contagem e inflacao de receita na fct_venda. Use SEMPRE que a tarefa envolver reconhecimento de receita, regime competencia vs caixa, ou consolidar/auditar faturamento em qualquer forma: \"qual a receita do periodo\", \"quanto faturamos de verdade\", \"reconhece essa venda\", \"a receita inflou\", \"tem venda contada duas vezes\", \"isso e competencia ou caixa\", \"como conta o financiamento da Lia\", \"quando o TikTok vira caixa\", \"expurga receita falsa\", \"Yampi e Bling batendo duas vezes\", \"Asaas duplicou a venda\", \"PIX gerado conta como venda?\", \"reembolso entra na receita?\". Tambem quando alguem for fechar faturamento, comparar receita reconhecida vs caixa, bater numero com o financeiro, ou questionar um total que parece alto demais. Esta skill da a regra firme (anti-erro), a tabela plataforma->evento->regime, as chaves de dedupe e o checklist anti-inflacao. NAO improvise reconhecimento de receita, NAO use a dash ad-hoc como fonte; siga a politica daqui."
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

# Reconhecimento de receita SIM (politica contabil do CFO)

Decide QUANDO uma venda vira receita reconhecida e impede dupla contagem e inflacao na `fct_venda`.

Grau de liberdade BAIXO. Reconhecimento de receita e regra firme, nao criatividade. Quando em duvida entre dois caminhos, escolha o MENOR (conservador) e declare a politica usada. Receita reconhecida nunca pode ser maior que a verdade.

## Guardrails (ler primeiro)

1. **Fonte da verdade UNICA: projeto do usuario** (Supabase, `fct_venda`, schemas `raw`/`stg`/`dwh`/`app`), a reconciliar com evidencia atual. NUNCA a dash ad-hoc `dados-view` (puxa API crua, sem dedupe, infla). Se o numero veio do `dados-view`, ele NAO e receita reconhecida; e estimativa bruta.
2. **Nunca fabricar:** se nao da pra confirmar que a venda esta paga e deduplicada, ela NAO entra. Sem chute.
3. **Competencia nao e caixa.** Receita reconhecida (competencia) e o direito sobre a venda; caixa e o dinheiro liquidado em conta. Sao numeros diferentes, declarar QUAL esta entregando.
4. **Conservadorismo:** na duvida, reconhece menos. Inflar receita e o erro caro (decisao errada de budget, imposto a maior, falso crescimento).
5. INTERNA. Credenciais so por NOME de variavel do ${USER_SECRET_FILE} (`SUPABASE_DATABASE_URL` etc). Nunca expor valor.

## Definicao: receita RECONHECIDA

Uma linha da `fct_venda` so conta como receita reconhecida quando, ao mesmo tempo:
- **Esta PAGA de verdade** (status de pago valido da plataforma; PIX/boleto so gerado NAO conta).
- **Nao e duplicata** de outra plataforma (passou pelo dedupe cross-plataforma).
- **Nao foi revertida** (sem reembolso/chargeback ativo).
- **E venda real**, nao parcela de financiamento ja reconhecida nem registro de teste/falso.

Valor reconhecido = valor LIQUIDO da venda (apos desconto), nunca o bruto inflado. Regra de DQ: liquido sempre menor ou igual ao bruto.

## Tabela: plataforma -> evento que reconhece -> regime -> quando vira caixa -> risco de dupla contagem

| Plataforma | Evento que reconhece receita | Regime | Quando vira CAIXA | Risco de dupla contagem |
|---|---|---|---|---|
| Yampi | pedido com status pago `[4, 6]` | competencia = caixa (aprovacao ja e liquidacao na pratica) | na aprovacao | Bling ESPELHA a Yampi: a venda crua Yampi e removida em favor do registro Bling. Sem isso, conta 2x. |
| Bling | pedido faturado/pago (canal indica origem) | competencia | conforme gateway por tras | E o registro VENCEDOR sobre o espelho Yampi. Nao somar Bling + Yampi do mesmo pedido. |
| Lia (curso) | order/billing/bill: ver POLITICA LIA abaixo | competencia no fechamento | parcela a parcela (bill) | Parcela de financiamento carrega produto GENERICO `${USER_RESOURCE_000024}`. Se contar a parcela como venda nova, infla. Filtrar. |
| TikTok Shop | pedido pago/entregue | competencia na venda | 1 a 2 semanas APOS entrega (`raw.tiktok_settlements`) | Confundir receita (na venda) com caixa (so na liquidacao). Venda recente sem settlement NAO e erro, e lag. |
| Asaas | cobranca paga (`PAYMENT_CONFIRMED/RECEIVED`) | competencia | na confirmacao | Asaas e GATEWAY TRANSVERSAL: pode ser o gateway por tras de OUTRA plataforma. Dedupe por `externalReference` pra nao somar a mesma venda 2x. |
| Assiny / Eduzz / Hotmart | venda aprovada/paga (status pago proprio da plataforma) | competencia | conforme repasse da plataforma | Receita FALSA ja injetada (caso Assiny). Auditar status e expurgar o que nao foi pago de verdade. |

Regra geral do "status de pago": **cada plataforma tem seu proprio conjunto de status que significa pago.** Yampi e `[4, 6]`. Nao assumir um status generico; usar o da plataforma. Status de "gerado/pendente/aguardando" NUNCA reconhece.

## Politica recomendada: financiamento Lia (curso parcelado)

Ambiguidade central: reconhecer pelo PRECO DA OFERTA (competencia, no fechamento) ou pelo VALOR PAGO NO DIA (caixa, parcela a parcela)?

**Politica padrao do grupo: COMPETENCIA.** Reconhecer a receita UMA VEZ, no fechamento do pedido (evento `order`), pelo preco da oferta. A venda do curso aconteceu ali; as parcelas sao so o fluxo de CAIXA daquele direito ja reconhecido.

Por que:
- Evita a inflacao classica de financiamento: somar oferta no fechamento + cada parcela depois = contar a mesma venda N+1 vezes.
- Mantem receita reconhecida estavel e comparavel mes a mes.

Regras operacionais (nao negociaveis):
1. **Reconhece no `order`** (fechamento), pelo preco da oferta. UMA vez por pedido.
2. **Parcela (`bill`) NAO reconhece receita nova.** A parcela e evento de CAIXA. Se a skill que precisa e caixa, somar parcelas; se e receita reconhecida, ignorar parcelas como receita.
3. **Filtro anti-parcela obrigatorio:** parcela de financiamento vem com produto GENERICO `${USER_RESOURCE_000024}`, nao o produto real. Descartar `product_id == '${USER_RESOURCE_000024}'` da contagem de VENDAS (senao cada parcela vira venda fantasma). O produto real so aparece no `order`.
4. Se o caso pedir explicitamente regime de CAIXA da Lia, declarar "regime caixa" e somar `bill` liquidado, nunca misturar com o reconhecimento por competencia no mesmo total.

Detalhe dos 3 dominios de evento da Lia: ver skill irma `lia-api`.

## Checklist anti-inflacao (rodar SEMPRE antes de entregar receita)

1. **PIX/boleto gerado contado como pago?** So conta pagamento confirmado. PIX/boleto apenas GERADO (Purchase disparado na geracao) infla e nao entrou dinheiro. Filtrar para status pago real.
2. **Receita FALSA?** Validar pagamento confirmado, status e proveniencia antes de reconhecer valores.
3. **Reembolso / chargeback** SUBTRAEM da receita reconhecida. Venda reembolsada ou estornada sai do total (idealmente como linha negativa ou exclusao), nunca fica.
4. **Dedupe cross-plataforma feito?**
   - Yampi crua REMOVIDA quando ha o espelho Bling do mesmo pedido.
   - Asaas deduplicado por `externalReference` contra a plataforma de origem.
   - Nenhum pedido somado em duas plataformas.
5. **Parcela de financiamento (Lia `e3f6cf36`) filtrada?** Conferir que parcelas nao viraram vendas novas.
6. **Competencia x caixa nao misturados?** TikTok: receita na venda, caixa so na liquidacao. Lia: receita no `order`, caixa nas parcelas. Nao somar os dois regimes no mesmo numero.

Detalhamento dos casos e das chaves de dedupe: `./references/dedupe-e-casos.md`.

## Data Quality (verificar antes de afirmar)

Nenhuma receita e declarada sem passar pelos checks. Rodar `dwh.fn_dq_checks()` e ler `dwh.dq_log`. Os checks cobrem: duplicidade, liquido menor ou igual ao bruto, e reconciliacao Yampi x gateway. Se algum check falhar, a receita NAO esta limpa; corrigir a causa antes de entregar o numero.

## Saida esperada

Entregar receita reconhecida LIMPA, com:
- O VALOR reconhecido (liquido, sem inflacao, sem dupla contagem).
- A POLITICA DE REGIME declarada explicitamente (competencia ou caixa) por plataforma quando relevante.
- O que foi EXPURGADO/DEDUPLICADO e por que (falsa, reembolso, espelho, parcela, PIX gerado), quando houver.
- Status dos DQ checks (passou / o que falhou).

Formato curto, direto, PT-BR, em tabela quando ajudar. Sem travessao.

