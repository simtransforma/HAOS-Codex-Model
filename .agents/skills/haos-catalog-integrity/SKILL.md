---
name: haos-catalog-integrity
description: "Gera e valida o catalogo canonico de agentes, skills, comandos e hooks do HAOS Codex, detectando drift e dependencias Claude-first."
---

# HAOS Catalog Integrity

Use apos criar, remover, importar ou atualizar agentes, skills, comandos ou hooks.

## Comandos

```powershell
python scripts/build-haos-catalog.py
python scripts/build-haos-catalog.py --check
python scripts/build-haos-catalog.py --check --fail-on-warnings
```

O catalogo gerado fica em `${USER_PROJECT_ROOT}/docs/CATALOGO_HAOS_CODEX.md`. O modo `--check` nao
altera arquivos e falha quando o documento esta desatualizado. Alertas ficam
visiveis sem impedir a geracao; use `--fail-on-warnings` quando o gate exigir
zero alerta.

## Gates

- agente precisa de TOML parseavel em `.codex/agents/`;
- skill precisa de `SKILL.md` e nome unico;
- comando de plugin precisa de frontmatter legivel;
- dependencia executavel `.claude/` e marcada como incompatibilidade;
- wrapper GSD precisa estar classificado como `active` ou `quarantine`;
- o digest inclui `hooks.json` e os handlers locais referenciados por ele;
- referencias historicas ficam documentadas, nao sao reescritas em massa;
- contagem declarada sem geracao fresca nao vale como evidencia.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
