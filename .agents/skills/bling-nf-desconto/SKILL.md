---
name: bling-nf-desconto
description: "Emissao de NF-e no Bling em pedido QUE TEM DESCONTO: como distinguir desconto NORMAL (com lastro de item, emite direto) de desconto ORFAO (sem lastro, a SEFAZ rejeita, precisa retrabalho), a regra B5 COMPLETA com as duas condicoes, e a receita de cada caso. Use SEMPRE que aparecer \"pedido com desconto nao emite\", \"desconto_nao_zero\", \"desconto orfao\", \"vDesc\", \"nota travada por desconto\", \"desconto por Pix da Yampi trava a NF\", \"pedido com item de R$ 0,00 e desconto\", \"o gate fiscal descartou N pedidos por desconto\", \"posso emitir com desconto?\", ou quando for MEXER em gate de emissao que envolva desconto (lote500_pipeline.py, reenvio_pedido.py, producao_diaria). Traz a prova historica (6 NF-e autorizadas nesta conta com vDesc > 0), a prova do rateio do Bling (por VALOR, nao por quantidade) e o script de diagnostico pedido a pedido. Nasceu do incidente de 22/07/2026: 599 pedidos pagos (R$ 37.572,63) parados 79-93 dias por meia regra implementada."
---

# NF-e com desconto no Bling (regra B5 completa)

Skill de dominio fiscal/operacional. Responde UMA pergunta que ja custou caro:
**este pedido tem desconto, eu emito ou nao emito?**

Nasceu do incidente de 22/07/2026 (Grabovoi/lote500): o gate implementado
bloqueava QUALQUER desconto porque copiou so metade da regra B5. Resultado:
**599 pedidos pagos, R$ 37.572,63, clientes esperando 79 a 93 dias**, todos
emitiveis. A ausencia desta skill foi o que deixou 8 casos virarem 599.

---

## 1. A regra B5, completa (as DUAS condicoes)

> **Bloquear a emissao quando: `desconto > 0` **E** nao existe item fisico que
> sustente esse desconto.**

As duas condicoes valem JUNTAS. Uma sozinha nao e a regra.

A traducao operacional exata (e o que deve estar em codigo):

```
BLOQUEIA se   desconto > soma(valor * quantidade dos itens fisicos)     -> ORFAO
EMITE   se    desconto <= soma(valor * quantidade dos itens fisicos)    -> NORMAL
```

O que a SEFAZ rejeita **nao e desconto**. E desconto **sem base de calculo**:
desconto lancado num pedido cujos itens somam menos que o proprio desconto (no
limite, itens somando R$ 0,00). Ai nao ha o que descontar e a nota nao fecha.

### Por que a metade errada e tao facil de escrever

O nome do defeito ("desconto orfao") faz o desconto parecer o vilao. Nao e. O
vilao e a **falta de lastro**. Quem le "problema de desconto orfao" e escreve
`if desconto != 0: descarta` acha que implementou a regra, os testes passam
(nenhuma nota errada sai), o alerta fica quieto, e o prejuizo aparece meses
depois em forma de fila parada. **Gate que so bloqueia nunca grita.**

---

## 2. Os dois casos, lado a lado

| | Desconto NORMAL | Desconto ORFAO |
|---|---|---|
| Definicao | `desconto <= soma dos itens fisicos` | `desconto > soma dos itens fisicos` |
| Exemplo tipico | Pix 12% da Yampi: itens 63,69 + frete 61,44 - desconto 7,64 = 117,49 | Pedido cujos itens somam 0,00 (so brinde/bonus) mas veio com desconto 5,00 |
| A nota fecha? | Sim: vProd + vFrete - vDesc = vNF = valor pago | Nao: nao ha base para o desconto |
| SEFAZ | Autoriza (cStat 100) | Rejeita |
| Receita | **Emitir direto.** Nada a corrigir. | **Retrabalho** (secao 5) antes de emitir |
| Frequencia real (lote Grabovoi, censo de 22/07) | 599 de 599 | 0 de 599 |

Detalhe que confunde e nao e o problema: **item de R$ 0,00 dentro do pedido**
(brinde, orderbump, miolo de kit). Ter item zerado NAO faz o desconto ser orfao.
O que conta e a SOMA dos itens. Em 545 dos 599 pedidos havia item de R$ 0,00 e
todos eram desconto normal.

---

## 3. Como diagnosticar (nunca no olho)

Use o script da skill (so leitura, nao muda nada):

```bash
export HAOS_MASTER_ENV=${HAOS_PRIVATE_ROOT}
python3 scripts/diagnosticar_desconto.py --pids ${RESOURCE_ID},${RESOURCE_ID}
python3 scripts/diagnosticar_desconto.py --arquivo /tmp/pids.txt --json /tmp/diag.json
```

Ele responde por pedido: `EMITIR_DIRETO`, `RETRABALHO_ORFAO` ou
`OUTRO_DEFEITO:<motivo>`, com os numeros que sustentam o veredito.

Os 6 sinais que ele confere (todos vem do GET `/pedidos/vendas/{id}`):

| Sinal | De onde vem | O que significa |
|---|---|---|
| `desconto.valor` / `desconto.unidade` | cabecalho | valor do desconto; unidade tem que ser `REAL` |
| `soma(item.valor * item.quantidade)` | itens | o lastro. Compare com o desconto |
| `totalProdutos` | cabecalho | tem que bater com a soma dos itens |
| `transporte.frete` + `outrasDespesas` | cabecalho | entram na aritmetica |
| `total` | cabecalho | `itens + frete + outras - desconto` tem que dar isso |
| `soma(parcelas.valor)` | parcelas | tem que ser igual ao total (o que o cliente pagou) |

**Sempre olhe o pedido AO VIVO** (GET), nunca so o pool/estado em disco: pool
velho ja mentiu antes (pedido que ja tinha nota, ja tinha mudado de situacao).

---

## 4. Receita do caso NORMAL: emitir direto

Nao ha correcao a fazer. O pedido esta certo, a Yampi/loja aplicou desconto
comercial legitimo, o cliente pagou o valor com desconto, e a nota tem que sair
com esse desconto.

O que conferir NA NOTA depois de emitir (nao antes, nao no lugar):

- `cStat 100` e `nProt` presente;
- `vDesc` (ICMSTot) **igual** ao desconto do pedido (tolerancia 1 centavo);
- `vNF` igual ao total do pedido **e** ao valor pago (parcelas);
- `vProd` (ICMSTot) igual a soma dos itens do pedido; `vFrete` igual ao frete;
- item a item: nenhum `vProd` negativo, nenhum `vDesc` de item maior que o
  proprio item, e a **soma dos `vDesc` dos itens igual ao `vDesc` do total**;
- transportadora correta (no fluxo Correios Log: `<transporta><CNPJ>${RESOURCE_ID}`).

### O rateio do Bling: por VALOR, nao por quantidade (PROVADO)

Essa era a unica duvida legitima: se o Bling rateasse o desconto de cabecalho
**por quantidade**, um item de R$ 0,00 receberia desconto sem base e sairia
**negativo** na nota. Testado em producao em 22/07/2026 no pior perfil possivel
(maior desconto do lote, R$ 21,97, pedido com item de R$ 0,00, 8 itens na nota):

```
NF 005402 - desconto 21,97 rateado PROPORCIONAL AO VALOR:
  item vProd 0,00   -> vDesc 0,00     (quatro itens assim)
  item vProd 9,36   -> vDesc 1,12     (~12%)
  item vProd 36,90  -> vDesc 4,43     (~12%)
  item vProd 99,90  -> vDesc 11,99    (~12%)
  soma dos vDesc = 21,97 = vDesc do total. Zero item negativo.
```

**Conclusao: item de R$ 0,00 + desconto de cabecalho e seguro.** Mesmo assim, o
gate item a item ficou no codigo, porque o custo de conferir e zero e a prova
vale para o comportamento observado, nao para sempre.

---

## 5. Receita do caso ORFAO: retrabalho antes de emitir

So quando `desconto > soma dos itens fisicos`. Nunca "por seguranca".

1. **Nao edite a NF** se ja existir alguma. Nota criada e snapshot congelado;
   corrigir cadastro nao retroalimenta nota. Ver regra da "3a geracao" no
   `GUIA_MESTRE_FULFILLMENT.md`.
2. **Crie um pedido NOVO** com o mesmo contato, itens, loja, `numeroLoja` e
   parcelas, mas **com desconto ZERO e o frete ajustado** de modo que
   `itens + frete = total pago`. O desconto some do campo de desconto e fica
   embutido no frete; o valor que o cliente pagou nao muda (e ele quem manda).
3. Emita a NF do pedido novo pelo caminho normal (transicao `gerarNfe`).
4. Valide o XML (secao 4). `vNF` tem que continuar sendo o valor pago.
5. Só entao cancele/encerre o pedido velho (situacao 12 ou Verificado 24,
   conforme o fluxo), deixando a nota velha, se houver, quarentenada e intocada.

Receita ja homologada em producao (${RESOURCE_ID}.py, 7 casos reais em
16/07/2026; caso NF 002572 em 16/07).

---

## 6. Gates que protegem de verdade vs zelo excessivo

Esta tabela e o coracao da skill. Vale para qualquer gate fiscal, nao so
desconto.

| Gate | Protege de verdade? | Por que |
|---|---|---|
| `vNF == total do pedido` | SIM | nota com valor diferente do pedido e erro fiscal e financeiro |
| `soma(parcelas) == total` | SIM | garante que a nota bate com o que o cliente pagou |
| `cStat 100` | SIM | sem autorizacao da SEFAZ nao existe nota |
| transportadora ECT matriz no XML | SIM | XML com transportadora errada e recusado no Correios Log |
| SKU/BOM cadastrado no CD | SIM | nota que o CD nao consegue separar vira pendencia fisica |
| pedido sem nota / situacao esperada | SIM | evita nota em dobro |
| CEP/municipio resolvidos | SIM | municipio fora da tabela IBGE derruba a nota (caso 002572) |
| `desconto > soma dos itens` (orfao) | SIM | e a rejeicao real da SEFAZ |
| aritmetica `itens + frete + outras - desconto == total` | SIM | payload incoerente = nota que nao fecha |
| **`desconto == 0`** | **NAO** | zelo excessivo: bloqueia venda legitima e nao previne nenhuma rejeicao |
| **`vDesc == 0` no XML** | **NAO** | espelho do erro acima. O certo e `vDesc == desconto do pedido` |

Como distinguir na hora de escrever um gate novo:

- Gate bom responde "**isto produziria uma nota errada?**".
- Gate de zelo responde "**isto e diferente do caso que eu ja vi passar?**".
- Todo gate que so bloqueia (nunca alerta, nunca enfileira para tratamento)
  precisa de um contador visivel. `descartes: {desconto_nao_zero: 599}` estava
  no placar desde 16/07 e ninguem leu porque descarte parecia normal.

---

## 7. Prova historica (a SEFAZ ja aceitou, nesta conta)

**nesta mesma conta/CNPJ**. Levantado em 22/07/2026 (`prova_xml_real.py`):

| NF | vProd | vDesc | vNF | cStat |
|---|---|---|---|---|
| 003287 | 139,00 | 120,10 | 18,90 | 100 |
| 003385 | 139,00 | 118,70 | 20,30 | 100 |
| 004291 | 99,90 | 79,60 | 20,30 | 100 |
| 003325 | 88,88 | 60,16 | 37,72 | 100 |
| 003358 | 63,69 | 43,79 | 19,90 | 100 |
| 004299 | 63,69 | 36,79 | 26,90 | 100 |

Em 6 de 6 o desconto aparece rateado item a item e a soma dos `vDesc` dos itens
bate exatamente com o `vDesc` do total. Nenhuma foi rejeitada.

E em 22/07/2026 entraram as 3 do piloto Grabovoi, mesma natureza
`${RESOURCE_ID}`, CFOP 5102/6102: **NF 005400 (vDesc 7,64), 005401 (17,30) e
005402 (21,97), todas cStat 100**, com transportadora ECT matriz.

---

## 8. Metodo: como provar isso em 40 minutos (reutilizavel)

O que funcionou em 22/07 e serve para qualquer "sera que pode?" fiscal:

1. **Censo ao vivo do universo inteiro**, item a item, so leitura. Nao amostra:
   599/599. Custo: 5 minutos a 2 req/s. Saida: quantos sao defeito de verdade
   (foram 0) e quais perfis existem (545 com item R$ 0,00, 54 sem).
2. **Procurar precedente na propria conta** antes de teorizar. Se a SEFAZ ja
   autorizou 6 notas iguais, a discussao acabou.
3. **Teste offline dos gates** com payload sintetico, incluindo os casos que
   DEVEM bloquear (28 testes em `test_gate_b5_2207.py`). Prova que voce nao
   afrouxou o que protege.
4. **Piloto de 3 com perfis diferentes**, escolhidos para estressar a duvida
   (um com item R$ 0,00, um sem, o de maior desconto), nao 3 quaisquer.
5. **Auditoria independente da nota**, com parser proprio, sem reusar a funcao
   que voce acabou de escrever. Se o gate tem furo, so isso pega.
6. **Grupo de controle quando o resultado for ambiguo.** No piloto, o
   "Enviar NFe" recusou as 3 notas. Mandar no MESMO lote 3 remessas antigas SEM
   desconto mostrou 6/6 recusadas igual: a recusa era da capacidade do CD, nao
   do desconto. Sem controle, isso teria virado "desconto quebra o envio".

---

## 9. NUNCA

- Nunca traduzir "problema de desconto orfao" para `if desconto != 0: bloqueia`.
- Nunca decidir por amostra quando o universo cabe num censo (599 pedidos custam
  5 minutos de leitura).
- Nunca editar NF ja criada para "consertar" desconto. Recria pedido.
- Nunca mexer nos gates da secao 6 marcados como "protege de verdade" para
  destravar fila.
- Nunca concluir "o desconto quebrou X" sem grupo de controle sem desconto.
- Nunca soltar lote inteiro direto: piloto de 3 com perfis escolhidos, conferido
  nota a nota, e so entao escala.

---

## 10. Onde estao as coisas

| O que | Onde |
|---|---|
| Pipeline com a B5 completa | Hetzner `${HAOS_PRIVATE_ROOT}` (espelho: `bling_fiscal/fulfillment/lote500/`) |
| Gate de selecao | funcao `validar_live` (motivos `desconto_orfao`, `aritmetica_nao_fecha`, `desconto_unidade_nao_real`, `desconto_dentro_do_item`) |
| Gate de XML | funcao `validar_xml` (`vDesc == desconto`, item a item via `RE_DET`) |
| Testes dos gates | `test_gate_b5_2207.py` (28 casos, roda offline, sem API) |
| Piloto dirigido | `python3 lote500_pipeline.py --pids <id1,id2,id3>` |
| Evidencias do piloto 22/07 | `bling_fiscal/fulfillment/lote500/out/evidencias_b5_2207/` |
| Journal | `bling_fiscal/fulfillment/lote500/out/pendencias_resolvidas_2207.jsonl` |
| Contexto do dominio | `bling_fiscal/GUIA_MESTRE_FULFILLMENT.md` (ler antes de agir) |
| API do Bling (client, OAuth, rate limit) | skill `bling` |



## Adaptacao Codex HAOS

- Carregar `${HAOS_PRIVATE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
