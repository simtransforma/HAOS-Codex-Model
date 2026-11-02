---
name: google-ads-copy-format
description: "Formato de ENTREGA obrigatorio quando o pedido for gerar copies para Google Ads (Responsive Search Ads / RSA). Entrega em 3 blocos separados prontos para colar em massa no Google Ads Editor ou na interface do Google Ads: Bloco 1 = 15 headlines em lista numerada (max 30 chars cada), Bloco 2 = 4 descriptions em code blocks separados (max 90 chars cada, uma por code block para colar direto), Bloco 3 = 2 display paths em lista numerada (max 15 chars cada). Objetivo: colar cada bloco direto no campo correspondente do Google Ads (que separa headline, description e path) sem remontar. Aplique SEMPRE que o pedido for gerar copies para Google Ads, anuncios Google, criativos de rede de pesquisa Google, RSA, Search Ads, campanha Google, ou variacoes tipo N copies pro Google / me da RSA / gera anuncio pro Google Ads / 15 titulos + 4 descricoes. NAO usar para Meta Ads (usar meta-ads-copy-format), TikTok Ads (usar tiktok-ads-copy-format), Display / YouTube / Performance Max (formatos proprios). Esta skill NAO gera a copy: ela define o FORMATO de entrega e delega a geracao ao copy-specialist / ad-creative / copywriting."
---

# Google Ads Copy Format (padrao HAOS) - RSA

Regra dura: **toda vez que gerar copies para Google Ads Responsive Search Ads (RSA), entregar em 3 BLOCOS separados** prontos para colar em massa no Google Ads Editor ou na interface web. Google separa headline, description e display path em campos distintos; se entregar em bloco unico, tabela ou paragrafo, quem opera tem que remontar na mao, que e exatamente o que essa skill evita.

Casa 1:1 com o formato oficial do RSA (fonte: Google Ads Help + guias 2026): 15 headlines de 30 chars + 4 descriptions de 90 chars + 2 paths de 15 chars. Esses limites nao sao capricho: sao o teto tecnico do RSA e o Google recomenda usar TODOS os campos para maximizar Ad Strength e combinacoes de rotacao.

## Quando ativar

Ative quando o pedido for (em qualquer variacao):
- "gera N copies pro Google Ads"
- "me da um RSA"
- "quero anuncios pro Google Ads"
- "gera criativo de rede de pesquisa"
- "15 titulos + 4 descricoes pro Google"
- "escreve os copies do anuncio X" quando o alvo e Google Ads
- "monta a RSA da campanha Y"

NAO aplique para: Meta Ads (usar `meta-ads-copy-format`, formato 5/5/5), TikTok Ads (usar `tiktok-ads-copy-format`), Google Display Ads, YouTube Ads (video assets), Performance Max (asset group misto), Google Shopping (feed de produto).

## Regra de entrega (OBRIGATORIA)

**Sempre entregar 3 blocos separados nesta ordem:**

### Bloco 1 - Headlines (15, max 30 chars cada)
15 headlines, numerados 1 a 15, um por linha, em **lista simples** (nao code block por linha, para permitir selecao em massa dos 15 titulos de uma vez e colar no Google Ads Editor).

### Bloco 2 - Descriptions (4, max 90 chars cada)
4 descriptions, uma por copy, cada uma dentro de um **code block markdown separado** (fenced ` ``` `). Numerar 1 a 4. Cada code block permite colar a description inteira com um clique (descriptions sao mais longas e costumam ter pontuacao delicada, o code block preserva formatacao).

### Bloco 3 - Display Paths (2, max 15 chars cada)
2 display paths, numerados 1 a 2, em **lista simples**. Sao os pedacos que aparecem depois do dominio no URL exibido (dominio.com/path1/path2). Nao precisa ser URL real, e cosmetico.

Se o pedido especificar quantidade diferente, respeitar - mas avisar que menos de 15 headlines e 4 descriptions puxa o Ad Strength para "Poor" ou "Average" e o Google limita a rotacao do anuncio. O minimo tecnico do Google e 3 headlines + 2 descriptions; abaixo disso o anuncio nem sobe.

## Limites do Google Ads RSA (validar antes de entregar)

| Campo | Limite tecnico | Nota |
|---|---|---|
| Headline | 30 chars | Espaco, letra, numero e pontuacao contam 1. Caractere CJK (chines/japones/coreano) conta 2. |
| Description | 90 chars | Mesma regra de contagem. |
| Display path | 15 chars | Cosmetico. Nao precisa existir no site. |
| Headlines por ad | ate 15 | Google recomenda usar TODOS os 15. |
| Descriptions por ad | ate 4 | Google recomenda usar TODAS as 4. |
| Paths por ad | ate 2 | Opcional, mas ajuda relevancia. |
| Minimo para o anuncio subir | 3 headlines + 2 descriptions | Abaixo disso da erro no Editor. |

**Regra:** se algum item PASSAR do limite, marcar visualmente no output (ex: `(32 chars - PASSOU 2, cortar)`). NUNCA truncar em silencio. Se estiver perto (ex: 29 de 30), tambem sinalizar para escolha consciente.

## Pinning (opcional, sinalizar)

Google Ads permite fixar (pin) headline / description em posicao especifica (P1, P2, P3). Uso comum:
- **P1 fixo:** oferta principal / marca (evita rotacao)
- **P2 fixo:** beneficio / prova / gatilho
- **P3 livre:** rotacao total

Se a campanha exigir pinning (ex: nome de marca obrigatorio em P1), o output deve marcar `[P1]` `[P2]` `[P3]` ao lado dos headlines fixados. Se o brief nao pediu pinning, deixar tudo livre e adicionar linha "Pinning: sugerir?" no final para o operador decidir.

## Sitelinks, callouts, structured snippets

RSA e SO o anuncio de texto. Sitelinks (4-6 links extras), callouts (frases curtas) e structured snippets (listas) sao **ad extensions** separados e ficam FORA desta skill. Se o pedido incluir extensions, gerar em bloco separado ao final, com nota "Extensions - opcional".

## Regras de forma (herdam do HAOS)

- **PT-BR sempre** (a menos que o brief diga que a campanha e para outro idioma).
- **ZERO em-dash (U+2014), en-dash (U+2013), reticencia unicode (U+2026), aspas curvas duplas (U+201C U+201D) e aspas curvas simples (U+2018 U+2019).** So hifen simples ASCII, tres pontos separados (`...`), aspas retas ASCII e acentos PT-BR normais. Regra global `rule_no_emdash` na memoria.
- **Sem clichê / cara de IA.** Aplicar heuristica da skill `escrita-ptbr` (evitar gerundismo, translationese, formalismo).
- **Voz da marca.** Se o brief citar marca do grupo (SIM, ${USER_BRAND}, HAU, ${USER_BRAND}), respeitar tom da IDENTITY (skill `identity` no RAG-SIM).
- **1 ideia central por headline.** Nao empilhar 3 promessas em 30 chars - nao cabe e vira ruido.
- **Variar angulo entre os 15 headlines.** Cobrir pelo menos 5 angulos distintos entre os 15 titulos (ex: oferta, beneficio, dor, prova, autoridade, urgencia, marca, palavra-chave, pergunta, garantia). Se os 15 forem variacao verbal do mesmo angulo, o RSA nao rotaciona e o Ad Strength cai.
- **Palavra-chave nos headlines.** No minimo 3 dos 15 headlines devem conter a palavra-chave principal da campanha (ajuda Quality Score e relevancia). Sinalizar quais no bloco de auditoria.
- **CTA em pelo menos 2 descriptions.** Descriptions carregam o CTA. Pelo menos 2 das 4 devem terminar com CTA ativo (`Compre agora`, `Saiba mais`, `Cadastre-se`, `Baixe gratis`, etc.).

## Formato exato de saida (template)

````
## Copies Google Ads RSA - <nome do produto/campanha>
URL final: <https://...>
Palavra-chave principal: <keyword>
Pinning: <nenhum / P1 fixo em headline X / etc.>

### Bloco 1 - Headlines (15, max 30 chars)

1. <headline 1> (<X> chars)
2. <headline 2> (<X> chars)
3. <headline 3> (<X> chars)
4. <headline 4> (<X> chars)
5. <headline 5> (<X> chars)
6. <headline 6> (<X> chars)
7. <headline 7> (<X> chars)
8. <headline 8> (<X> chars)
9. <headline 9> (<X> chars)
10. <headline 10> (<X> chars)
11. <headline 11> (<X> chars)
12. <headline 12> (<X> chars)
13. <headline 13> (<X> chars)
14. <headline 14> (<X> chars)
15. <headline 15> (<X> chars)

### Bloco 2 - Descriptions (4, max 90 chars)

**Description 1** (<X> chars)
```
<description 1>
```

**Description 2** (<X> chars)
```
<description 2>
```

**Description 3** (<X> chars)
```
<description 3>
```

**Description 4** (<X> chars)
```
<description 4>
```

### Bloco 3 - Display Paths (2, max 15 chars)

1. <path 1> (<X> chars)
2. <path 2> (<X> chars)

### Angulos usados (auditoria)
- Headlines 1-3: <angulo> (ex: oferta / beneficio / dor / prova / autoridade / urgencia / marca / pergunta / garantia)
- Headlines 4-6: <angulo>
- Headlines 7-9: <angulo>
- Headlines 10-12: <angulo>
- Headlines 13-15: <angulo>
- Descriptions: <mix de angulos, quais CTAs>
- Palavra-chave "<keyword>" aparece nos headlines: <lista de numeros>
````

## Exemplo completo (ficticio, produto: SaaS de gestao de tarefas)

````
## Copies Google Ads RSA - TaskFlow Pro (campanha marca + generico)
URL final: https://taskflow.exemplo.com/pro
Palavra-chave principal: gestao de tarefas
Pinning: nenhum (rotacao livre)

### Bloco 1 - Headlines (15, max 30 chars)

1. Gestao de Tarefas em 1 App (26)
2. TaskFlow Pro - Teste Gratis (27)
3. Organize Sua Equipe Hoje (24)
4. Kanban, Sprint e Prazo em 1 (27)
5. Chega de Planilha Perdida (25)
6. Time Alinhado em 5 Minutos (26)
7. Gestao de Tarefas Sem Dor (25)
8. 14 Dias Gratis, Zero Cartao (27)
9. Usado por 8.000 Equipes BR (26)
10. Adeus ao Excel de Tarefa (24)
11. Todo Prazo na Mesma Tela (24)
12. Seu Time no Mesmo Ritmo (23)
13. Comece Gratis em 2 Minutos (26)
14. Nota 4,8 na Google Play (23)
15. Gestao de Tarefas Que Funciona (30)

### Bloco 2 - Descriptions (4, max 90 chars)

**Description 1** (87 chars)
```
Sprint, kanban, prazo e time em um so painel. Sem planilha. Teste 14 dias gratis agora.
```

**Description 2** (82 chars)
```
Mais de 8.000 equipes brasileiras ja migraram. Nota 4,8. Sem cartao no cadastro.
```

**Description 3** (89 chars)
```
Do freelancer ao time de 100. Integra com Slack, Google e WhatsApp. Comece hoje mesmo.
```

**Description 4** (76 chars)
```
Cansou de cobrar tarefa por chat? Coloque todo o time em ordem em 5 minutos.
```

### Bloco 3 - Display Paths (2, max 15 chars)

1. TaskFlow (8)
2. Teste-Gratis (12)

### Angulos usados (auditoria)
- Headlines 1-3: oferta + marca + acao
- Headlines 4-6: beneficio (funcionalidade + resultado)
- Headlines 7-9: dor + oferta (14 dias) + prova social
- Headlines 10-12: dor (Excel) + beneficio (visao unica) + resultado (alinhamento)
- Headlines 13-15: acao + prova social (nota) + reforco de categoria
- Descriptions: 1=oferta+CTA / 2=prova+garantia / 3=escalabilidade+integracao / 4=dor+CTA
- Palavra-chave "gestao de tarefas" aparece nos headlines: 1, 7, 15 (3 de 15, OK)
````

## Como o operador usa a entrega

1. Copiar as 15 linhas do Bloco 1 -> colar no campo Headlines do Google Ads Editor (ou na interface, uma por uma). No Editor, o formato de 15 linhas numeradas cola limpo em massa.
2. Copiar cada code block do Bloco 2 -> colar no campo Description 1-4 do anuncio.
3. Copiar as 2 linhas do Bloco 3 -> campo Display path 1 e 2.
4. Se houver pinning marcado, aplicar em cada headline (Editor: menu de pin ao lado do campo).
5. Salvar o anuncio no ad group correto e checar Ad Strength (meta: Excellent ou Good).

## Relacionadas

- `copywriting`: frameworks classicos (AIDA / PAS / FAB). Use para ESCREVER a copy.
- `ad-creative`: geracao em escala e iteracao com dados. Complementar; use para gerar variacao / iterar.
- `escrita-ptbr`: qualidade de PT-BR, remocao de cara de IA. Roda como ultimo passe antes de entregar.
- `meta-ads-copy-format`: irma para Meta Ads. Formato 5/5/5 (primary text + headline + description).
- `tiktok-ads-copy-format`: irma para TikTok Ads. Formato 5 ad texts + 5 display names.
- `marketing-psychology`: gatilhos mentais que sustentam os angulos.
- `haos-google-ads-gtm-api`: acesso a API Google Ads e GTM (audit read-only, MCC, developer token). Nao gera copy; e infra.

## Delegacao HAOS

Quando ativada, o main HAOS deve delegar a geracao a **@copy-specialist** com brief que inclua:
- Contexto do produto (materia-prima: pagina, oferta, VSL, PDF)
- Publico / momento de consciencia
- Palavra-chave principal e secundarias da campanha
- URL final
- Voz da marca (se marca do grupo)
- Pinning obrigatorio? (ex: marca fixa em P1)
- Instrucao explicita: **entregar no formato de 3 blocos desta skill (15 headlines + 4 descriptions + 2 paths)**

O output do @copy-specialist deve seguir 100% o template acima. Se nao seguir, o main devolve pedindo reformatacao antes de mostrar.

## Validacao antes de entregar

Checklist obrigatorio (o agente ou o main confere):
1. 3 blocos separados presentes?
2. Bloco 1 tem 15 headlines em lista numerada?
3. Bloco 2 tem 4 descriptions, cada uma em code block proprio?
4. Bloco 3 tem 2 display paths em lista numerada?
5. Contagem de chars marcada em cada item?
6. Nenhum headline > 30 chars? Nenhuma description > 90 chars? Nenhum path > 15 chars?
7. Zero em-dash / en-dash / reticencia unicode / aspas curvas?
8. 5+ angulos distintos entre os 15 headlines?
9. Palavra-chave principal em pelo menos 3 dos 15 headlines?
10. CTA em pelo menos 2 das 4 descriptions?
11. Auditoria de angulos ao final?
12. Pinning sinalizado (ou "nenhum") no cabecalho?
13. PT-BR sem cara de IA?

Se qualquer item falhar, corrigir antes de mandar.


## Adaptacao Codex HAOS

- Carregar `${HAOS_PRIVATE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
