---
name: clint-meta-audience-sync
description: "Cria Custom Audience na Meta Ads a partir de uma tag do Clint CRM + workflow n8n de auto-sync (cron 30min). Use SEMPRE quando o user mencionar criar público ou audience Meta com leads do Clint, sincronizar tag Clint com Meta Ads, auto-alimentar público Meta com leads novos, manter audience atualizada com leads novos do CRM, RMKT baseado em tag, ou variações tipo \"cria um público pros leads com tag X\", \"sincroniza tag X com a Meta\", \"mantém esse público alimentado com Clint\". Executa as 3 fases (upload inicial via Clint API, workflow auto-sync n8n, documentação na vault Obsidian) automaticamente. Padrão validado em produção 06/06/2026."
---

# Clint → Meta Audience Sync

Pipeline completo: tag Clint → Custom Audience Meta → workflow n8n autossustentado.

## Quando usar (triggers do user)

- "criar público na Meta com tag X do Clint"
- "audience Meta com leads que têm tag X"
- "sincronizar tag X com Meta Ads"
- "auto-alimentar público Meta com Clint"
- "manter público X atualizado com Clint"
- "público pra retarget de quem tem a tag Y"
- "público combinado de várias tags" / "junta essas tags num público só"
- "compartilha o público nas duas contas" / "usa esse público no C01 e C02"
- "cria um lookalike disso" / "LAL 1% da tag X"

> Para combinado multi-tag, compartilhamento entre contas e Lookalike, ver `references/multi_account_combined_lal.md` (padrões validados 19/06/2026: QRcode/369flix, 6 por-produto + 1 combinado + LAL 1% BR nas contas C01 `${RESOURCE_ID}` e C02 `${RESOURCE_ID}`).

## O que faz

3 fases em sequência:

1. **Upload inicial** — busca contatos da tag na Clint, normaliza, hash SHA-256 multi-key, cria audience na Meta, faz upload
2. **Workflow n8n** — duplica workflow base de auto-sync (cron 30min) que mantém o público alimentado com leads novos da mesma tag
3. **Documentação** — salva tudo na vault Obsidian em pasta com data `DD-MM-AAAA`

## Inputs requeridos (peça/confirme antes de executar)

| Input | Obrigatório? | Default |
|---|---|---|
| Tag Clint (nome exato) | sim | — |
| Nome da audience Meta | sim | — |
| Conta de ads Meta (`act_*`) | não | `${RESOURCE_ID}` (SIM BM01 C01-Perpétuo) |
| BM (BM01/BM02/...) | não | BM01 |

**Confirme com o user antes de executar.** Mostre os 4 valores e peça "OK assim?" antes de disparar.

## Execução

Tudo orquestrado pelo script principal:

```bash
PYTHONIOENCODING=utf-8 python "scripts/run_pipeline.py" \
  --tag "Assinou_LP-060626" \
  --audience-name "[Clint] [FPV369] [Assinou ListaP]" \
  --ad-account "${RESOURCE_ID}" \
  --bm BM01
```

O script lê o MASTER.env, faz todas as 3 fases e imprime IDs no final.

Detalhes técnicos de cada fase: ver `references/`.

## Outputs esperados (reporte sempre pro user)

```
✅ Audience criada: [Nome] (id 120248...)
   - Tag origem: <nome>
   - Total contatos na tag: X
   - Únicos enviados: Y
   - Meta recebeu: Z

✅ Workflow n8n ativo: [Auto-Sync] Clint Tag → Meta Audience: <slug>
   - ID: <workflow_id>
   - URL: https://service.example.invalid<id>
   - Próxima execução: <timestamp>

📁 Documentação: HAOS-Tarefas-Projetos-Vault/Tarefas/DD-MM-AAAA_publico_<slug>/
```

## Pegadinhas técnicas (já mapeadas)

Leia `references/troubleshooting.md` se algo falhar:

- Erro `2654/1870053` "subtipo não aceito" → omitir `subtype=WEBSITE`
- Erro `require('crypto') blocked` n8n → SHA-256 puro JS (já no workflow base)
- Clint sem `created_after` → walk reverso paginação
- Erros de auth → conferir vars no MASTER.env
- Workflow base ID: `${RESOURCE_ID}` (Hetzner)

## Restrições

- NUNCA persistir tokens em arquivos da vault ou logs
- Tokens só em Credentials n8n + MASTER.env
- Hash SHA-256 antes de enviar à Meta (PII em texto puro = bloqueio)

## Convenção de naming

- Folder vault: `DD-MM-AAAA_publico_<slug>/`
- Workflow n8n: `[Auto-Sync] Clint Tag → Meta Audience: <slug>`
- Folder n8n: "Public Audience Sync" (id `${RESOURCE_ID}`)
- Slug = lowercase, espaços → `_`, sem chars especiais

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
