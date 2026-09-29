---
name: haos-worktree
description: Isolar mudancas em Git worktrees quando houver necessidade real, sem perder trabalho existente.
---

# Worktree

Antes de criar uma worktree, confira branch, diff, arquivos nao rastreados,
espaco e destino. Use isolamento quando trabalhos independentes precisam de
checkout separado; nao imponha worktree para toda tarefa.

Registre base, ownership e forma de integrar. Subagentes nao criam worktrees
ou commits independentes por padrao. Nao remova uma worktree com mudancas
pendentes sem preservar o conteudo e obter aprovacao quando a limpeza for
destrutiva.
