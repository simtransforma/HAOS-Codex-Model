---
name: haos-memory-triple
description: "Rotina de memoria HAOS no SSD H: repo local, Obsidian, GitHub do projeto e HAOS_Memory global, com claude-mem isolado."
---

# HAOS Memory Triple

Use ao salvar, consultar, fechar ou sincronizar memória.

## Camadas

1. `${HAOS_PRIVATE_ROOT}` - fonte operacional local.
2. `${HAOS_PRIVATE_ROOT}` - leitura humana organizada.
3. GitHub privado `simtransforma/your-private-project` - versao do projeto.
4. `${HAOS_PRIVATE_ROOT}` - memoria global sanitizada, remote `simtransforma/HAOS_Memory`.

## Regras

- Nunca salvar segredos.
- Sanitizar dados sensíveis.
- Separar fatos duráveis de logs de sessão.
- `${USER_PROJECT_ROOT}/memory/durable/`: fatos permanentes.
- `memory/sessions/<session_slug>/`: historico organizado por tarefa.
- `HAOS_Memory/sessions/<session_slug>/`: espelho global da mesma tarefa.
- `Obsidian/HAOS-Codex-Xtreme3/01-Sessoes/<session_slug>/`: espelho humano.
- `${USER_PROJECT_ROOT}/memory/episodic/`: aprendizados por projeto.
- `${USER_PROJECT_ROOT}/memory/claude-mem/`: dados do claude-mem isolado, não misturar com Claude Code.

## Fechamento

Executar `${USER_PROJECT_ROOT}/scripts/finish-task-haos.ps1`.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
