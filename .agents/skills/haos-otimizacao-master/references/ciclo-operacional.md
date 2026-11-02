# Ciclo operacional de campanhas existentes

## 1. Contrato por produto e execução

Registrar antes da análise:

| Campo | Evidência necessária |
| --- | --- |
| Escopo | Conta, produto/funil, campanhas permitidas, destinos, exclusões e versão do perfil |
| Resultado principal | Objetivo de negócio vigente do perfil, com evento financeiro confirmado, regime, fonte canônica e deduplicação. Trilha: retorno do funil Livro + ${USER_BRAND}, não CPA isolado do livro |
| Atribuição | ID canônico, aliases únicos validados, cobertura e registros não atribuídos |
| Financeiro | Moeda/base de valor, receita bruta/líquida, custos vigentes por SKU/coorte, taxas, impostos, frete, devoluções e backend |
| Tempo | Fuso, hoje parcial, ontem/D3/D7 fechados, acumulado, atraso e completude das fontes |
| Decisão | Meta operacional, amostra mínima, maturidade, repetição, cooldown, teto por entidade e total autorizado |
| Execução | Evidência de autorização, donos, QA, journal, reversão e destino da planilha |

Não inferir orçamento ilimitado, autorização de outra tarefa ou objetivo de compra a partir de um nome. Produto de geração de leads pode ter métrica intermediária própria, explicitamente definida e sem ser chamada de venda. Aplicar os padrões HAOS vigentes para novas estruturas; reler conta e destino reais antes de agir.

## 2. Estado, identidade e coleta eficiente

Criar pasta por rodada com `task_id/revision`, horários UTC/BRT, fontes/hash, baseline e cobertura. Consultar agentes/processos e lock; retomar execução existente em vez de sobrepor. Manter um owner por API/escrita e por planilha.

Usar GETs agrupados/paginados, limitar inventário ao escopo e conferir ausências. Registrar cache por fonte e horário; não renomear snapshot antigo como fresco. Separar descoberta de IDs novos da coleta principal; ID desconhecido não entra automaticamente no escopo.

Conferir conta/billing, campanha/conjunto/anúncio, `status`, `effective_status`, `issues_info`, orçamento CBO/ABO real, início/fim, pixel/evento, destino e criativo. `ACTIVE`, nome "ABO", ausência de erro ou HTTP200 não provam entrega, estrutura ou editabilidade da UI. Entrega exige impressões/gasto observados; primeira observação tem data persistente, distinta da primeira impressão exata quando desconhecida.

Comparar snapshot, journal e estado vivo. Atribuir delta ao executor somente com recibo. Divergência manual ou não explicada preserva a entidade e bloqueia apenas a escrita dependente; não sobrescrever nem restaurar automaticamente o baseline.

Tratar vídeo/imagem e derivações como família quando houver identidade comprovada; nome parecido não basta. Manter código criativo, hash/asset, `creative_id`, `ad_id`, conjunto e campanha separados. Pausa de uma variante não invalida todas as instâncias nem apaga a condição histórica de campeão. Armazenar IDs como strings; nunca arredondar números para casar IDs. Alias arredondado legado só pode ser usado com prova de correspondência única no universo pertinente da conta.

## 3. Conciliação e qualidade financeira

- Usar gasto/entrega Meta e pedidos efetivamente pagos do gateway/DWH canônico. Registrar status pago aceito, data de pagamento ou data de negócio utilizada e testes/refundos. Deduplicar pedido/transação; não contar parcelas, linhas de SKU ou bump como compras adicionais do produto principal.
- Casar IDs exatos ou aliases únicos validados globalmente. Colisões, ausência de origem e campanhas fora do escopo ficam em resíduo explícito. Não atribuir anúncio/backend por proximidade de horário, e-mail, valor ou suposição. Resolução de identidade de cliente não prova atribuição de mídia.
- Mostrar compras atribuídas Meta separadamente. Não converter Lead, clique, IC, Purchase, valor de conversão ou razão Meta/banco em proxy de pago. Comparar fonte, janela e modelo de atribuição antes de diagnosticar diferença.
- `created_at` de uma linha não é watermark de sincronização. Registrar atraso/completude por fonte; contagem vazia não certifica zero vendas. Backlog/completude desconhecidos bloqueiam cortes baseados em ausência, sem impedir investigação ou outra ação com evidência suficiente.
- Separar produto principal e backend comprovado, receita bruta e líquida, caixa e margem. Evitar dupla contagem do mesmo pedido e não chamar backend atribuído de receita incremental causal. Calcular margem de contribuição somente com custos vigentes por SKU/coorte; não descontar taxa duas vezes se a receita já vier líquida. Antes de agregar moedas diferentes, explicitar conversão, data, taxa e fonte. Ticket, ROAS e CPA operacional não são break-even ou lucro.
- Mostrar métricas por anúncio e conjunto, inclusive zeros comprovados; agregar campanha sem dupla contagem. Valor ausente, indisponível, leitura incompleta ou entrega ainda não observada fica `A CONFIRMAR`/nulo, nunca zero presumido. D3 dentro de D7 são janelas sobrepostas. Repetição para escala exige períodos fechados independentes ou critério temporal explicitado e validado.

## 4. Ranking e plano concreto

Priorizar pelo objetivo vigente do perfil, impacto nominal, confiança e risco de remover volume vendedor. Para cada candidato, listar IDs/parents, regra do perfil, maturidade, gasto, valor vendido confirmado, recebimentos, backend, custos/retorno e comparador equivalente, alteração única, valores atuais/propostos, limite autorizado e próximo cheque. CPA é diagnóstico quando pertinente, não substituto automático do resultado do funil. Na Trilha, avaliar Livro + ${USER_BRAND} com origem e defasagem, incluindo competência versus caixa por plataforma; não usar os antigos gates de CPA25/R75 para decidir isoladamente.

Classificações: sem entrega; entrega exploratória; teste maduro; candidato; resultado repetido; campeão histórico; pausado; bloqueado por fonte/arquivo. Não promover peça a testada/campeã por publicação, CTR ou uma venda. Comparar ganchos/CTAs somente quando identificados pelos assets.

Pausa de variante exige considerar irmãos e efeito no conjunto; não pausar o último anúncio vendedor por regra genérica. Redução de campanha considera receita paga/backend e orçamento no nível correto. Retomada exige evidência nova e autorização para o gasto correspondente. Sem candidato forte, manter e investigar; não aumentar gasto por falta de campeão.

## 5. Execução, reversão e falhas

QA vincula IDs, fontes e payloads exatos por hash; não concede autorização do usuário. O executor usa autorização vigente da tarefa. Preparar proposta concreta antes de pedir somente a aprovação que realmente faltar.

Sequência por ação: GET fresco → comparar campos/`updated_time` e cooldown → persistir `pending` com ID/payload/antes/hash → enviar uma vez → persistir resposta → GET readback → conferir campo alterado e campos preservados → limpar `pending` → registrar horário e próximo limite. Manter PII e segredos fora dos artefatos; usar loader seguro, sem imprimir valores, URLs autenticadas ou conteúdo do cofre.


Salvar reversão exata, sem executá-la automaticamente: reativação/aumento restauram gasto e dependem do escopo autorizado, estado vivo e QA. Mudança manual posterior não pode ser sobrescrita para "voltar ao antes". Falha de um objeto não exige recriar pares íntegros. Não usar DELETE como rollback.

Em quota/429, respeitar cabeçalhos e backoff compartilhado, reduzir consultas opcionais e guardar próxima tentativa. Em transporte/5xx, usar retries limitados de leitura. POST com timeout/resposta ambígua permanece pendente: reconciliar IDs/títulos/fingerprint com cobertura declarada por GET antes de nova escrita. Nunca repetir cegamente ou trocar credenciais para contornar limite. Erro permanente encerra a tentativa com motivo sanitizado. Retomadas finitas preservam recibos, sem loop ocupado ou bloqueio declarado como sucesso.

## 6. Planilha e recorrência no Codex

Sincronizar somente células/linhas previstas por IDs atuais; reler antes, preservar fórmulas, Copy, validações e alterações manuais; deduplicar cadastros. Conferir readback dos IDs, status e métricas e guardar recibo próprio. Falha na planilha não desfaz silenciosamente ação Meta já confirmada.

Quando solicitado acompanhamento contínuo, procurar `automation_update`, inspecionar automações existentes por nome/prompt e atualizar a correspondente com campos completos. Usar heartbeat na conversa existente; não criar outra task, daemon, n8n, servidor ou rotina duplicada. Sem pedido de recorrência, entregar a rodada e próximo cheque sugerido, sem agendar por conta própria.

Cadência de referência para acompanhamento solicitado: leitura a cada 4h e relatório completo às 09h em `America/Sao_Paulo`; preservar horários/preferências explícitos e ajustar ao produto. Nos demais ciclos, notificar somente mudança relevante, ação executada, falha ou decisão necessária. Não incluir mensagens externas. Usar a ferramenta do app para agenda; não escrever diretivas de automação manualmente.

Prompt recorrente inclui escopo/perfil, donos, fontes, limites/cooldown, prevenção de sobreposição, critérios de notificação, próxima revisão e falhas. Fazer readback da configuração e registrar ID/status/horários. Configuração ativa não prova execução: conferir recibo da primeira rodada agendada e resultados subsequentes; até lá, recorrência executada fica `A CONFIRMAR`. Atualizar/parar automação quando o pedido mudar ou seu motivo terminar, respeitando a vontade do usuário.

## 7. Relatório e fechamento

Entregar resultado pago fechado; hoje parcial; ranking por impacto/confiança; executado versus proposto; IDs/status configurado/efetivo; orçamento nominal antes/depois; limitações de custo, atribuição e atualização; recibo Sheet; próximo cheque e cooldown. Um acumulado misturando antes/depois não mede efeito causal do ajuste.

Terminar a rodada em estado verificável: concluída, parcial com pendência concreta ou bloqueada com próxima tentativa/insumo. Uma chamada disparada não é resultado. Main aplica Evoluir conforme autorização e HAOS; não embutir scripts datados de execução automática nesta skill.
