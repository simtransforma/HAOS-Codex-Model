---
name: dash-master-leadscore
description: "Auditar, especificar e validar o Lead Score RFM-E da Dash Master SIM, especialmente divergência entre ranking, detalhe e filtros ou score alterado após compra. Não autoriza comunicação, mudança de pesos, execução em produção ou adoção de ML."
---

# Lead Score da Dash Master

Aplicar ao CRM próprio da Master; Clint é legado de migração, nunca dependência obrigatória do score. O achado histórico D01 mostrou compra manual gravando `qtd_tags + total_pago`, divergente do cálculo normalizado. Revalidar o código atual antes de afirmar que o defeito persiste. Pontos não são reais nem probabilidade.

## Fluxo de trabalho

1. **Entrada:** identificar pedido e modo: diagnóstico/especificação por padrão; implementação local somente se solicitada. Fixar repo/revisão, contrato financeiro, identidade, janela, `decision_at`, corte de conhecimento, modo do snapshot (decisão ou restatement), versão de score/faixas e escopo de acesso. Reusar decisões válidas; registrar lacunas materiais sem inventar pesos.
2. **Inspeção:** localizar todos os escritores e consumidores do score, incluindo compra manual, refresh, MV, listagem, detalhe, filtros e export. Comparar com as fontes históricas declaradas em [SOURCE.json](SOURCE.json); caminhos/linhas são pontos de partida, não prova atual. Não executar ETL, compras ou refresh contra produção para testar.
3. **Diagnóstico:** demonstrar divergência com fixture sintética/offline ou leitura estática identificada. Separar regra atual, defeito e proposta. Sem fonte suficiente, retornar inconclusivo; dado ausente não significa mau lead.
4. **Contrato:** ler [contrato e validação](references/contrato-e-validacao.md). Preservar a fórmula RFM-E vigente validada enquanto unifica escritores; se nenhuma for confirmada, propor contrato pendente e bloquear uso acionável. Não aprovar pesos/faixas por conta própria. Separar comercial, engajamento e risco; DNC permanece trava externa.
5. **Teste:** rodar verificações offline com fontes isoladas, depois shadow sem escrita externa. Exigir equivalência de snapshot entre ranking/detalhe/filtro/export, idempotência, corte temporal e supressão. Testes previstos não são testes realizados. ML é opcional e tem gate próprio na referência.
6. **Saída:** entregar achados com arquivo/linha/revisão, mapa de escritores, contrato/versionamento, diffs explicados, testes executados/resultados, limitações e plano de rollback. Vincular cada conclusão à evidência.

## Gate operacional

Liberar versão de leitura somente com fórmula/faixas aprovadas, testes aplicáveis aprovados, qualidade suficiente e revisão independente. Score inconsistente fica pendente ou em snapshot anterior explicitamente datado, sem alimentar ação automática. Para corrigir D01, implementar um único caminho de cálculo ou invalidar o score até recomputação; nunca manter writer tags + reais em paralelo.

Não enviar mensagens, exportar audiência real, alterar campanha, gravar banco remoto, implantar, instalar dependências ou recalibrar silenciosamente. A skill não concede autorização externa. Não acessar PII se fixtures/agregados bastarem. Consentimento, elegibilidade e autorização de comunicação não resultam de score alto.

Fechar com `STATUS`, evidências, pendências e próximo passo. Proveniência do pacote não prova correção do produto ou implantação. Main coordena QA, instalação e fechamento; esta skill não escreve memória nem faz commits automaticamente.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
