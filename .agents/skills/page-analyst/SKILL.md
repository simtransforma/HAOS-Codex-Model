---
name: page-analyst
description: "Analista visual de p\u00e1ginas \u2014 recebe URLs, tira screenshots desktop e mobile com Playwright, e usa vis\u00e3o para extrair o que h\u00e1 de bom no design de cada site. Dois modos: REFER\u00caNCIA (analisa sites que voc\u00ea gosta para extrair seu gosto visual) e AUDITORIA (avalia site rec\u00e9m-publicado no Lovable). Triggers: \"analisa esse site\", \"o que tem de bom nesse design\", \"avalia o site publicado\", \"page analyst\", \"analisa essas urls\", \"extrai o estilo desses sites\".\n"
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

# Page Analyst — Visão Visual de Sites

Tira screenshots reais de cada URL via Playwright e analisa o design com visão.
Execução em uma resposta. Sem round-trips.

---

## Modos

**REFERÊNCIA** — URLs de sites que você gosta. Extrai padrões visuais e monta um perfil de gosto.
**AUDITORIA** — URL de site publicado no Lovable. Avalia qualidade vs. brief original.

Se o usuário não especificar, detecte pelo contexto: URLs aleatórias = REFERÊNCIA, URL do Lovable = AUDITORIA.

---

## Fluxo de Execução

### Passo 1 — Criar pasta temporária

```powershell
New-Item -ItemType Directory -Force -Path "$env:TEMP\page-analyst"
```

### Passo 2 — Tirar screenshots de cada URL

Para cada URL recebida, execute **dois comandos** (desktop e mobile):

```powershell
# Desktop (1440x900)
npx playwright screenshot --full-page --browser chromium --viewport-size "1440, 900" --timeout 15000 "[URL]" "$env:TEMP\page-analyst\[slug]-desktop.png"

# Mobile (iPhone 12)
npx playwright screenshot --full-page --browser chromium --device "iPhone 12" --timeout 15000 "[URL]" "$env:TEMP\page-analyst\[slug]-mobile.png"
```

**slug** = nome curto da URL (ex: `stripe` para stripe.com, `site1` para URLs genéricas).

Se um screenshot falhar, tente 1x mais. Se falhar de novo, registre o erro e continue com as demais URLs.

### Passo 3 — Ler todos os screenshots

Use a ferramenta Read para abrir cada arquivo PNG gerado, na ordem: desktop1 → mobile1 → desktop2 → mobile2...

### Passo 4 — Analisar (modo REFERÊNCIA)

Analise todos os screenshots e entregue o relatório nesta estrutura:

---

```
ANÁLISE VISUAL — [N] sites
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Site 1 — [nome/domínio]
Modo:        claro | escuro
Paleta:      [cor dominante] + [accent] — sensação: [adjetivo]
Tipografia:  [serif/sans-serif/display] — peso: [leve/médio/bold]
Layout:      [tipo: hero grande/bento/editorial/minimalista/etc]
Espaçamento: [generoso/denso/equilibrado]
Diferencial: [o que esse site faz que poucos fazem — máx 2 linhas]
Premium:     [elemento específico mais sofisticado que vê]
Mobile:      [ótimo/bom/mediano — por quê em 1 linha]
Replicável:  [1 técnica ou decisão de design que vale copiar]

### Site 2 — [nome/domínio]
[mesma estrutura]

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PERFIL DE GOSTO — Padrões em comum
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tom visual:      [claro/escuro/misto — qual preferem]
Espaçamento:     [generoso/compacto — tendência]
Tipografia:      [sans-serif moderno/serif editorial/display bold]
Elementos recorrentes: [lista das técnicas que aparecem em 2+ sites]
O que NÃO aparece: [o que esses sites evitam — também é gosto]

INSTRUÇÃO PARA O VIBE-DESIGNER:
[3 bullet points diretos: o que aplicar nos próximos projetos com base nesse gosto]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Passo 4 — Analisar (modo AUDITORIA)

```
AUDITORIA — [nome do site]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESKTOP
  Hierarquia:   [clara/confusa — o olho sabe para onde ir?]
  Espaçamento:  [ok/excessivo/insuficiente]
  CTA:          [visível/escondido — onde está, funciona?]
  Tipografia:   [legível/pequena/grande — consistente?]
  Paleta:       [coerente/inconsistente — alguma cor que destoa?]
  Premium:      nota [1-10] — [o que pesa contra e a favor]

MOBILE
  Navbar:       [logo + hambúrguer? drawer funciona?]
  Hero:         [foto antes dos botões? texto legível?]
  CTAs:         [full-width? espaçamento adequado?]
  Leiturabilidade: [ok/fontes pequenas/elementos cortados]

VEREDICTO
  ✅ Aprovado   — [motivo em 1 linha]
  ⚠️ Ajustes   — lista os problemas específicos (elemento + o que mudar)
  ❌ Refazer    — [o que está fundamentalmente errado]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Regras

- **Nunca descreva o que vê de forma genérica** — "bom design" não significa nada. Seja específico: qual elemento, por quê é bom.
- **Se o site não carregar**, registre o erro com a URL e continue.
- **Máximo de URLs por execução:** 5. Acima disso, processe em lotes de 5 e entregue os relatórios em sequência.
- **Limpeza:** após a análise, informe o caminho dos screenshots para o usuário poder apagar: `$env:TEMP\page-analyst\`

---

## Pré-requisito

Playwright deve estar instalado. Para verificar:
```powershell
npx playwright --version
```

Se não estiver: `npm install -D playwright` e depois `npx playwright install chromium`.
