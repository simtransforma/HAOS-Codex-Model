---
name: haos-multi-agent-review
description: Use quando uma mudanca relevante exigir revisao independente de varias especialidades ou quando achados divergentes precisarem de consolidacao verificavel.
---

# Revisao independente por evidencias

Acione com `$haos-multi-agent-review`. Revisores trabalham em modo somente leitura;
os donos da implementacao corrigem. Independencia e autoria distinta, nao apenas
uma segunda leitura do autor com outro titulo.

## Entradas

Receba objetivo, criterios de aceite, risco, baseline capturado, ownership, pacote
de mudanca e checks. O pacote inclui staged, unstaged e untracked pertinentes,
com conteudo de arquivos novos. Em baseline sujo, preserve snapshots ou outra
evidencia suficiente para separar alteracoes preexistentes das desta tarefa.

## Passos

1. Confira cobertura do pacote contra o estado atual. Comparacao entre commits
   isolada nao cobre trabalho sem commit. Se a origem de uma mudanca for incerta,
   registre cobertura incerta e nao atribua autoria por suposicao.
2. Escolha eixos distintos conforme risco: comportamento, contratos, dados,
   acessibilidade ou seguranca tecnica. Um revisor pode bastar para escopo curto.
   Conselho estrategico e parecer juridico nao substituem QA ou seguranca.
3. O coordenador aciona revisores por chamada real, em ondas de ate tres. Envie
   briefing com baseline, escopo, read_files, criterios e limite read-only.
   Sem ferramenta de agentes, declare falta de revisao independente; nao invente
   pareceres nem altere o nome do autor para simular revisor.
4. Cada revisor inspeciona diff e contexto real, incluindo novos arquivos. Checks
   somente quando nao alterarem estado; testes que escrevem artefatos devem ser
   executados pelo owner ou integrador em escopo autorizado.
5. Registre achados com severidade, path relativo e linha, causa, prova,
   impacto, reproducao e proposta. Diferencie defeito demonstrado de pergunta
   ou sugestao. Nao inclua segredos no trecho de evidencia.
6. Consolide por causa raiz, mantendo evidencias e divergencias. Resolva disputa
   por codigo, contrato e teste; contagem de votos nao determina correcao.
7. Encaminhe correcoes a owners disjuntos. Revisor distinto verifica novamente
   o pacote atualizado e os checks relevantes. Limite a tres ciclos; defeito
   de aceite remanescente resulta em REVISAO NECESSARIA, nunca aprovacao automatica.

## Saida

Use STATUS; escopo e baseline; cobertura staged/unstaged/untracked; revisores
efetivamente acionados; achados; correcoes pelo owner; verificacao fresca;
limites. Achado: ID, P0/P1/P2/P3, path:linha, causa, prova, impacto, acao e dono.
P0 indica impedimento critico imediato; P1 alto impacto; P2 impacto moderado;
P3 baixo impacto. Explique a severidade em funcao do contrato afetado.

## Criterios de aceite

Todos os criterios relevantes foram revisados no pacote real. Ausencia de
achados significa apenas ausencia no escopo inspecionado. Falha impeditiva
permanece aberta ate correcao comprovada ou demonstracao de falso positivo.
Nenhum revisor corrige o recurso que revisa nem realiza commit, push ou merge.

## Erros e recuperacao

Baseline ausente pede reconstrucao verificavel ou cobertura limitada explicita.
Mudanca concorrente pede atualizar o pacote antes do parecer. Achados duplicados
viram um item com varias evidencias, sem apagar manifestacoes distintas da causa.

## Cenarios de verificacao

- Arquivo novo untracked contem defeito: inclui-lo no pacote e no parecer.
- Repositorio ja estava sujo: separar baseline e preservar trabalho anterior.
- Dois revisores acham a mesma causa: consolidar e manter ambas as evidencias.
- Defeito persiste apos tres ciclos: REVISAO NECESSARIA com handoff objetivo.
## Material portavel da origem (lote A)

Consultar [procedimento de origem](references/source-procedure.md), adaptado sem dados privados.
O nucleo publico acima prevalece em gates, opt-outs, fechamento e ferramentas.
Consultar [contrato de dependencias](EXPORT_DEPENDENCIES.md) antes de comandos dependentes.
