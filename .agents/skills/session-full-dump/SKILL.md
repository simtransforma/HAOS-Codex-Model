---
name: session-full-dump
description: "Cria um dump completo, redigido e transport\u00e1vel de uma sess\u00e3o Codex para handoff ou auditoria."
---

## Contrato publico de execucao

Material de dominio portado da fonte real, nao uma instalacao de infraestrutura.
As regras do usuario e do AGENTS.md prevalecem sobre comandos e exemplos abaixo.
Publicar, enviar, gastar, alterar servidores, reiniciar, apagar, push e merge
exigem consentimento explicito para o destino e a acao. Nao executar comandos
com placeholders. Nao buscar o cofre ou ambientes do autor. Ferramentas/MCPs
citados precisam existir na instalacao do usuario; nomes nao provam acesso.
Consulte [PORTABILITY.md](PORTABILITY.md) para dependencias, recursos omitidos,
licencas e adaptacoes. Exemplos preservados nao sao prova de estado vivo.

# Session Full Dump para Codex

Use quando o usuário pedir dump da sessão, exportação completa, handoff bruto ou
contexto para continuar o trabalho em outra sessão/agente.

## Execução

```powershell
python "${USER_WORKSPACE_ROOT}" --input <transcript.jsonl>
```

Opções: `--session-id <id>`, `--output <arquivo.md>`, `--include-full-content`,
`--no-memory-content` e `--depth <n>`.

## Contrato

1. Localizar um transcript JSONL real do Codex; nunca presumir o schema do Claude.
2. Processar linha a linha, tolerando registros inválidos e tipos futuros.
3. Produzir as 13 seções: metadata/schema, timestamps, ferramentas, arquivos,
   comandos, agentes, URLs, serviços/APIs, skills, MCP, memória tocada,
   memória atual e auditoria de redação.
4. Correlacionar subagentes somente quando o transcript fornecer evidência;
   caso contrário registrar `não observado`.
5. Redigir segredos antes de qualquer saída ou escrita. Variáveis podem aparecer
   apenas pelo nome, nunca pelo valor.
6. Excluir instruções de sistema e contexto bruto por padrão. `--include-full-content`
   permite texto de conversa redigido, mas continua excluindo o bootstrap interno.
7. Validar que o arquivo exista e tenha as seções esperadas antes de anunciar sucesso.

## Segurança e escopo

O dump é local e não faz commit, push, deploy, chamada externa nem altera Claude Code.
Em HAOS, a saída padrão fica em `Downloads` para ser anexada manualmente; um caminho
explícito pode ser escolhido com `--output`. Para handoffs normais, use também
`session-handoff` e `<USER_DEPENDENCY:memory/handoffs/>`.

## Limitação conhecida

O formato do transcript Codex não é contrato público. O relatório inclui contagens
de tipos e registros desconhecidos para tornar mudanças de versão detectáveis.

## Playbook

O procedimento operacional completo está em
`<USER_DEPENDENCY:playbooks/session-dump-codex.md>` (user-supplied dependency; see PORTABILITY.md).
Consulte-o para resolver a sessão, executar o smoke test, verificar a redação e
transportar o arquivo para outra sessão.
