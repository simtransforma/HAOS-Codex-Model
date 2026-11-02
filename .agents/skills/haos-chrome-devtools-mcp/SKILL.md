---
name: haos-chrome-devtools-mcp
description: "Diagnóstico verificável de frontend e integrações web com Chrome DevTools MCP em perfil temporário isolado."
---

# HAOS Chrome DevTools MCP

Use quando a tarefa exigir observar DOM, console, requests, performance, layout, screenshot ou comportamento responsivo real.

- O servidor padrão roda headless, isolado, sem perfil pessoal, telemetria ou consulta CrUX.
- Navegue apenas para URLs necessárias à tarefa.
- Não preencha credenciais nem execute ação externa sensível sem OK explícito.
- Capture evidência mínima: URL, viewport, erro observado e resultado após a correção.
- Para validar frontend, combine inspeção visual, console, rede e testes automatizados quando existirem.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
