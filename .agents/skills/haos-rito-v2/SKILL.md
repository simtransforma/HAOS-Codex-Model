---
name: haos-rito-v2
description: Use quando houver pedido explicito de Rito ou projeto amplo com varias disciplinas, fases dependentes e gates de aprovacao.
---

# Rito de treze fases

## Entradas

Objetivo, escopo, exclusoes, aceite, risco, autorizacoes e estado de fase com
evidencias. Consultar estado existente apenas se disponivel e pertinente.
Nao criar servico ou hook para conduzir o Rito.

## Passos

1. Sem estado valido, iniciar na fase 1. Para retomar, conferir entrega,
   evidencia e aceite registrados; preservar fase e aceites ainda validos.
   Mudanca material reabre somente gates afetados, com motivo.
2. Definir owner, skills, revisores, dependencias e verificacao por fase.
   Usar `haos-execution-waves` na execucao e `haos-task-loop` nas correcoes.
3. Aplicar a tabela abaixo. Gate pode ser criterio verificavel ou aprovacao
   humana quando exigida pelo pedido, risco ou acao externa. N/A exige motivo,
   impacto nas dependencias e validacao do main; nunca representa PASS.
4. Conselho mantem `estrategista-chefe`, `diretor-criativo` e `cmo` como
   nucleo decisor. Antes da sintese, obter insumos de `oraculo` para
   precedentes/alternativas e `brabo` para analise juridica; incluir `cfo`
   quando houver decisao financeira. Consultar assessores e depois nucleo em
   ondas de no maximo tres. Declarar indisponibilidade real.
   `security-reviewer` cuida de seguranca tecnica; nao substitui juridico.
5. Avancar somente com gate satisfeito ou N/A justificado. Preservar OK valido
   para o escopo; ampliar destino, risco ou acao exige nova autorizacao.
6. Main integra evidencias e conduz a fase 13. Em read-only ou dry-run,
   relatar estado na resposta sem persistir nem ativar recursos.

## Fases, entregas e gates

| Fase | Entrega | Gate para avancar | Evidencia minima |
| --- | --- | --- | --- |
| 1. Intake e validacao | Objetivo, escopo e aceite | Lacunas materiais resolvidas | Pedido e decisoes confirmados |
| 2. Pesquisa e diagnostico | Estado real e lacunas | Fontes suficientes para decidir | Fontes/localizadores e limites |
| 3. Estrategia | Alternativa escolhida e riscos | Decisao fundamentada; conselho quando aplicavel | Comparacao e pareceres distintos |
| 4. Plano tatico | Itens, owners, dependencias e reversao | Plano executavel dentro do escopo | Baseline, checks e gates externos |
| 5. Copy e mensagens | Texto adequado ao publico | Alegacoes sustentadas e aceite editorial | Revisao com haos-copy e fontes |
| 6. Design e criativos | Artefatos visuais/interface | Criterios de uso e acessibilidade | Revisao com haos-design |
| 7. Funil e automacao | Fluxos e contratos | Sucesso, erro e recuperacao verificados | Testes em ambiente autorizado |
| 8. Trafego e midia | Plano de distribuicao | Destino, verba e ativacao autorizados se executados | Plano e OK aplicavel |
| 9. Tracking e dados | Eventos e reconciliacao | Qualidade e coleta proporcional | Amostras sanitizadas e checks |
| 10. QA, seguranca e conformidade | Achados e aceite | Nenhum defeito bloqueante aberto | Checks frescos e pareceres pertinentes |
| 11. Deploy e ativacao | Pacote pronto e ativacao autorizada | OK explicito para acao/destino e reversao | Resultado observado; preparo nao e deploy |
| 12. Monitoramento | Resultado vivo e desvios | Janela e metricas de aceite observadas | Leituras atuais ou pendencia de acesso |
| 13. Debrief | Entrega consolidada e candidatos duraveis | Fechamento coerente com provas e opt-outs | Avaliacao do main via haos-evoluir |

## Saida

Por fase: estado, owner, entrega, evidencia, gate, N/A e motivo, bloqueios e
proxima fase. Usar CONCLUIDO, BLOQUEADO ou REVISAO NECESSARIA para o escopo
contratado; fases futuras fora do escopo nao impedem concluir uma etapa local.

## Criterios de aceite

Treze fases contabilizadas; dependencias respeitadas; aceites rastreaveis;
nenhuma ativacao inferida de planejamento. `haos-quality-gates` orienta QA e
`haos-evidence` limita afirmacoes. Nao exigir deploy para entrega somente local.

## Erros comuns

- Reiniciar intake em toda retomada: reutilizar estado comprovadamente valido.
- Encobrir check falho com N/A: manter bloqueio da fase dependente.
- Misturar parecer juridico, financeiro e tecnico: registrar responsabilidades.

## Cenarios de pressao

- Retomada na fase 7 com plano aceito: conferir evidencias e seguir dessa fase,
  sem cobrar novamente decisoes validas.
- Prazo curto, QA falhou e ativacao esta agendada: bloquear fase 11; agenda
  nao remove defeito nem fornece OK.
- Projeto interno sem midia ou deploy: justificar N/A nas fases pertinentes,
  preservar as dependencias e fechar apenas o escopo contratado.
