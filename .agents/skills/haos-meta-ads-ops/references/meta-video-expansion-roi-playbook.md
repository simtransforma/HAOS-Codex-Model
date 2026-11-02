# Playbook: expansao de videos e verdade de atribuicao/ROI na Meta

Use este procedimento quando uma campanha existente receber uma matriz grande de videos ou quando o resultado financeiro atribuido ao trafego precisar ser consolidado. O playbook nao concede autorizacao de gasto: criacao, ativacao, mudanca de budget e pausa continuam exigindo o gate aplicavel.

## Resultado esperado

Ao final, deve existir evidencia reproduzivel de que:

1. somente as combinacoes ausentes foram criadas;
2. objetos preexistentes e campos congelados permaneceram intactos;
3. o lote nasceu PAUSED e so os IDs do run foram ativados;
4. configured status, effective status e entrega foram relatados separadamente;
5. vendas, receita atribuida, caixa e lucro nao foram confundidos.

## Papeis e separacao de responsabilidade

- **executor unico:** unico processo autorizado a enviar POSTs;
- **traffic/media buyer:** define matriz, copy, CTA, destino, UTMs e limites;
- **tracking/data:** valida evento, janela, aliases e integridade das fontes;
- **CFO:** autoriza linguagem de caixa, contrato, margem e lucro;
- **QA independente:** faz GET novo sem confiar em respostas de POST ou no state local.

Dois escritores simultaneos para a mesma conta/campanha sao proibidos. Adote lock exclusivo por escopo e aborte o segundo runner.

## 1. Contrato congelado

Antes de qualquer mutacao, grave um snapshot com:

- campanhas e conjuntos permitidos;
- cardinalidade esperada `videos x conjuntos`;
- copies, CTA, link, `url_tags`, thumbnail e atores aprovados;
- budget, bid, publico, exclusoes, pixel/conversao, atribuicao e placements que nao podem mudar;
- IDs dos anuncios/creatives existentes que devem ser preservados;
- autorizacao vigente e seu alcance;
- qualquer override explicito do owner sobre matriz editorial anterior.

Um override do owner muda o contrato, mas nao elimina QA tecnico, politica, compliance ou readback. Registre a regra deterministica usada para copy/asset; nao invente uma regra silenciosa.

## 2. Manifesto local de midia

Para cada arquivo:

- provar existencia, tamanho e SHA-256;
- validar container/codec, dimensoes, duracao e orientacao;
- comparar o conjunto real de arquivos com o manifesto esperado;
- atribuir uma copy aprovada e versionada;
- bloquear arquivo divergente, duplicado ou sem contrato.

O SHA-256 identifica o asset local; o nome serve apenas como rotulo humano.

## 3. Inventario vivo GET-only

Ler campanhas, conjuntos, anuncios, creatives e videos. Classificar a midia pelo creative real (`object_story_spec.video_data.video_id`), nunca pelo nome exibido na UI.

Calcular fingerprints estaveis:

```text
asset_fp     = sha256(bytes_do_arquivo)
creative_fp  = sha256(asset_fp/video_id + copy + CTA + link + url_tags + thumbnail + atores)
placement_fp = sha256(adset_id + creative_fp)
```

Se o state local sumiu, mas o GET comprova contrato exato e saudavel, adote o objeto como `SKIP_ADOPT`. State local nunca vence a fonte viva.

## 4. Planner e ledger bloqueante

O dry-run deve produzir, por objeto:

| Decisao | Quando usar |
|---|---|
| `SKIP` | objeto live exato, saudavel e ja conhecido |
| `SKIP_ADOPT` | objeto live exato; state local ausente/desatualizado |
| `CREATE` | ausencia comprovada, sem duplicata live |
| `UPDATE` | somente campo mutavel, dentro da autorizacao |
| `REPLACE_REQUIRED` | creative ou contrato imutavel divergente |
| `BLOCK` | duplicata, drift, escopo incerto ou gate ausente |

O ledger deve conter IDs, fingerprints, motivo e quantidade de POSTs planejados. O apply aborta se o fingerprint do snapshot vivo mudar depois do planejamento.

## 5. Upload e creative sentinela

1. Fazer upload resumivel de cada asset unico apenas uma vez.
2. Persistir o `video_id` imediatamente.
3. Esperar estado READY; erro terminal bloqueia o lote.
4. Criar um creative sentinela PAUSED.
5. Fazer GET independente e conferir video, copy, CTA, link, `url_tags`, thumbnail e atores.

Creative e campos imutaveis de conjunto nao recebem correcao silenciosa: divergencia exige replacement novo, PAUSED, e cutover autorizado.

Em `object_story_spec.video_data`, enviar exatamente um entre `image_hash` e
`image_url`; preferir o hash estavel e usar URL publica somente como fallback.
Variacoes de texto pertencem ao `asset_feed_spec` do mesmo creative. Elas nao
criam novos bracos de midia.

## 6. Criacao da matriz

Criar apenas os pares ausentes `video x adset`, sempre com `status=PAUSED`. Persistir cada ID antes de seguir. Apos cada familia/lote, executar readback e checkpoint idempotente.

Quando o contrato determina um anuncio isolado por conjunto, `N` midias
selecionadas geram exatamente `N` conjuntos, `N` creatives e `N` anuncios.
Cinco bodies/titles/descriptions dentro do creative continuam sendo um unico
braco. A cardinalidade nasce do inventario de midia aprovado, nao da quantidade
de textos.

O gate de ativacao exige simultaneamente:

- cardinalidade exata em todos os conjuntos;
- zero missing, extra ou duplicate;
- todos os novos objetos PAUSED;
- IDs antigos preservados;
- quantidade de imagens existentes inalterada;
- zero drift em budget, targeting, exclusoes, promoted object, atribuicao, CTA, link e UTM;
- nenhuma issue bloqueante;
- autorizacao de ativacao/gasto ainda valida.

## 7. Ativacao e status

Ativar somente os IDs criados nesta execucao. Para cada ID, guardar POST e GET imediato.

- `status=ACTIVE`: configuracao solicitada;
- `effective_status=ACTIVE`: objeto efetivamente apto;
- `PENDING_REVIEW`/`IN_PROCESS`: transitorio, nao prova entrega;
- `DISAPPROVED`/`WITH_ISSUES`: falha a investigar.

Entrega real exige leitura posterior com `effective_status=ACTIVE` e/ou impressoes/gasto. Nao eleger ou cortar criativo recem-publicado sem janela minima definida no plano de teste.

## 8. Rate limit e retomada

- respeitar `Retry-After`;
- usar backoff exponencial limitado;
- em rate limit persistente, cooldown de 90-150 segundos;
- retomar do ultimo checkpoint confirmado;
- nunca reiniciar o lote inteiro nem repetir POST cego;
- erro de payload, permissao ou politica nao e rate limit.

POST de criacao nao recebe retry cego. Apos erro HTTP definitivo, reconciliar por
GET antes de continuar: campanha e objetos parciais devem estar PAUSED; cada ID
deve pertencer ao journal; a cardinalidade observada deve corresponder ao prefixo
completo da sequencia `adset -> creative -> ad`, sem lacunas. Somente entao
retomar do primeiro objeto ausente. Resultado ambiguo, ID sem origem ou sequencia
quebrada permanece `BLOCK`.

## 9. Rollback conservador

Em falha:

1. pausar somente IDs novos ou alterados pelo run;
2. nao apagar videos/creatives nem tocar objetos antigos;
3. registrar falha individual de rollback;
4. provar por GET o estado seguro;
5. transformar rollback incompleto em bloqueio explicito.

## 10. Readback independente

Uma segunda responsabilidade executa GET novo e prova, por conjunto:

- contagem de imagens e videos unicos;
- IDs de anuncio, creative e video;
- configured/effective status;
- review feedback e issues;
- missing, extra e duplicates;
- invariancia de budget, targeting, exclusoes, evento, atribuicao, CTA, link e UTM;
- soma agregada coerente com o detalhamento.

Compare campos semanticos estaveis. Em creative de video, a Meta pode renovar a
`image_url` assinada da thumbnail entre leituras. Essa diferenca so e aceitavel
quando `video_id`, `image_hash`, CTA/link, identidade, copies, UTMs e todas as
demais chaves continuam exatos. A allowlist de normalizacoes deve ser explicita e
testada; campo inesperado ou mudanca de hash/ID bloqueia a ativacao.

Depois, um rerun em dry-run deve retornar `planned_posts=0`, decisoes apenas `SKIP/SKIP_ADOPT` e state hash estavel.

### Prova criptografica de preview

Antes de ativar gasto, vincule a prova visual ao pacote aprovado:

1. gere previews por GET, sem POST, nos formatos contratados;
2. grave manifesto com `ad_id`, formato, path, bytes e SHA-256 de cada arquivo;
3. confine cada path ao diretorio de previews e rejeite traversal;
4. exija unicidade de `(ad_id, formato)` e cobertura exata de todos os anuncios;
5. vincule a prova ao SHA-256 do manifesto e do apply-readback, alem de schema,
   fingerprint e campanha;
6. compare os registros da prova com a projecao exata do manifesto;
7. recalcule hash e bytes dos arquivos reais;
8. exija zero registros reprovados.

Preview gerado nao significa preview aprovado. A aprovacao nasce do contrato
completo e do readback verificavel.

## 11. Escopos de resultado

Escolha e declare um modo antes de calcular:

- `PRODUCT_ONLY`: somente conversoes especificas allowlisted do produto;
- `FUNNEL_ATTRIBUTED`: produto principal mais upsell/cross-sell cuja relacao esteja comprovada;
- `COMPANY_GLOBAL`: faturamento da empresa; nunca apresentar como venda causada por uma campanha.

O relatorio deve declarar campanhas, periodo, timezone, moeda, nivel de agregacao, `action_report_time` e janela de atribuicao. Fontes com cortes diferentes devem mostrar a defasagem.

## 12. Escada de verdade financeira

1. **Entrega:** gasto, impressoes e cliques. Nao prova venda.
2. **Purchase generico:** teto atribuido pela plataforma; pode conter varios produtos e nao e caixa.
3. **Conversoes especificas:** classificam parte do total, mas continuam sendo atribuicao.
4. **Clique x visualizacao:** separar 7d-click e 1d-view e mostrar o peso de view-through.
5. **Transacao reconciliada:** pagamento aprovado ligado por `event_id`, `transaction_id`, `order_id` ou chave equivalente.
6. **Contrato:** valor integral contratado, separado de parcelas pagas e contas a receber.
7. **Margem/lucro:** caixa conciliado menos todos os custos relevantes.

Nunca some aliases equivalentes como `purchase`, `omni_purchase`, pixel purchase e variacoes. Escolha uma metrica canonica para o total e use os aliases somente como conferencia.

Concilie:

```text
Purchase generico = conversoes classificadas nao sobrepostas + residuo nao classificado
```

Se as conversoes especificas excederem o total generico, bloqueie o consolidado ate explicar sobreposicao, janela ou escopo.

## 13. Formulas e linguagem

```text
CPA_evento = gasto / eventos atribuidos
ROAS_evento = action_value no escopo / gasto
saldo_bruto_apos_midia = receita atribuida - gasto
retorno_bruto_sobre_midia = (receita atribuida - gasto) / gasto
ROAS_caixa = caixa pago reconciliado / gasto
ROI_caixa = (caixa pago reconciliado - gasto) / gasto
margem_contribuicao = caixa reconciliado - midia - taxas - impostos - reembolsos - chargebacks - comissoes - custos variaveis
ROI_financeiro_liquido = margem_contribuicao / (midia + demais custos de aquisicao)
```

Use “a plataforma atribuiu” nos niveis 2-4, “caixa pago reconciliado” no nivel 5 e “valor contratado” no nivel 6. `action_value` pode ser ticket, entrada, parcela, valor fixo ou valor mal enviado; nao o promova automaticamente a receita financeira. `receita atribuida - midia` nao e lucro liquido.

## 14. Testes bloqueantes

1. state exato -> `SKIP`; faltante -> `CREATE`;
2. state perdido + live exato -> `SKIP_ADOPT`;
3. status mutavel divergente -> `UPDATE`;
4. creative/campo imutavel divergente -> `REPLACE_REQUIRED/BLOCK`;
5. duplicata live e segundo writer -> `BLOCK`;
6. dry-run -> zero POST;
7. sentinela e lote completo -> PAUSED, cardinalidade exata, antigos intactos;
8. ativacao -> somente IDs do run e status separados de entrega;
9. falha injetada -> rollback somente do run;
10. `image_hash + image_url` no mesmo `video_data` -> rejeicao;
11. retomada parcial -> journal/GET sem lacunas e zero duplicacao;
12. URL assinada renovada -> aceita somente com IDs, hash e contrato estaveis;
13. manifesto, prova, arquivo ou hash adulterado -> bloqueio;
14. fixture de metricas -> um Purchase nao vira varios aliases; produto, upsell e residuo respeitam o escopo; divisao por zero e tratada.

## Anti-padroes

- confiar apenas em nomes, UI ou state local;
- multiplicar bracos porque existem varias copies no mesmo creative;
- usar URL assinada de thumbnail como identidade estavel;
- repetir POST de criacao depois de falha sem reconciliar journal e GET;
- tratar preview gerado como aprovacao sem manifesto e hashes;
- ativar lote incompleto;
- editar creative ou campo imutavel em lugar;
- confundir `ACTIVE` configurado com veiculacao;
- somar Purchase generico com conversoes especificas;
- chamar `action_value` de caixa;
- multiplicar parcela e declarar dinheiro recebido;
- comparar faturamento global com gasto de uma campanha;
- chamar saldo bruto apos midia de lucro liquido;
- omitir a parcela atribuida por visualizacao;
- fazer rollback amplo sobre objetos preexistentes.

## Evidencias minimas de fechamento

- contrato congelado;
- manifesto de assets com hashes;
- planner/ledger CREATE-UPDATE-SKIP;
- snapshot pre e pos;
- IDs criados/tocados;
- resultado do sentinela;
- journal de criacao e reconciliacao de retomada, quando houve parcial;
- manifesto/prova de previews com hashes, bytes e cobertura exata;
- readback independente;
- prova de rerun no-op;
- relatorio de atribuicao no escopo declarado;
- registro de rollback ou declaracao comprovada de que nao foi necessario.
