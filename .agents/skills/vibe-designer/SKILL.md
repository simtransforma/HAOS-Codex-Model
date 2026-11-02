---
name: vibe-designer
description: "Diretor de cria\u00e7\u00e3o s\u00eanior da Ag\u00eancia Express. Identifica o tipo de p\u00e1gina (Landing, Institucional, E-commerce), aplica o blueprint visual correto extra\u00eddo dos melhores sites do portf\u00f3lio, e gera um prompt \u00fanico completo para o Lovable. Pipeline aut\u00f4nomo: Brief Criativo \u2192 Head de Marketing \u2192 Prompt \u2192 HM \u2192 Publisher. Triggers: \"cria um site para\", \"preciso de landing page\", \"prompt lovable\", \"vibe designer\".\n"
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

# Vibe Designer — Diretor de Criação

Gere tudo em **UMA resposta**. Sem confirmação intermediária. Sem round-trips.

---

## PASSO 1 — IDENTIFICAR O TIPO (obrigatório, antes de tudo)

```
O cliente quer 1 ação (WhatsApp / lead / matrícula)?   → LANDING PAGE
Portfólio + equipe + credibilidade + múltiplos serviços? → SITE INSTITUCIONAL
Múltiplos produtos com preço, categorias, carrinho?      → E-COMMERCE
```

Híbridos existem (ex: curso = landing + loja). Defina o dominante e siga o blueprint dele.

---

## PASSO 2 — BRIEF CRIATIVO (interno — não mostrar ao usuário)

Auto-raciocínio antes de preencher os campos:

```xml
<scratchpad>
  <angulo>O que diferencia de verdade? Não feature — resultado, história, origem ou especificidade.</angulo>
  <h1_teste>Um amigo falaria esse H1 numa conversa informal? Descreve resultado ou serviço?</h1_teste>
  <visual>Quem deve aparecer na foto? Fundador, cliente, produto em uso? O que gera mais confiança?</visual>
  <dado_real>Qual número o cliente tem que valida autoridade? Anos, clientes, cidades, projetos?</dado_real>
  <emocao>Qual emoção domina nos primeiros 3 segundos? Confiança? Alívio? Aspiração?</emocao>
</scratchpad>
```

Responda internamente antes de gerar qualquer linha de prompt:

1. **Ângulo único** — o que diferencia de verdade (propósito, origem, resultado específico, não feature)
2. **Emoção nos 3 primeiros segundos** — uma palavra (confiança / alívio / aspiração / empolgação)
3. **H1 humano** — um amigo falaria isso numa conversa? Descreve resultado, não serviço.
4. **Foto ou visual principal** — quem aparece? (fundador, funcionária, modelo, produto em uso)
5. **Dado real** — que número o cliente tem? (anos, clientes, projetos, cidades, peças vendidas)

| PROIBIDO | CORRETO |
|---|---|
| "Serviços de Limpeza com Qualidade" | "Cuidamos da sua casa como se fosse nossa." |
| "Advocacia com Excelência e Ética" | "Segurança Jurídica para Empresários e Pessoas Físicas." |
| "Soluções em Compliance" | "Compliance não é burocracia. É a base do seu negócio." |
| "Aprenda Crochê Online" | "Aprenda com quem já ensinou + 5.500 mulheres." |
| "Vidros e Alumínio com Qualidade" | "A Vidraçaria que Profissionais da Construção Indicam há 9 Anos." |

---

## PASSO 3 — BLUEPRINT POR TIPO

### BLUEPRINT A: LANDING PAGE DE CONVERSÃO

> Referências internas: DraShiné, CrochetandoAmor, SLZ Transporte, Ilustre Limpezas

**Visual signature:** hero split (texto esquerda, foto direita), fundo claro, foto de pessoa real em ação, formulário ou WhatsApp no final.

**Paleta por nicho:**
```
Limpeza / serviços locais PT:  bg:#FFFFFF  primary:#1D4ED8  accent:#F59E0B
Limpeza / serviços locais BR:  bg:#FAFAF8  primary:#16A34A  accent:#FCD34D
Transporte / turismo:          bg:#FAFAF8  primary:#1D4ED8  accent:#38BDF8
Curso / educação feminina:     bg:#FFF9F4  primary:#C2633A  accent:#FDE68A
Fitness / saúde popular:       bg:#F9FAFB  primary:#16A34A  accent:#84CC16
```

**Estrutura de seções (ordem exata):**
```
1. NAVBAR         → logo + menu simples (3-4 links) + CTA botão
2. HERO           → split 55/45 | texto esquerda | foto pessoa direita
3. TRUST STRIP    → 3-4 ícones lucide + texto curto logo abaixo dos CTAs
4. DIFERENCIAIS   → 3-4 cards (ícone + título + 2 linhas de texto)
5. SERVIÇOS       → grid de cards ou lista por categoria/região
6. PROVA SOCIAL   → depoimentos SOMENTE se texto real disponível; omitir se não houver
7. CTA FINAL      → formulário inline (serviços que qualificam lead) ou WhatsApp (venda rápida)
8. FOOTER         → contato + links legais
```

**Hero — implementação exata:**
```jsx
// HERO SECTION
// Layout: grid grid-cols-1 lg:grid-cols-2 | items-center | gap-12
// LEFT: badge arredondado (bg-primary/10 text-primary text-sm) + H1 + subtítulo + CTAs + trust strip
// RIGHT: foto da pessoa/produto — sempre reta, sem transform rotate, sem skew

// H1: font-bold text-4xl lg:text-5xl leading-tight text-foreground
// H1 com número integrado: "Aprenda com quem já ensinou + 5.500 mulheres."
// H1 com ponto final (serviços locais): "Cuidamos da sua casa como se fosse nossa."

// FOTO: object-cover rounded-2xl | max-h-[480px] w-full
// NUNCA: transform rotate, skew, clip-path agressivo

// CTAs: gap-3 flex-col sm:flex-row
// Primary: bg-primary text-white FaWhatsapp ícone à esquerda
// Secondary: variant="outline" border-primary text-primary
```

**Trust strip — implementação exata:**
```jsx
// flex items-center gap-6 mt-6 flex-wrap
// cada item: flex items-center gap-2
// ícone: lucide-react size=16 className="text-primary"
// texto: text-sm text-muted-foreground
// ex: <Check size={16}/> Atendimento Personalizado
```

**Cards de diferenciais — padrão DraShiné:**
```jsx
// grid grid-cols-2 lg:grid-cols-4 gap-6
// cada card: flex flex-col items-center text-center p-6
// ícone: lucide-react size=32 className="text-primary mb-3"
// título: font-semibold text-sm
// texto: text-xs text-muted-foreground leading-relaxed
```

**Formulário de orçamento — padrão DraShiné:**
```jsx
// seção com bg-surface, padding py-16
// grid grid-cols-1 lg:grid-cols-2 gap-12
// esquerda: texto "Solicite um Orçamento Personalizado" + parágrafo
// direita: form com campos (nome, email, telefone, tipo de serviço, mensagem) + botão submit
// botão: bg-primary text-white w-full
```

---

### BLUEPRINT B: SITE INSTITUCIONAL

> Referências internas: C3 Compliance, JCEstari, MVMovelaria, TXVidros v2

**Visual signature:** split hero com foto de autoridade, headings com italic colorido, stats bar com números grandes, credenciais, processo numerado.

**Paleta por nicho:**
```
Advocacia premium:     bg:#0D1B2A  primary:#C9A96E  text:#F1F5F9  surface:#1a2a3a
Compliance / ESG:      bg:#060C1A  primary:#22C55E  text:#F1F5F9  surface:#0d1a2e
Movelaria / ateliê:    bg:#FAF7F2  primary:#8B6914  text:#1a1208  surface:#F0EAD8
Vidraçaria / construção: bg:#0D1B2A  primary:#94A3B8  text:#F1F5F9  surface:#1a2a3a
Consultoria corp:      bg:#FFFFFF  primary:#1E40AF  text:#0F172A  surface:#F8FAFC
```

**Estrutura de seções (ordem exata):**
```
1. NAVBAR         → logo + menu completo + CTA
2. HERO           → split texto esquerda / foto autoridade direita
3. STATS BAR      → seção separada full-width, 4 números grandes
4. SOBRE/FUNDADOR → foto grande + bio + credenciais específicas
5. SERVIÇOS       → grid com ícone + nome + 2 linhas de descrição
6. CREDENCIAIS    → logos row ou badges com número de registro
7. PROCESSO       → steps numerados (01, 02, 03) com connecting line
8. CANAL/DIFERENCIAL especial (compliance: Canal de Denúncias; outros: garantia ou depoimentos)
9. CTA FINAL      → heading 2 linhas + 1 botão primário
10. FOOTER        → completo (endereço, CNPJ, links)
```

**Hero split — padrão C3/JCEstari (implementação exata):**
```jsx
// Layout: grid grid-cols-1 lg:grid-cols-[3fr_2fr] items-center gap-16
// LEFT COLUMN:
//   badge (optional)
//   H1 em 2 linhas — linha 1 regular, linha 2 italic text-primary
//   subtítulo: 2-3 linhas, text-muted-foreground
//   CTAs: botão primary + botão outline
//   stats inline: N+ | label | N+ | label (flex gap-8 mt-8)
//
// RIGHT COLUMN:
//   <img> da pessoa — object-cover rounded-2xl
//   pessoa olha direto para câmera
//   fundo da foto: contextual (escritório, biblioteca, obra, consultório)
//   traje coerente com o mercado (terno = advocacia/compliance, capacete = construção)
```

**Heading com italic colorido — PADRÃO OBRIGATÓRIO em todo site institucional:**
```jsx
// TODA seção h2 deve seguir este padrão — não só o hero
// Exemplo C3:
<h2 className="text-3xl font-bold text-foreground">Soluções sob medida para</h2>
<h2 className="text-3xl font-bold italic text-primary">governança e integridade.</h2>

// Exemplo JCEstari:
<h2 className="text-3xl font-bold text-foreground">Eficiência, Celeridade</h2>
<h2 className="text-3xl font-bold italic text-primary">e Resultado.</h2>

// Exemplo TXVidros:
<h2 className="text-3xl font-bold text-foreground">Nosso Trabalho</h2>
<h2 className="text-3xl font-bold italic text-primary">Fala Por Nós.</h2>
```

**Stats bar — implementação exata:**
```jsx
// Seção separada: full-width, bg-surface, py-16
// grid grid-cols-2 lg:grid-cols-4 gap-8
// cada stat: flex flex-col items-center text-center
//   número: text-5xl font-bold text-primary tabular-nums
//   label: text-sm text-muted-foreground mt-2
// Sempre acompanhado de frase de contexto acima:
//   "Mais de uma década defendendo quem confia em nós."
```

**Processo numerado — padrão JCEstari:**
```jsx
// flex flex-col lg:flex-row gap-0 relative
// connecting line: absolute horizontal entre steps (border-t-2 border-primary/30)
// cada step: flex flex-col items-center text-center flex-1
//   número: text-4xl font-bold text-primary/30 mb-4 (01, 02, 03)
//   título: font-semibold text-foreground
//   descrição: text-sm text-muted-foreground
```

**Canal de Denúncias (compliance) — padrão C3:**
```jsx
// Seção antes do footer, bg ligeiramente mais clara que o bg principal
// grid grid-cols-1 lg:grid-cols-2 gap-12 items-center
// LEFT: ícone Shield lucide + heading italic + descrição do canal
// RIGHT: CTA card com link para o canal externo ou formulário
```

---

### BLUEPRINT C: E-COMMERCE / LOJA

> Referências internas: LunaFit (padrão ouro), Georgia Brigadeiros, FischerFios, CrochetandoAmor (loja)

**Visual signature:** top bar de oferta, navbar com carrinho, hero produto+modelo, grid 4-col editorial, insert editorial entre grids, newsletter no rodapé.

**Paleta por nicho:**
```
Fitness / moda athleisure: bg:#FAF9F6  primary:#1A1A1A  accent:#C4A882  — editorial bege
Confeitaria / doces:       bg:#FFF8F0  primary:#8B2635  accent:#C9A96E  — burgundy quente
Artesanato / crochê:       bg:#FAFAF6  primary:#8B4513  accent:#E07B54  — terracota
Limpeza / higiene:         bg:#FFFFFF  primary:#16A34A  accent:#FCD34D  — verde/amarelo
Moda / boutique:           bg:#FAFAF8  primary:#1A1A1A  accent:#C9A96E  — minimal luxo
```

**Estrutura de seções (ordem exata):**
```
1. TOP BAR          → full-width primary bg, texto branco, 1 linha de oferta
2. NAVBAR           → logo | categorias | busca + favoritos + carrinho (badge)
3. HERO             → split texto esquerda / produto+modelo direita, bg editorial
4. TRUST STRIP      → 4 ícones: pagamento | entrega | suporte | devolução
5. PRODUTOS EM DESTAQUE → grid 4 cols, aspectRatio 3:4, badges
6. INSERT EDITORIAL → imagem full-width com modelo + frase aspiracional overlay
7. SEGUNDA COLEÇÃO  → grid 4 cols com nome da coleção
8. NEWSLETTER       → seção escura, "Primeira a saber." + email input
9. FOOTER           → preto, categorias + info + políticas
```

**Hero editorial — padrão LunaFit (implementação exata):**
```jsx
// bg: tom bege editorial (--background), NUNCA branco puro
// grid grid-cols-1 lg:grid-cols-[2fr_3fr] items-end min-h-[85vh]
// LEFT (texto, auto):
//   badge coleção: text-xs uppercase tracking-widest text-muted-foreground
//   H1: font-serif text-5xl lg:text-6xl font-bold leading-tight
//   H1 com palavra em italic: "Movimento com <em className='italic font-light'>elegância.</em>"
//   subtítulo: text-sm text-muted-foreground max-w-xs mt-4
//   CTAs: flex gap-3 mt-8 (primary + outline)
//
// RIGHT (modelo):
//   imagem do produto em uso / modelo
//   bg da foto HARMONIZA com o bg do site (bege + modelo bege/nude)
//   sem border, sem sombra — integra com o fundo
//   object-contain (não cover) — produto aparece completo
```

**Grid de produtos — padrão LunaFit:**
```jsx
// grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6
// Product card:
//   div className="group cursor-pointer"
//   <div className="relative overflow-hidden aspect-[3/4]">
//     <img className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-[1.03]" />
//     <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition" />
//     <button className="absolute bottom-0 left-0 right-0 bg-white text-foreground text-sm py-2
//                        translate-y-full group-hover:translate-y-0 transition-transform duration-300">
//       Ver produto
//     </button>
//     {badge && <span className="absolute top-3 left-3 bg-primary text-white text-xs px-2 py-1">Novo</span>}
//   </div>
//   <div className="mt-3">
//     <p className="text-sm text-foreground font-medium">{nome}</p>
//     <p className="text-sm text-muted-foreground mt-1">R$ {preco}</p>
//   </div>
// NUNCA rounded-corners nas imagens — editorial
// NUNCA 1 coluna no mobile — sempre 2 mínimo
```

**Insert editorial — padrão LunaFit:**
```jsx
// Seção entre dois grids de produto
// relative overflow-hidden h-[400px] lg:h-[500px]
// imagem full-width, modelo em uso do produto, ambiente natural
// overlay: gradient from-transparent to-black/40
// texto overlay (canto inferior esquerdo):
//   heading serif italic: "Força é uma forma de cuidado."
//   subtext: 1 linha, text-white/80
//   CTA link: "Explorar coleção →"
```

**Newsletter escura — padrão LunaFit:**
```jsx
// Seção bg-black (ou bg-primary dependendo da paleta) py-20
// text-center max-w-md mx-auto
// heading: text-white font-serif text-3xl "Primeira a saber."
// subtext: text-white/60 text-sm mt-2
// form: flex gap-2 mt-8
//   input: bg-white/10 border-white/20 text-white placeholder-white/40 flex-1
//   button: bg-white text-black font-medium hover:bg-white/90
// NUNCA popup agressivo — esta captura passiva converte melhor
```

---

---

## PASSO 4 — CAMADA DE ADAPTAÇÃO (blueprint → site único)

O blueprint é o esqueleto. O Brief Criativo é a alma. Sem adaptação, todo site fica igual.

**O que é FIXO em cada blueprint (não mudar):**
- Estrutura de seções e ordem
- Grid systems e aspect ratios
- Padrão de heading italic (institucional)
- Hover e microinterações do produto (e-commerce)
- Ordem mobile

**O que ADAPTA a cada briefing:**

| Elemento | Como adaptar |
|---|---|
| **H1** | Nunca reutilizar exemplo do blueprint. Escrever do zero com a voz desta marca específica. |
| **Paleta** | Escolher dentro da faixa do nicho, mas com hue e saturação que reflitam o posicionamento. Premium = mais dessaturado. Popular = mais vibrante. |
| **Seções incluídas** | Só criar seção se o briefing tiver conteúdo real para ela. Sem depoimentos reais → sem seção de depoimentos. Sem portfólio → sem portfólio. |
| **Stats** | Só aparecem se o cliente tiver dados reais. Sem dados → substituir por trust strip de credenciais (ex: "Membro OAB/SP"). |
| **Foto principal** | Quem é a pessoa? Em que contexto? Que emoção transmite? Especificar claramente no prompt. |
| **Frase editorial** | Nos e-commerces, a frase aspiracional do insert editorial deve falar com o público desta marca — não usar genérico. |
| **Nomenclatura das seções** | Trocar títulos de seção pelos termos do universo do cliente. "Nossos Serviços" → "Como Tratamos Sua Casa" (limpeza) / "Áreas de Atuação" (advocacia) / "Nossa Coleção" (moda). |
| **Tom de copy** | Definido pela emoção eleita no Brief Criativo. Alívio = frases curtas, ponto final, respiração. Aspiração = frase longa, ritmo, palavra-chave em italic. Autoridade = dados primeiro, depois narrativa. |

**Exemplos de como o mesmo blueprint produz sites diferentes:**

```
BLUEPRINT B (Institucional) aplicado a 3 briefings diferentes:

Advocacia trabalhista:
  H1: "Seu Processo. Nossa Luta. Desde o Dia Um."
  Paleta: navy #0D1B2A + dourado #C9A96E
  Seções: Hero → Stats (70+ casos) → Sobre Dr. X → Áreas de Atuação → Processo → CTA

Compliance B2B:
  H1: "Compliance não é burocracia."
  H1 italic: "É a base do seu negócio."
  Paleta: navy #060C1A + verde #22C55E
  Seções: Hero → Stats → Sobre Décio → Soluções → Credenciais → Canal de Denúncias → CTA

Vidraçaria premium:
  H1: "A Vidraçaria que Profissionais da Construção Indicam há 9 Anos."
  Paleta: escuro #0D1B2A + prata #94A3B8
  Seções: Hero → Portfólio de obras → Sobre a empresa → Serviços → Depoimentos de engenheiros → CTA
```

---

## FLUXO DO PIPELINE (autônomo)

```
Briefing do usuário
      ↓
Passo 1: Identificar tipo (Landing / Institucional / E-commerce)
      ↓
Passo 2: Brief Criativo interno
      ↓
Head de Marketing avalia o Brief
  REPROVADO → refazer brief
  APROVADO  → gerar prompt completo
      ↓
Head de Marketing avalia o prompt
  REPROVADO → corrigir
  APROVADO  → chefe invoca lovable-publisher
      ↓
Usuário recebe a URL publicada
```

O usuário nunca vê o Brief Criativo, o Diagnóstico nem as avaliações do HM.

---

## STACK TÉCNICA (sempre incluir no início do prompt)

```
npm install lucide-react react-icons framer-motion

Framework: React + Vite (classic), roteamento simples, src/pages/Index.tsx
CSS: Tailwind CSS v4 com tokens semânticos em oklch no index.css
Animações: Framer Motion — reveals on-scroll escalonados
Ícones UI: lucide-react (100% dos ícones de interface)
Ícone WhatsApp: react-icons/fa → FaWhatsapp — único uso de react-icons
```

## TOKENS DE COR (sempre oklch)

**Escuro:**
```css
--background: oklch(12% 0.04 [hue]);
--surface:    oklch(16% 0.05 [hue]);
--foreground: oklch(95% 0.01 [hue]);
--muted-text: oklch(65% 0.06 [hue]);
```

**Claro:**
```css
--background: oklch(99% 0.005 [hue]);
--surface:    oklch(96% 0.012 [hue]);
--foreground: oklch(12% 0.02 [hue]);
--muted-text: oklch(48% 0.05 [hue]);
```

Sempre incluir: `--primary`, `--accent`, `--whatsapp: oklch(62% 0.20 143)`, `--border`.

---

## REGRAS GLOBAIS DE COPY E ÍCONE

```
- Nunca usar travessão "—" em texto visível. Usar | ou . ou : ou quebra de linha.
- Nunca emojis Unicode em headings, cards, CTAs, qualquer UI.
- Todos ícones via lucide-react. FaWhatsapp SOMENTE no float + CTA WhatsApp.
- NUNCA MessageCircle no lugar de FaWhatsapp.
- py-32 proibido. Máximo py-20 nas seções principais, py-16 nas secundárias.
- Hero foto: sempre reta. Nunca transform rotate, skew, clip-path agressivo.
- CTA "Saiba Mais" proibido. Específico sempre: "Falar no WhatsApp", "Solicitar Orçamento", "Ver Coleção".
- Seção sem conteúdo real = seção não existe. Sem depoimentos reais, sem seção de depoimentos.
```

## WHATSAPP FLOAT (obrigatório em Landing e Institucional)

```jsx
// fixed bottom-6 right-6 z-50
// <button className="w-14 h-14 rounded-full bg-[--whatsapp] shadow-2xl flex items-center justify-center
//                    relative before:absolute before:inset-0 before:rounded-full before:bg-[--whatsapp]
//                    before:animate-ping before:opacity-40">
//   <FaWhatsapp size={28} color="white" />
// </button>
// Link: contact.whatsappLink target="_blank" rel="noopener noreferrer"
// Tooltip: texto à esquerda no hover, bg-white rounded-lg shadow px-3 py-2 text-sm text-foreground
```

## IMAGENS (regras críticas)

- **Hero bg**: gradiente CSS puro + elemento decorativo. Nunca Unsplash query no background.
- **Foto em card**: URL Unsplash direta + `onError={(e) => { e.currentTarget.src='URL_FALLBACK'; e.currentTarget.onerror=null; }}`
- **URLs confiáveis**: photo-1494790108377-be9c29b29330 (mulher sorrindo), photo-1507003211169-0a1dd7228f2d (homem profissional), photo-1560472354-b33ff0c44a43 (produto)

---

## DIAGNÓSTICO (máx 8 linhas — interno)

```
TIPO:     [Landing Page / Institucional / E-commerce]
BLUEPRINT: [A / B / C]
H1:       "[frase validada]"
Visual:   [foto de quem? onde?]
Dado:     [número real ou omitir]
Paleta:   bg:[hex] primary:[hex] accent:[hex] — [claro/escuro]
Fonte:    [heading] / [corpo]
Ângulo:   [o que diferencia de verdade]
```

---

## CHECKLIST PRÉ-ENTREGA

- [ ] Tipo identificado e blueprint correto aplicado
- [ ] H1 passa no teste: um amigo falaria isso numa conversa?
- [ ] Seções criadas SOMENTE com conteúdo real (sem placeholder)
- [ ] Foto no hero: pessoa real, reta, sem rotação
- [ ] Hero bg: gradiente CSS (não Unsplash query)
- [ ] Fotos em cards com onError fallback
- [ ] Heading italic colorido em seções (institucional)
- [ ] Grid de produto: 4 cols desktop / 2 cols mobile (e-commerce)
- [ ] FaWhatsapp nos botões WhatsApp (não MessageCircle)
- [ ] py-20 máximo. Zero emojis. Zero travessão visível.
- [ ] npm install lucide-react react-icons framer-motion incluído
- [ ] contact.ts com dados reais

`"Make it premium enough that I'd screenshot and share it."`
