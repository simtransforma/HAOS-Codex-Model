---
name: haos-structural-refactor
description: Use quando avaliar responsabilidades misturadas, acoplamento, arquivos extensos ou uma refatoracao incremental que precise preservar contratos e comportamento.
---

# Refatoracao estrutural com contratos

Acione com `$haos-structural-refactor`. O modo padrao e AUDIT, estritamente
read-only: nenhuma escrita, geracao de indice ou comando que altere o workspace.
Tamanho e sinal de triagem, nao prova de divida tecnica.

## Entradas

Receba objetivo, escopo, modo solicitado, sintomas, contratos, versao da stack,
estado Git, ownership e checks existentes. Identifique comportamento que deve
permanecer igual, dependencias compartilhadas e mudancas preexistentes.

## Passos em AUDIT

1. Leia manifests, estrutura, arquivos candidatos e comandos de verificacao.
   Inspecione baseline e conteudo sem executar instalacao, build ou teste que
   possa escrever. Liste checks necessarios como planejados, quando for o caso.
2. Avalie coesao, responsabilidades, dependencias, estado compartilhado, efeitos
   colaterais, pontos de mudanca e contratos publicos. Confirme cada risco no
   codigo; arquivos gerados ou tabelas extensas podem ser coesos.
3. Use mapa arquitetural somente se ja disponivel e pertinente. Ferramentas de
   mapa sao opcionais; confira versao, escopo e relacoes no codigo. Criar indice
   exige outra etapa autorizada, fora de AUDIT. Nao instale ferramentas por padrao.
4. Identifique fronteiras naturais de dominio, entrada/saida, validacao e
   apresentacao. Compare beneficio observavel, risco, custo e opcao de nao mudar.
5. Entregue candidatos priorizados e plano incremental com owners, dependencias,
   contratos preservados, checks, condicoes de parada e estrategia de reversao
   restrita a mudancas da tarefa. Termine AUDIT sem editar arquivos.

## Passos em APPLY

1. Entre somente com pedido claro de implementacao. Em mudanca ampla ou
   transversal, apresente baseline e plano e passe pelo gate de aprovacao antes
   da escrita. Reutilize aprovacao atual comprovada para o mesmo escopo.
2. Revalide o estado. Capture resultados dos checks de baseline autorizados e
   diferencie falhas preexistentes. Falta de cobertura relevante pede teste de
   caracterizacao ou bloqueio explicito antes da extracao dependente.
3. Mude uma fronteira por vez, com ownership exclusivo. Preserve assinaturas,
   formatos, ordem de efeitos e comportamento observavel, salvo mudanca de
   contrato explicitamente aprovada. Nao reformate o projeto inteiro.
4. Verifique cada incremento e integracao. Se houver regressao, dependencia
   inesperada ou conflito de ownership, pare a unidade, investigue e corrija.
   Nao descarte trabalho alheio para restaurar um teste.
5. Solicite revisao independente com `$haos-multi-agent-review`. Limite a tres
   ciclos de correcao; falha restante exige REVISAO NECESSARIA ou BLOQUEADO.

## Saida

Informe modo, STATUS, baseline, candidatos e provas, fronteiras propostas,
plano/arquivos alterados, contratos, checks executados e nao executados,
regressoes e riscos residuais. AUDIT concluido significa analise concluida,
nao refatoracao implementada. APPLY concluido exige evidencia fresca do aceite.

## Criterios de aceite

A mudanca reduz um problema demonstrado e preserva contratos verificados. O diff
fica restrito ao plano. Testes novos verificam comportamento relevante, sem
espelhar mecanicamente a nova estrutura. Commit, push, merge e deploy nao sao
consequencias automaticas desta skill.

## Erros e recuperacao

Nao divida arquivo apenas para reduzir linhas. Se a fronteira aumentar acoplamento,
reavalie o plano. Se faltar ferramenta de mapa, use leitura dirigida e declare
cobertura. Nao chame check estatico de teste comportamental.

## Cenarios de verificacao

- Arquivo longo e coeso: registrar ausencia de prova de divida, sem extracao automatica.
- Pedido apenas de auditoria: produzir parecer na resposta, sem criar indice ou arquivo.
- APPLY amplo sem gate: preparar plano e baseline; aguardar aprovacao dependente.
- Teste de contrato regride: interromper incremento e corrigir com evidencia.
## Material portavel da origem (lote A)

Consultar [procedimento de origem](references/source-procedure.md), adaptado sem dados privados.
O nucleo publico acima prevalece em gates, opt-outs, fechamento e ferramentas.
Consultar [contrato de dependencias](EXPORT_DEPENDENCIES.md) antes de comandos dependentes.
