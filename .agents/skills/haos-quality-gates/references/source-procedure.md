---
name: haos-quality-gates
description: "Gates progressivos por stack para lint, tipos, testes, build, seguranca e comportamento, sem impor ESLint ou Biome globalmente."
---

# HAOS Quality Gates

Use ao criar, migrar ou endurecer validacoes de um projeto.

## Descoberta primeiro

Leia manifests, scripts e CI existentes. Identifique stack e comandos oficiais.
Nao instale uma ferramenta nova quando o projeto ja possui gate equivalente.

## Escada de promocao

1. `OBSERVAR`: rode o gate atual e salve baseline reproduzivel.
2. `CONTER`: novas mudancas nao podem aumentar falhas conhecidas.
3. `REDUZIR`: corrija lotes mecanicos com write-sets pequenos e testes.
4. `ZERAR`: confirme zero no escopo definido, sem esconder arquivos.
5. `BLOQUEAR`: promova para erro/CI somente apos estabilidade e rollback testado.

Nao confunda zero warnings com comportamento correto. O conjunto minimo, quando
aplicavel, inclui lint, typecheck, testes, build, verificacao de segredo e um teste
do sintoma ou jornada critica.

## Contrato por lote

- baseline e meta numerica;
- regra/ferramenta e versao;
- arquivos sob owner unico;
- classificacao `MECANICA` ou `COMPORTAMENTAL`;
- comando de verificacao e resultado;
- stop-loss e rollback;
- risco residual.

Mudanca de configuracao global, auto-fix amplo ou supressao em massa exige tarefa
