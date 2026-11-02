---
name: haos-execution-waves
description: "Planeja e executa trabalho HAOS/Codex em ondas pequenas, com arquivos sob ownership exclusivo, dependências, revisão read-only, evidências verificáveis e gates externos."
---

# HAOS Execution Waves

## Modos

- `PLAN`: transformar objetivo ou briefing em `EXECUTION_PLAN.md`; não implementar.
- `EXECUTE`: validar e executar um `EXECUTION_PLAN.md`; registrar `EXECUTION_EVIDENCE.md` ao lado do plano.

## Contrato do plano

O plano deve declarar:

1. objetivo, escopo, fora de escopo e critérios de aceite;
2. caminho exato de cada arquivo que pode ser criado ou alterado;
3. uma tabela de itens com `id`, `onda`, `objetivo`, `arquivos`, `depende_de`, `owner`, `revisor`, `evidencia` e `gate_externo`;
4. riscos, lacunas e decisões ainda pendentes;
5. comandos locais de validação e resultado esperado.

Cada arquivo tem um único owner durante toda a execução. Itens com arquivos sobrepostos não podem ter owners diferentes nem executar em paralelo. Dependências devem usar IDs existentes e formar um grafo sem ciclos.

## Ondas e agentes

- Uma onda contém somente itens cujas dependências já terminaram.
- Use no máximo três agentes por onda.
- Toda delegação declara `fork_turns: none`, objetivo, contexto, saída, qualidade, limites e dependências.
- O revisor deve ser diferente do owner, atuar em modo read-only e não corrigir arquivos.
- Se não houver agente especializado real, o orquestrador assume o item; não invente agentes.

## Execução e evidências

Antes de cada onda, confira o worktree e preserve alterações preexistentes. Cada item só fica `CONCLUÍDO` quando a evidência prevista foi executada, lida e registrada com comando, resultado e arquivos observados. Falha de validação retorna o item ao owner; conflito de escopo bloqueia o item.

`EXECUTION_EVIDENCE.md` deve conter, por item: status, owner, arquivos alterados, validações, resultado da revisão e pendências. O fechamento usa `STATUS: CONCLUÍDO | BLOQUEADO | REVISÃO NECESSÁRIA`, seguido de evidências e próximos passos.

## Gates externos


## Validação deste port

Execute na raiz do repositório:

```powershell
pwsh -NoProfile -File .agents/skills/haos-execution-waves/scripts/validate-port.ps1
```
