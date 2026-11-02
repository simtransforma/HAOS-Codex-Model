---
name: competitor-profiling
description: "Use quando o usuário quiser pesquisar, perfilar ou analisar concorrentes a partir das URLs deles. Use também quando ele mencionar 'perfil de concorrente', 'pesquisa de concorrente', 'análise de concorrente', 'perfilar esse concorrente', 'inteligência competitiva', 'mergulho no concorrente', 'quem são meus concorrentes', 'cenário de concorrentes', 'dossiê de concorrente', 'auditoria competitiva' ou 'pesquisar esses concorrentes'. A entrada é uma lista de URLs de concorrentes. A saída são arquivos markdown estruturados de perfil. Alimenta o agente @pesquisador. Para pesquisa de reviews e sentimento em profundidade, veja customer-research."
---

# Perfil de Concorrentes (HAOS)

Você é um analista de inteligência competitiva. Seu objetivo é pegar uma lista de URLs de concorrentes e produzir perfis estruturados e abrangentes, combinando scraping do site ao vivo com dados de SEO e mercado.

> **Tooling HAOS.** Use a skill **firecrawl** (scraping/busca) como ferramenta principal de coleta e a **Brave Search** (API HAOS) para descoberta. Dados de SEO quantitativos (DataForSEO) só se a API estiver disponível; senão, registre como inferência. Esta skill alimenta o agente @pesquisador.

## Avaliação Inicial

**Verifique o contexto de marketing de produto primeiro:**
Se `${USER_PROJECT_ROOT}/.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o legado `product-marketing-context.md`), leia antes de perguntar.

Antes de perfilar, confirme:

1. **URLs dos concorrentes** — a lista a perfilar
2. **Seu produto** — o que você faz (se não estiver no contexto de produto)
3. **Nível de profundidade** — varredura rápida (só fatos-chave) ou perfil profundo (pesquisa completa)
4. **Áreas de foco** — dimensões a priorizar (preço, posicionamento, força de SEO, estratégia de conteúdo)

Se o usuário fornecer URLs e o contexto estiver disponível, prossiga sem perguntar.

---

## Princípios Centrais

### 1. Fatos Acima de Opiniões
Toda afirmação num perfil deve ser rastreável até uma fonte — conteúdo raspado, dados de review ou métricas de SEO. Rotule inferências claramente.

### 2. Estruturado e Comparável
Todos os perfis seguem o mesmo template para comparação lado a lado. Consistência importa mais que completude em um perfil isolado.

### 3. Dados Atuais
Perfis são fotografias. Sempre inclua a data de geração. Sinalize o que parecer velho (ex.: "página de preço atualizada em 2023").

### 4. Avaliação Honesta
Não exagere as fraquezas nem minimize as forças do concorrente. Perfis precisos são úteis.

---

## Salvando Dados Brutos

Antes de sintetizar, persista todos os dados brutos de scrape, SEO e review em disco para reauditoria e reuso sem rodar chamadas caras de novo.

**Layout de diretórios** (relativo à raiz do projeto):

```
competitor-profiles/
├── raw/
│   └── <slug-concorrente>/
│       └── <AAAA-MM-DD>/
│           ├── scrapes/    # um .md por página raspada (homepage.md, pricing.md, ...)
│           ├── seo/        # um .json por chamada de SEO
│           └── reviews/    # um .md ou .json por fonte de review
├── <slug-concorrente>.md   # perfil sintetizado final
└── _summary.md             # resumo entre concorrentes
```

Regras:
- `<slug-concorrente>` em minúsculas, com hífen
- `<AAAA-MM-DD>` é a data da coleta — suporta rerun e diff de fotografias
- Salve cada scrape do Firecrawl como markdown bruto em `scrapes/<nome-pagina>.md`
- Salve cada resposta de SEO como JSON em `seo/<endpoint>.json`
- Salve cada fonte de review em `reviews/<fonte>.md` ou `.json`
- Sempre crie a pasta de data nova num novo run; nunca sobrescreva data anterior

O perfil sintetizado referencia a pasta de dados brutos na seção `## Fontes de Dados Brutos`.

---

## Processo de Pesquisa

### Fase 1: Scraping do Site (Firecrawl)

Para cada URL, raspe páginas-chave para extrair posicionamento, funcionalidades, preço e mensagem.

#### Passo 1: Mapeie o site
Use **Firecrawl Map** para descobrir a estrutura e identificar páginas-chave. Priorize: homepage, página de preço, funcionalidades/produto, sobre/empresa, blog (top-level), clientes/cases, integrações, changelog/novidades.

#### Passo 2: Raspe as páginas-chave
Use **Firecrawl Scrape** em cada página. Salve cada resultado em `competitor-profiles/raw/<slug>/<AAAA-MM-DD>/scrapes/<nome-pagina>.md` antes de extrair campos.

| Página | O que extrair |
|--------|---------------|
| **Homepage** | Headline, subheadline, proposta de valor, CTA principal, prova social, sinais de público |
| **Preço** | Planos, preços, recursos por plano, opções de cobrança, free tier/trial, sinais de enterprise |
| **Funcionalidades** | Categorias, capacidades-chave, como descrevem cada feature |
| **Sobre** | História, tamanho do time, investimento, missão, sede |
| **Clientes** | Clientes nomeados, logos, setores, temas dos cases |
| **Integrações** | Quantidade, integrações-chave, categorias |
| **Changelog** | Velocidade de release, foco recente, direção do produto |

#### Passo 3: Raspe reviews dos concorrentes (opcional, alto valor)
Use **Firecrawl Search/Scrape** para achar páginas de review (BR: Reclame Aqui, Google Reviews; B2B: G2, Capterra). Salve em `reviews/<fonte>.md`. Extraia: nota geral, número de reviews, temas comuns de elogio e reclamação, e 3-5 citações representativas.

---

### Fase 2: Dados de SEO & Mercado

Se a API de SEO (DataForSEO ou equivalente) estiver disponível, colete inteligência quantitativa e salve cada resposta bruta em JSON em `seo/`. Métricas: autoridade de domínio e backlinks, keywords orgânicas e tráfego estimado, posicionamento competitivo (concorrentes orgânicos próximos, páginas de maior tráfego). Se não houver API, marque como inferência baseada no que foi raspado.

---

### Fase 3: Síntese
Combine conteúdo raspado com dados de SEO. Cruze afirmações (se eles dizem "10.000 clientes", veja se o tráfego/backlinks suportam essa escala).

---

## Formato de Saída

### Estrutura do Documento de Perfil

Gere um markdown por concorrente em `competitor-profiles/`.

**Nome do arquivo**: `competitor-profiles/[nome-concorrente].md`

**Para os templates completos de perfil e resumo**: veja [references/templates.md](references/templates.md)

Cada perfil segue:

```markdown
# [Nome do Concorrente] — Perfil de Concorrente

**URL**: [site]
**Gerado**: [data]
**Profundidade**: [varredura rápida / perfil profundo]

## Visão Geral
| Métrica | Valor |
|---------|-------|
| Slogan | [da homepage] |
| Fundação | [ano] |
| Sede | [local] |
| Tamanho do time | [estimativa] |
| Investimento | [se conhecido] |
| Rank de domínio | [SEO] |
| Tráfego orgânico est. | [mensal] |
| Domínios de referência | [contagem] |
| Keywords orgânicas | [contagem] |

## Posicionamento & Mensagem
**Proposta de valor principal**: [headline + subheadline]
**Público-alvo**: [com base na análise de copy]
**Ângulo de posicionamento**: [ex.: "simplicidade", "enterprise", "tudo-em-um"]
**Temas-chave de mensagem**: [com fonte]

## Produto & Funcionalidades
### Capacidades centrais
### Diferenciadores notáveis
### Integrações
### Sinais de direção do produto

## Preço
| Plano | Preço | Inclusões-chave |
|-------|-------|-----------------|
**Cobrança**: [mensal/anual, desconto]
**Teste grátis**: [sim/não, duração]
**Notável**: [peculiaridades de preço]

## Clientes & Prova Social
**Clientes nomeados** / **Setores** / **Temas de case** / **Notas de review**

## SEO & Estratégia de Conteúdo
**Força orgânica** / **Top páginas orgânicas** / **Sinais de estratégia** / **Perfil de backlinks**

## Forças & Fraquezas
### Forças (com fonte)
### Fraquezas (com fonte)

## Implicações Competitivas para [Seu Produto]
**Onde eles são fortes vs. nós** / **Onde somos fortes vs. eles** / **Oportunidades** / **Ameaças**

## Fontes de Dados Brutos
- Homepage raspada: [data]
- Página de preço raspada: [data]
- Dados de SEO: [data]
- Dados de review: [data, fontes]
```

---

### Documento de Resumo

Após perfilar todos, gere `competitor-profiles/_summary.md` com:
1. **Visão do cenário** — um parágrafo resumindo o campo competitivo
2. **Tabela de comparação** — métricas-chave lado a lado
3. **Mapa de posicionamento** — onde cada um se situa (simples↔complexo, barato↔premium)
4. **Principais conclusões** — 3-5 observações estratégicas
5. **Lacunas e oportunidades** — onde o mercado está mal atendido

---

## Varredura Rápida vs. Perfil Profundo

### Varredura Rápida (mais rápida, menor custo)
- Scrape: só homepage + preço
- SEO: visão de rank de domínio + resumo de keywords
- Pula: reviews, stack, detalhes de backlink
- Saída: perfil abreviado

### Perfil Profundo (abrangente)
- Scrape: todas as páginas-chave + sites de review
- SEO: análise completa de backlink + keywords + descoberta de concorrentes
- Inclui: stack tecnológico, estratégia de conteúdo, mineração de review
- Saída: template completo

Default: **varredura rápida**, salvo se o usuário pedir profundo ou tiver poucos concorrentes (3 ou menos).

---

## Lidando com Múltiplos Concorrentes

1. **Paralelize o scraping** — raspe todas as homepages ao mesmo tempo, depois as páginas de preço, etc.
2. **Use métricas consistentes** — as mesmas métricas para todos
3. **Construa o resumo por último**
4. **Priorize por relevância** — com 10+ concorrentes, sugira os top 5 primeiro

---

## Atualizando Perfis

- Cheque páginas de preço primeiro (mais voláteis)
- Repuxe métricas de SEO
- Escaneie o changelog por mudanças de produto
- Atualize a data "Gerado"
- Note o que mudou numa seção `## Histórico de Mudanças` no fim

---

## Perguntas Específicas da Tarefa

Só pergunte se não respondido pelo contexto:
1. Que URLs de concorrente devo perfilar?
2. Varredura rápida ou perfil profundo?
3. Dimensões específicas a focar (preço, SEO, posicionamento)?
4. Devo comparar os achados com seu produto?

---

## Skills Relacionadas

- **customer-research**: para minerar reviews e sentimento de comunidade em profundidade
- **content-strategy**: para usar lacunas de conteúdo do concorrente
- **seo-optimizer**: para auditar seu próprio site relativo aos concorrentes
- **ads**: para analisar estratégias de anúncio do concorrente
- **firecrawl**: ferramenta de scraping/busca usada por esta skill

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
