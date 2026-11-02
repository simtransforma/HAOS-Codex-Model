---
name: haos-caveman-compression
description: "Comprime saidas locais grandes no HAOS Codex com Caveman Engine, recuperacao do original e guardrails para evidencias criticas."
---

# HAOS Caveman Compression

Use o Caveman como compressor local de contexto, nao como persona ou estilo de
resposta. A prioridade continua sendo preservar evidencia antes de economizar
tokens.

## Runtime

- Wrapper: `${USER_PROJECT_ROOT}/scripts/caveman-haos.ps1`.
- Runtime isolado: `${HAOS_PRIVATE_ROOT}`.
- Telemetria desativada.

## Quando usar

Use explicitamente em saidas locais grandes e repetitivas:

- testes, lint e build;
- logs locais sem segredos;
- JSON grande sem dados pessoais ou credenciais;
- resultados extensos de `rg` ou `fd`.

Prefira a saida bruta quando ela for curta. Economia inferida nao prova economia
na fatura do provedor.

## Bloqueios

Nunca comprimir por padrao:

- `git diff`, patches, reviews ou historico necessario para auditoria;
- auditoria de seguranca, incidentes, deploy, infraestrutura e migracoes;
- dados financeiros, banco, producao ou evidencias legais;
- `.env`, `MASTER.env`, segredos, chaves, tokens, cookies ou dados pessoais;
- qualquer saida cuja perda de uma linha possa mudar a decisao.

Nao usar `caveman wrap codex`, proxy global, conversao de skills, pixel mode,
persona Caveman ou hooks do Claude Code.

## Operacao

```powershell
pwsh -NoProfile -File scripts\caveman-haos.ps1 -Action status
& scripts\caveman-haos.ps1 -Action shrink -ToolCommand @('pytest','-q')
pwsh -NoProfile -File scripts\caveman-haos.ps1 -Action compress -InputPath .\app.log
pwsh -NoProfile -File scripts\caveman-haos.ps1 -Action retrieve -Handle ccr_0123456789abcdef0123456789abcdef
```

Quando houver handle `ccr_*`, mantenha-o disponivel ate a verificacao terminar.
Se faltar detalhe necessario, recupere o original. Se nao houver handle, releia a
fonte bruta. Nunca trate resumo comprimido como unica prova de conclusao.

## Validacao

Antes de concluir uma tarefa que usou compressao:

1. confirme que codigos de erro, caminhos e valores decisorios permaneceram;
2. recupere o original quando a conclusao depender de trecho omitido;
3. compare com a fonte bruta em seguranca, deploy ou mudanca irreversivel;
4. descreva a economia apenas como estimada, salvo medicao real do provedor.

Referencia: `${USER_PROJECT_ROOT}/docs/BENCHMARK_RTK_VS_CAVEMAN_2026-08-30.md`.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
