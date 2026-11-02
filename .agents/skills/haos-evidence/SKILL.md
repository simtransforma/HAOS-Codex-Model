---
name: haos-evidence
description: Use quando uma entrega precisar de aceite, uma afirmacao depender de verificacao ou houver divergencia entre relato e estado observado.
---

# Evidencia proporcional a afirmacao

## Entradas

Afirmacoes pretendidas, criterios de aceite, baseline, artefatos alterados,
fontes disponiveis e limites de acesso. Identificar a revisao do artefato
testado; usar task_id/revision quando disponivel, sem criar infraestrutura.

## Passos

1. Converter cada afirmacao de conclusao em pergunta verificavel. Exemplo:
   "o arquivo tem formato valido" exige parsing; "o recurso esta carregado"
   exige observacao do runtime correspondente.
2. Escolher evidencia adequada: leitura exata, diff, teste reproduzivel,
   estado vivo ou readback. Memoria e documentacao podem orientar a busca,
   mas nao provam funcionamento atual.
3. Registrar por check: alvo, revisao ou hash quando disponivel, procedimento,
   resultado esperado, resultado observado, momento da observacao e limite.
   Remover segredos dos trechos apresentados.
4. Executar dentro da autorizacao e ler saida e codigo de retorno. Check
   iniciado, ferramenta saudavel e retorno de outro agente nao substituem
   verificacao do criterio. Consultar o artefato que sustenta o retorno.
5. Apos correcao, repetir verificacoes afetadas. Resultado anterior continua
   historico, nao prova da nova revisao. Usar `haos-quality-gates` para decidir
   cobertura e `haos-claim-verification` para afirmacoes externas.
6. Resolver divergencias pela fonte e pelo escopo observado. Se nao houver
   acesso suficiente, marcar NAO VERIFICADO e explicar qual conclusao depende
   disso. Usar `haos-source-quality-auditor` para fontes conflitantes.
7. Entregar ao main a matriz de evidencias e os limites de conclusao.

## Saida

Tabela: afirmacao | alvo/revisao | procedimento/fonte | observado | status |
limite. Status por check: PASS, FAIL, NAO EXECUTADO ou N/A com justificativa.
Acrescentar `STATUS: CONCLUIDO | BLOQUEADO | REVISAO NECESSARIA` para a entrega.

## Criterios de aceite

Cada afirmacao material tem evidencia pertinente e localizavel, com cobertura
explicita. Fato observado, inferencia e pendencia estao separados.
N/A indica irrelevancia demonstrada; nao representa teste aprovado.
Conclusao documental nao afirma comportamento de agentes ou hot reload.

## Erros comuns

- Arquivo presente como prova de uso: verificar consumo no runtime.
- Busca vazia como ausencia definitiva: declarar alcance e limites da consulta.
- Omitir arquivo novo do pacote: comparar tambem conteudo nao rastreado.
- Contar intencao ou checklist preenchido como execucao: exigir resultado lido.

## Cenarios de pressao

- Todos afirmam que a integracao funciona, mas so ha configuracao: registrar
  formato validado e operacao NAO VERIFICADA.
- Teste passou antes da ultima edicao e o prazo acabou: repetir o check afetado
  ou manter a conclusao pendente.
- Revisor pede PASS para ferramenta ausente: registrar NAO EXECUTADO; usar N/A
  apenas se o criterio realmente nao se aplicar.
