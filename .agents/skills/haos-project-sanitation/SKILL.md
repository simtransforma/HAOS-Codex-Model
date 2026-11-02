---
name: haos-project-sanitation
description: "Saneamento medido e conservador de projetos, audit-only por padrao, com baseline, classificacao de residuos e comparacao antes/depois."
---

# HAOS Project Sanitation

Use para organizar repositorios, reduzir residuos ou preparar uma base para
manutencao. O modo padrao e **auditoria sem remocao**.

## Fluxo

1. Capture baseline: raiz resolvida, branch, `git status`, tamanho relevante,
   comandos de teste/build existentes e alteracoes preexistentes.
2. Inventarie candidatos sem seguir junctions/symlinks e sem atravessar a raiz.
3. Classifique cada candidato como:
   - `GERADO_RECRIAVEL`: cache/build comprovadamente reproduzivel;
   - `STALE_COM_EVIDENCIA`: sem referencia e com substituto confirmado;
   - `ATIVO_OU_DESCONHECIDO`: preservar;
   - `SENSIVEL`: preservar e redigir do relatorio.
4. Mostre impacto estimado e mecanismo de rollback.
5. Remocao, movimento recursivo ou limpeza externa exige OK explicito no turno.
6. Quando autorizado, altere somente o conjunto aprovado.
7. Compare tamanho, status e verificacoes antes/depois.

## Regras bloqueantes

- Worktree sujo nunca autoriza apagar ou reverter mudancas.
- Nao classificar por nome apenas; prove origem e recriabilidade.
- Nao tocar em `.git`, cofres, bancos, memoria, sessoes do usuario ou outro
  runtime sem escopo explicito.
- Nao instalar formatador/linter para justificar uma limpeza.
- Se a verificacao piorar, pare e restaure apenas o que esta rotina alterou.

## Evidencia

O relatorio deve listar manifestos de candidatos e removidos, bytes antes/depois,
checks executados, falhas e risco residual. Nunca registrar valores secretos.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
