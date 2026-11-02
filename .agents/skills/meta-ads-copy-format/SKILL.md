---
name: meta-ads-copy-format
description: "Formato de ENTREGA obrigatorio quando o usuario pede copies para Meta Ads (Facebook/Instagram). Entrega em 3 blocos separados prontos para colar em massa no Meta Ads Manager: Bloco 1 = 5 textos principais (primary text, um em cada code block), Bloco 2 = 5 titulos (headlines, lista numerada), Bloco 3 = 5 descricoes (descriptions, lista numerada). O objetivo e o usuario copiar e colar cada bloco direto no campo correspondente do Meta Ads Manager (que separa primary text, headline e description) sem precisar remontar. Aplique SEMPRE que o pedido for gerar copies para Meta Ads, anuncios Facebook, anuncios Instagram, criativos de trafego pago Meta, primary text + headline + description para Meta, ou variacoes tipo N copies pro Meta / me da 5 copies / 5 anuncios pro Meta / gera criativo pro Meta. NAO usar para Google Ads (usar ad-creative + specs de RSA), TikTok Ads (usar tiktok-creative-playbook / ad-creative), LinkedIn nem outras plataformas. Esta skill NAO gera a copy: ela define o FORMATO de entrega e delega a geracao ao copy-specialist / ad-creative / copywriting."
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

# Meta Ads Copy Format (padrao HAOS)

Regra durada do usuario: **toda vez que gerar copies para Meta Ads, entregar em 3 BLOCOS separados** prontos para colar em massa no Meta Ads Manager. Meta separa primary text, headline e description em 3 campos distintos; se entregar em bloco unico ou tabela, o usuario tem que remontar na mao, que e exatamente o que essa skill evita.

Casa 1:1 com o `asset_feed_spec` da API Meta (`bodies` + `titles` + `descriptions`, ate 5 de cada), documentado na skill `haos-meta-ads-ops`. A estrutura 5/5/5 nao e capricho: e o teto do multi-texto do Meta.

## Quando ativar

Ative quando o usuario pedir (em qualquer variacao):
- "gera N copies pro Meta"
- "me da 5 copies do Meta Ads"
- "quero anuncios pro Facebook / Instagram / Meta"
- "gera criativo de trafego pago Meta"
- "primary text + headline + description pro Meta"
- "escreve os copies do anuncio X" quando o alvo e Meta

NAO aplique para: Google Ads (RSA usa 15 headlines + 4 descriptions, formato diferente), TikTok Ads (usa `ad-creative` + specs proprios), LinkedIn, outras plataformas de midia paga.

## Regra de entrega (OBRIGATORIA)

**Sempre entregar 3 blocos separados nesta ordem:**

### Bloco 1 - Textos principais (primary text)
5 textos principais, um por copy, cada um dentro de um **code block markdown separado** (fenced ` ``` `). Numerar 1 a 5. Cada code block permite o usuario copiar o texto inteiro com um clique.

### Bloco 2 - Titulos (headline)
5 titulos, numerados 1 a 5, um por linha, em **lista simples** (nao code block por linha, para permitir selecao em massa dos 5 titulos de uma vez).

### Bloco 3 - Descricoes (description)
5 descricoes, numeradas 1 a 5, um por linha, em **lista simples** (mesma logica do Bloco 2).

Se o usuario pedir quantidade diferente (ex: 3 copies, 10 copies), respeitar. O padrao default e 5 porque o Meta aceita ate 5 no `asset_feed_spec`; acima de 5 nao entra em 1 unico ad set multi-texto.

## Limites do Meta (validar antes de entregar)

| Campo | Limite pratico | Limite tecnico | Nota |
|---|---|---|---|
| Primary text | 125 chars visiveis no feed | 2200 chars total | Front-load o gancho nos primeiros 125. Acima disso vira "... Ler mais". |
| Headline | 40 chars | 255 chars | 40 e o recomendado do Meta; acima trunca no feed mobile. |
| Description | 30 chars | 255 chars | 30 e o recomendado; alguns placements omitem description. |

**Regra:** se algum item passar do limite RECOMENDADO, marcar visualmente no output (ex: `(45 chars - sobra 5)`) para o usuario decidir. Nao truncar em silencio.

## CTA de botao

O botao do anuncio Meta e escolhido no Ads Manager (nao vai no texto). Opcoes comuns:
- `SIGN_UP` (Cadastre-se)
- `LEARN_MORE` (Saiba mais)
- `SHOP_NOW` (Comprar)
- `SUBSCRIBE` (Assinar)
- `GET_OFFER` (Aproveitar oferta)
- `DOWNLOAD` (Baixar)
- `CONTACT_US` (Fale conosco)

Se o pedido nao especificar, sugerir o CTA no final da entrega (uma linha, formato `CTA sugerido: SIGN_UP (Cadastre-se) - motivo: ...`). Nao dar como fato: o usuario decide.

## Regras de forma (herdam do HAOS)

- **PT-BR sempre.**
- **ZERO em-dash (U+2014), en-dash (U+2013), reticencia unicode (U+2026), aspas curvas duplas (U+201C U+201D) e aspas curvas simples (U+2018 U+2019).** So hifen simples ASCII, tres pontos separados (`...`), aspas retas ASCII e acentos PT-BR normais. Regra global `rule_no_emdash` na memoria.
- **Sem clichê / cara de IA.** Aplicar heuristica da skill `escrita-ptbr` (evitar gerundismo, translationese, formalismo).
- **Voz da marca.** Se o brief citar marca do grupo (SIM, EdsonBurger, HAU, Editora Mindset), respeitar tom da IDENTITY (skill `identity` no RAG-SIM).
- **1 ideia central por copy.** Nao empilhar 3 promessas em 1 primary text.
- **Variar angulo.** As 5 copies devem cobrir 3+ angulos distintos (dor / desejo / prova / curiosidade / autoridade / urgencia). Se as 5 forem variacao verbal do mesmo angulo, o teste morre.

## Formato exato de saida (template)

```
## Copies Meta Ads - <nome do produto/campanha>
Publico: <segmento>
CTA sugerido: <BOTAO> (motivo)

### Bloco 1 - Primary Text (5)

**Copy 1** (<X chars> visiveis / <Y chars> total)
```
<texto principal 1, com quebra de linha se precisar>
```

**Copy 2** (<X chars> visiveis / <Y chars> total)
```
<texto principal 2>
```

**Copy 3** (<X chars> visiveis / <Y chars> total)
```
<texto principal 3>
```

**Copy 4** (<X chars> visiveis / <Y chars> total)
```
<texto principal 4>
```

**Copy 5** (<X chars> visiveis / <Y chars> total)
```
<texto principal 5>
```

### Bloco 2 - Headlines (5, max 40 chars)

1. <headline 1> (<X> chars)
2. <headline 2> (<X> chars)
3. <headline 3> (<X> chars)
4. <headline 4> (<X> chars)
5. <headline 5> (<X> chars)

### Bloco 3 - Descriptions (5, max 30 chars)

1. <description 1> (<X> chars)
2. <description 2> (<X> chars)
3. <description 3> (<X> chars)
4. <description 4> (<X> chars)
5. <description 5> (<X> chars)

### Angulos usados (auditoria)
- Copy 1: <angulo> (ex: dor / desejo / prova / autoridade / curiosidade / urgencia)
- Copy 2: <angulo>
- ...
```

## Exemplo completo (ficticio, produto: curso de PNL de 4 semanas)

```
## Copies Meta Ads - PNL usuario (aquisicao frio)
Publico: mulheres 35-55, insatisfacao / recomeco
CTA sugerido: LEARN_MORE (Saiba mais) - oferta pede leitura antes de decidir

### Bloco 1 - Primary Text (5)

**Copy 1** (118 chars visiveis / 118 chars total)
```
Voce tenta mudar de vida ha anos e o padrao volta. Nao e falta de esforco. E o codigo que roda dentro. Ele muda em 4 semanas.
```

**Copy 2** (122 chars visiveis / 240 chars total)
```
Se voce ja fez terapia, meditou, tentou de tudo e continua no mesmo ponto: existe uma camada que ninguem tocou.

Nossa turma de 4 semanas mostra qual e e como reescrever. Comeca dia 15.
```

**Copy 3** (109 chars visiveis / 109 chars total)
```
"Em 3 semanas, eu tomei uma decisao que evitava ha 8 anos." - Aline, aluna da turma passada. Vem para a proxima.
```

**Copy 4** (124 chars visiveis / 124 chars total)
```
Metodo desenvolvido em 12 anos com mais de 4.000 alunas. Nao e afirmacao positiva. Nao e coach. E o codigo por tras da decisao.
```

**Copy 5** (98 chars visiveis / 98 chars total)
```
Ultima turma de 2026. Sao 40 vagas. Vinte ja foram nas primeiras 48h. Trava sua no link.
```

### Bloco 2 - Headlines (5, max 40 chars)

1. O padrao volta porque o codigo nao mudou (38)
2. 4 semanas para reescrever o que trava (36)
3. Metodo com 4.000 alunas comprovando (34)
4. "Decidi o que evitei por 8 anos" (31)
5. Ultima turma de 2026 - 20 vagas (30)

### Bloco 3 - Descriptions (5, max 30 chars)

1. Comeca dia 15. Sem retorica. (28)
2. 4 semanas. Metodo com codigo. (29)
3. Prova de 4.000 alunas (21)
4. Historia real, aluna real. (26)
5. So 40 vagas. Metade foi. (24)

### Angulos usados (auditoria)
- Copy 1: dor (padrao volta) + framework proprio (codigo)
- Copy 2: dor de tentativa exaustiva + solucao especifica
- Copy 3: prova social (depoimento aluno)
- Copy 4: autoridade (12 anos, 4.000 alunas, metodo)
- Copy 5: urgencia / escassez (ultima turma, vagas)
```

## Como o usuario usa a entrega

1. Copiar cada code block do Bloco 1 -> colar no campo "Primary text" de cada anuncio (ou no `asset_feed_spec.bodies` da API se subir via `haos-meta-ads-ops`).
2. Selecionar as 5 linhas do Bloco 2 -> colar no campo "Headline" (ou `asset_feed_spec.titles`).
3. Selecionar as 5 linhas do Bloco 3 -> colar no campo "Description" (ou `asset_feed_spec.descriptions`).
4. No Ads Manager, se estiver rodando multi-texto no MESMO ad, colar todas as 5 no ad unico (Meta rotaciona). Se estiver rodando 1 texto por ad (padrao anti-DCO da `haos-meta-ads-ops`), colar 1 copy por ad e replicar os 5 titulos + 5 descriptions em cada.

## Relacionadas

- `copywriting`: frameworks classicos (AIDA / PAS / FAB). Use para ESCREVER a copy.
- `ad-creative`: geracao em escala e iteracao com dados. Complementar; use para gerar variacao / iterar.
- `escrita-ptbr`: qualidade de PT-BR, remocao de cara de IA. Roda como ultimo passe antes de entregar.
- `copy-editing`: passe de revisao dos 7 passes (clareza / voz / e-dai / prove / especificidade / emocao / risco zero). Roda antes de fechar.
- `haos-meta-ads-ops`: OPERACAO (subir campanha via API). Consome o 5/5/5 no `asset_feed_spec.bodies/titles/descriptions`.
- `marketing-psychology`: gatilhos mentais que sustentam os 5 angulos.
- `meta-ads-policy`: se a copy tocar em tema sensivel (saude, financas, promessa de renda), passar por politica antes.

## Delegacao HAOS

Quando ativada, o main HAOS deve delegar a geracao a **@copy-specialist** com brief que inclua:
- Contexto do produto (materia-prima: VSL, PDF, print, pagina)
- Publico / momento de consciencia
- CTA desejado (ou "sugerir")
- Voz da marca (se marca do grupo)
- Instrucao explicita: **entregar no formato de 3 blocos desta skill**

O output do @copy-specialist deve seguir 100% o template acima. Se nao seguir, o main devolve pedindo reformatacao antes de mostrar ao usuario.

## Validacao antes de entregar

Checklist obrigatorio (o agente ou o main confere):
1. 3 blocos separados presentes?
2. Bloco 1 tem 5 primary texts, cada um em code block proprio?
3. Bloco 2 tem 5 headlines em lista numerada?
4. Bloco 3 tem 5 descriptions em lista numerada?
5. Contagem de chars em cada item?
6. Zero em-dash / en-dash / reticencia unicode / aspas curvas?
7. 3+ angulos distintos entre os 5?
8. Auditoria de angulos ao final?
9. CTA sugerido (se nao foi dado)?
10. PT-BR sem cara de IA?

Se qualquer item falhar, corrigir antes de mandar ao usuario.

