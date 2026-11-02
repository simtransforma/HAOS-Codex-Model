# Quota Meta por dimensão e endpoint

Aplicar em operações de leitura e otimização da Marketing API. A regra não amplia conta, objetos, permissões ou autorização de escrita. APIs de Pages e outros produtos exigem a própria análise de roteamento.

## Evidência antes da decisão

Registrar horário, endpoint, método, HTTP, código de erro e apenas os headers de quota necessários. Nunca registrar Authorization, tokens, cookies, dados de compradores ou URLs que contenham credenciais. Preservar a origem do valor: observado nesta resposta, histórico ou não informado.

Um header omitido não significa uso zero nem confirma bloqueio. Um valor alto de uma resposta anterior continua sendo histórico; não deve ser copiado para uma resposta nova como se tivesse acabado de ser observado. HTTP 200 confirma a resposta, não a recuperação de todas as dimensões de quota.

Se o header bruto anterior não foi retido, o parser e a sequência de eventos podem sustentar sua proveniência. Declarar essa limitação; não reconstruir um header bruto fictício nem afirmar um horário de reset não informado pela Meta.

## Selecionar a dimensão aplicável

A documentação oficial distingue limites da plataforma e limites por caso de uso de negócio, ou BUC. Para pedidos aos quais ambos se aplicam, BUC tem precedência. Na Marketing API, selecionar o tipo correspondente ao endpoint e à conta na resposta atual:

- Gestão de objetos: BUC ads_management.
- Relatórios de desempenho: BUC ads_insights.
- Quando não houver BUC aplicável informado, avaliar X-App-Usage fresco, se presente e válido. Ausência de ambos exige parar ou uma verificação leve, finita e autorizada.
- Quando retornados, conferir também X-Ad-Account-Usage e X-FB-Ads-Insights-Throttle. O segundo informa carga de aplicação e conta para Insights.

BUC baixo não comprova reset da quota de aplicativo. Quando BUC rege aquela resposta, manter eventual observação de aplicativo separada, sem usá-la como substituta da dimensão selecionada. Não inferir o tipo do token pelo nome da variável; verificar o roteamento documentado e os headers efetivamente retornados, mantendo as mesmas credenciais.

## Validar o parser e preservar a parada

Distinguir header ausente de header presente com JSON null. JSON inválido, tipo incorreto, conta ou tipo BUC incompatível, campo obrigatório ausente e números não finitos ou negativos bloqueiam a decisão dependente. Não fazer fallback silencioso de um BUC malformado para outra dimensão.

Usar limiares de pausa e retomada da política operacional configurada; não tratá-los como limites universais da Meta. A correção de origem ou seleção de dimensão não autoriza aumentar esses limiares. Validar call_count, total_cputime e total_time, além dos indicadores de carga aplicáveis.

Respeitar HTTP 429, os códigos de throttling documentados, estimated_time_to_regain_access e Retry-After. Retry-After numérico precisa ser finito e não negativo; se vier em outro formato, interpretá-lo de forma documentada ou parar. Espera calculada localmente não é reset confirmado pelo servidor.

## Execução finita e verificável

1. Reutilizar checkpoint, locks e journals; confirmar owner único e pending antes da consulta.
2. Começar por uma leitura leve quando necessário. Definir previamente quantidade de tentativas, limite de chamadas e timeouts. Não usar loop aberto de probes.
3. Preservar cada resposta de quota sanitizada e a dimensão usada. Não transportar ausência de header como observação fresca.
4. Interromper em erro, dimensão necessária desconhecida ou pressão acima da política. Guardar progresso e fontes completas/parciais separadamente.
5. Reutilizar janelas fechadas com os carimbos originais; não marcá-las como recém-consultadas.
6. Para escrita, exigir o payload e os IDs autorizados, QA e release vigentes, GET protegido antes/depois e pending persistido antes do POST. Resposta ambígua ou falha de leitura após POST exige reconciliação; nunca replay automático.
7. Não trocar credenciais, conta ou rota para evitar limites. Alteração no guard deve ficar isolada, revisada e testada antes de uso; não modificar um módulo global incidentalmente.

O sucesso de um teste local não prova alteração externa. Relatar a chamada efetiva, o journal e o readback; distinguir execução bloqueada antes do POST, POST ambíguo e mudança verificada.

## Verificação mínima do delta

Cobrir precedência BUC com aplicativo histórico ou observado separadamente; ausência de header sem herança; BUC alto; tipos e contas incorretos; JSON null/malformado; Retry-After NaN, infinito e negativo; tempo de recuperação; HTTP/códigos de throttle; carga de conta/Insights; escopo permitido e POST negado por padrão. Reutilizar os testes transacionais existentes de pending, drift, resposta ambígua e ausência de replay quando o executor não mudou.

Precedente técnico de 28/10/2026: guard isolado com 41 casos locais positivos/negativos e revisão independente; coleta delimitada confirmou seis GETs, com BUC para gestão/Insights e uma resposta contendo uso de aplicativo fresco. A evidência não estabelece um reset global ou uma garantia para chamadas futuras. Artefatos privados de origem: monitoring-${RESOURCE_ID}-1200/meta-quota-documentation-evidence.json, meta-quota-guard-tests.json e meta-quota-reader-final-state.json, sob runtime/artifacts/trilha-astra-${RESOURCE_ID}.

## Fontes oficiais

- [Graph API: rate limiting e precedência BUC](https://developers.facebook.com/docs/graph-api/advanced/rate-limiting).
- [Marketing API: dimensões, headers e tratamento de throttling](https://developers.facebook.com/documentation/ads-commerce/marketing-api/overview/rate-limiting).
- [Insights: limites de carga](https://developers.facebook.com/documentation/ads-commerce/marketing-api/insights/best-practices).

Consultadas via ${RESOURCE_ID} em 28/10/2026. Revalidar ao alterar contrato, versão ou produto da API.
