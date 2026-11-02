---
name: haos-meta-ads-ops
description: "Operacao de campanha (mídia paga) na Meta via Marketing API/Graph para HAOS/SIM/${USER_BRAND} - criar e editar campanha, conjunto e anuncio, beneficiario/pagador (disclaimer de transparencia BR), evento de otimizacao, estrutura (1x1x10/Advantage+/ABO/CBO), exclusoes, upload de imagem, url_tags, rate limit e troubleshooting de criacao. Use SEMPRE que a tarefa for SUBIR ou MEXER em trafego pago Meta - \"cria a campanha\", \"sobe o conjunto/anuncio\", \"monta a campanha no Meta\", \"muda o orcamento/publico/criativo\", \"duplica o ad set\", \"ativa/pausa a campanha\", \"erro ao criar ad set\", \"anunciante nao verificado / beneficiario e pagador\", \"como subo imagem pro Meta\", \"qual evento de otimizacao\", \"Advantage+ ou ABO\". NAO use pra tracking/pixel/CAPI/Stape (= haos-meta-stape-api), pra politica/recuperacao de conta (= meta-ads-policy), nem pra criar publico do Clint (= clint-meta-audience-sync). Esta skill foca em OPERAR campanha; puxa credencial da haos-meta-stape-api."
---

# Meta Ads Ops (operacao de campanha)

Operar midia paga Meta via Marketing API (tools MCP `ads_create_*` / `ads_update_entity` / `ads_get_ad_entities`) e Graph direto (v21.0). Para acesso/credencial ver a skill **haos-meta-stape-api** (token `META_TOKEN_BM01` no MASTER.env). Para publico ver **clint-meta-audience-sync**. Para politica/conta restrita ver **meta-ads-policy**.

## Contexto fixo (${USER_BRAND} / SIM)
- Conta principal: C01-Perpetuo `${RESOURCE_ID}` (BM01 `${RESOURCE_ID}`, BRL, min daily 514c = R$5,14). Outras: C02-Engajamento `${RESOURCE_ID}`.
- Pixel `${RESOURCE_ID}`. Page ${USER_BRAND} `${RESOURCE_ID}`. IG `${RESOURCE_ID}` (@${USER_BRAND}).
- App "SIM Operations Hub" `${RESOURCE_ID}` (Live). System User "HAOS Backend" `${RESOURCE_ID}`.

## ⚠️ ANUNCIANTE BR (transparencia) - COMO CRIAR AD SET BR VIA API (RESOLVIDO 21/06/2026)
Em conta BR **sinalizada (flagged)**, criar ad set novo com entrega BR via API/MCP da:
> erro 100 / subcode **3858634** (`blame_field_specs:[["compliance_section"]]`): "O anunciante esta ausente / Advertiser is missing".

### SOLUCAO PROVADA (cria 100% via API, System User token, SEM UI):
O trilho do BRASIL **NAO** e `dsa_beneficiary`/`dsa_payor` (esses sao SO UE/Taiwan/Singapura/Australia). Sao **DOIS campos** no POST do ad set:
```
regional_regulated_categories  = ["BRAZIL_REGULATION","VOLUNTARY_VERIFICATION"]
regional_regulation_identities = {"universal_beneficiary":"<BUSINESS_ID>","universal_payer":"<BUSINESS_ID>"}
```
- `<BUSINESS_ID>` = **business id da BM verificada** (na C01 = BM 01 `${RESOURCE_ID}`). Chaves = `universal_beneficiary`/`universal_payer` (NAO existe `brazil_*`).
- Funciona com **System User token (META_TOKEN_BM01)**. Nao precisa user token de admin.
- Provado por teste A/B na conta: SEM os 2 campos = 3858634; COM os 2 campos = ad set criado. Achado por workflow multi-agente (deep research + teste A/B). Fonte: SDK oficial facebook-business `adset.py` / `regionalregulationidentities.py`.

### LICAO DE OURO - descobrir o business id em qualquer conta:
Ler um ad set JA criado pela UI e copiar o objeto:
```
GET /{ADSET_ID_DA_UI}?fields=regional_regulated_categories,regional_regulation_identities
```
Os ad sets da UI tem `dsa_beneficiary`/`dsa_payor` VAZIOS porque o dado real mora nesses 2 campos regionais.

### FATOS de apoio:
- So dispara na CRIACAO de ad set novo. **ADS dentro do ad set HERDAM o compliance do pai** -> criar ad/creative/url_tags via API funciona normal (nao re-dispara o gate). Provado: ad criado sob o ad set BR sem erro.
- ABO sem bid de campanha exige `bid_strategy` explicito no ad set (ex: `LOWEST_COST_WITHOUT_CAP`), senao da 2490487 ANTES do 3858634.
- NAO e confirmacao de identidade PESSOAL (CPF/CEP, facebook.com/id) - esse fluxo e outro e fica em loop a toa. NAO mandar o dono fazer isso por causa do 3858634.
- Ajuda (mas nao basta pra API) ter o "Anunciante e Pagador PADRAO" setado na conta: Config. de publicidade > Verificacoes e transparencia dos anuncios (`/adsmanager/manage/advertising_settings/beneficiary_payer`) > "Definir padrao". Isso faz a UI auto-preencher; pra API o que resolve sao os 2 campos regionais acima.
- `compliance_section` (blame do erro) NAO e parametro setavel (GET retorna "nonexisting field"); e so caminho interno, satisfeito via os 2 campos.
- Rate limit da conta e agressivo (erro 17) apos ~60 chamadas; espacar / cooldown ~150s.

Precedentes operacionais devem vir dos builders seguros e versionados em `scripts/`; nao use arquivos temporarios como fonte canonica.

### Regra de negocio (qual entidade usar)
- **DIGITAL BROS AGENCY CRIACAO E LANCAMENTO DE INFOPRODUTOS LTDA** = padrao, campanhas em geral (incl. formacoes tipo FPV369).
- **${USER_BRAND}** = campanhas que vendem LIVRO.
- **SIM (${USER_BRAND})** = nova empresa, a incluir (CNPJ no RAG-SIM; inclusao de nova entidade e na Central de Transparencia da Meta UI + documento, NAO via API).

## Upload de imagem (a tool MCP NAO sobe imagem)
`ads_create_creative` so aceita `image_hash` (ja no Meta) ou `image_url` publica. Para subir arquivo local:
- Graph: `POST /${RESOURCE_ID}/adimages` com o arquivo. Em Windows usar **base64 via PowerShell** (curl do Git Bash corrompe multipart com nome acentuado). Retorna `hash` por imagem. Guardar mapa nome->hash.

## Criar a estrutura (PAUSED sempre)
1. Campanha: `ads_create_campaign` objetivo `OUTCOME_SALES` (vendas). CBO = setar `campaign_daily_budget`; ABO = NAO setar budget na campanha (vai no ad set). `special_ad_categories` = [] (PNL/mindset nao e categoria especial, mas PODE ser flagado como tema social - ver acima).
3. Ad/creative: ver secao **Criativo certo** abaixo (multi-texto 5/5/5 + 1:1 + 9:16 via asset_feed_spec). Simples (1 texto/1 imagem) = `object_story_spec.link_data` (link, image_hash, message, name, description) + `call_to_action`.
4. `url_tags` pertence ao **creative**, nao ao anuncio. Criar ou ler o creative com `utm_source=MetaAds&utm_medium=paid&utm_campaign={{campaign.id}}&utm_content={{adset.id}}&utm_term={{ad.id}}` (exigido pelo dash master/BI; `utm_source=MetaAds`, nao `facebook`). Creative divergente deve ser substituido por outro creative; nao tente corrigir `url_tags` com POST no `/{ad_id}`.

### Duracao e orcamento padrao
- `lifetime_budget` exige prazo e valor total explicitamente aprovados para essa campanha. Nao transformar verba total em `daily_budget` nem inventar prazo para satisfazer a API; se ela exigir esses dados, interromper a criacao ou manter o objeto PAUSED ate resolver a decisao material.
- No preflight e no GET apos criacao/alteracao, comparar duracao e budget antes/depois no nivel correto (campanha CBO, conjunto ABO). Divergencia bloqueia a ativacao; esta regra nao autoriza editar campanhas existentes fora do escopo aprovado.

- Na C01, converter campanha existente de lifetime para daily foi rejeitado em 02/10/2026 (Graph 100/1885630); enviar ambos os campos, mesmo lifetime=0, foi rejeitado por 1487164. Nao repetir esses POSTs nem declarar conversao concluida. Quando o pedido aprovado exigir verba diaria continua, preparar substituicao idempotente preservando criativos/publicos e historico, validar pausada e impedir gasto simultaneo na troca; registrar novos IDs na planilha principal.

## Editabilidade no Ads Manager (padrao para novas campanhas)
- Antes de afirmar que o orcamento esta editavel, conferir no Ads Manager o fluxo de edicao **e publicacao** do nivel correto. Quando houver OK para a alteracao externa e for viavel, validar com o valor aprovado em objeto PAUSED, ler de volta o valor publicado e manter a veiculacao pausada ate autorizacao de ativacao. Um valor visivel em rascunho ou GET isolado nao prova que a Meta aceitara a publicacao. Se o fluxo nao puder ser testado, registrar `EDITABILIDADE A CONFIRMAR` e o motivo; nao prometer disponibilidade permanente da UI.
- Se um conjunto legado bloquear ate a mudanca de orcamento por exigir atualizacao de localizacao, diagnosticar o erro completo e comparar o publico antes/depois. A selecao atual pode ampliar o alcance em relacao a "moradores"; migrar esse conjunto somente com OK explicito para o impacto em publico e orcamento. Corrigir apenas os IDs aprovados, publicar, fazer readback e relatar o resultado; nao aplicar a migracao em massa por padrao.

## Criativo certo (multi-texto 5/5/5) - PADRAO HIBRIDO que ENTREGA (validado FPV369 22/06)
⚠️ **A ARMADILHA (custou 1 dia de debug + R$0 de entrega em 24h):** se voce joga TUDO no `asset_feed_spec` (images + bodies + titles + descriptions + link_urls + ad_formats), o creative sai `optimization_type=REGULAR` e a Meta **flipa o ad set pra `is_dynamic_creative=true` (DCO)**. Com varios ads no ad set vira estado DCO INVALIDO -> **0 impressao, SEM erro nenhum** (issues_info e ads_get_errors vazios, learning_stage e delivery_estimate vazios, ad set "ACTIVE" mas nunca entra no leilao). DIAGNOSTICO em 1 chamada: comparar `is_dynamic_creative` + `asset_feed_spec{optimization_type}` com uma campanha que ENTREGA -> a que entrega = `false` + `DEGREES_OF_FREEDOM`; a travada = `true` + `REGULAR`.

**PADRAO CERTO = HIBRIDO** (copiado da campanha que entrega): `object_story_spec` COMPLETO (midia+link+CTA) + `asset_feed_spec` SO com texto em `DEGREES_OF_FREEDOM`. E criar o AD SET com `is_dynamic_creative="false"` EXPLICITO.
1. Ad set: incluir `is_dynamic_creative="false"` no POST de criacao.
2. Creative `POST /act_/adcreatives`:
   - `object_story_spec` = `{page_id, instagram_user_id, link_data:{link, image_hash:<FEED 1:1>, call_to_action:{type:"SIGN_UP", value:{link}}}}` (SEM message/name/description aqui, vem do asset_feed_spec).
   - `asset_feed_spec` = `{bodies:[<=5 {text}], titles:[<=5 {text}], descriptions:[<=5 {text}], optimization_type:"DEGREES_OF_FREEDOM"}` (SO texto, SEM images/link/ad_formats no asset_feed_spec).
   - `url_tags=<utm>`.
3. Ad `POST /act_/ads` com `creative={creative_id}`. 1 ad por imagem/conceito (varios ads OK num ad set is_dynamic_creative=false).
- **9:16 / multi-placement:** para imagem hibrida, o padrao usa 1 imagem de feed + Advantage+ placements; a customizacao confiavel de duas imagens por placement continua pendente. Para **video vertical**, MP4 H.264 1080x1920 via `object_story_spec.video_data` ja e um caminho validado. NAO botar 2 imagens no `asset_feed_spec` nem combinar `asset_customization_rules` com multi-texto sem novo teste sentinela.
- Advantage+ Creative seletivo (opcional): `degrees_of_freedom_spec.creative_features_spec={text_optimizations:{enroll_status:"OPT_OUT"}, image_brightness_and_contrast:{enroll_status:"OPT_IN"}, image_touchups:{enroll_status:"OPT_IN"}}`. NAO mandar `standard_enhancements` (deprecado -> 3858504).

## ⚠️ CAMPOS IMUTAVEIS pos-publicacao (so RECRIANDO o ad set)
Depois que o ad set foi publicado/ativado, a Meta NAO deixa editar (erros reais coletados na FPV369):
- `is_dynamic_creative` -> POST retorna "success" mas IGNORA (continua o valor antigo).
- `attribution_spec` -> erro `1504040`.
- `promoted_object` (pixel / evento de conversao / otimizacao) -> erro `3260011` "nao e possivel editar conjunto publicado".
- `optimization_goal` (ex: trocar pra LANDING_PAGE_VIEWS) -> exige mudar attribution (imutavel) -> bloqueado `1885559`/`1504040`.
Pra mudar QUALQUER um desses = **criar ad set NOVO** (copiando o resto), ativar, e pausar/deletar o velho. Ja considerar isso ANTES de publicar (evento, atribuicao, is_dynamic_creative).

## Advantage+ Audience - pegadinha ao EDITAR
- Com `targeting_automation.advantage_audience=1`, depois de criado NAO da pra alterar `custom_audiences` (erro `1359202` "nao e possivel desabilitar Advantage"). So `excluded_custom_audiences` e editavel. Pra mudar o publico de INCLUSAO de um ad set Advantage+, **recriar o ad set**. (No frio amplo isso quase nao importa: Advantage+ usa o publico so como sugestao de peso baixo.)

## Ativacao em massa (resiliente)
- Operacoes com dezenas de chamadas podem bater o rate limit 17. Usar job retomavel, retry limitado, `Retry-After`, cooldown de 90-150s e espacamento. No fim, separar `status=ACTIVE` (configurado) de `effective_status`: `PENDING_REVIEW`/`IN_PROCESS` sao estados transitorios aceitaveis depois da ativacao, mas **nao provam veiculacao**. Entrega exige `effective_status=ACTIVE` e/ou impressoes/gasto em leitura posterior.
- Em bateria isolada, `N` midias aprovadas geram `N` conjuntos e `N` anuncios. Variacoes de texto vivem no `asset_feed_spec` do mesmo creative e nao viram conjuntos ou anuncios extras.
- Em `video_data`, enviar exatamente um entre `image_hash` e `image_url`; preferir o hash estavel. Depois de falha definitiva ou ambigua, nunca repetir POST no escuro: reconciliar journal e estado vivo por GET antes de retomar do primeiro objeto ausente.

## Integridade de creative e preview antes da ativacao

- A Meta pode regenerar a `image_url` assinada da thumbnail entre GETs. Nao use igualdade dessa URL como identidade do creative. Exija `video_id`, `image_hash`, CTA, destino, identidade, copies e `url_tags` exatos; aceite somente normalizacoes explicitamente comprovadas e allowlisted.
- Preview visual sem proveniencia nao libera gasto. O gate deve vincular manifesto, apply-readback e arquivos reais por SHA-256; confinar paths; conferir bytes; exigir os formatos contratados por anuncio, unicidade `(ad_id, format)` e zero registros reprovados.
- O procedimento completo, inclusive retomada parcial, readback semantico, adulteracao e evidencias, esta em [references/meta-video-expansion-roi-playbook.md](references/meta-video-expansion-roi-playbook.md).

## Evento de otimizacao
- `PURCHASE` nao significa origem exclusivamente CAPI/API: `promoted_object` seleciona pixel e evento, sem seletor de transporte "API-only". A expressao "Compra API" nao dispensa verificar origem/deduplicacao no tracking nem permite prometer que eventos de navegador serao ignorados.
- Escopo prospectivo: novas campanhas, duplicacoes e substitutos expressamente aprovados. Nao migrar campanhas antigas em massa. Se o conjunto existente recusar alteracao do `promoted_object`, manter PAUSED e criar substituto somente no escopo aprovado; QA, ativacao e planilha devem usar os novos IDs corretos.
- Janela: 7d-click/1d-view pra ticket alto (ciclo de decisao longo).

## Estrutura / Andromeda
- Advantage+ Audience: `targeting_automation.advantage_audience` = 1 (publico amplo, LAL como sugestao). ABO manual: `advantage_audience` = 0 + `custom_audiences`.
- O motor Andromeda premia VOLUME e diversidade de criativo -> 7+ criativos por campanha (1x1x10 = 1 campanha, 1 ad set, 10 criativos).
- Historico C01 (produtos baixo ticket): ABO rendeu mais que Advantage+ (1,80 vs 1,45). Em ticket alto + Andromeda, Advantage+ e defensavel; rodar os dois e comparar (hedge).
- Excluir compradores 180d em todo ad set de aquisicao (excluir o publico EXPLICITO de compradores, nao so o "combinado").

### Recursos premium pra ligar (pesquisa multi-agente 21/06)
- **Advantage+ Audience** =1 SO no frio amplo de prospeccao; retarget e LAL com =0 (nao deixar vazar pro frio).
- **Advantage+ Placements**: liberar (NAO restringir publisher_platforms/positions), mas SO depois de ter o 9:16 (senao a Meta corta o 1:1 feio no Stories).
- **Feed 4:5 (1080x1350)** rende mais que 1:1 (mais tela no mobile) = maior ganho de 1 ajuste; precisa arte nova.
- Criativo = ~56% do resultado no Andromeda: mirar 8-12 angulos distintos, 3-5 novos/semana; adicionar **video/VSL**.
- **CBO pra ESCALAR** o vencedor (ABO testa, CBO escala). Otimizacao por **VALUE/ROAS** exige volume estavel, moeda e valores reais reconciliados, deduplicacao, distribuicao de ticket conhecida e tratamento de reembolso/chargeback; uma contagem bruta isolada nao libera esse gate.
- NAO ligar: Dynamic Creative (suja teste 1-img/ad), ASC/`smart_promotion_type` (deprecado v25), Catalogo/DPA (sem feed).

## Pegadinhas
- Rate limit agressivo (erro 17) apos muitas chamadas (ex: dezenas de uploads) -> espacar.
- Tudo que `ads_create_*` cria nasce PAUSED.
- Conta C01 e PERPETUO; subir lancamento ali mistura aprendizado - confirmar conta-alvo.
- **Rate limit 17 e o gargalo real:** validar estrutura em 1 ad ANTES de processar muitos (self-abort no 1o se a estrutura estiver errada, pra nao queimar os 30); job em background com retry no 17.
- **PowerShell**: `$x = MinhaFuncao` CAPTURA todos os `Write-Output` da funcao na variavel (nao imprime) -> usar `Write-Host` pro log ou nao capturar. Erro HTTP no PS7 = ler `$_.ErrorDetails.Message` (HttpResponseMessage nao tem GetResponseStream). Ler token com `Get-Content -LiteralPath` (path com espaco/acento); nunca imprimir o token.

## Expansao massiva de videos e reconciliacao de resultado

Quando a tarefa envolver anexar muitos videos a conjuntos existentes ou responder "quanto o trafego vendeu", aplique o playbook bloqueante em [references/meta-video-expansion-roi-playbook.md](references/meta-video-expansion-roi-playbook.md).

Regras minimas:

- fazer planner GET-only e ledger `CREATE|UPDATE|SKIP|SKIP_ADOPT|REPLACE_REQUIRED|BLOCK` antes de qualquer POST;
- identificar cada alvo por fingerprint semantico e chave `asset x creative x adset`, nunca apenas por nome ou state local;
- criar tudo PAUSED, validar a matriz completa e ativar somente IDs desta execucao;
- rollback conservador: pausar apenas objetos novos/tocados no run;
- distinguir configuracao ativa, revisao e entrega real;
- no financeiro, deduplicar aliases Purchase, separar produtos classificados do residuo e nunca chamar `action_value` de caixa ou lucro sem join transacional.

## Relacionado
- haos-meta-stape-api (acesso/token + tracking pixel/CAPI/Stape)
- clint-meta-audience-sync (criar Custom Audience/LAL a partir de tag Clint)
- meta-ads-policy (conta restrita, apelacao, anuncio de tema social)
- Memoria: learning_meta_ads_api_creative_edit (editar url_tags/link em massa em ad existente), project_fpv369_campanha (caso real desta skill).
- Doc tecnico completo (Obsidian): `Codex-Vault/03-Resumos-Tecnicos/21-06-2026_fpv369-campanha-meta-api.md`.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
