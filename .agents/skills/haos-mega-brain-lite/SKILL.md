---
name: haos-mega-brain-lite
description: "Use para mb:briefing, mb:ingest, mb:scan, mb:process, mb:extract-dna, mb:ask, mb:conclave, mb:dossier e gestão de conhecimento sem plugin externo."
---

# HAOS Mega Brain Lite

Implementa localmente a lógica do Mega Brain usando arquivos do repositório.

## Comandos equivalentes
- `mb:briefing`: status operacional do sistema.
- `mb:ingest`: registrar material em `${USER_PROJECT_ROOT}/memory/inbox/`.
- `mb:scan`: listar materiais pendentes.
- `mb:process`: processar inbox em 8 fases.
- `mb:extract-dna`: extrair DNA Cognitivo.
- `mb:ask`: responder com agente + DNA aplicado.
- `mb:conclave`: decisão estratégica em 4 fases.
- `mb:dossier`: gerar dossiê.

## Pipeline de processamento
1. Chunking
2. Resolução de entidades
3. Extração de insights
4. Classificação
5. Síntese narrativa
6. Compilação de dossiê
7. Geração de playbook
8. Indexação em `${USER_PROJECT_ROOT}/memory/MEMORY.md`

## DNA Cognitivo
- L1 — Filosofias
- L2 — Modelos Mentais
- L3 — Heurísticas com limites numéricos
- L4 — Frameworks
- L5 — Metodologias passo a passo

## Conclave
1. Debate paralelo
2. Crítico com score 0–100
3. Advogado do Diabo
4. Sintetizador

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
