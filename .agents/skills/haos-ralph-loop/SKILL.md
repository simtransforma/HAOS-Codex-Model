---
name: haos-ralph-loop
description: "Execute bounded, resumable Codex work and review loops for multi-step coding tasks with explicit acceptance criteria and local verification."
---

# HAOS Ralph Loop

Use this skill for a coding task that is too large, uncertain, or repetitive for one Codex turn. It runs a fresh-context worker followed by a fresh-context reviewer until the task is ready, blocked, or a safety limit stops it.


## Required Setup

Before starting, obtain or write:

- one concrete objective;
- measurable acceptance criteria;
- the target repository;
- relevant source-of-truth files;
- project validation commands when they exist.

Default to a short, bounded run: 8 iterations, 2 consecutive phase failures, 3 stagnant iterations, and 30 minutes per phase. Raise a limit only when the task justifies it.

## Operating Contract

1. Run the PowerShell runner with `-DryRun` first.
2. Start only with `-Run`; write state under `<repo>/.codex/haos-ralph-loop/`.
3. The worker uses `workspace-write`; the reviewer uses `read-only` and receives fresh context.
4. Completion requires all three: worker `COMPLETE`, reviewer `SHIP`, and every configured validation command passing.
5. A real blocker creates `RALPH-BLOCKED.md`. A `STOP` file ends a run safely. Use `-Resume` after adding feedback or resolving the blocker.
6. Never add `--dangerously-bypass-approvals-and-sandbox`, `--full-auto`, automatic commit, push, deploy, or message sending. Escalate such steps through the normal HAOS approval gate.

## Runner

```powershell
$runner = '${HAOS_PRIVATE_ROOT}'

pwsh -NoProfile -File $runner `
  -Cwd '${HAOS_PRIVATE_ROOT}' `
  -Objective 'Corrigir o fluxo de login sem alterar a API publica.' `
  -AcceptanceCriteria 'Os testes de autenticacao passam.', 'O build passa.', 'Nenhuma chave ou configuracao de producao foi alterada.' `
  -ValidateCommand 'npm test -- --runInBand', 'npm run build' `
  -DryRun
```

After reviewing the effective configuration, replace `-DryRun` with `-Run`. To resume, use the same `-Cwd` with `-Resume -Run`.

## Evidence To Return

Read `<repo>/.codex/haos-ralph-loop/run-summary.md`, the last review result, and validation records. Report the stop reason, verified checks, changes made, and any remaining blocker. Do not claim completion from the worker message alone.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
