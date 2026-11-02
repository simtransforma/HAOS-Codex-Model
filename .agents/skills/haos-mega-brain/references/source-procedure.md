---
name: haos-mega-brain
description: "Adaptação Codex do Mega Brain: ingestão, processamento, DNA Cognitivo, dossiês, conclave e busca em memória."
---

# HAOS Mega Brain para Codex

Use em comandos `mb:*` e tarefas de conhecimento.

## Comandos

| Comando | Ação |
|---|---|
| `mb:briefing` | Status operacional, memória, pendências e riscos |
| `mb:ingest` | Ingerir material em `${USER_PROJECT_ROOT}/memory/inbox/` |
| `mb:scan` | Listar inbox |
| `mb:process` | Processar inbox em 8 fases |
| `mb:extract-dna` | Extrair DNA Cognitivo em 5 camadas |
| `mb:ask` | Consultar agente com contexto aplicado |
| `mb:conclave` | Debate → Crítico → Advogado do Diabo → Sintetizador |
| `mb:dossier` | Gerar/consultar dossiê |

## Pipeline de 8 fases

1. Chunking
2. Resolução de entidades
3. Extração de insights
4. Classificação
5. Síntese narrativa
6. Compilação de dossiê
7. Playbook prático
8. Indexação em memória

## DNA Cognitivo

L1 Filosofias  
L2 Modelos mentais  
L3 Heurísticas  
L4 Frameworks  
L5 Metodologias

## Observação

Se o claude-mem isolado estiver ativo, usar a busca semântica dele. Caso contrário, usar `memory/` + busca textual local.
