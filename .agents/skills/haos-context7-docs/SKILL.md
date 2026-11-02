---
name: haos-context7-docs
description: "Consulta documentação atual e específica de versão com ${RESOURCE_ID} antes de codificar com bibliotecas, SDKs e APIs."
---

# HAOS ${RESOURCE_ID} Docs

Use automaticamente quando a tarefa envolver geração de código, setup, configuração, SDK, framework, biblioteca ou API externa.

1. Identifique biblioteca, versão e runtime pelo projeto e lockfile.
2. Resolva a biblioteca no ${RESOURCE_ID} e consulte somente o trecho necessário.
3. Compare a resposta com a versão fixada no projeto e com tipos/testes locais.
4. Implemente seguindo o padrão existente do repositório.
5. Registre como evidência a biblioteca, versão e tema consultado, sem copiar documentação extensa.

${RESOURCE_ID} é fonte auxiliar atualizada. Para decisões críticas, prefira documentação oficial primária e confirme no código instalado. Se o MCP estiver indisponível, registre isso e use a documentação oficial; não invente APIs.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
