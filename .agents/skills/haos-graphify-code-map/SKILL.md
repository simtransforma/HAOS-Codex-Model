---
name: haos-graphify-code-map
description: "Mapeia arquitetura, dependências e impacto em projetos complexos com Graphify local, filtrado e sem envio de código a LLM."
---

# HAOS Graphify Code Map

Use automaticamente antes de:

- refatoração transversal;
- alteração de contratos compartilhados;
- investigação de arquitetura desconhecida;
- análise de impacto e blast radius;
- delegação de trabalho entre vários módulos.

O MCP Graphify atualiza o índice no primeiro uso do projeto. A integração HAOS copia apenas arquivos de código permitidos para `${HAOS_PRIVATE_ROOT}`, exclui segredos, memória, runtime, logs, dependências e artefatos, e executa `--code-only --no-cluster` sem LLM.

Fluxo:

1. Consulte `status` ou inicie uma consulta; o refresh é idempotente.
2. Use `query` para arquitetura, `affected` para impacto e `god-nodes` para hubs.
3. Abra os arquivos reais citados pelo grafo.
4. Confirme cada relação relevante no código, tipos e testes.
5. Trate relações inferidas ou ambíguas como hipótese, nunca como fato.

O grafo acelera descoberta, mas não substitui busca textual, leitura do código, Git ou testes.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
