---
name: tiktok-ads-copy-format
description: "Formato de ENTREGA obrigatorio quando o pedido for gerar copies para TikTok Ads (In-Feed Ad, Spark Ad, TikTok Shop Ad). Entrega em 2 blocos separados prontos para colar em massa no TikTok Ads Manager: Bloco 1 = 5 ad texts / descriptions em code blocks separados (max 100 chars cada, ideal 40-80, uma por code block para colar direto), Bloco 2 = 5 display names / brand names em lista numerada (max 40 chars, sem emoji). Objetivo: colar cada bloco direto no campo correspondente do TikTok Ads Manager (que separa Ad text e Display name) sem remontar. Aplique SEMPRE que o pedido for gerar copies para TikTok Ads, anuncios TikTok, criativos TikTok, In-Feed Ad, Spark Ad, TikTok Shop ads, ou variacoes tipo N copies pro TikTok / me da 5 copies TikTok / gera criativo pro TikTok / 5 textos pro TikTok Ads. NAO usar para Meta Ads (usar meta-ads-copy-format), Google Ads (usar google-ads-copy-format), TopView / Brand Takeover (formatos reservados, especificacoes proprias). Esta skill NAO gera a copy: ela define o FORMATO de entrega e delega a geracao ao copy-specialist / ad-creative / copywriting."
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

# TikTok Ads Copy Format (padrao HAOS) - In-Feed Ad

Regra dura: **toda vez que gerar copies para TikTok Ads, entregar em 2 BLOCOS separados** prontos para colar em massa no TikTok Ads Manager. TikTok separa Ad text (descricao/caption) e Display name (brand name / app name) em campos distintos; se entregar em bloco unico ou paragrafo, quem opera tem que remontar na mao, que e exatamente o que essa skill evita.

Casa 1:1 com o formato oficial do In-Feed Ad (fonte: TikTok Ads Help + guias 2026): 100 chars de description + 40 chars de display name, sem emoji no display name, sem `{`, `}` ou `#` na description. Recomendacao pratica: 40-80 chars na description, porque TikTok trunca em "See more" apos 4 linhas no feed mobile e a atencao morre no scroll.

## Quando ativar

Ative quando o pedido for (em qualquer variacao):
- "gera N copies pro TikTok Ads"
- "me da 5 copies do TikTok"
- "quero anuncios pro TikTok"
- "gera criativo de trafego pago TikTok"
- "5 textos pro TikTok Ads Manager"
- "escreve os copies do anuncio X" quando o alvo e TikTok
- "monta a copy do In-Feed"
- "copy pra TikTok Shop ad"

NAO aplique para: Meta Ads (usar `meta-ads-copy-format`, formato 5/5/5), Google Ads (usar `google-ads-copy-format`, formato 15/4/2), TopView / Brand Takeover (formatos reservados premium com especificacoes proprias), Branded Effect / Hashtag Challenge (formato de campanha, nao ad text).

## Regra de entrega (OBRIGATORIA)

**Sempre entregar 2 blocos separados nesta ordem:**

### Bloco 1 - Ad texts / Descriptions (5, max 100 chars, ideal 40-80)
5 textos de anuncio, um por copy, cada um dentro de um **code block markdown separado** (fenced ` ``` `). Numerar 1 a 5. Cada code block permite copiar o texto inteiro com um clique.

### Bloco 2 - Display Names (5, max 40 chars, sem emoji)
5 display names / brand names, numerados 1 a 5, um por linha, em **lista simples** (nao code block por linha, para permitir selecao em massa dos 5 nomes de uma vez).

Se o pedido especificar quantidade diferente (ex: 3 copies, 10 copies), respeitar. O padrao default e 5 porque o teste A/B/C/D/E de criativo TikTok normalmente sobe com 3-5 variacoes por ad group e o algoritmo precisa de volume para calibrar.

## Limites do TikTok Ads In-Feed (validar antes de entregar)

| Campo | Limite tecnico | Limite pratico | Nota |
|---|---|---|---|
| Ad text / Description | 100 chars latinos (50 asiaticos) | 40-80 chars | TikTok mostra 4 linhas antes de "See more". Passou disso, trunca no feed mobile. |
| Display name / Brand name | 40 half-width chars | 20-30 chars | Emoji NAO permitido. Aparece na parte de cima do anuncio junto com o CTA. |
| Caracteres proibidos na description | `{`, `}`, `#` | - | TikTok rejeita a subida do anuncio se aparecer. |
| Emoji na description | Permitido | Uso com peso | Emoji funciona bem no TikTok (nativo do feed), mas nao encher. |
| Emoji no display name | PROIBIDO | - | Falha na aprovacao. |

**Regra:** se algum item PASSAR do limite ou usar caractere proibido, marcar visualmente no output (ex: `(105 chars - PASSOU 5, cortar)` ou `(usa # - PROIBIDO, remover)`). NUNCA truncar em silencio.

## CTA de botao

O botao do anuncio TikTok e escolhido no Ads Manager (nao vai no texto). Opcoes comuns:
- `Shop Now` (Comprar agora)
- `Learn More` (Saiba mais)
- `Sign Up` (Cadastre-se)
- `Download` (Baixar)
- `Watch Now` (Assistir)
- `Contact Us` (Fale conosco)
- `Order Now` (Peca agora)
- `Get Quote` (Solicitar orcamento)
- `Book Now` (Reservar)

Se o pedido nao especificar, sugerir o CTA no final da entrega (uma linha, formato `CTA sugerido: Shop Now - motivo: ...`). Nao dar como fato: o operador decide.

## Regras de forma (herdam do HAOS)

- **PT-BR sempre** (a menos que o brief diga outro idioma).
- **ZERO em-dash (U+2014), en-dash (U+2013), reticencia unicode (U+2026), aspas curvas duplas (U+201C U+201D) e aspas curvas simples (U+2018 U+2019).** So hifen simples ASCII, tres pontos separados (`...`), aspas retas ASCII e acentos PT-BR normais. Regra global `rule_no_emdash` na memoria.
- **Sem clichê / cara de IA.** Aplicar heuristica da skill `escrita-ptbr` (evitar gerundismo, translationese, formalismo).
- **Voz da marca.** Se o brief citar marca do grupo (SIM, EdsonBurger, HAU, Editora Mindset), respeitar tom da IDENTITY (skill `identity` no RAG-SIM).
- **Front-load do gancho.** Primeiros 40 chars precisam segurar o scroll. TikTok e feed vertical rapido; se o gancho vem na segunda linha, morreu.
- **1 ideia central por copy.** Nao empilhar 3 promessas em 100 chars - nao cabe e vira ruido.
- **Variar angulo.** As 5 copies devem cobrir 3+ angulos distintos (dor / desejo / prova / curiosidade / autoridade / urgencia / trend / ugc). Se as 5 forem variacao verbal do mesmo angulo, o teste morre.
- **Voz nativa do TikTok.** Copy TikTok tem cara de conversa, nao de outdoor. Evitar "revolucionario", "transformador", "descubra o segredo". Preferir "olha isso", "voce nem imagina", "testei e", "por que ninguem contou que", "pov:".
- **Display name curto.** 20-30 chars roda melhor. Nome longo compete com o gancho.
- **Sem emoji no display name (proibido).** Emoji na description ok, com peso.
- **Sem hashtag na description (proibido).** Hashtag vive na descricao organica do Spark Ad ou em outros campos; no Ad text pago, TikTok rejeita.

## Formato exato de saida (template)

````
## Copies TikTok Ads - <nome do produto/campanha>
Publico: <segmento>
Formato: In-Feed Ad (ou Spark Ad / TikTok Shop Ad, se aplicavel)
CTA sugerido: <BOTAO> (motivo)

### Bloco 1 - Ad Texts (5, max 100 chars)

**Copy 1** (<X> chars)
```
<ad text 1>
```

**Copy 2** (<X> chars)
```
<ad text 2>
```

**Copy 3** (<X> chars)
```
<ad text 3>
```

**Copy 4** (<X> chars)
```
<ad text 4>
```

**Copy 5** (<X> chars)
```
<ad text 5>
```

### Bloco 2 - Display Names (5, max 40 chars, sem emoji)

1. <display name 1> (<X> chars)
2. <display name 2> (<X> chars)
3. <display name 3> (<X> chars)
4. <display name 4> (<X> chars)
5. <display name 5> (<X> chars)

### Angulos usados (auditoria)
- Copy 1: <angulo> (ex: dor / desejo / prova / autoridade / curiosidade / urgencia / trend / ugc)
- Copy 2: <angulo>
- ...
- Chars proibidos verificados: ok (nenhum `{`, `}`, `#` na description; nenhum emoji no display name)
````

## Exemplo completo (ficticio, produto: app de meditacao)

````
## Copies TikTok Ads - MindQuiet App (aquisicao frio)
Publico: 25-40, ansiedade / sono ruim / trabalho remoto
Formato: In-Feed Ad
CTA sugerido: Download - app pede instalacao antes de uso

### Bloco 1 - Ad Texts (5, max 100 chars)

**Copy 1** (78 chars)
```
Passei 2 anos com insonia. Baixei esse app na semana passada. Durmo em 8 minutos.
```

**Copy 2** (68 chars)
```
Meditacao que voce faz enquanto lava a louca. Sem sentar em posicao chique.
```

**Copy 3** (89 chars)
```
Se voce trabalha home office e ta ficando com pavio curto, testa 5 minutos disso aqui.
```

**Copy 4** (72 chars)
```
Ansiedade nao passa com "respire fundo". Passa quando o cerebro para.
```

**Copy 5** (63 chars)
```
Baixaram 400 mil em 2 meses. So o Brasil. Nao e por acaso.
```

### Bloco 2 - Display Names (5, max 40 chars, sem emoji)

1. MindQuiet - App do Sono (22)
2. MindQuiet Meditacao (19)
3. MindQuiet BR (12)
4. App MindQuiet (13)
5. MindQuiet - Calma em 5min (24)

### Angulos usados (auditoria)
- Copy 1: dor + resultado + prova pessoal (UGC voice)
- Copy 2: quebra de objecao (nao precisa de setup)
- Copy 3: dor especifica de nicho (home office) + convite
- Copy 4: contra-narrativa (respire fundo nao resolve)
- Copy 5: prova social (400 mil downloads)
- Chars proibidos verificados: ok (nenhum `{`, `}`, `#` na description; nenhum emoji no display name)
````

## Como o operador usa a entrega

1. Copiar cada code block do Bloco 1 -> colar no campo Ad text de cada anuncio no TikTok Ads Manager (ou API `ad_text` se subir programaticamente).
2. Copiar as 5 linhas do Bloco 2 -> ir em cada anuncio e colar 1 display name por anuncio no campo Display name / Brand name (rotacao pareada com o Ad text da mesma posicao, ou mix livre a criterio do operador).
3. Setar CTA na interface do Ads Manager (nao vai no texto).
4. Se for Spark Ad (post organico impulsionado), a legenda do post organico vem do post original; ainda assim, os 5 ad texts podem virar overlay de video / hook variantes / descricoes B-roll.

## TikTok Shop Ad - notas

Se o pedido for TikTok Shop Ad (Video Shopping Ad ou LIVE Shopping Ad), o formato de copy segue o mesmo padrao (100 chars description + 40 chars display), MAS o produto vem do catalog e o CTA e fixado em `Shop Now`. O foco muda para:
- Preco explicito no Ad text quando cabe (helpful com o feed comercial).
- Menos storytelling, mais oferta / urgencia / prova.
- Display name = nome curto da loja (nao do produto).

Nao muda a estrutura da skill, so o tom.

## Relacionadas

- `copywriting`: frameworks classicos (AIDA / PAS / FAB). Use para ESCREVER a copy.
- `ad-creative`: geracao em escala e iteracao com dados. Complementar; use para gerar variacao / iterar.
- `escrita-ptbr`: qualidade de PT-BR, remocao de cara de IA. Roda como ultimo passe antes de entregar.
- `meta-ads-copy-format`: irma para Meta Ads. Formato 5/5/5.
- `google-ads-copy-format`: irma para Google Ads. Formato 15/4/2.
- `tiktok-creative-playbook`: como PENSAR criativo TikTok (roteiro, gancho, ritmo, formato). Roda ANTES da copy.
- `tiktok-ads-fundamentals`: fundamentos operacionais do TikTok Ads Manager (estrutura de campanha, target, otimizacao). Contexto.
- `tiktok-shop-sim`: se o produto for TikTok Shop do grupo SIM (usuario), puxa integracao. Contexto de operacao.
- `marketing-psychology`: gatilhos mentais que sustentam os angulos.

## Delegacao HAOS

Quando ativada, o main HAOS deve delegar a geracao a **@copy-specialist** com brief que inclua:
- Contexto do produto (materia-prima: video de referencia, pagina, oferta, print de tela)
- Publico / momento de consciencia
- Formato do anuncio (In-Feed / Spark / TikTok Shop)
- CTA desejado (ou "sugerir")
- Voz da marca (se marca do grupo)
- Tom (UGC / testemunho / comercial / dinamico)
- Instrucao explicita: **entregar no formato de 2 blocos desta skill (5 ad texts + 5 display names)**
- Restricao: nao usar `{`, `}`, `#` na description; nao usar emoji no display name.

O output do @copy-specialist deve seguir 100% o template acima. Se nao seguir, o main devolve pedindo reformatacao antes de mostrar.

## Validacao antes de entregar

Checklist obrigatorio (o agente ou o main confere):
1. 2 blocos separados presentes?
2. Bloco 1 tem 5 ad texts, cada um em code block proprio?
3. Bloco 2 tem 5 display names em lista numerada?
4. Contagem de chars marcada em cada item?
5. Nenhum ad text > 100 chars? Nenhum display name > 40 chars?
6. Zero `{`, `}`, `#` no ad text?
7. Zero emoji no display name?
8. Zero em-dash / en-dash / reticencia unicode / aspas curvas?
9. 3+ angulos distintos entre os 5 ad texts?
10. Gancho nos primeiros 40 chars em cada ad text?
11. Auditoria de angulos ao final?
12. CTA sugerido (se nao foi dado)?
13. PT-BR sem cara de IA?

Se qualquer item falhar, corrigir antes de mandar.


## Adaptacao Codex HAOS

- Carregar `${USER_WORKSPACE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nao executar push, deploy, publicacao, mensagem, gasto, servidor ou infraestrutura externa sem OK explicito do usuario.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.
