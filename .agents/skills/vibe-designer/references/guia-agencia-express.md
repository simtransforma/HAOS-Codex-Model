# Guia de Design — Agência Express
## Baseado em análise visual de sites reais do portfólio + referências aprovadas

---

## Os 3 Tipos de Página

A agência produz 3 formatos distintos. Cada um tem estrutura, objetivo e lógica de prompt diferente.
**Identificar o tipo correto antes de qualquer prompt é obrigatório.**

---

## TIPO 1 — LANDING PAGE DE CONVERSÃO

**Objetivo:** Uma ação. WhatsApp, formulário ou compra. Nada mais.
**Nichos comuns:** Transporte, serviços locais, saúde, advocacia, cursos, consultoria.
**Medida de sucesso:** Taxa de clique no CTA principal.

### Estrutura obrigatória (ordem exata)

```
1. NAVBAR         → Logo + menu simples + CTA botão (WhatsApp ou "Agendar")
2. HERO           → H1 forte + subtítulo + foto real + CTA principal + trust strip
3. PROBLEMA/DOR   → O que o cliente sente antes de encontrar vocês (1-3 bullets)
4. SOLUÇÃO        → O que vocês fazem de diferente (features com ícone + texto curto)
5. PROVA SOCIAL   → Depoimentos reais + números (clientes, anos, casos)
6. CTA FINAL      → Repetição do CTA principal com urgência ou garantia
7. FOOTER         → Contato + links legais
```

### Regras de design da Landing Page

**H1 — a regra mais importante:**
- NUNCA descreve o serviço. Descreve o resultado ou a transformação.
- Teste: um amigo falaria isso numa conversa? Se não, reescreva.
- Integrar número real quando disponível: "5.500 mulheres já aprenderam"

| ❌ PROIBIDO | ✅ CORRETO |
|---|---|
| "Serviços de Transporte com Qualidade" | "Chegue Descansado. As Dunas Vão Estar Lá." |
| "Advocacia com Excelência e Ética" | "Você Cuida da Sua Vida. A Gente Cuida do Processo." |
| "Soluções de Limpeza Profissional" | "Sua Casa Limpa. Seu Tempo de Volta." |
| "Curso de Crochê Online" | "Aprenda com quem já ensinou + 5.500 mulheres." |

**Paleta por perfil de Landing Page:**

| Nicho | Fundo | Primary | Accent | Tom |
|---|---|---|---|---|
| Serviços locais / transporte / saúde popular | Claro (#FAFAF8) | Verde (#16A34A) ou Azul (#2563EB) | Branco | Acolhedor, próximo |
| Jurídico / advocacia premium | Escuro (#0D1B2A navy) | Dourado (#C9A96E) | Branco | Autoridade, poder |
| Compliance / B2B / consultoria | Escuro (#0A1628) | Verde (#22C55E) | Branco itálico | Institucional, direto |
| Cursos / educação | Claro (#FFFBF5) | Rosa/terracota (#E07B54) ou Índigo (#4F46E5) | Âmbar | Acolhedor, aspiracional |
| Fitness / bem-estar | Escuro (#09090B) ou Claro | Primário forte | Accent vibrante | Energético, motivacional |

**WhatsApp float:** obrigatório em toda landing page.
**Stats no hero:** sempre que o cliente tiver números reais (anos, clientes, casos).
**Foto real de pessoa:** fundador, advogado, médico, professora — humaniza e vende mais que qualquer feature.

### Prompt padrão de Landing Page

```
LANDING PAGE — [Empresa] | [Nicho]
Inherit: design system above.

HERO SECTION
H1: "[headline transformacional — resultado, não serviço]"
Subtitle: "[dor que resolve em 1 frase]"
Photo: [foto do responsável OU do produto/serviço em uso — reta, sem transform]
CTA primary: "Falar no WhatsApp" (FaWhatsapp icon, bg-whatsapp)
CTA secondary: "[ação secundária]" (outline)
Trust strip below CTAs: [ícone] [credencial 1] | [ícone] [credencial 2] | [ícone] [credencial 3]
Stats bar: [N]+ [métrica] | [N]+ [métrica] | [N]+ [métrica]

Mobile order: Badge → H1 → Subtitle → Photo → CTAs (flex-col w-full) → Trust strip

Interactions: CTA primary pulse on load 1x, hover scale(1.02) 150ms
```

---

## TIPO 2 — SITE INSTITUCIONAL

**Objetivo:** Autoridade + credibilidade + conversão de lead qualificado.
**Nichos comuns:** Advocacia, compliance, consultoria B2B, clínicas, imobiliárias, SaaS.
**Diferença da Landing Page:** Mais profundidade, mais seções, múltiplos pontos de contato.

### Estrutura obrigatória

```
1. NAVBAR         → Logo + menu completo + CTA
2. HERO           → H1 de posicionamento + dados/stats + foto de autoridade
3. STATS BAR      → Números de credibilidade (anos, casos, clientes, certificações)
4. SERVIÇOS       → Grid de serviços com descrição (não só ícone)
5. SOBRE/FUNDADOR → Foto + bio + credenciais específicas
6. PROCESSO       → Como funciona (timeline ou steps numerados)
7. CASES/RESULTS  → Resultados reais com contexto
8. CREDENCIAIS    → Certificações, parcerias, prêmios, publicações
9. CTA CONTATO    → Formulário ou WhatsApp com contexto de urgência
10. FOOTER        → Completo com endereço, CNPJ, links
```

### Regras específicas do Institucional

**O diferencial visual obrigatório:** foto do responsável com postura de autoridade no hero.
- Olhar direto para a câmera
- Fundo contextual (escritório, consultório, biblioteca)
- Traje coerente com o mercado-alvo

**Stats bar:** sempre presente antes do scroll. Nunca esconder credenciais.

**Tom de copy:** mais formal que Landing Page, mas ainda humano.
- Evitar "excelência", "qualidade", "comprometimento" — são palavras vazias
- Usar especificidade: "80 processos trabalhistas ganhos em 2024"

**Paleta institucional:**
```
Jurídico premium:    bg:#0D1B2A | primary:#C9A96E | text:#F1F5F9
Compliance/B2B:      bg:#060C1A | primary:#22C55E | accent:italic-green
Clínica/Saúde B2B:   bg:#FFFFFF | primary:#0F4C81 | accent:#E8F4F8
Consultoria corp:    bg:#FFFFFF | primary:#1E40AF | text:#0F172A
```

**Seção "Canal de Denúncias" ou equivalente:** quando existir, posicionar antes do footer.
Cria diferencial imediato em compliance/ESG.

### Prompt padrão de Site Institucional

```
INSTITUTIONAL SITE — [Empresa] | [Nicho]
Inherit: design system above.

HERO
H1 (bold): "[posicionamento — o que fazem diferente]"
H1 accent (italic, primary-color): "[resultado ou proposta de valor]"
Body: "[elaboração em 2 linhas]"
Photo: [responsável em postura de autoridade — reta, sem inclinação]
CTA: "[ação principal]"
Stats: [N]+ [métrica] in [anos] | [N] [certificação] | [ranking/prêmio]

STATS BAR (section after hero, full-width, surface bg)
4 stats: [número grande] + [label] cada

Interactions: stats numbers count-up on scroll-enter, 1.2s ease-out
```

---

## TIPO 3 — E-COMMERCE / LOJA

**Objetivo:** Venda direta + navegação por produto + recorrência.
**Nichos comuns:** Brigadeiros, artesanato, crochê, produtos de limpeza, moda, alimentos.
**Diferença dos outros:** Não tem H1 de transformação — tem produto em destaque.

### Estrutura obrigatória

```
1. TOP BAR        → Frete grátis / promoção / urgência (fundo primary, texto branco)
2. NAVBAR         → Logo + busca + carrinho + menu categorias
3. HERO BANNER    → Produto destaque OU coleção OU oferta sazonal
4. TRUST STRIP    → Pagamento seguro | Entrega rápida | Suporte | Devolução
5. PRODUTOS EM DESTAQUE → Grid 4 colunas (desktop) / 2 colunas (mobile)
6. CATEGORIAS     → Cards visuais com foto + nome da categoria
7. MAIS VENDIDOS  → Carrossel ou grid com badge "Mais Vendido"
8. POPUP CAPTURA  → Email + oferta de desconto (10-15%) no 1º acesso
9. FOOTER         → Categorias + Info + Contato + Políticas + Redes
```

### Regras específicas do E-commerce

**Popup de captura:** obrigatório. Aparece após 3 segundos ou no exit-intent.
- Oferta clara: "Ganhe X% de desconto na primeira compra"
- Campo de email + CTA = 2 elementos apenas, nada mais

**Foto de produto:** nunca usar imagem placeholder. Usar foto real com fundo limpo.

**Grid de produtos:**
- Desktop: 4 colunas, máx
- Tablet: 2-3 colunas
- Mobile: 2 colunas (nunca 1 — desperdiça espaço)

**Preço:** sempre visível, com desconto riscado quando aplicável.

**Paleta por nicho de e-commerce:**
```
Doces/Confeitaria:  bg:#FFF8F0 | primary:#8B2635 (burgundy) | accent:#C9A96E
Artesanato/Crochê:  bg:#FAFAF6 | primary:#8B4513 (terracota) | accent:#E07B54
Limpeza/Higiene:    bg:#FFFFFF | primary:#16A34A (verde) | accent:#FCD34D
Moda/Boutique:      bg:#FAFAF8 | primary:#1A1A1A | accent:#C9A96E
```

**Top bar é obrigatória:** "Frete grátis acima de R$X" ou "Distribuidor oficial na Europa"
— é o primeiro argumento de compra antes de ver qualquer produto.

### Prompt padrão de E-commerce

```
E-COMMERCE — [Loja] | [Nicho]
Inherit: design system above.

TOP BAR
Full-width, bg-primary, text-white, text-sm
Content: "[oferta de frete ou credencial principal]"

NAVBAR
Logo left | Search center (input + icon) | Icons right: Account, Wishlist, Cart (badge counter)
Mobile: Logo + Hamburger + Cart icon only

HERO BANNER
Full-width image (product/collection), overlay gradient bottom-to-top
Headline: "[nome da coleção ou oferta]" — serif or display bold
CTA: "Ver Coleção" or "Aproveitar Oferta"

FEATURED PRODUCTS
Section title: "[categoria em destaque]"
Grid: 4 cols desktop / 2 cols mobile
Product card: image (aspect-ratio:3/4) + name + price + "Adicionar" button
Hover: image zoom scale(1.04) 300ms + "Adicionar" slides up from bottom

POPUP (rendered but hidden, shows after 3s)
Overlay dark, card center, max-w-md
Headline: "Oferta especial para você"
Body: "Cadastre-se e ganhe [X]% de desconto na primeira compra"
Input: email, CTA: "Resgatar Desconto", X to close

Interactions: product card hover zoom 300ms, popup fade-in 400ms after 3s delay
```

---

## Categorização do Portfólio Atual

| Site | Tipo | Nicho | Paleta | Qualidade |
|---|---|---|---|---|
| MVMovelaria | Institucional | Movelaria premium | Bege/marrom/âmbar dark | ⭐⭐⭐⭐⭐ |
| C3 Compliance | Institucional | Compliance B2B | Navy + verde itálico | ⭐⭐⭐⭐⭐ |
| JCEstari (ref) | Institucional | Advocacia premium | Navy + dourado | ⭐⭐⭐⭐⭐ |
| SLZ Transporte | Landing Page | Turismo/transporte | Claro/bege + verde | ⭐⭐⭐ (seções vazias) |
| CrochetandoAmor (ref) | Landing Page + Loja | Curso/e-commerce | Rosa/terracota | ⭐⭐⭐⭐ |
| FischerFios (ref) | E-commerce | Artesanato/crochê | Terrosa/marrom | ⭐⭐⭐ |
| BoraHigienizar (ref) | E-commerce | Limpeza/distribuidora | Verde/branco | ⭐⭐ |
| TXVidros | — | Vidros/alumínio | Não publicado | — |

---

## Padrões que SEMPRE Funcionam (extraídos dos melhores sites)

### 1. Foto de Pessoa no Hero = Conversão
Todos os sites de maior impacto têm foto real do responsável ou do usuário do produto.
Nunca substituir por ilustração ou foto de stock genérica.

### 2. Números no H1 ou Imediatamente Abaixo
`"5.500 mulheres ensinadas"` `"10+ anos"` `"80 casos ganhos"`
Prova social antes do scroll = objeção respondida antes de ser levantada.

### 3. Stats Bar Após o Hero
4 números grandes em linha horizontal (desktop) / 2×2 grid (mobile).
Sempre: número grande (bold, primary) + label pequeno (muted).

### 4. WhatsApp Float Pulsante
Presente em TODA landing page e site institucional.
FaWhatsapp, fixed bottom-right, animação de pulse com ::before e ::after.

### 5. Trust Strip
3-4 ícones + texto curto logo abaixo dos CTAs do hero.
Ex: ✓ Saídas Diárias | ✓ Van Climatizada | ✓ Viagem Segura

### 6. Popup de Captura (E-commerce obrigatório)
Aparece em 3 segundos. Email + desconto. Fecha com X.
É o maior gerador de lista de e-mail sem custo adicional.

---

## O Que NUNCA Fazer

1. **Seções vazias ou com placeholder** — se não tem conteúdo real, não cria a seção
2. **H1 descritivo** — "Empresa X com Qualidade e Atendimento" reprova automático
3. **Foto de van/produto inclinada ou com transform rotate** — sempre reta
4. **Emojis em headings ou CTAs** — zero tolerância
5. **Travessão "—" em textos visíveis** — usar | ou . ou quebra de linha
6. **Slider/carrossel no hero de landing page** — só em e-commerce
7. **CTA "Saiba Mais"** — específico sempre: "Falar no WhatsApp", "Agendar Visita", "Ver Cardápio"
8. **py-32 em qualquer seção** — espaço morto, usar py-20 no máximo
9. **MessageCircle no lugar de FaWhatsapp** — usar sempre react-icons/fa → FaWhatsapp
10. **Foto de AI ou stock óbvia** — foto real ou gradiente CSS puro

---

## Decisão Rápida: Qual Tipo de Página?

```
O cliente quer vender UN produto/serviço específico com 1 CTA?
└─ SIM → LANDING PAGE

O cliente tem portfólio, equipe, processo e quer credibilidade?
└─ SIM → SITE INSTITUCIONAL

O cliente tem múltiplos produtos com preço e carrinho?
└─ SIM → E-COMMERCE
```

Híbridos existem (CrochetandoAmor = Landing + Loja), mas sempre tem um tipo dominante.
Defina o dominante e siga a estrutura dele. Elementos do outro tipo entram como seções, não como arquitetura.
