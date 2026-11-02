---
name: haos-design
description: Use quando criar, revisar ou implementar interfaces que precisem de hierarquia visual, fluxos claros, acessibilidade, responsividade e estados completos.
---

# Design orientado ao uso

Acione com `$haos-design`. Projete a partir da tarefa do publico e das restricoes
reais do produto. Esta skill nao depende de biblioteca visual, plugin ou acervo
externo; componentes e assets devem ter origem e direito de uso conhecidos.

## Entradas

Receba publico, tarefa principal, fluxo, conteudo, identidade autorizada, telas
ou componentes envolvidos, stack e dispositivos relevantes. Identifique objetivo
mensuravel de usabilidade e ownership de arquivos. Reutilize decisoes aprovadas;
pergunte somente o que alterar o resultado ou bloquear implementacao.

## Passos

1. Mapeie entrada, acao principal, decisao e retorno do usuario. Liste caminhos
   alternativos, recuperacao de erro e pontos que exigem explicacao.
2. Inventarie componentes e padroes existentes. Defina hierarquia de informacao,
   agrupamentos, rotulos, espacamento, tipografia e contraste com criterios
   legiveis. Use dados sinteticos representativos, sem expor dados reais.
3. Especifique estados inicial, carregando, vazio, sucesso, erro, indisponivel,
   foco e desabilitado quando aplicaveis. Diga como recuperar e o que preservar
   da entrada do usuario; nao dependa apenas de cor para comunicar estado.
4. Descreva comportamento responsivo pelo conteudo: reordenacao, quebra de texto,
   tabelas, menus e areas de toque. Inclua textos longos, zoom e telas estreitas;
   nao reduza a interface a uma imagem de largura fixa.
5. Defina semantica, ordem de foco, navegacao por teclado, rotulos acessiveis,
   mensagens de erro associadas e alternativas a movimento. Ao alegar aderencia
   normativa, consulte a norma atual pertinente e informe o escopo verificado.
6. Produza especificacao ou implemente somente no escopo solicitado. Confira
   versao e documentacao oficial da stack ao codificar. Preserve ownership e
   convencoes locais; assets sem licenca ficam pendentes ou sao substituidos
   por solucao original autorizada.
7. Realize QA visual e funcional nas larguras e estados definidos. Inspecione
   artefato renderizado quando houver ferramenta permitida; teste teclado e
   fluxos. Sem renderizacao, declare QA visual NAO EXECUTADO e entregue roteiro.

## Saida

Entregue mapa de fluxo, decisoes visuais justificadas, matriz de estados,
comportamento responsivo, requisitos de acessibilidade, arquivos alterados e
evidencias de QA. Use STATUS: CONCLUIDO, BLOQUEADO ou REVISAO NECESSARIA e
separe especificacao pronta de implementacao e verificacao visual realizadas.

## Criterios de aceite

O usuario identifica a acao principal, conclui o fluxo e recupera erros. Conteudo
permanece legivel e operavel nas condicoes testadas. Evidencia identifica tela,
estado e viewport sem dados privados. Ferramenta automatica de acessibilidade
complementa a inspecao, mas nao prova sozinha conformidade completa.

## Erros e recuperacao

Nao invente tela renderizada, screenshot ou teste de leitor de tela. Problema
visual pede reproducao e correcao localizada. Nao reestilize areas fora do pedido
nem esconda erro com texto generico. Publicacao e deploy exigem OK aplicavel.

## Cenarios de verificacao

- Titulo longo em tela estreita: verificar quebra, hierarquia e ausencia de corte.
- Erro no formulario: preservar entrada, associar mensagem e permitir recuperacao.
- Uso so por teclado: verificar foco visivel e ausencia de armadilhas.
- Navegador indisponivel: entregar especificacao com QA visual pendente, sem simular sucesso.
