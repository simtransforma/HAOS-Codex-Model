---
name: haos-deep-research
description: "Research OS for HAOS researcher. Use for deep research, current web-backed investigation, market intelligence, academic/regulatory research, unfamiliar subjects, source-backed synthesis, claim verification, buying/recommendation research, or any task where evidence quality matters."
---

# HAOS Deep Research

Pesquisa profunda para qualquer assunto, sem transformar incerteza em certeza.

## Primeiro passo

Classificar o pedido:

- `FAST_SCAN`: resposta rapida, 3 a 5 fontes, lacunas claras.
- `STANDARD_RESEARCH`: 5 a 10 fontes, comparacao e sintese.
- `DEEP_RESEARCH`: 10+ fontes, queries iterativas, ledger de evidencias e verificacao de claims.
- `ACADEMIC`: papers, consensos, qualidade metodologica.
- `MARKET_INTEL`: concorrentes, ofertas, anuncios, canais, precos e posicionamento.
- `REGULATORY`: orgaos oficiais, leis, normas, vigencia e risco.
- `RED_TEAM`: contraevidencia, vieses, risco e falhas do argumento.
- `LOCAL_RESEARCH`: pesquisa orientada por cidade, bairro, raio, proximidade e fontes locais.

Se a pergunta estiver vaga, pedir apenas o minimo necessario: decisao a apoiar, escopo, prazo/profundidade e formato de entrega.

## Fluxo obrigatorio

1. Definir pergunta de pesquisa e criterio de aceite.
2. Verificar ferramentas com `${USER_PROJECT_ROOT}/scripts/research_tool_status.ps1` quando estiver no repo HAOS.
3. Usar `haos-query-expansion` para queries por sinonimos, idioma, fonte, entidade, periodo e contraevidencia.
4. Coletar fontes atuais quando o assunto puder ter mudado.
5. Usar `haos-source-quality-auditor` para classificar fontes.
6. Criar ledger de evidencias: claim, fonte, data, tipo, confianca.
7. Usar `haos-claim-verification` antes de conclusoes fortes.
8. Escrever com `haos-research-report-writer`.

Para `LOCAL_RESEARCH`, aplicar tambem `haos-local-research`: travar o escopo geografico,
perguntar antes de expandir, validar distancia e separar resultados locais de resultados
proximos ou fora do escopo.

## Regras de evidencia

- Toda afirmacao factual importante precisa de fonte e data de coleta.
- Conclusao forte exige pelo menos duas fontes independentes ou explicacao de incerteza.
- Separar `FATO`, `OBSERVACAO`, `ESTIMATIVA`, `INFERENCIA` e `HIPOTESE`.
- Para topicos atuais, legais, financeiros, medicos, politicos, tecnicos ou recomendacoes de compra, web/fontes atuais sao obrigatorias quando disponiveis.
- Se web/API nao estiver disponivel, declarar limite da pesquisa.
- Nao usar copy literal longa de fontes; sintetizar e citar.
- Nao coletar dado privado, acessar area fechada ou violar termos.

## Ferramentas

- `web.run` do Codex: busca e fontes atuais quando disponivel.
- Brave API: usar `${USER_PROJECT_ROOT}/scripts/brave-search.ps1` quando `.env.research.codex` estiver configurado.
- Tavily: usar se CLI/API estiver configurada.
- Firecrawl: usar para mapear/extrair sites quando CLI/API estiver configurada.
- Browser: usar para inspecao visual ou paginas que exigem navegacao.

Para verificar ferramentas, rode `${USER_PROJECT_ROOT}/scripts/research_tool_status.ps1`. O script nao imprime chaves.

## Referencias

- `references/source-types.md`: hierarquia de fontes.
- `references/research-modes.md`: criterios por modo.
- `references/report-template.md`: estrutura de entrega.
