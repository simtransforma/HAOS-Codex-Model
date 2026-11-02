---
name: haos-execution-waves
description: Use quando um plano tiver subtarefas especializadas, dependencias ou trabalho paralelo que precise de ownership e integracao.
---

# Ondas com responsabilidade exclusiva

## Entradas

Objetivo, escopo e exclusoes, aceite, estado atual, especialistas realmente
disponiveis, arquivos/recursos permitidos e autorizacoes aplicaveis.
Em modo PLAN produzir plano; em EXECUTE usar plano valido e aceites existentes.

## Passos

1. Preparar itens com id, entrega, depende_de, owner, revisor, read_files,
   write_files, criterio de aceite, evidencias, risco e gate externo.
   Declarar limite de correcao: tres ciclos por item por padrao.
2. Verificar que dependencias existem e nao formam ciclos. Cada arquivo ou
   recurso tem um owner ativo; caminhos sobrepostos, inclusive pai/filho,
   exigem unificar ownership ou serializar. Limitar a onda a tres executores,
   respeitando tambem capacidade e restricoes da plataforma.
3. Capturar baseline dos arquivos de cada item, incluindo staged, unstaged
   e novos. Iniciar apenas itens com dependencias satisfeitas. Nenhuma onda
   pode sobrescrever mudancas preexistentes ou de outro owner.
4. Selecionar skills por metadados e ler as pertinentes. Briefing contem
   objetivo, contexto, fontes, arquivos, skills e motivos, limites,
   consentimento aplicavel, formato de retorno e aceite. Usar
   `haos-model-router` e parametros admitidos pela ferramenta real.
5. Delegar por chamada real quando autorizado e disponivel; preferir contexto
   minimo. Sem ferramenta, informar indisponibilidade e encaminhar ao main
   para ajuste do plano. Nao alegar delegacao por apenas citar um papel.
   Executores nao delegam recursivamente sem escopo explicito.
6. Receber arquivos e resultados; verificar o pacote contra o baseline.
   Revisor distinto do autor atua read-only, usando
   `haos-multi-agent-review` quando pertinente. O owner corrige e o revisor
   verifica novamente; aplicar `haos-task-loop` se houver falha.
7. Integrar somente itens aceitos. Bloquear o item com dependencia real e
   continuar os independentes. Main cuida do fechamento; executores nao
   fazem commits, push ou memoria independente por padrao.

## Saida

Plano por item e quadro: status, owner, arquivos alterados, checks executados,
resultado da revisao, bloqueios e proximo passo. Usar
`STATUS: CONCLUIDO | BLOQUEADO | REVISAO NECESSARIA`; declarar revisao
independente indisponivel quando for o caso.

## Criterios de aceite

Owners disjuntos, dependencias satisfeitas e evidencia lida para cada entrega.
Acao externa sensivel so avanca com OK explicito aplicavel; plano nao e OK.
Reutilizar consentimento valido sem exigir renovacao por mero decurso de tempo.

## Erros comuns

- Paralelizar edicoes do mesmo arquivo: serializar antes de qualquer escrita.
- Main absorver item sem declarar mudanca de papel: replanejar conforme regras.
- Limite esgotado virar aceite: manter falha e fazer handoff.

## Cenarios de pressao

- Dois agentes precisam editar o mesmo manifesto com urgencia: designar owner
  unico e serializar a dependencia antes de iniciar.
- Um item depende de publicacao sem OK: bloquear somente essa acao e seguir
  trabalho local independente.
- Terceira correcao falha: devolver REVISAO NECESSARIA com tentativas e defeito;
  nao abrir outra onda identica para reiniciar o contador.
## Material portavel da origem (lote A)

Consultar [procedimento de origem](references/source-procedure.md), adaptado sem dados privados.
O nucleo publico acima prevalece em gates, opt-outs, fechamento e ferramentas.
Consultar [contrato de dependencias](EXPORT_DEPENDENCIES.md) antes de comandos dependentes.
