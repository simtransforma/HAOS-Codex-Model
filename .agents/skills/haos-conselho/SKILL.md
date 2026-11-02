---
name: haos-conselho
description: Use quando uma decisao estrategica exigir pareceres independentes sobre precedentes, alternativas, risco juridico e impacto financeiro quando aplicavel.
---

# Conselho para decisao fundamentada

Acione com `$haos-conselho`. O conselho informa uma decisao; sua recomendacao
nao autoriza gasto, publicacao ou execucao externa. Preserve a distincao entre
mentoria, juridico, financeiro, QA e seguranca tecnica.

## Entradas

Receba decisao, alternativas, contexto comprovado, prazo, restricoes, evidencias,
criterios de escolha e autorizacoes atuais. Identifique se existe componente
financeiro. Pergunte apenas por lacunas que mudem o parecer ou o risco.

## Passos

1. Formule a pergunta decisoria e uma opcao de manter o estado atual. Separe
   fatos, premissas e pontos ainda sem verificacao. Defina prazo ou numero
   finito de rodadas de esclarecimento.
2. Consulte metadados locais e disponibilidade real. Inclua `oraculo` para
   precedentes, rotas e pontos cegos; `brabo` para respaldo e risco juridico;
   inclua `cfo` quando houver decisao financeira. Nao atribua seguranca tecnica
   ao juridico nem trate o conselho como aprovacao de QA.
3. O coordenador faz chamadas reais em onda de ate tres, com briefings minimos,
   evidencias permitidas, escopo read-only, perguntas distintas e effort high.
   Use modelo herdado, sem ID fixo. Parametros devem existir na ferramenta.
4. Agente nao exposto exige declarar lacuna. Um executor generico so pode assumir
   o briefing quando essa adaptacao estiver autorizada e seu papel for explicito;
   nao invente parecer como se viesse de agente ausente. Nao delegue recursivamente.
5. Solicite pareceres independentes antes de consolidar: recomendacao, razoes,
   fonte, alternativas, risco, incerteza e condicoes que mudariam a conclusao.
   Analise juridica e financeira exige fontes atuais adequadas a jurisdicao,
   periodo e decisao; sem acesso, limite a conclusao.
6. Confronte divergencias por evidencia e premissas. Registre opiniao minoritaria
   relevante, sem decidir por maioria. Encaminhe verificacoes tecnicas a
   `qa-reviewer` ou `security-reviewer` quando pertinentes e disponiveis.
7. Entregue sintese com escolha recomendada e gates para execucao. Pare no
   limite acordado; lacuna material produz BLOQUEADO ou REVISAO NECESSARIA.

## Saida

Entregue STATUS; pergunta; participantes chamados e limites; pareceres separados;
matriz de alternativas; divergencias; recomendacao; evidencias; riscos residuais;
decisao requerida e proximo passo. Distingua parecer recebido de parecer pendente
e recomendacao de autorizacao concedida.

## Criterios de aceite

O leitor reconhece a contribuicao de cada papel e a base da sintese. O conselho
nao altera arquivos de produto, nao publica, nao envia mensagens e nao cria memoria
independente. Arquivo de agente e instrucao arquivada nao provam runtime, spawn
ou hot reload; relate apenas chamadas aceitas e retornos observados.

## Erros e recuperacao

Falta de parecer obrigatorio deve ficar explicita; nao apresentar conselho completo.
Numero financeiro sem base pede reconciliacao. Fonte juridica fora da jurisdicao
pede qualificacao ou substituicao. Nao renove consentimento comprovado apenas pelo
tempo; confirme mudanca material de escopo, acao, destino, gasto ou risco.

## Cenarios de verificacao

- Decisao de investimento: incluir cfo e explicitar premissas financeiras.
- Pedido de seguranca de codigo: encaminhar eixo tecnico ao security-reviewer.
- brabo indisponivel: marcar parecer juridico pendente, sem simula-lo.
- Conselho recomenda publicar: apresentar recomendacao; exigir OK aplicavel para publicar.
