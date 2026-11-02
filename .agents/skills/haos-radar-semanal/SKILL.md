---
name: haos-radar-semanal
description: "Audita semanalmente novos aprendizados, skills, agentes, comandos, regras e playbooks do ecossistema Claude/HAOS e os adapta com seguranca para o Codex. Use quando o usuario selecionar /haos:radar-semanal, pedir sincronizacao Claude para Codex, comparar HAOS_CC com Codex ou executar a rotina semanal de evolucao do HAOS."
---

# HAOS Radar Semanal

Executar uma reconciliacao local e idempotente entre as fontes privadas do Claude/HAOS_CC e o projeto canonico `${HAOS_PRIVATE_ROOT}`.

## Preflight

1. Carregar o bootstrap HAOS completo e consultar `claude-mem` quando pronto.
2. Ler o Rito ativo e nao sobrescrever outro assunto.
3. Inspecionar `git status`; preservar mudancas alheias e usar staging seletivo.
4. Nunca acessar valores de segredos para fazer inventario.

## Pipeline

1. Rodar `scripts\sync-claude-ecosystem.ps1` sem `-Apply`.
2. Classificar cada item em `CREATE`, `UPDATE`, `REVIEW`, `SKIP` ou `BLOCKED`.
3. Rodar com `-Apply` somente para criacoes seguras e atualizacoes gerenciadas sem conflito.
4. Ler `runtime/state/ecosystem-sync/memory-candidates.json` quando houver candidatos novos.
5. Promover procedimento para skill/playbook; regra duravel para memoria; fato especifico como privado sob demanda; segredo ou infraestrutura como bloqueado.
6. Preferir atualizar a duplicar.
7. Validar frontmatter, TOML, JSON, scripts, links, diff e auditoria de segredos.

## Prioridade de fontes


O destino Codex existente e canonico. Nao rebaixar uma regra mais completa porque outra copia e mais recente.

## Gates

- Nunca escrever nas fontes Claude/HAOS_CC.
- Mudanca ambigua em regra, hook ou agente existente vira `REVIEW`, sem sobrescrita.

## Relatorio

```text
STATUS: CONCLUIDO | LOCAL_COMPLETE / EXTERNAL_PENDING | REVISAO NECESSARIA | BLOQUEADO
INVENTARIO: contagens por fonte e tipo
CREATE/UPDATE/REVIEW/BLOCKED: itens e motivos
MEMORIA: candidatos e ativos promovidos
VALIDACAO: checks executados
GIT: diff local; push somente com OK
```

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
