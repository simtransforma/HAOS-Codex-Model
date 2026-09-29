---
name: haos-execution-waves
description: Organizar trabalho complexo em ondas pequenas com ownership e verificacao.
---

# Ondas de execucao

Defina escopo, dependencias, owner por arquivo, aceite, testes e rollback.
Limite cada onda a poucos agentes com arquivos distintos. Um revisor
independente avalia a entrega em modo somente leitura.

Antes de editar, confira branch, diff e arquivos nao rastreados. Depois,
registre arquivos alterados, teste executado, resultado observado e risco
residual. Falha de teste reabre o item. Deploy, push e acao externa exigem
aprovacao especifica.
