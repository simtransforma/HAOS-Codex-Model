---
name: haos-worktree
description: Use quando tarefas concorrentes ou validacao de bases distintas precisarem de isolamento real de checkout Git.
---

# Isolamento opcional e recuperavel

## Entradas

Motivo do isolamento, repositorio, branch/base pretendida, ownership, destino
relativo proposto, estado do workspace e plano de integracao. Esta skill nao
torna worktree obrigatoria nem autoriza commit, push, merge ou limpeza.

## Passos

1. Avaliar se ownership disjunto no checkout atual resolve a necessidade.
   Se resolver, dispensar worktree e explicar. Pedido que proiba criacao
   prevalece; nao criar copia alternativa para contornar essa restricao.
2. Ler branch, HEAD, worktrees existentes, staged, unstaged e arquivos novos.
   Capturar baseline. Se houver trabalho sem commit necessario a tarefa,
   decidir explicitamente como preserva-lo: uma nova worktree parte de uma
   referencia Git, nao inclui automaticamente edicoes locais.
3. Confirmar base e destino sem colisao, capacidade de disco e regras do
   projeto. Verificar que o caminho resolvido fica na area permitida.
   Nao trocar branch ocupada, sobrescrever pasta existente ou usar force.
4. Main decide a criacao dentro do escopo permitido; subagente nao cria
   worktree independente por padrao. Registrar base, branch, destino, owner,
   motivo e forma de integracao antes da criacao.
5. Apos criar, verificar branch/base e estado. Nao copiar automaticamente
   arquivos ignorados, configuracoes locais, segredos ou dependencias;
   nao instalar ferramentas globais. Se setup for necessario, declarar
   requisitos e executar apenas o que o escopo ja autorizar.
6. Validar a mudanca no checkout correto com `haos-engineering` e
   `haos-quality-gates`. Entregar diff completo, inclusive arquivos novos,
   ao main. Aplicar `haos-execution-waves` se houver varios owners.
7. Antes de integrar ou limpar, reler o estado de ambos os checkouts.
   Preservar trabalho pendente. Integracao e remocao sao decisoes separadas;
   merge, push ou exclusao destrutiva exigem autorizacao explicita.
   Nunca remover uma worktree apenas porque a tentativa terminou.

## Saida

Decisao criar/reutilizar/dispensar, justificativa, base e branch, destino
relativo, ownership, baseline, verificacoes, plano de integracao e pendencias.
Nao declarar integrado por apenas existir uma branch ou um diff.

## Criterios de aceite

Isolamento necessario ou dispensado com motivo; trabalho anterior preservado;
destino validado; checks executados no checkout correto. Nenhuma copia,
instalacao, commit ou limpeza automatica foi inferida do metodo.

## Erros comuns

- Nova worktree como backup do workspace sujo: ela nao contem edicoes locais.
- Testar no checkout principal: conferir alvo e revisao antes dos comandos.
- Remover com force para liberar espaco: preservar conteudo e respeitar gate.
- Fazer commit para cumprir ritual: seguir escopo de entrega, sem imposicao.

## Cenarios de pressao

- Metodo auxiliar exige worktree, usuario pediu edicao local simples: dispensar
  isolamento se desnecessario, preservando as regras superiores.
- Destino ja existe e ha urgencia: escolher destino valido ou bloquear criacao;
  nunca sobrescrever ou apagar o existente.
- Tarefa terminou, mas a worktree tem arquivos novos: entregar inventario e
  preservar conteudo; limpeza depende de avaliacao e OK aplicavel.
