---
name: bling-coautoria-envio
description: "Procedimento de emissao de NF e etiqueta de envio dos coautores/coprodutores do livro 39 Leis (Livro 2) via Bling + auto-remessa Araras (Correios). Ativar quando pedirem para emitir as notas da coautoria, gerar os pedidos dos coautores no Bling, enviar os livros dos coautores, processar a planilha de coautoria, rodar a coautoria, emitir coautoria 39 Leis, rodar o lote da coautoria, ou criar os pedidos de coautoria e a etiqueta de Araras."
---

# Bling Coautoria Envio (39 Leis Livro 2 via Araras)

Rodou em producao 2 vezes: **lote 1 em 22/07/2026** (11 pedidos, com retrabalho fiscal no meio) e
**lote 2 em 28/07/2026** (10 selecionados, 8 emitidos limpo de primeira). Tudo abaixo e verificado
ao vivo, nao e teoria.

Em **29/07/2026** o ciclo fechou **ponta a ponta pela primeira vez**: planilha lida, pedido criado, NF
autorizada, etiqueta gerada e **rastreio de volta na planilha por API** (ver c.0).

## a. QUANDO USAR

- "emitir as notas da coautoria"
- "gera os pedidos dos coautores no bling"
- "envia os livros dos coautores"
- "processa a planilha de coautoria"
- "roda a coautoria" / "roda o lote da coautoria"
- "emitir coautoria 39 leis"
- "cria os pedidos de coautoria e a etiqueta de araras"

Tambem quando alguem pedir para despachar exemplares de coautor ou coprodutor de livro.

**Contexto de negocio:** a coautoria foi vendida SEM faturamento (2 Asaas, SIM + DigitalBros,
confirmado pelo Leo). A contadora Clarice liberou a contragosto ("nao e o correto mas pode ser").
adicionais (R$ 15,90 cada) + paga o frete. Emitente: ${USER_BRAND} LTDA
(CNPJ ${RESOURCE_ID}).

## b. PRE-REQUISITOS

- Skill `bling` (cliente BlingClient, OAuth). **Atencao ao enum de situacao da NF: a skill `bling`
  diz so "6 = autorizada", o que e INCOMPLETO** (ver secao d).
- Skill `bling-nf-desconto` (a regra do desconto com lastro).
- Acesso a planilha Google pela service account do grupo (`contact@example.invalid`,
  credencial `GCP_SIM_MAKE_SA_JSON` no MASTER.env). **Leitura sempre; escrita desde 29/07/2026**, quando
- Worker bling-headless no Hetzner (`http://example.invalid:8377/internal-fetch` -> endpoint interno
  `/Api/v3/vendasinternal/<pid>`). E o UNICO caminho que grava volume e desconto do jeito que a UI
  grava. Sem o worker de pe, a fase de prep nao roda.
- Token Bling via `token_probe.py` no Hetzner (dono unico do token).
- **Pipeline de referencia:** `bling_fiscal/coautoria/` no repo de fulfillment. O `README.md` de la
  mapeia as 6 fases e o inventario script a script; o codigo do lote 1 esta em
  `bling_fiscal/coautoria/_origem_scratchpad_22jul/`.

## c. PASSO A PASSO

**Fonte:** planilha Google Sheets id `${RESOURCE_ID}`, aba gid
`${RESOURCE_ID}`. Dados a partir da linha 33.

Mapa de colunas:
- A = STATUS | **B = rastreio** | F = nome | G = whatsapp | I = total de exemplares | J = CPF
- K-Q = endereco (K = estado por extenso, converter para sigla; Q = CEP)
- R = peso | S = valor do frete | T = valor dos adicionais (SO tratar como adicional se U > S;
  senao T apenas repete o frete) | H = adicionais em texto livre

### c.0 Selecao: STATUS = "PF" (pago) E coluna B (rastreio) VAZIA

O criterio de selecao e **STATUS=PF + coluna B vazia**. Isso nao mudou.

> **SUPERADO em 29/07/2026 09:14** o que esta escrito neste bloco de citacao. Fica registrado porque
> explica o historico e porque os leitores antigos pedem escopo `readonly` de proposito:
>
> ~~"A planilha NUNCA teve write-back automatico. A coluna B sempre foi preenchida a mao pela Jane
> (`janebrunelli`). Nao e que o write-back parou de funcionar: ele nunca existiu. (...) Estado em
> 29/07/2026: a conta `contact@example.invalid` e so leitora da planilha (a dona e
> `contact@example.invalid`), entao escrever na coluna B por API esta bloqueado por ACL."~~
>
> `contact@example.invalid`, e o write-back rodou com sucesso as 09:1x de
> 29/07/2026: **8 celulas gravadas** (`totalUpdatedCells: 8`), confirmadas por releitura independente.
> Ate esse momento, o texto acima era verdadeiro.

**Estado atual (verificado ao vivo 29/07/2026):**

- A planilha `${RESOURCE_ID}`, aba `Respostas ao formulário 1`, tem
  **`canEdit: true` para a service account** `contact@example.invalid`.
- A conta OAuth de usuario `contact@example.invalid` **continua com `canEdit: false`** nessa planilha.
  Quem ganhou acesso foi a identidade que o dono escolheu compartilhar, nao a que tem o token mais
  amplo. Ver [[learning_google_oauth_usuario_vs_service_account_2807]].
- O write-back roda pela **service account, backend padrao, SEM a flag `--oauth`**. Se alguem rodar
  com `--oauth`, o proprio script barra sozinho na trava de identidade/ACL.
- Como nao depende do OAuth de usuario, o write-back tambem **nao herda a armadilha dos 7 dias** do
  consent screen em "Testes" -> e **automatizavel por cron** nos proximos lotes.

Comando (dry-run primeiro, sempre):

```
python bling_fiscal/coautoria/escrever_rastreios_lote2.py               # dry-run pela SA, nao escreve
python bling_fiscal/coautoria/escrever_rastreios_lote2.py --executar    # escreve pela SA
```

As **6 travas** do script (nao remover nenhuma):

1. so escreve depois de comprovar capacidade de escrita (`capabilities.canEdit` na Drive API no modo SA;
   identidade da conta autorizada no modo `--oauth`);
2. **releitura AO VIVO imediatamente antes de escrever**;
3. **so escreve celula B VAZIA, nunca sobrescreve**;
4. casa por **CPF (coluna J)** contra o lote; divergiu, **aborta tudo**;
5. escreve **somente** as celulas da coluna B listadas no mapa `TRACKS` do lote;
6. releitura de confirmacao depois da escrita.

> **A trava 3 e a mais importante e continua sendo.** A Jane **ainda edita a mesma planilha a mao**:
> automacao e mao humana convivem no mesmo documento. "So escreve celula vazia" e o que impede o robo
> de passar por cima do que a pessoa digitou. Nunca troque por "escreve sempre" nem por "sobrescreve
> se diferente".
>
> O mapa `TRACKS` (linha -> rastreio) do script esta fixo no lote 2 de 28/07. Lote novo = mapa novo.

### c.1 Molde de criacao correto: `recriar.py`, NAO `coaut.py`

**`coaut.py` esta SUPERADO na valoracao.** Ele criava o item com `valor: 0` (bonificacao) e o Bling
**barra na pre-validacao** ("informacoes obrigatorias faltando": item precisa de valor e unidade).
Foi o que custou o retrabalho de 22/07.

Do `coaut.py` aproveita-se **apenas**: (a) a idempotencia por `numeroLoja` e (b) a resolucao de
contato por CPF (acha ou cria). O resto da criacao vem do `recriar.py`.

Molde correto (`recriar.py`, valoracao que passa):

| Campo | Valor |
|---|---|
| `numeroLoja` | `COAUT-<CPF>-<AAAAMMDD>` (recriacao usa sufixo `-R`) |
| item | produto `${RESOURCE_ID}` id `${RESOURCE_ID}`, `unidade: "UN"`, `quantidade` = coluna I, `valor: 15.90`, `desconto: 0` |
| `desconto` do pedido | `{"valor": 15.90 * qtd, "unidade": "REAL"}` = **desconto 100% COM LASTRO** |
| `transporte` | `fretePorConta: "R"`, `frete` = coluna S, `contato: {"id": 0}` (contrato proprio) |
| `parcelas` | 1 parcela = valor do frete, `formaPagamento.id 4744692` |

Resultado: liquido zero no produto, a nota fecha **so no frete**, zero receita declarada.
Excecao historica: o volume anterior usa SKU `${RESOURCE_ID}` id `${RESOURCE_ID}`.

### c.2 Volume Araras ANTES da nota (ordem critica)

Prep interno via worker (`vendasinternal`), com whitelist de campos e **revalidacao lendo de volta**:
1 volume, peso 0,5 kg x exemplares, servico **PAC CONTRATO AG** codigo `03298`,
`idServico ${RESOURCE_ID}`, contato transportadora id `0`. Estrutura de transporte espelhada do pedido
irmao `${RESOURCE_ID}`.

**O volume NAO entra depois da NF** (lock `VENDA_POSSUI_NOTA_FISCAL`: o PUT devolve 200 e descarta o
volume em silencio). Pedido que ja pegou nota errada: cancelar/recriar, nao editar.

### c.3 Piloto de 1 em `--so-prep`, inspecionar, so entao emitir

**Este e o protocolo que fez o lote 2 sair limpo. Nao pule.**

```
python run_lote2.py --linhas <UMA_LINHA> --so-prep
```

O modo `--so-prep` roda contato + pedido + volume e **PARA antes da nota**, deixando o registro em
`PRONTO_PARA_EMITIR`. Inspecionar o pedido nesse estado e conferir, item por item:

- item com `valor 15,90` e `unidade "UN"`
- `desconto` = 15,90 x qtd (**com lastro**: desconto = soma dos itens)
- `totalProdutos` = 15,90 x qtd e **`total` = so o frete**
- 1 volume com `vol_idServico ${RESOURCE_ID}` / `vol_servico "PAC CONTRATO AG"`
- **`notaFiscal: 0`** (ou seja: ainda nao tem nota, da tempo de corrigir)

> **Por que aqui e nao depois:** esta e a **ultima janela em que o erro ainda e reversivel**. Depois da
> nota o volume nao entra mais (c.2) e o conserto vira cancelar/recriar. 30 segundos de inspecao aqui
> economizam o retrabalho inteiro.

### c.4 Emitir, gate, mover

1. **Emitir:** PATCH de situacao para `822234` "Emitir NF (robo)" (transicao `${RESOURCE_ID}`, acao 44
   `gerarNfe`, NF-e modelo 55). Natureza cai na padrao da conta = **Venda `${RESOURCE_ID}`, CFOP 5102**
2. **Polling ate o GATE CONJUNTIVO** (secao d). O lote 2 usou 14 rodadas de 12s.
3. **Auto-remessa:** ao autorizar a NF, a integracao Correios Araras `482825` gera a pre-postagem
   SOZINHA, com rastreio `AP*BR`, servico PAC CONTRATO AG.
4. **Mover** o pedido para `822185` "Pronto para Embalar" (transicao `${RESOURCE_ID}`) = a fila do Thales.
5. **Thales** imprime "DANFE Simplificado + Etiqueta de transporte" (Notas de Saida ate 50, ou bipando
   no Checkout), confere o codigo de barras de 44 digitos, embala, despacha PAC CONTRATO AG, carimba
   Separado (`816880`). POP: `Downloads/POP-coautoria-despacho-thales.pdf`, fonte
   `bling_fiscal/pops/pop_coautoria_despacho.py`.
6. **Rastreio de volta pra planilha:** desde 29/07/2026, **automatico** pela service account
   (`escrever_rastreios_lote2.py`, dry-run e depois `--executar`), com as 6 travas de c.0. Antes disso
   era manual, com a Jane. A mao humana continua valendo como caminho alternativo, e por isso a trava
   "so escreve celula vazia" nao sai.

## d. VERIFICACAO

### Enum de situacao da NF no Bling (a skill `bling` esta incompleta)

| Codigo | Significado |
|---|---|
| 1 | Pendente |
| 2 | Cancelada |
| 4 | Rejeitada |
| **5** | **Autorizada** |
| **6** | **Autorizada** |

**5 E 6 sao autorizada, os dois.** A skill `bling` cita so o 6, o que ja gerou duvida na hora de ler o
resultado. Teste sempre `situacao in (5, 6)`, nunca `== 6`.

### GATE CONJUNTIVO para liberar o lote (as duas condicoes, senao para)

1. **NF autorizada:** `situacao in (5,6)` **E** `chaveAcesso` com 44 digitos **E** no XML
   `cStat == "100"` **E** `nProt` presente (protocolo).
2. **Etiqueta gerada:** volume com `codigoRastreamento` batendo `^AP\w+BR$`.

Falhou qualquer uma: **para o lote**, nao segue no automatico. Situacao de NF em `(2, 4, 9)` = aborta
aquele coautor na hora.

### Prova de que a mercadoria vai circular (nota autorizada NAO e prova de envio)

Casar as pre-postagens por **`numeroPlp`** na integracao **Araras `482825`** e confirmar **situacao 1
"Emitido"**. So isso prova que o objeto entrou de fato. Nota autorizada prova o fiscal, nao a
logistica: ja tivemos nota autorizada com objeto que nunca circulou (ver o incidente do contrato dos
Correios suspenso, em [[learning_contrato_correios_suspenso_credito_2807]]).

Outras verificacoes:
- Pedido em `822185`.
- Prova de entrega da mensagem ao time = DELIVERY_ACK (NAO SERVER_ACK).

## e. PEGADINHAS E ANTI-PADROES

- **Item com vProd = 0 o Bling BARRA na pre-validacao.** Por isso o 15,90 + desconto 100% com lastro.
- **Desconto tem que ser COM LASTRO** (desconto = soma dos itens). Desconto orfao (desconto > soma) a
  SEFAZ rejeita. Ver skill `bling-nf-desconto`.
- **A data entra no `numeroLoja`, entao a trava so vale DENTRO DO MESMO DIA.** A idempotencia real
  esta no **Bling**, no `numeroLoja` = `COAUT-<CPF>-<AAAAMMDD>`, **nao na planilha**. Rodar a MESMA
  linha em outro dia **cria um segundo pedido**, porque o `numeroLoja` muda junto com a data. Antes de
  reprocessar uma linha de outro dia: buscar por `COAUT-<CPF>-` no Bling e conferir o que ja existe.
- **Retry cego em POST/PATCH e perigoso.** Timeout em POST pode significar "**ja criou**". Retentar ali
  duplica pedido ou duplica nota. **Sempre conferir com GET antes de retentar** (por `numeroLoja` no
  caso do pedido, por `notaFiscal.id` no caso da nota). Retry automatico so em GET.
- **CPF invalido na planilha trava o coautor, e NAO se conserta por conta propria.** No lote 2, 2 de 10
  reprovaram no digito verificador. Num deles existia no Bling um contato com **nome identico e CPF
  valido diferente por 1 digito**: **NAO usar**. Casar pessoa por nome e como se emite nota no CPF
  errado. **Escalar para quem tem contato com o coautor (a Layra)** e deixar a linha de fora do lote.
- **Natureza "Remessa em Bonificacao" (`${RESOURCE_ID}`) NAO gruda por API:** o PUT ignora
  `naturezaOperacao` em silencio e o recurso nao tem CRUD (404). So entra pela UI. Por isso emitimos
  como Venda.
- **A integracao Araras `482825` e tipo nativo "Correios"**, entao `POST /logisticas/objetos` (publica)
  NAO serve (so logistica personalizada). A pre-postagem so vem da auto-remessa ao autorizar a NF com
  o volume ja setado.
- **Exposicao do R$ 15,90:** aparece no DANFE completo/XML, mas NAO na consulta publica SEFAZ por chave
  (so o total) e a nota nao tem QR Code.
- **PII:** os artefatos de dados (nome, CPF, telefone, endereco) NAO entram no git. O estado do lote
  grava CPF mascarado e nome curto. Manter assim.

### Resultado real do lote 2 (28/07/2026), como referencia do que e "limpo"

- **8 de 10 emitidos limpo** (2 fora por CPF invalido, escalados).
- Pedidos **93604 a 93611**, NFs **006514 a 006521**, todas **cStat 100**.
- Valoracao de cada uma: **`vProd 238,50` / `vDesc 238,50` / `vNF` = so o frete**
  (15,90 x 15 exemplares, desconto com lastro exato).
- Etiquetas `AP*BR` geradas para as 8.

## f. ROLLBACK

- **NF autorizada errada:** cancelar dentro de 24h via worker bling-headless `/cancelar-nfe`
  (justificativa min 15 chars).
- **NF PENDENTE (nunca autorizada):** NAO cancela nem exclui (trava o pedido para sempre). Quarentena
  o pedido em situacao Verificado (`24`, fallback `12`) e recria com `numeroLoja` de sufixo `-R`.
- **Pedido criado mas prep falhou (sem nota ainda):** da pra consertar no lugar, e o unico estado
  totalmente reversivel. E o motivo do `--so-prep`.
- **Duplicata suspeita:** GET por `numeroLoja` comecando em `COAUT-<CPF>-`. Se houver 2, o extra so
  pode ser cancelado enquanto nao tiver NF autorizada.

## g. CREDITOS



## Adaptacao Codex HAOS

- Carregar `${HAOS_PRIVATE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
