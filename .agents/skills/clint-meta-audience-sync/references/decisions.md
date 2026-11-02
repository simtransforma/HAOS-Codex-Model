# Decisões técnicas registradas

Decisões tomadas durante a construção desta skill (06/06/2026). Explica o **porquê** de cada escolha.

## Por que polling 30min e não webhook

- Clint não tem webhook nativo confiável de "tag added"
- Polling sobrevive a falhas de entrega (retroativo)
- 30min é equilíbrio entre reatividade e custo
- Cron é trivial de monitorar/depurar

## Por que duplicar workflow via API em vez de criar do zero

- Workflow base já tem SHA-256 puro JS validado byte-a-byte
- Já tem retry exponencial + alerta WhatsApp
- Já tem walk reverso paginação Clint
- Custo de manter um template > custo de manter 1 base + N duplicatas

Quando a base evoluir, futuras duplicações herdam as melhorias. Workflows já criados NÃO atualizam automaticamente — se for crítico, aplicar manualmente.

## Por que `audience_id` e `audience_name` no Init State em vez de buscar dinamicamente

- 1 workflow = 1 audience (1:1 fixo)
- Buscar dinamicamente adicionaria latência e ponto de falha
- Imutabilidade explícita é mais auditável

## Por que NÃO embutir exclusão de compradores na audience

Recomendação do `@tracking-engineer`:

- Audience reutilizável em N ad sets, cada um com sua exclusão
- Audiência com exclusão hardcoded vira lixo se a estratégia muda
- BI/análise fica mais legível ("audience X inclui Y, ad set exclui Z")

Setup recomendado no ad set:
```
Inclusão: [Auto-sync audience da tag]
Exclusão: [Yampi Compra do produto correspondente]
```

## Por que folder `DD-MM-AAAA_publico_<slug>/` na vault

Convenção HAOS (memória `reference_obsidian_vault.md`):
- Prefix `publico_` segrega de outras tarefas
- Slug do audience name garante unicidade

## Por que `subtype=CUSTOM` (e não WEBSITE/LOOKALIKE/etc)

Esta skill é especificamente pra audiences **file-based** (lista de leads do Clint).

- WEBSITE = baseado em pixel + URL — usa outra skill/fluxo
- LOOKALIKE = derivado de outra audience — derivado, não primário
- CUSTOM = upload de lista hasheada — caso correto aqui

Se o user pedir "lookalike da tag X", primeiro cria a CUSTOM com esta skill, depois cria lookalike apontando pra ela.

## Por que credentials reutilizadas (não criar nova por workflow)

3 credentials globais no n8n:
- Clint API: `${RESOURCE_ID}`
- Meta Graph API: `${RESOURCE_ID}`
- Evolution API: `${RESOURCE_ID}`

Se rotacionar token, atualiza em 1 lugar e todos os workflows pegam. Cria credential nova só se BM/conta diferente.


- Padrão de monitoramento HAOS já existe via Evolution
- Latência menor que email

## Por que script Python (e não n8n só)

Fase 1 (upload inicial) é one-shot de alguns milhares de contatos. Rodar como script Python local:
- Mais fácil debugar/iterar
- Não polui histórico de execuções do n8n
- Pode rodar sob demanda sem ativar/desativar workflow

Fase 2 (auto-sync ongoing) é o workflow n8n — case correto pra n8n.

