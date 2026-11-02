---
name: sim-dash
description: "Gerar a dashboard SIM-Dash de vendas consolidadas multi-plataforma de um periodo (dia, ontem, intervalo). Processo ponta-a-ponta: extracao paralela das plataformas (Assiny via webhooks n8n, LIA EdTech, Bling/Yampi/TikTokShop, Eduzz, Hotmart, Asaas), consolidacao com dedupe cross-plataforma, build do HTML self-contained com a identidade SIM-Dash (azul #1E9BF0 + navy #1B2A3A, toggle claro/escuro, Chart.js) e deploy idempotente no Hetzner (container dados-view). Acione quando o usuario pedir \"vendas de hoje/ontem/do periodo\", \"dash de vendas\", \"atualiza a SIM-Dash\", \"fechamento de vendas\", \"quanto vendeu\", \"consolida as vendas\", \"relatorio de vendas consolidado\" ou variacoes. NUNCA expor credenciais; ler nomes de variavel do ${USER_SECRET_FILE}."
---

## Contrato publico de execucao

Material de dominio portado da fonte real, nao uma instalacao de infraestrutura.
As regras do usuario e do AGENTS.md prevalecem sobre comandos e exemplos abaixo.
Publicar, enviar, gastar, alterar servidores, reiniciar, apagar, push e merge
exigem consentimento explicito para o destino e a acao. Nao executar comandos
com placeholders. Nao buscar o cofre ou ambientes do autor. Ferramentas/MCPs
citados precisam existir na instalacao do usuario; nomes nao provam acesso.
Consulte [PORTABILITY.md](PORTABILITY.md) para dependencias, recursos omitidos,
licencas e adaptacoes. Exemplos preservados nao sao prova de estado vivo.

# SIM-Dash (dashboard de vendas consolidadas multi-plataforma)

Processo ponta-a-ponta para fechar as vendas de um periodo das marcas SIM / usuario / HAU / Editora Mindset e publicar a dashboard SIM-Dash. Tudo SINCRONO. Sem
`run_in_background`.

> Objetivo: dado um periodo (dia, ontem, intervalo de datas), extrair as vendas
> PAGAS de todas as plataformas, deduplicar os espelhos cross-plataforma,
> consolidar na hierarquia PLATAFORMA > OFERTA > UTM e publicar uma dashboard
> visual unica em https://service.example.invalid

## Guardrails (ler primeiro)

- NUNCA imprimir, citar, mascarar ou commitar segredos: API keys, tokens, Bearer,
  senhas, headers de auth. Usar `${USER_SECRET_FILE}` apenas como FONTE. So referenciar
  NOMES de variavel.
- Caminho do ${USER_SECRET_FILE} (local Windows):
  `${USER_WORKSPACE_ROOT}`
- Endpoints e formato de cada API estao no TOOLS.md (workspace HAOS). Conferir la
  antes de chamar.
- So contar vendas **PAGAS / aprovadas / RECEIVED / CONFIRMED**. Pendentes,
  reembolsos e chargebacks vao SEPARADOS (nao somar no total).
- **"Eu Quero" NAO e plataforma.** Foi mal-entendido uma vez (e comeco de frase, nao
  gateway). Nao procurar plataforma com esse nome.
- SEM travessao (`—`) em nenhum lugar: copy, codigo, comentarios, rodape da dash.
  Vale tambem para `–`, `…`, aspas curvas e apostrofo curvo.
- A dash e INTERNA: **NAO incluir GTM** nem qualquer pixel/tracking.
- Tudo sincrono. Nao usar background.

## Roteamento de especialistas

- `dev-backend`: extracao das APIs, scripts de probe, parser de webhooks n8n, dedupe.
- `data-analyst` / `bi-engineer`: consolidacao, regras de dedupe, sanity-check de totais.
- `dev-frontend` / `designer`: build do HTML SIM-Dash, identidade visual, charts, toggle tema.
- `devops`: deploy no Hetzner (container `dados-view`), via skill `haos-hetzner-map`.

## Visao geral das 4 fases

1. **Extracao** multi-plataforma (paralela) das vendas pagas do periodo.
2. **Consolidacao + dedupe** cross-plataforma; hierarquia PLATAFORMA > OFERTA > UTM.
3. **Build** do HTML SIM-Dash self-contained (identidade, charts, toggle tema).
4. **Deploy** idempotente no Hetzner (scp pro `dados-view`, verificar 200).

---

## Fase 1: Extracao multi-plataforma (paralela)

Puxar so vendas **pagas/aprovadas** do periodo. Rodar as plataformas em paralelo
(varios agentes ou chamadas concorrentes), cada uma devolvendo uma lista normalizada
de vendas: `{plataforma, oferta, utm_source, utm_medium, utm_campaign, valor,
email, telefone, datahora, id, status, base_valor}`.

### Conversao de fuso (CRITICO antes de filtrar por periodo)

As APIs trabalham em UTC ou no fuso da conta. O periodo do usuario e sempre BRT
(America/Sao_Paulo, UTC-3). Converter as bordas do periodo antes de filtrar para
nao vazar nem perder vendas:

- Inicio do dia D em BRT `D 00:00:00` = `D 03:00:00 UTC`.
- Fim do dia D em BRT `D 23:59:59` = `D+1 02:59:59 UTC`.
- Ex.: dia 09/06 fechado em BRT = de `2026-06-09T03:00:00Z` ate `2026-06-10T02:59:59Z`.

Documentar no rodape qual fuso foi usado para o corte.

### Plataformas e como puxar

| Plataforma | Fonte | Auth (nome da var) | Filtro de status | Base do valor |
|---|---|---|---|---|
| **Assiny** | Sem API de vendas. Historico de **webhooks no n8n** | `N8N_API_URL` + `N8N_API_KEY` | paga/aprovada no payload | **liquido produtor** |
| **LIA EdTech** | `external-api.lia.com.br/external_api/v1` | Bearer (var LIA no MASTER) | paga/aprovada | ver alerta abaixo |
| **Bling** (ERP v3) | API v3 OAuth | OAuth Bling (vars no MASTER) | pedido pago | **pago pelo cliente** |
| **Eduzz** | API Eduzz | OAuth/token Eduzz | aprovada/paga | conforme retorno |
| **Hotmart** | API Hotmart | OAuth client credentials | APPROVED/COMPLETE | conforme retorno |
| **Asaas** | `api.asaas.com/v3` | header access_token (var Asaas) | `RECEIVED` / `CONFIRMED` | **liquido** |

#### Assiny (via webhooks n8n)

1. Listar workflows do n8n (`GET /api/v1/workflows`) e achar o **workflow webhook da
   Assiny** (nome contem Assiny / webhook de venda).
2. Puxar as **executions** do periodo desse workflow:
   `GET /api/v1/executions?workflowId=<id>&includeData=true` e **paginar** via
   `nextCursor` ate esgotar.
3. Extrair do `data` de cada execution o payload do webhook (comprador, valor,
   oferta, UTMs, status). So manter status pago/aprovado.
4. Valor da Assiny = **liquido produtor** (ja descontadas taxas). Sinalizar isso no
   rodape (base mista, ver Fase 2).

#### LIA EdTech (ALERTA de base de valor)

LIA pode reportar dois numeros diferentes. **Documentar qual foi usado e padronizar:**

- **"preco da oferta"** = regime de competencia (valor cheio da oferta no momento da
  venda).
- **"valor pago no dia"** = regime de caixa (o que efetivamente entrou no dia).

Escolher UMA base para o fechamento (default: caixa, "valor pago no dia", pra bater
com Asaas/Assiny que sao liquidos de entrada), e **sinalizar no rodape** qual base a
LIA esta usando. Se houver duvida, mostrar os dois e marcar.

#### Bling (separar subcanal Yampi vs TikTokShop)

- Bling e o ERP e **espelha a Yampi** (todo pedido Yampi vira pedido no Bling). Por
  isso a fonte da venda Yampi e o Bling, e o dedupe remove o lado Yampi cru se
  aparecer em dobro.
- Separar o subcanal pelo **canal/loja do pedido** no Bling:
  - pedidos da loja/canal Yampi -> subcanal **`yampi`**.
  - pedidos da loja/canal TikTok Shop -> subcanal **`tiktokshop`**.
- Valor Bling = **pago pelo cliente** (bruto da venda, antes de taxas de gateway).

#### Asaas (pode ser gateway de outra plataforma)

- Puxar pagamentos `RECEIVED` e `CONFIRMED` em `api.asaas.com/v3/payments` no
  periodo (converter datas pro fuso, paginar).
- Asaas as vezes e o **gateway** por tras de outra plataforma (a venda aparece la E
  na plataforma de origem). Dedupe por **`externalReference`** (id do pedido na
  origem) na Fase 2 para nao contar duas vezes.
- Valor Asaas = **liquido** (valor recebido).

### Saida da Fase 1

Uma lista unica de vendas normalizadas com a coluna `plataforma` e `base_valor`
preenchidas. Guardar tambem os **pendentes/reembolsos** numa lista separada (contagem
e total a parte, nunca no total geral).

---

## Fase 2: Consolidacao + dedupe

### Dedupe cross-plataforma

Remover **espelhos** (mesma venda contada em duas plataformas). Pares conhecidos de
espelho: **Bling <-> Yampi** e **Asaas <-> plataforma de origem**.

Regra de match (uma venda e duplicata de outra se baterem):

1. **id / externalReference** igual (match forte, prioridade maxima); OU
2. **email normalizado** (lower, trim) OU **telefone normalizado** (so digitos, E.164
   BR) iguais, **E**
3. **valor** dentro de tolerancia (~R$ <USER_AMOUNT>absoluto OU 1% relativo), **E**
4. **datahora proxima** (janela de 90 min).

Ao achar duplicata, **manter a plataforma de ORIGEM** (a que realmente processou a
venda) e descartar o espelho:

- Yampi processada via Bling -> manter o registro Bling (subcanal yampi), descartar
  Yampi cru.
- Venda de plataforma X que tambem caiu no Asaas como gateway -> manter X, descartar
  Asaas.

### Hierarquia de saida

Agregar em 3 niveis, com **quantidade** e **R$** em cada nivel, mais subtotais e
**TOTAL GERAL**:

```
PLATAFORMA            qtd   R$ (subtotal plataforma)
  └─ OFERTA           qtd   R$ (subtotal oferta)
       └─ UTM         qtd   R$ (linha folha: utm_source/medium/campaign)
...
TOTAL GERAL           qtd   R$
```

### Bases de valor mistas (sinalizar SEMPRE)

As bases de valor diferem por plataforma e nao sao 100% comparaveis:

- Assiny / Asaas = **liquido**.
- Bling (Yampi/TikTokShop) = **pago pelo cliente** (bruto).
- LIA = caixa ou competencia (ver Fase 1).

Sempre incluir no **rodape da dash** uma nota explicando as bases mistas, para o
total geral nao ser lido como apples-to-apples. Nunca "limpar" essa nota.

### Saida da Fase 2

Objeto `DATA` pronto pro template (totais, hierarquia, pendentes/reembolsos a parte,
notas de base, periodo e fuso).

---

## Fase 3: Build da dash (identidade SIM-Dash)

Ver `./references/build-spec.md` para a especificacao completa de identidade, layout,
tema e estrutura do `DATA`.

Resumo operacional:

- **HTML unico self-contained**, Chart.js via **CDN**, dados **embutidos** no objeto
  `DATA` (nada de fetch externo).
- **Template reutilizavel**:
  `workspace\dev-frontend\out\dash-vendas\sim-dash-template.html`. Para uma nova dash,
  **editar so o objeto `DATA`** (e o periodo/rodape), nao reescrever o HTML.
- Identidade: azul **`#1E9BF0`** + navy **`#1B2A3A`**.
- **Logos**: pasta `${USER_WORKSPACE_ROOT}` (variante **clara** =
  texto navy, para tema claro; variante **escura** = texto branco, para tema escuro).
  Otimizar com **Pillow** e embutir em **base64** no HTML. As logos precisam estar em
  ARQUIVO no disco (anexo de chat NAO serve para embutir).
- **Toggle claro/escuro** com persistencia em `localStorage`, **default dark**, troca
  o logo conforme o tema e **re-renderiza os charts** por tema (cores de eixo/grid).
- **Responsivo** nos breakpoints **920px** e **560px**.
- Regras: **SEM travessao** (`—`), **SEM GTM** (dash interna).

---

## Fase 4: Deploy (Hetzner, idempotente)

> **Carregar a skill `haos-hetzner-map` ANTES** de qualquer acao no servidor.

Infra ja existente (NAO recriar):

- Container **`dados-view`** (imagem `nginx:alpine`), servindo `${USER_SERVICE_ROOT}/resource`.
- **Traefik + TLS** ja configurados.
- URL publica: **https://service.example.invalid
- **DNS Cloudflare proxied** (zona `service.example.invalid`, id
  `${USER_RESOURCE_000027}da850fc3557f0ed8afdc836998e4c11`).

Atualizar a dash = **scp do index.html novo** para `${USER_SERVICE_ROOT}/resource` (NAO
recriar container, NAO mexer em DNS/Traefik). SSH curto e individual (conexao
instavel), chave no ${USER_SECRET_FILE}:

```bash
# enviar o build (caminho da chave no ${USER_SECRET_FILE})
scp -i "<HETZNER_SSH_KEY>" -o StrictHostKeyChecking=no \
  "<build local>/index.html" root@192.0.2.1:${USER_SERVICE_ROOT}/resource
```

### Verificacao (obrigatoria, AGENTS.md §13)

Nunca declarar deploy concluido sem evidencia:

```bash
curl -s -o /dev/null -w "%{http_code}" https://service.example.invalid
# esperar 200
curl -s https://service.example.invalid | grep -o "SIM-Dash" | head -1
# confirmar que o conteudo novo (periodo, total) esta servido
```

Se 200 + conteudo do periodo correto -> deploy OK. Caso contrario, investigar
(cache do nginx, scp no path errado, Traefik) antes de reportar.

---

## Armadilhas e aprendizados (registrar/conferir SEMPRE)

- **Pastas duplicadas no OneDrive**: existe `"Agencia HAU - Soluções Digitais"` (COM
  acento/cedilha) e `"...Solucoes..."` (SEM). Ao gravar ou ler arquivos do projeto,
  considerar os **DOIS** caminhos. Um workflow ja falhou por escrever num e ler do
  outro. Conferir os dois antes de concluir que um arquivo "sumiu".
- **Dia fechado vs fuso**: o erro classico e filtrar em UTC achando que e BRT (ou
  vice-versa), vazando vendas da virada do dia. Converter as bordas (ver Fase 1).
- **"Eu Quero" nao e plataforma.** Nao gastar tempo procurando.
- **Logos so embutem a partir de ARQUIVO no disco** (`sim-dash-logos\`). Anexo de
  chat nao da pra ler/otimizar/base64.
- **So vendas pagas no total.** Pendentes/reembolsos sempre a parte.
- **Bases de valor mistas** por plataforma: nunca apagar a nota do rodape.
- **Dedupe e obrigatorio** (Bling<->Yampi, Asaas<->origem), senao o total infla.
- **Deploy e idempotente**: so scp do index.html; nunca recriar container/DNS.
- Tudo **sincrono**, sem `run_in_background`.

## Checklist de fechamento

- [ ] Periodo convertido BRT -> UTC corretamente nas bordas.
- [ ] Todas as plataformas extraidas (so pagas); pendentes/reembolsos separados.
- [ ] Dedupe cross-plataforma aplicado (espelhos removidos, origem mantida).
- [ ] Hierarquia PLATAFORMA > OFERTA > UTM com qtd + R$ e TOTAL GERAL.
- [ ] Nota de bases mistas no rodape.
- [ ] Build a partir do template (so `DATA` editado), logos base64, toggle tema OK.
- [ ] Zero travessao; sem GTM.
- [ ] scp pro `dados-view`; `curl` 200 + conteudo do periodo confirmado.

