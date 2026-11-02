---
name: bling-nf-1026-1037-diagnostico
description: "Diagnostico e correcao de rejeicao da SEFAZ 1026 (\"Aliquota do IBS da UF invalida\") e 1037 (\"Aliquota da CBS invalida\") em NF-e emitida pelo Bling, tipicamente em natureza de amostra gratis, remessa, bonificacao ou outra operacao especial. Use SEMPRE que aparecer \"NF rejeitada 1026\", \"1037\", \"aliquota do IBS invalida\", \"aliquota da CBS invalida\", \"a nota de amostra nao autoriza\", \"a SEFAZ recusou a remessa\", \"rejeicao de IBS/CBS\", \"Reforma Tributaria travou a NF\", ou quando uma NF que sempre autorizou em VENDA passar a rejeitar em outra natureza com os mesmos itens. Traz a arvore de diagnostico em 5 passos, a pegadinha central (Situacao Tributaria \"000 - Tributacao Integral\" combinada com aliquota 0,0000% e INVALIDA; \"410 - Imunidade\" com 0,0000% e valida), a limitacao de que a config de IBS/CBS da Natureza de Operacao so e editavel e legivel pela UI do Bling (a API da 404 no detalhe) e o caso real resolvido em 24/07/2026. NAO use para desconto em NF (skill bling-nf-desconto) nem para operar a API do Bling em geral (skill bling).\n"
---

# Skill: Diagnóstico de Rejeição SEFAZ 1026/1037 em NF de Amostra — Bling

## Objetivo

Procedimento replicável para debugar e resolver erros 1026 (IBS inválida) e 1037 (CBS inválida) em rejeições de NF-e no Bling, especialmente em naturezas de amostra grátis ou operações especiais.

## Situação Típica

NF rejeitada 4x com erro tipo: **"1026 - Rejeição: Aliquota do IBS da UF invalida [nItem: 2]"** ou **"1037 - Rejeição: Aliquota da CBS invalida [nItem: 2]"**

## Árvore de Diagnóstico (Fluxo Sequencial)

### Passo 1: Confirmar o Item Rejeitado
- Erro cita `nItem: X` — identifique o item exato da NF
- Nota-se o NCM do item (ex: 4817.30.00 = carta)
- Verificar se o mesmo NCM autoriza em VENDA NORMAL (pedido com mesma origem/destino, natureza "Venda" padrão)
  - **Sim**: o problema é na NATUREZA atual, não no produto
  - **Não**: problema é no produto (NCM vazio, CST inválido, CFOP errado)

### Passo 2: Verificar a Natureza de Operação (UI, não API)
- Menu Cadastros > Naturezas de Operação > procure a natureza atual (ex: "Remessa de Amostra Gratis" id ${RESOURCE_ID})
- Abra a aba **IBS** (Imposto sobre Bens e Serviços)
- Procure a regra que se aplica ao item rejeitado:
  - Destino: "Qualquer" ou estado específico?
  - Produto: "Qualquer" NCM ou faixa específica?
  - A linha deve ter:
    - **Situação Tributária**: 000 (Tributação Integral), 410 (Imunidade), etc.
    - **Aliquota IBS**: valor % (ex: 0,1000%, 0,0000%)

### Passo 3: Validar a Combinação [Situação + Aliquota]
**A PEGADINHA CRÍTICA:**
- **Situação "000 - Tributação Integral" + Aliquota 0,0000%** = INVÁLIDO (SEFAZ recusa)
- **Situação "410 - Imunidade" + Aliquota 0,0000%** = VÁLIDO (combina corretamente)
- **Situação "000" + Aliquota > 0** = VÁLIDO (normal)

**Ação:** se a natureza tem "000 + 0%" em uma regra que pega seu item:
- Procure uma natureza de VENDA que funciona com o MESMO NCM
- Copie a aliquota dessa venda (ex: 0,1000% IBS)
- Volte na natureza de amostra, edite a regra, cole a aliquota copiada
- Repita na aba **CBS** (Contribuição Social sobre Bens e Serviços) com a aliquota de venda (ex: 0,9000%)
- Salve

### Passo 4: Validar a Regra 1 (Livro, se aplicável)
Se o pedido tem múltiplos itens (vendável em BOM: livro + carta + marcador):
- A regra linha 1 (NCM 4901.99.00 = livro, "Qualquer" destino)
- Deve ter Situação **410 - Imunidade** (livro é isento no Brasil)
- Aliquota **0,0000%** (combina com imunidade)
- ✅ Deixe assim — essa regra está correta

### Passo 5: Reemitir a NF
Após corrigir a config na UI:
1. No Bling, Vendas > Notas Fiscais
2. Procure a NF rejeitada (situação = 4 "Rejeitada")
3. **NÃO reutilize a mesma NF** — cancele ou abandone
4. Crie um pedido novo (ou clone) com os mesmos dados, timestamp HHMMSS novo
5. Emita a NF nova
6. Acompanhe o status (GET `/nfe`, campo situacao; ou UI Vendas > Notas)
   - Situação 5 = Autorizada ✅
   - Situação 4 = Rejeitada novamente → volte ao Passo 3 (pegadinha diferente)

## Referência Técnica

### Motivo Não Aparece na API
- `GET /nfe/{id}` (endpoint público do Bling) NÃO retorna o motivo exato (cStat/xMotivo) de rejeição
- O motivo **só aparece na UI**: Vendas > Notas Fiscais > a NF > caixa laranja "Erro no envio de NFe"
- **Solução:** screenshot da UI ou leia o XML de retorno da SEFAZ (harder)

### Config IBS/CBS Não é Verificável por API
- `GET /Api/v3/naturezaoperacao` (lista) funciona — retorna array
- `GET /Api/v3/naturezaoperacao/{id}` (detalhe) retorna 404
- POST/PUT de natureza = 404 em todos os endpoints testados
- **Solução:** edição é UI-only, sempre via Cadastros > Naturezas de Operação

## Pegadinhas Confirmadas

| Pegadinha | Sintoma | Solução |
|---|---|---|
| Payload duplicado | "Informações idênticas à última venda salva" | Adicione timestamp HHMMSS à observação do pedido novo |
| NF rejeitada orfã | Pedido fica parado, não reaproveita | Cancele a NF, crie pedido novo (nunca reutilize pedido com NF rejeitada) |
| Mesmo NCM autoriza em venda | Problema é na natureza, não no produto | Configure corretamente a natureza de operação |
| BOM explode em 3 itens | Transição 822234 desmembra vendável | Normal do Bling, não é o problema (a config IBS/CBS afeta cada item da BOM) |

## Escalação

Se após seguir os passos 1-5 a NF continuar rejeitando com 1026/1037:
1. Tire screenshot da UI (aba IBS/CBS da natureza, regras visíveis)
2. Acompanhe o XML de retorno da SEFAZ (motivo em xMotivo)

---

**Ligado a:** learning_ibs_cbs_aliquota_natureza_amostra_bling.md, rule_dry_run_shadow_nao_e_producao.md (design de automações com gates explícitos)


## Adaptacao Codex HAOS

- Carregar `${HAOS_PRIVATE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
