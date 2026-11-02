---
name: haos-otimizacao-master
description: "Procedimento especializado de haos-otimizacao-master; consultar requisitos e evidencias antes de executar."
---

# Otimização master HAOS

Melhorar a eficiência das vendas pagas; avaliar margem somente com custos atuais e receita conciliada. Tratar aumento de vendas e redução de gasto como objetivos a verificar, sem prometer resultado.


## Carregar o contexto necessário

1. Reutilizar bootstrap HAOS válido, autorização da tarefa, último snapshot, journals e automação existente. Carregar haos-superpowers (dependency not bundled: ../haos-superpowers/SKILL.md) e haos-meta-ads-ops (dependency not bundled: ../haos-meta-ads-ops/SKILL.md). Consultar documentação oficial via ${RESOURCE_ID} antes de payload/API novo ou alterado.
2. Para quota da Meta, aplicar [quota por dimensão e endpoint](references/quota-meta-por-dimensao.md). Ler [ciclo-operacional.md](references/ciclo-operacional.md). Para o Livro Trilha, carregar também perfil-trilha.md (dependency not bundled: references/perfil-trilha.md). Para outro produto, definir seu contrato de dados, limites e critérios; nunca herdar números desse perfil.
3. Resolver por fontes disponíveis conta, produto, destinos, IDs, objetivo, janela, custo vigente, métrica paga e teto autorizado. Perguntar somente pela lacuna material que impedir a ação dependente; continuar o trabalho independente.

## Executar uma rodada finita

1. **Retomar:** verificar execução ativa, lock, `pending`, deduplicação e horário real. Reconciliar pendência antes de reenviar qualquer escrita.
2. **Observar:** coletar Meta e fonte paga nas mesmas datas/fuso; conferir configuração, entrega, falhas, orçamento no nível real e alterações manuais. Reutilizar janela fechada recente com origem/horário explícitos.
3. **Conciliar:** separar compra Meta, pedido pago, receita, backend e margem. Manter registros sem atribuição fora do denominador por anúncio. Não substituir pagamentos por proxy Meta.
4. **Decidir:** ordenar pelo objetivo vigente do perfil, impacto, confiança e amostra; classificar manter, investigar ou candidato a pausa/redução/retomada/escala. Na Trilha, considerar retorno Livro + ${USER_BRAND} e não o antigo CPA-alvo isolado. Distinguir peça criativa, variante por `ad_id` e campeão histórico. Priorizar melhorias sustentadas antes de elevar gasto.
5. **Validar e executar:** obter QA dos IDs, campos e valores concretos; usar autorização vigente dentro do escopo. Sem autorização aplicável, permanecer em leitura e apresentar proposta pronta. Não exigir novo consentimento por turno, relógio, clique ou ritual. Ampliação material de gasto/destino/risco exige autorização correspondente.
6. **Conferir:** GET imediatamente antes/depois, journal persistido, estado efetivo e evidência de entrega. Sincronizar a planilha canônica por ID e conferir o destino. Preservar fórmulas, histórico e edições manuais.
7. **Acompanhar:** quando solicitado, configurar/reutilizar a automação do app conforme o playbook; verificar configuração e primeira execução. Ler a skill não agenda nada. Fechar a rodada com próximo horário e pendências reais.

## Distribuir responsabilidades

Main coordena; tráfego é dono único da Meta; BI/CFO concilia dados e mantém a planilha; QA revisa independentemente. CMO prioriza quando necessário. Fazer chamadas reais, reutilizar agentes e limitar cada onda a três especialistas, com `read_files`, `write_files`, recursos e dependências disjuntos. Revisores não corrigem os arquivos revisados. Main integra Evoluir e commits conforme o pedido; subagentes não mantêm memória ou commits independentes.

## Preservar o escopo

- Reutilizar objetos e IDs; não duplicar campanha ou campeão para fabricar uma ação. Criar substitutos apenas se necessário e autorizado, com vínculo ao histórico e sem gasto simultâneo indevido.
- Não editar vídeos, artes, copies, páginas, públicos ou eventos sem pedido/autorização aplicável. Diagnóstico pós-clique pode gerar proposta separada.
- Escalar apenas com repetição do resultado pago, amostra e custo confiáveis, capacidade operacional e orçamento explicitamente autorizado. Janelas sobrepostas não são repetição independente. Nunca aplicar aumento percentual universal.
- Uma falha temporária não conclui a tarefa. Preservar checkpoint, erro sanitizado e retomada limitada; nunca repetir POST ambíguo. Não contornar quota, trocar credenciais ou criar daemon/n8n como atalho.

## Entregar evidências

Informar período e fuso, fonte/atualização/completude, gasto, valor vendido reconhecido, recebimentos e retorno do funil, custos/margem quando verificáveis; depois ranking pelo objetivo do perfil, ações executadas com IDs/antes/depois, pendências e próximo cheque. Pedidos e CPA podem ser diagnósticos, sem substituir o objetivo Livro→${USER_BRAND}. Distinguir configurado, efetivo, entregando e resultado financeiro. Mudança nominal de orçamento não é economia realizada; um intervalo curto após ajuste não demonstra efeito causal.

Usar `CONCLUÍDO`, `REVISÃO NECESSÁRIA` ou `BLOQUEADO` com recibos verificáveis. Em acompanhamento, silêncio para estado não acionável, exceto relatório periódico explicitamente solicitado. Não enviar WhatsApp, e-mail ou outra mensagem externa sem autorização específica.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
