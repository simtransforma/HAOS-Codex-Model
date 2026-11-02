# Contrato e validação RFM-E

## Âncoras e precedência

Fontes internas auditadas em 04/10/2026, com paths e hashes em `../SOURCE.json`: 01-dados.md (D01), 07-crm-jornadas.md e 11-cobertura-crm-score.md. Baseline de código informado pela auditoria: `${HAOS_PRIVATE_ROOT}`, HEAD `d9faab9580fb67c0229ed6d2723b2acb9f4068e4`. Não representa HEAD futuro nem implantação atual.

Pontos históricos: `lib/leads.ts:1299,1324–1333` recalcula após compra; listagem `:393,449`; detalhe `:767–784`; `bigdata-etl/lead_score_v2.sql:92–129,155–164` normaliza/materializa. Localizar funções reais antes de editar. Decisão vigente do usuário nesta tarefa: CRM próprio independente do Clint. Pedido atual e contratos aprovados prevalecem sobre exemplos de revops e desta referência.

## Contrato único, sem fórmula inventada

Snapshot mínimo: `person_id`, `identity_version`, `model_version`, `feature_version`, `band_version`, `snapshot_mode` (`DECISION` ou `RESTATEMENT`), `decision_at`, `as_of`, `knowledge_cutoff`, `computed_at`, janela `[start,end)`, timezone, moeda/base financeira, watermarks, R/F/M/E, faltantes, cobertura, contribuições, evidências referenciadas e status. Restatement inclui `restated_at` e referência ao snapshot original. Guardar hash dos inputs normalizados quando útil à reprodução; logs não carregam PII.

- R: tempo desde última operação paga elegível até o corte; sem compra pode ser não aplicável, não “mau lead”.
- F: operações econômicas distintas na janela. Dedupe de evento não basta para dedupe econômico; pedido espelhado só se unifica com bridge comprovada. Itens, cobranças e parcelas não viram novas compras.
- M: valor na base/moeda aprovada, com refund/estorno e critério financeiro explícitos. Não assumir que receita, caixa, contrato e recebível sejam equivalentes.
- E: eventos humanos comprovados, deduplicados, com caps/decaimento aprovados. Formulário tentado não é cadastro; convite clicado não é entrada; pagamento não prova acesso entregue.

RFM-E é vetor de características. Preservar e documentar a fórmula atual validada, unidades e escala antes de corrigir escritores. Não somar reais crus a tags/pontos; valor monetário só pode entrar por transformação aprovada, explicável e limitada. Scores comercial, engajamento e risco são dimensões separadas; a proposta de escala 0–100 não torna qualquer resultado uma probabilidade. Se a escala vigente diferir, planejar migração explícita, não alterar silenciosamente.

Faixas, pesos, quantis, caps, decaimento e thresholds são versionados e dependem de decisão validada. Empates/base pequena/outliers exigem regra determinística. Congelar limites por versão; evitar quantis móveis por consulta. Falta de origem/identidade ambígua produz `INSUFFICIENT_DATA` ou revisão, não zero/default plausível. F=0 só quando cobertura suficiente confirma ausência de operação; score nulo não equivale score baixo.

## Point-in-time e segmentação

Em `DECISION`, fixar o instante histórico da decisão: `as_of <= decision_at` e `knowledge_cutoff <= decision_at`. Features usam `occurred_at <= as_of` e `received_at <= knowledge_cutoff`; janelas respeitam contrato inclusivo/exclusivo. Calcular hoje não permite elevar o corte de conhecimento da decisão passada. Features, identidade, regras, taxas, faixas e parâmetros usados para reconstruir uma decisão devem ter sido conhecidos/disponíveis no instante pertinente, no máximo `decision_at`; uma versão aprendida depois não pode ser apresentada como a decisão histórica. Sem prova dessa disponibilidade, marcar reconstrução inconclusiva. Simulação de regra candidata fica identificada e não é confundida com decisão realmente tomada.

Em `RESTATEMENT`, conservar a referência e `decision_at` originais, registrar `restated_at` e permitir conhecimento posterior até esse instante (`knowledge_cutoff <= restated_at`). É uma revisão explícita da visão histórica, nunca sobrescrita do snapshot `DECISION` nem substituto dele em backtest preditivo. Evento tardio pode entrar nessa revisão conforme `as_of`, mas não provar o que o sistema sabia na decisão original. Novas decisões usam novo `decision_at` e novo snapshot; não renomear o passado para contornar o limite.

Lista/detalhe/filtro/export devem consumir o mesmo snapshot, versão e corte. Segmento guarda definição/AST validada, escopo, versões e membership reproduzível. JSON/campo/operador inválido retorna erro, nunca lista de filtros vazia ampliando audiência. UI não reaproveita preview inválido como autorização.

DNC, opt-out, bloqueio, identidade ambígua, escopo e restrição de canal/finalidade são gates separados e obrigatórios. Nenhum saldo de pontos compensa supressão. Antes de qualquer futura ação autorizada, revalidar elegibilidade atual e intersectar com snapshot aprovado; não incluir pessoas novas silenciosamente. Merge/unmerge provoca nova versão de identidade, preservando fatos e bloqueios, com reavaliação dos afetados.

## Validação offline e shadow

Usar infraestrutura de testes já disponível no projeto, sem nova biblioteca por padrão. Impedir conexão/escrita de produção no ambiente de teste. Se não houver isolamento demonstrado, fazer especificação/fixtures locais e reportar bloqueio do teste dependente.

| Cenário | Resultado exigido, independente de pesos inventados |
|---|---|
| Mesmo evento reprocessado | Mesmos R/F/M/E e único efeito de projeção |
| Compra manual seguida de refresh | Mesma função/contrato; nenhum caminho tags + reais |
| Mesma operação espelhada com bridge válida | F/M não dobram; aliases preservados |
| Duas compras distintas da mesma pessoa | Ambas contam conforme janela; não colapsar por e-mail/valor/dia |
| Parcela liquidada | Não gera nova aquisição/F; caixa permanece no domínio correto |
| Refund/chargeback | Nova revisão explicável conforme contrato financeiro; histórico preservado |
| Evento futuro ou ainda desconhecido no corte | Não aparece nas features do snapshot antigo |
| Decisão dia1; evento ocorreu dia1 mas chegou dia3 | Excluído de DECISION dia1; permitido em RESTATEMENT dia3 identificado, nunca como evidência preditiva da decisão dia1 |
| Faixa ou vínculo de identidade aprendido dia3 | Não reconstrói DECISION dia1 como se já fosse conhecido; revisão/simulação identificada separadamente |
| Identidade conflitante ou fonte incompleta | Qualidade insuficiente/revisão; não fabricar zero nem penalização pessoal |
| DNC com score máximo | Inelegível para contato no escopo da supressão |
| Filtro inválido | Erro explícito e nenhum segmento acionável |
| Ranking/detalhe/filtro/export | Mesmo snapshot, versão e explicação |
| Empates, cliente novo e base pequena | Resultado determinístico segundo política aprovada |

Exemplo sintético sem pesos: pessoa P-SYN possui operação O1 elegível antes do corte; chegam dois eventos paid idênticos e três notificações de parcelas. Com cobertura íntegra e janela contendo O1, F esperado é 1, não 5. Evento O2 ocorrido depois do corte não muda esse snapshot. Um DNC válido mantém a pessoa inelegível independentemente do valor calculado. M esperado depende da base aprovada de O1, não dos valores das notificações de parcelas. Esse exemplo testa grão/elegibilidade, não calibração comercial.

Shadow calcula candidato sem substituir oficial ou produzir mensagens. Comparar diferenças por pessoa sintética/agregado e causa; volume real afetado só pode ser declarado após medição autorizada. Backtest descritivo não demonstra aumento causal de vendas.

## ML futuro, somente se solicitado

Não adotar modelo ou biblioteca nesta rotina. Se houver proposta futura: definir alvo, horizonte e população com origem temporal coerente com a decisão. Para previsão a partir de `decision_at`, label em `(decision_at,decision_at+horizonte]`; se optar por origem `as_of`, exigir `as_of = decision_at` nessa avaliação. Features nunca usam label, compra futura ou atividade posterior ao corte de conhecimento da decisão. Restatement não substitui features point-in-time.

No treino/ajuste de cada divisão temporal, usar apenas labels com horizonte completo e resultado já conhecido no cutoff de treino, anterior ao início da janela de avaliação. Remover ou marcar como censuradas amostras cujo horizonte invada a avaliação ou não tenha observação madura; não aprender com respostas futuras. Usar separação/purga temporal proporcional ao horizonte, com desenho por entidade para evitar vazamento; documentar limites e amostras excluídas. Resultados de avaliação só são medidos após seus próprios labels amadurecerem, sem devolvê-los ao treino da mesma divisão. Não exigir biblioteca nova para esses controles.

Comparar com baseline de regras. Escolher métricas segundo uso: ranking/precisão/recall e capacidade operacional; calibração se emitir probabilidade, além de cobertura, estabilidade por coorte e drift. Avaliação retrospectiva deve ser seguida de observação prospectiva em shadow antes de promoção. Não transformar correlação em causalidade; mudança de comunicação exige avaliação própria. Thresholds não são benchmark universal.

## Promoção e rollback

Aceite: contrato/formula/faixas aprovados; writers unificados; invariantes aplicáveis executados; qualidade e comparação documentadas; revisão independente; todos os consumidores convergem. Bug D01/APP-08 ou perda de supressão impede uso acionável. Uma fórmula candidata “melhor” sem avaliação não passa.

Rollback seleciona versão/snapshot anterior explicitamente datado, preserva fatos/ledger e pausa ações dependentes. Não restaurar writer defeituoso, apagar fatos ou remover DNC. Reprocessamento exige inputs/versionamento e idempotência. Deploy, migração, refresh remoto ou mudanças externas continuam sujeitos ao escopo autorizado pelo usuário, não à instalação desta skill.

Saída mínima: estado atual vs proposto; arquivos/revisão inspecionados; tabela writer→contrato→consumidor; versão/input/corte; fixtures executadas e falhas; comparação shadow quando realizada; limitações; gate aprovado/bloqueado e rollback concreto. Não declarar produto corrigido com base apenas em documento ou validador de frontmatter.
