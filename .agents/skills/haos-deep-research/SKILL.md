---
name: haos-deep-research
description: Use quando uma decisao exigir pesquisa aprofundada, fontes atuais, comparacao de alternativas ou investigacao de evidencias contraditorias.
---

# Pesquisa com rastreabilidade

Acione com `$haos-deep-research`. A entrega e uma resposta delimitada por
evidencias, com incertezas explicitas. Uma lista de links nao encerra a pesquisa.

## Entradas

- Pergunta e decisao que a resposta deve apoiar.
- Escopo tematico, geografico e temporal; publico e formato da entrega.
- Fontes autorizadas, restricoes de acesso, prazo e limite de rodadas de busca.
- Hipoteses iniciais e criterios que poderiam refuta-las.

Se uma lacuna mudar a decisao, esclareca-a antes da coleta dependente. Reutilize
o briefing valido. Nunca amplie silenciosamente territorio, periodo ou finalidade.

## Passos

1. Divida a pergunta em subperguntas verificaveis. Defina o que constitui uma
   resposta suficiente e um limite finito de tempo ou rodadas antes de buscar.
2. Descubra as ferramentas realmente disponiveis. Se a informacao puder ter
   mudado, consulte fontes atuais; sem acesso, limite a conclusao ao material
   observado e registre a lacuna. Nao simule consultas.
3. Prepare buscas por entidade, periodo, sinonimos e contraevidencia. Priorize
   documentos primarios e metodologia acessivel. Em questoes tecnicas, confira
   documentacao oficial e versao aplicavel. Respeite acesso e licenca.
4. Mantenha um livro de fontes com identificador, localizador, autoria, data de
   publicacao, data de consulta, trecho ou secao pertinente e limite de uso.
   Registre indisponibilidade sem tratar pagina nao lida como evidencia.
5. Aplique `$haos-source-quality-auditor` aos fundamentos centrais. Identifique
   republicacoes para nao contar a mesma origem como confirmacao independente.
6. Relacione cada afirmacao central as fontes que a sustentam e as que a
   contradizem. Use `$haos-claim-verification` para decidir sua redacao final.
7. Encerre ao cumprir o aceite, atingir o limite ou encontrar bloqueio real.
   Uma nova rodada precisa de lacuna e hipotese novas; nao repita buscas sem
   ganho. Prazo esgotado produz entrega parcial identificada, nunca certeza.

## Saida

Entregue resposta a pergunta, escopo, metodo, livro de fontes, contradicoes,
limites e proxima verificacao util. Inclua esta matriz para claims decisivos:

| Claim | Tipo | Fontes e localizadores | Contraevidencia | Atualidade | Veredito |
| --- | --- | --- | --- | --- | --- |
| Afirmacao delimitada | Fato, inferencia ou hipotese | Referencias consultadas | Conflito ou nao encontrada | Periodo coberto | Sustentada, parcial ou inconclusiva |

## Criterios de aceite

O leitor consegue localizar a evidencia de cada conclusao relevante e distinguir
observacao de interpretacao. Conclusoes fortes exigem corroboracao independente
proporcional ao risco; quando uma fonte primaria unica for a autoridade pertinente,
explique essa limitacao. Sintetize em texto original e cite sem copiar extensamente.

## Erros e recuperacao

Trecho de busca nao substitui leitura da fonte. Quantidade de fontes nao compensa
baixa qualidade. Diante de conflito, compare definicoes, datas e amostras antes de
conciliar; mantenha divergencia nao resolvida. Nao pesquise dados privados fora do
escopo nem transforme pesquisa em operacao externa.

## Cenarios de verificacao

- Duas noticias repetem o mesmo estudo: registrar uma origem e buscar corroboracao.
- Fonte antiga contradiz revisao recente: comparar periodo e metodo, explicar a mudanca.
- Prazo termina com claim central sem fonte: entregar parcial, com claim inconclusivo.
- Rede indisponivel: identificar fontes locais lidas e nao alegar atualidade externa.
## Material portavel da origem (lote A)

Consultar [procedimento de origem](references/source-procedure.md), adaptado sem dados privados.
O nucleo publico acima prevalece em gates, opt-outs, fechamento e ferramentas.
Consultar [contrato de dependencias](EXPORT_DEPENDENCIES.md) antes de comandos dependentes.
