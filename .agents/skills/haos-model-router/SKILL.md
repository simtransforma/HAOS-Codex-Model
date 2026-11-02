---
name: haos-model-router
description: Use quando o main precisar classificar complexidade ou recomendar capacidade e effort para uma delegacao autorizada.
---

# Recomendacao consultiva de capacidade

## Entradas

Pedido, classe de trabalho, risco, fase, preferencia explicita de capacidade,
effort herdado e schema real da ferramenta. Perfis locais descrevem intencao;
somente a sessao atual informa quais parametros sao aceitos.

## Passos

1. Classificar pelo trabalho real, usando a tabela. Quantidade de arquivos
   sozinha nao define complexidade; uma linha pode envolver risco alto.
2. Ler piso solicitado e herdado. Se high for pedido ou herdado como piso,
   preserva-lo; nunca reduzir por custo, rotina ou falta de opcao. Pedido de
   capacidade especifica permanece restricao, sem substituicao silenciosa.
3. Verificar capacidades expostas pela ferramenta e restricoes de cada papel.
   Escolher capacidade adequada ao risco sem fixar provedor ou ID de modelo.
   Diagnostico profundo, seguranca e julgamento exigem capacidade compativel;
   incerteza eleva cautela, nao autoriza troca automatica.
4. Recomendar classe, especialista, capacidade, effort e motivo. A recomendacao
   nao faz spawn nem altera o modelo da conversa. Nao enviar prompt ou dados
   a classificador externo nem instalar proxy, hook ou configuracao global.
5. Main confronta recomendacao com autorizacao e schema vivo. Se papel tem
   effort fixo insuficiente, declarar indisponibilidade; alternativa admitida
   exige preservar piso e instrucoes do especialista em briefing explicito.
   Se nenhuma opcao satisfizer o contrato, retornar UNAVAILABLE.
6. Na chamada feita pelo main, usar apenas campos suportados. Nao passar
   overrides que o papel proiba, nao deduzir carregamento pelo arquivo local
   e nao fazer chamadas pagas de teste para descobrir capacidade.
7. Registrar os quatro estados abaixo, sem confundir pedido aceito com
   execucao efetiva. Integrar evidencias via `haos-execution-waves`.

## Classes

| Classe | Criterio | Encaminhamento |
| --- | --- | --- |
| C0 | Pergunta autocontida e simples | Resposta direta, sem delegacao ritual |
| C1 | Leitura ou triagem delimitada | Verificacao direta proporcional |
| C2 | Execucao de uma especialidade | Plano curto, skill pertinente e owner |
| C3 | Multiplas frentes dependentes | Plano e ondas com ownership disjunto |

Classe nao reduz gate externo. C0/C1 nao podem disfarcar mutacao sensivel.

## Saida

- RECOMENDADO: classe, capacidade/effort, especialista e justificativa.
- SOLICITADO: parametros realmente enviados, ou NAO SOLICITADO.
- ACEITO: retorno real da ferramenta, rejeicao ou NAO EXECUTADO.
- EFETIVO: capacidade/effort confirmados pelo runtime, ou NAO INFORMADO.

Acrescentar READY, NO_DELEGATION ou UNAVAILABLE e motivo. Nao preencher
SOLICITADO/ACEITO/EFETIVO por previsao. Mesmo quando coincidem, manter a
distincao entre politica, solicitacao e observacao.

## Criterios de aceite

Piso high preservado quando aplicavel, preferencia explicita respeitada e
campos compativeis com o schema. Sem IDs fixos, troca de servico, instalacao
ou alegacao de hot reload. `haos-router` escolhe o fluxo; esta skill aconselha.

## Erros comuns

- ACEITO como prova do modelo efetivo: registrar NAO INFORMADO se ausente.
- Papel fixo inferior receber override inventado: retornar UNAVAILABLE.
- Reduzir effort para encaixar numa opcao: manter o piso e declarar limitacao.

## Cenarios de pressao

- Pedido high, apenas papel com effort inferior disponivel: UNAVAILABLE,
  sem degradar nem trocar silenciosamente.
- Spawn aceita chamada mas nao informa capacidade real: ACEITO confirmado
  e EFETIVO NAO INFORMADO.
- Tarefa C0 e matriz recomenda squad: responder diretamente; recomendacao
  declarativa nao cria necessidade de agentes.
