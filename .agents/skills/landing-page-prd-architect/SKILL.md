---
name: landing-page-prd-architect
description: "Cria PRDs (Product Requirements Documents) t\u00e9cnicos ultra detalhados para landing pages e sites premium usando Gemini CLI. Faz discovery interativo, pesquisa inspira\u00e7\u00f5es visuais (Dribbble, Awwwards, Behance), define identidade visual completa, cria wireframes desktop/mobile, gera prompts de imagem para IA, e entrega documenta\u00e7\u00e3o pronta para execu\u00e7\u00e3o.\n"
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

# Landing Page PRD Architect

Arquiteto de PRDs para landing pages premium. Transforma briefings em documentação técnica completa que permite ao Gemini CLI criar páginas de nível agência.

## Filosofia

- **Nunca genérico** - Cada landing page é única
- **Pesquisa extensiva** - Buscar inspirações reais antes de definir
- **Interação profunda** - Extrair máximo contexto antes de criar
- **Qualidade premium** - Sempre buscar nota 10
- **Documentação completa** - PRD + Visual + Wireframe + Prompts

## Fluxo Obrigatório

### Fase 1: Discovery

Solicitar materiais:
1. Imagens de referência (logo, produto, fotos)
2. Conteúdos textuais (sobre, benefícios, features)
3. Identidade visual existente (se houver)
4. Objetivo da página (vendas, leads, apresentação)
5. Público-alvo

Perguntas obrigatórias - Ver [references/discovery-questions.md](references/discovery-questions.md)

### Fase 2: Pesquisa e Inspiração

**Usar MCP Playwright para acessar:**
- Dribbble: `https://dribbble.com/search/[segmento]-landing-page`
- Awwwards: `https://www.awwwards.com/websites/`
- Land-book: `https://service.example.invalid`

Para cada inspiração documentar:
- URL da referência
- O que especificamente inspirou
- Como adaptar para o projeto

Pesquisar também:
- Efeitos/animações adequados - Ver [references/animation-library.md](references/animation-library.md)
- Tipografia - Ver [references/typography-pairings.md](references/typography-pairings.md)
- Ícones - Ver [references/icon-libraries.md](references/icon-libraries.md)
- Cores - Ver [references/color-psychology.md](references/color-psychology.md)

### Fase 3: Planejamento de Seções

Para CADA seção definir:
```
SEÇÃO: [Nome]
├── Objetivo: [O que comunicar/converter]
├── Layout: [Estrutura visual]
├── Conteúdo: [Headline, subheadline, body, CTA]
├── Visual: [Background, imagens, ícones]
├── Animações: [Entrada, interação, scroll]
└── Responsividade: [Adaptações mobile]
```

Ver templates em [references/section-templates.md](references/section-templates.md)

### Fase 4: Hero Section (Atenção Máxima)

A hero é a seção mais importante. Definir:

```
HERO BLUEPRINT:
├── Layout: [Centralizado/Split/Full-screen/Video]
├── Headline: [Max 10 palavras, impactante]
├── Visual Principal: [Imagem/Vídeo/Ilustração/3D]
├── CTA: [Texto, estilo, efeito hover]
├── Elementos Extras: [Badges, social proof, decorativos]
├── Animações: [Entrada, background, parallax]
└── Responsivo: [Desktop, tablet, mobile]
```

### Fase 5: Prompts para Imagens

Gerar prompt detalhado para cada imagem:

```
IMAGE PROMPT - [SEÇÃO]
├── Subject: [Descrição detalhada]
├── Composition: [Enquadramento, perspectiva]
├── Style: [Fotográfico, ilustração, 3D]
├── Color Palette: [Cores alinhadas com identidade]
├── Lighting: [Tipo de iluminação]
├── Mood: [Atmosfera/sensação]
├── Aspect Ratio: [16:9, 4:3, 1:1, 9:16]
└── Notes: [Observações específicas]
```

### Fase 6: Tecnologia

Definir stack - Ver [references/tech-stack-guide.md](references/tech-stack-guide.md)

### Fase 7: Criar Documentos

Estrutura de saída:
```
/[nome-projeto]-landing-page/
├── PRD.md
├── VISUAL-IDENTITY.md
├── WIREFRAME.md
├── IMAGE-PROMPTS.md
├── TECH-SPEC.md
├── REFERENCES.md
└── assets/
    ├── colors.json
    └── typography.json
```

Usar templates em assets/document-templates/ (user-supplied dependency; see PORTABILITY.md)

## Checklist de Qualidade

Antes de entregar:

**Discovery:**
- [ ] Coletou materiais de referência
- [ ] Fez perguntas de discovery
- [ ] Entendeu objetivo e público-alvo

**Pesquisa:**
- [ ] Buscou inspirações no Dribbble/Awwwards
- [ ] Documentou referências visuais
- [ ] Pesquisou efeitos/animações

**Identidade Visual:**
- [ ] Paleta de cores completa
- [ ] Hierarquia tipográfica
- [ ] Sistema de espaçamento

**Estrutura:**
- [ ] Todas seções planejadas
- [ ] Hero com atenção especial
- [ ] Wireframes desktop e mobile

**Assets:**
- [ ] Prompts de imagem completos
- [ ] Ícones especificados
- [ ] Fontes definidas

**Documentação:**
- [ ] PRD.md completo
- [ ] VISUAL-IDENTITY.md completo
- [ ] WIREFRAME.md completo
- [ ] IMAGE-PROMPTS.md completo
- [ ] TECH-SPEC.md completo

## Regras

1. NUNCA criar PRD genérico - Pesquisar e personalizar
2. SEMPRE pesquisar inspirações antes de definir visual
3. SEMPRE interagir profundamente para extrair contexto
4. SEMPRE definir hero com atenção máxima
5. SEMPRE gerar prompts de imagem para Nano Banana
6. SEMPRE criar documentação completa
7. SEMPRE considerar responsividade desde o início
8. SEMPRE buscar qualidade premium (nível agência)
9. SEMPRE especificar animações por seção
10. SEMPRE usar Playwright MCP para acessar Dribbble
