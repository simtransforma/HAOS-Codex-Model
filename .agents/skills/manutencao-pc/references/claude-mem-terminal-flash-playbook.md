---
name: claude-mem-terminal-flash-playbook
scope: pessoal-local
---

# Playbook — terminal transitório nos hooks Claude-Mem

## Sintoma

`cmd.exe`, `conhost.exe` ou janelas de PowerShell piscam a cada prompt/ferramenta, enquanto
Claude-Mem e GBrain continuam respondendo.

## Diagnóstico seguro

1. Confirmar que o fenômeno é recorrente e registrar apenas nome, pai e linha de comando dos
   processos novos; não capturar conteúdo de prompts, tokens ou arquivos.
2. Inspecionar o `bun-runner.js` de cada instalação ativa. No Windows, procurar `where bun`
   com `shell: true`, `bun.cmd` e `spawn(... shell: true)`.
3. Confirmar os healthchecks independentes: Claude Code em `37777`, Codex em `37778` e
   GBrain em `18791`. Dois workers Claude-Mem são esperados e não são duplicação acidental.
4. Auditar tarefas agendadas e a pasta Startup. Um `.cmd` de inicialização do GBrain pode
   ser substituído por um `.vbs` invisível, mantendo o `.cmd` como backup.

## Correção

1. Em cada `bun-runner.js` ativo, preferir caminhos absolutos para `bun.exe` existentes e
   iniciar Bun diretamente, com `shell: false` e `windowsHide: true`.
2. Remover qualquer bypass temporário que saia quando os argumentos contêm `hook`; captura
   de memória deve continuar funcionando.
3. No `<USER_DEPENDENCY:.codex/hooks.json>`, trocar chamadas aninhadas `powershell -File` por invocação direta
   do script com `&`, preservando os mesmos argumentos, timeouts e ordem dos hooks.
4. Substituir o inicializador visível do GBrain por um `WScript.Shell.Run` com janela `0`,
   sem desabilitar ou recriar a tarefa `HAOS_GBrain_Serve_Watch`.

## Validação obrigatória

- `node --check` passa para cada `bun-runner.js` alterado.
- Um hook de observação retorna sucesso e mantém a captura ativa.
- Claude-Mem: `/api/health` com `status=ok`, `initialized=true`, `mcpReady=true` e readiness
  HTTP 200 nas duas portas.
- GBrain: health HTTP 200 em `18791`.
- A auditoria de processos não encontra novo `cmd.exe` gerado pelos runners; PowerShell do
  próprio Codex e tarefas legítimas não devem ser confundidos com o sintoma.
- Nenhuma tarefa/serviço de Claude-Mem ou GBrain foi desabilitado; não encerrar o worker do
  outro runtime.

## Rollback

Restaurar somente o arquivo do runner ou hooks a partir do backup da mesma instalação e
repetir os healthchecks. Não apagar bancos, diretórios de memória, OneDrive ou caches sem
escopo explícito.
