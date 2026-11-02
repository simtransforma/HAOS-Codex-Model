---
name: haos-company-trust-audit
description: "Audit company trustworthiness, reputation and integrity with OSINT, public records, reviews, complaints, regulatory checks, sanctions/watchlists, domain signals, claim verification, evidence scoring, council opinion, pros/cons and reliable alternative recommendations. Use when the user asks if a company is reliable, safe, legit, trustworthy, a scam, worth buying from, worth partnering with, or asks for due diligence, reputational audit, business integrity review, company background check, vendor risk review, or comparable trusted companies."
---

# HAOS Company Trust Audit


## Guardrail central

Tratar "dados sensiveis" como sinais sensiveis de risco, nao como permissao para buscar vazamentos, credenciais, dados privados, doxxing, dumps, areas logadas ou informacao obtida por engano. Nunca coletar, publicar ou reproduzir CPF, endereco residencial, telefone pessoal, documento privado, token, cookie, senha, chave, lista vazada ou dado pessoal desnecessario.

Se houver noticia publica, comunicado oficial, processo, regulador ou fonte jornalistica confiavel sobre incidente/vazamento, usar apenas o fato verificavel como sinal de risco. Nao acessar, baixar, comprar, reproduzir ou resumir dumps, pastes ou bases vazadas.

Se uma fonte publica contiver dado pessoal, usar minimizacao: citar so o fato relevante, a fonte e o impacto, sem copiar o dado bruto.

## Gate bloqueante de execucao

Quando a auditoria for acionada por `/haos:auditor-confianca`, `haos-auditor-confianca`, plugin visual, pedido de due diligence ou pedido para saber se uma empresa e confiavel, o agente deve tratar este protocolo como obrigatorio.

Antes de finalizar, confirme que a entrega contem:

- query plan gerado antes da coleta;
- modo declarado (`FAST_SCAN`, `STANDARD_AUDIT`, `DEEP_AUDIT`, `RED_TEAM` ou `VENDOR_SHORTLIST`);
- entidade resolvida com site, CNPJ/registro quando encontrado, jurisdicao e categoria;
- evidencias coletadas em registros oficiais, reputacao/reclamacoes, midia/processos/sancoes quando aplicavel, website/transparencia, preco/orcamento e alternativas;
- auditoria de qualidade das fontes (`A`, `B`, `C`, `D` ou `X`);
- verificacao de claims centrais com tipo (`FATO`, `OBSERVACAO`, `ESTIMATIVA`, `INFERENCIA`, `HIPOTESE` ou `OPINIAO`);
- score, veredito, confianca, pros, contras, red flags e green flags;
- conselho com visao estrategica, compliance, seguranca e comercial;
- alternativas comparadas com motivo, tradeoff, faixa de preco e melhor indicacao;
- quando envolver compra/contratacao, consultoria, advisory, caixa pressionado ou `G4 Advisor`, shortlist de pelo menos 5 alternativas verificadas com canal oficial/caminho de contato quando publico; se faltar, `STATUS: REVISAO NECESSARIA`;
- lacunas, proximos passos, artefato Markdown salvo e status de PDF/WhatsApp quando aplicavel.



## Fluxo obrigatorio

1. Definir alvo: nome da empresa, site, CNPJ/registro, pais, produto/servico, decisao que a auditoria apoia e profundidade.
2. Verificar ferramentas: usar `haos-deep-research`; no repo HAOS, rodar `.agents/skills/haos-deep-research/scripts/research_tool_status.ps1` quando precisar saber se Brave/Tavily/Firecrawl estao disponiveis.
3. Resolver entidade: separar homonimos, matriz/filial, marca fantasia, razao social, dominio, perfis sociais, marketplace e app.
4. Montar query plan com `haos-query-expansion`, incluindo termos de prova e contraevidencia.
5. Coletar evidencias em camadas:
   - registros oficiais e reguladores;
   - reclamacoes, reviews e atendimento;
   - processos, sancoes e midia;
   - website, dominio, seguranca basica e transparencia;
   - preco/orcamento, condicoes comerciais, reembolso, recorrencia e faixa de mercado;
   - prova social, clientes, parceiros e anuncios;
   - alternativas confiaveis na mesma categoria.
6. Auditar fontes com `haos-source-quality-auditor`.
7. Verificar claims com `haos-claim-verification`.
8. Aplicar score de confianca e red flags. Ler `references/scoring.md` quando precisar pontuar.
9. Escrever o relatorio. Ler `references/report-template.md` para o formato final.
10. Incluir recomendacao de empresas parecidas e confiaveis; sempre indicar a melhor alternativa quando houver dados suficientes. Para cada alternativa, explicar por que foi indicada, em que e melhor/pior que a auditada, qual cenario de escolha, qual evidencia sustenta a comparacao, faixa de orcamento/preco e canal oficial/caminho quando publico.
12. Em toda auditoria de compra/contratacao, incluir media/faixa de orcamento da empresa auditada e de cada alternativa indicada, separando preco oficial, observacao de terceiros e estimativa.

## Regra especial: caixa pressionado e consultoria/advisory


Obrigatorio:

- Separar se a necessidade e `auditoria financeira/diagnostico de caixa`, `consultoria de reestruturacao`, `mentoria estrategica` ou `educacao/comunidade`.
- Verificar se a empresa auditada entrega diagnostico financeiro pratico, plano de 13 semanas, revisao de DRE/DFC, margem por produto/canal, contas a pagar/receber, CAC/payback, renegociacao de dividas e rotina de indicadores.
- Exigir caminho de contato direto, proposta formal, escopo itemizado, cronograma, donos da entrega, SLA de suporte, regras de cancelamento/reembolso, multas, recorrencia e custo total de 12 meses.
- Rebaixar a recomendacao quando o fornecedor vender programa anual, comunidade ou mentorias com poucas sessoes individuais sem uma frente clara de caixa/reestruturacao.
- Para `G4 Advisor` especificamente, checar G4, G4 Educacao/G40, termos do Advisor, parceiros executores citados oficialmente, Reclame Aqui, preco oficial ou faixa observada, suporte/cancelamento e alternativas diretas como consultorias financeiras/gestao que possam resolver caixa antes de investimento em ecossistema.
- Executar `VENDOR_SHORTLIST` como parte obrigatoria, com pelo menos 5 alternativas verificadas ou status `REVISAO NECESSARIA`: executor financeiro/turnaround, consultoria de gestao, CFO as a Service, opcao mais barata/rapida e alternativa dentro do ecossistema/parceiros oficiais quando houver.
- Se o caixa estiver pressionado, recomendar primeiro um sprint curto de diagnostico financeiro e runway com entregaveis verificaveis; so recomendar contrato anual depois de provar ROI, payback e risco de cancelamento.

Subprotocolo `G4 Advisor` + caixa:

- Tratar o Advisor como oferta de ecossistema/advisory anual ate que a proposta prove consultoria financeira hands-on.
- Caminho recomendado: pagina oficial do Advisor/formulario, WhatsApp oficial, e-mail oficial, suporte/plataforma e parceiro executor publico/oficial quando aplicavel.
- A mensagem de abordagem deve pedir: fluxo de caixa 13 semanas, DRE/DFC, margem por produto/canal, contas a pagar/receber, CAC/payback, plano de cortes/renegociacao, donos da entrega, SLA, cronograma 30/60/90 dias, custo total, cancelamento, reembolso e multas.
- Checklist minimo para diagnostico: DRE 12 meses, extratos/caixa 6 meses, contas a pagar/receber, dividas, faturamento por produto/canal, margem, CAC, midia, contratos recorrentes, impostos e forecast de 13 semanas.
- Decisao padrao quando nao houver proposta formal: `nao assinar ainda`; recomendar sprint curto de diagnostico financeiro e comparar com Auddas direto, Mid Falconi, Triunfae, EXM ou CFO as a Service conforme gravidade do caixa.

## Fontes e referencias

Ler estes arquivos conforme a tarefa:

- `references/source-map.md`: mapa de fontes publicas por jurisdicao e categoria.
- `references/scoring.md`: score, gates bloqueantes, red flags e confianca.
- `references/report-template.md`: estrutura de relatorio final.
- `references/master-prompt.md`: prompt mestre operacional para acionar o agente.
- `references/workflows.md`: fluxos FAST_SCAN, STANDARD_AUDIT, DEEP_AUDIT, RED_TEAM e VENDOR_SHORTLIST.
- `references/quality-patterns.md`: padroes de qualidade, stop rules, conselho e anti-padroes.

## Modos

- `FAST_SCAN`: 5 a 8 fontes, veredito preliminar, ate 3 alternativas.
- `STANDARD_AUDIT`: 10 a 20 fontes, score completo, pros/contras, conselho e alternativas.
- `DEEP_AUDIT`: 20+ fontes, ledger detalhado, contraevidencia, historico, padroes de reclamacao e comparativo robusto.
- `RED_TEAM`: procurar sinais de fraude, inconsistencias, abuso de afiliados, promessas exageradas e tentativas de ocultacao.
- `VENDOR_SHORTLIST`: comparar varias empresas e recomendar a melhor escolha.

## Regras de evidencia

- Conclusao forte exige fonte primaria/oficial ou confirmacao independente.
- Review isolado nao prova fraude nem confianca; usar padrao agregado, recencia, volume e resposta da empresa.
- Ausencia de reclamacao nao prova confianca; pode ser empresa pequena, nova ou pouco conhecida.
- Reclamacao alta pode ser normal em empresas de grande volume; analisar taxa, padrao, severidade e resolucao.
- Nunca chamar uma empresa de criminosa/golpista sem decisao oficial, evidencia robusta ou qualificacao clara como "sinal de alto risco".
- Separar `FATO`, `OBSERVACAO`, `ESTIMATIVA`, `INFERENCIA`, `HIPOTESE` e `OPINIAO DO CONSELHO`.

## Saida minima

Entregar:

- query plan usado antes da coleta;
- veredito: `confiavel`, `confiavel com ressalvas`, `inconclusivo`, `nao recomendado` ou `alto risco`;
- score 0-100 e nivel de confianca;
- prós e contras;
- red flags e green flags;
- tabela de qualidade das fontes;
- tabela de verificacao de claims centrais;
- ledger de evidencias com links, data de coleta e score da fonte;
- opiniao do conselho: estrategia, compliance, seguranca e comercial;
- alternativas parecidas confiaveis, com melhor recomendacao;
- justificativa comparativa das alternativas e motivo da melhor escolha;
- orcamento/preco da empresa auditada e das alternativas, com fonte e confianca;
- caminho/status do relatorio Markdown salvo;
- artefato PDF gerado, validado e status da entrega WhatsApp/Evolution para o destino padrao autorizado quando houver PDF validado;
- lacunas e proximos passos.

## Evals

Usar `evals/evals.json` para checar se o agente:

- recusa coleta privada/doxxing;
- exige evidencia e alternativas;
- separa fato de inferencia antes de cravar veredito.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
