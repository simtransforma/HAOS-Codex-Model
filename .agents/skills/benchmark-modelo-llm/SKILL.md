---
name: benchmark-modelo-llm
description: "Compara modelos LLM para um consumidor Codex/HAOS com baseline, payload fiel, qualidade, perda de dados e custo; nao e roteador de subagentes nem autoriza troca automatica."
---

# Benchmark de Modelo LLM

Todos os caminhos relativos nesta skill partem do repo canonico `${HAOS_PRIVATE_ROOT}`, nao do cwd nem do cache do plugin.

Use para decidir sobre modelo de um servico. Para escolher tier de agente Codex, use `haos-model-router`; nao altere o runtime Claude ou seu claude-mem.

## Antes de chamar API

1. Identifique consumidor, objetivo, modelo/ID exato atual, baseline e decisao que o teste deve informar.
2. Consulte catalogo atual do provedor e contrato da API. Nome comercial nao basta: registre IDs exatos, disponibilidade, preco e limites no momento da consulta.
3. Confira experimentos anteriores pelo mesmo ID e causa de rejeicao. Falha estrutural do payload/codigo deve ser corrigida ou explicitada antes de retestar.
4. Estime amostra e custo maximo; sem autorizacao de gasto, prepare plano ou use dados locais existentes. Nao inicie chamadas pagas por conta propria.

## Desenho fiel

- Use prompt, estrutura, tamanho, parametros e limite de saida reais quando acessiveis. Se nao puder obter o prompt, marque a simulacao como proxy.
- Rode pares comparaveis no mesmo conjunto, com inputs rotulados e variacao suficiente para casos dificeis. Registre versao do consumidor e ambiente.
- Meça saida vazia/inutil, parseabilidade quando aplicavel, fidelidade factual, perda de dados, latencia e custo total observado.
- Classifique truncamento por limite, sinal do provedor e inspecao da saida. `finish_reason != stop` isoladamente nao prova truncamento em todo provedor.
- Inspecione amostras manualmente contra input e criterio. Zero falhas observadas em N casos nao equivale a risco zero; reporte N, incerteza e cobertura.

## Controle da rodada

- Defina antes do teste casos normais, longos, ambiguos e sensiveis a perda de dados.
- Inclua casos de falha conhecidos do baseline quando houver, sem otimizar so para eles.
- Registre timestamp, ID do endpoint e revisao do modelo quando o catalogo fornecer.
- Capture erros, rate limits e recusas separadamente de saida vazia.
- Valide JSON contra o schema esperado, nao apenas sintaxe, quando houver contrato estruturado.
- Calcule custo pela cobranca observada ou uso retornado e tabela vigente; diferencie estimativa de fatura.
- Nao compare modelo novo com baseline em parametros diferentes sem rotular essa limitacao.
- Evite enviar dados pessoais ou segredos reais ao provedor; use conjunto permitido e redigido.
- Se a API for instavel, repita amostras suficientes e reporte variancia, sem esconder falhas.
- Criterio de parada inclui teto autorizado de chamadas/custo e impossibilidade de teste fiel.
- Preferencia de modelo do OWNER e restricao de escopo, nao hipotese a ser revogada pelo benchmark.
- A recomendacao pode ser manter baseline, testar mais ou trocar em tarefa posterior.

## Decisao e prova

Compare primeiro qualidade e integridade dos dados, depois custo e latencia conforme requisitos do servico. Inclua baseline e limites do experimento no veredito.
Nao trocar configuracao, reiniciar servico ou ampliar gasto automaticamente. Mudanca exige pedido/OK aplicavel e plano de reversao.
Se houver troca autorizada em tarefa posterior, prove o ID ativo por fonte viva e amostras pos-troca; arquivo de config sozinho nao prova uso.
Entregue tabela por ID exato, payload/parametros, amostra, falhas, custo, incerteza e recomendacao. Evite segredos em artefatos.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
