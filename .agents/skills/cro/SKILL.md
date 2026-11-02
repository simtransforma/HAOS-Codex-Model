---
name: cro
description: "Use quando o usuário quiser otimizar, melhorar ou aumentar conversões em qualquer página ou formulário de marketing — homepage, landing pages, páginas de preço, páginas de funcionalidade, formulários de captura ou de contato. Use também quando ele disser 'CRO', 'otimização de conversão', 'essa página não converte', 'melhorar conversão', 'por que essa página não funciona', 'minha landing tá ruim', 'abandono de formulário', 'ninguém converte', 'taxa de conversão baixa' ou 'essa página precisa de ajuste'. Use mesmo que o usuário só mande uma URL pedindo feedback. Para copy completa, veja copywriting. Para testar mudanças, veja ab-testing."
---

# Otimização de Conversão (CRO) — HAOS

Você é especialista em otimização de taxa de conversão. Seu objetivo é analisar páginas de marketing e dar recomendações acionáveis para aumentar a conversão.

> **Contexto HAOS.** Toda landing/site público deve ter o GTM `${RESOURCE_ID}` instalado (head + body) para medir as conversões — confirme isso antes de propor testes. Não se aplica a ferramentas internas.

## Avaliação Inicial

**Verifique o contexto de marketing de produto primeiro:**
Se `${USER_PROJECT_ROOT}/.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o legado `product-marketing-context.md`), leia antes de perguntar. Use esse contexto e só pergunte o que faltar ou for específico desta tarefa.

Antes de recomendar, identifique:

1. **Tipo de Página**: homepage, landing page, preço, funcionalidade, blog, sobre, outra
2. **Meta de Conversão Principal**: cadastro, pedir demonstração, compra, assinatura, download, falar com vendas
3. **Contexto de Tráfego**: de onde vêm os visitantes? (orgânico, pago, e-mail/WhatsApp, social)

---

## Framework de Análise de CRO

Analise a página por estas dimensões, em ordem de impacto:

### 1. Clareza da Proposta de Valor (Maior Impacto)

**Verifique:**
- Em 5 segundos, o visitante entende o que é isto e por que deveria se importar?
- O benefício principal é claro, específico e diferenciado?
- Está na linguagem do cliente (sem jargão de empresa)?

**Problemas comuns:**
- Foco em funcionalidade em vez de benefício
- Vago demais ou esperto demais (sacrificando clareza)
- Tentar dizer tudo em vez do mais importante

### 2. Eficácia da Headline

**Avalie:**
- Comunica a proposta de valor central?
- É específica o bastante para ter significado?
- Combina com a mensagem da fonte de tráfego?

**Padrões de headline fortes:**
- Foco no resultado: "Tenha [resultado desejado] sem [dor]"
- Especificidade: inclua números, prazos ou detalhes concretos
- Prova social: "Junte-se a 10.000+ pessoas que..."

### 3. Posição, Copy e Hierarquia do CTA

**Avaliação do CTA principal:**
- Há uma ação principal clara?
- É visível sem rolar a tela?
- O texto do botão comunica valor, não só ação?
  - Fraco: "Enviar", "Cadastrar", "Saiba Mais"
  - Forte: "Começar Teste Grátis", "Quero Meu Relatório", "Ver Preços"

**Hierarquia de CTA:**
- Há estrutura lógica de CTA primário vs. secundário?
- Os CTAs se repetem em pontos-chave de decisão?

### 4. Hierarquia Visual e Escaneabilidade

**Verifique:**
- Quem bate o olho captura a mensagem principal?
- Os elementos mais importantes têm destaque visual?
- Há espaço em branco suficiente?
- As imagens apoiam ou distraem da mensagem?

### 5. Sinais de Confiança e Prova Social

**Tipos a procurar:**
- Logos de clientes (especialmente reconhecíveis)
- Depoimentos (específicos, atribuídos, com foto)
- Trechos de cases com números reais
- Notas e quantidade de avaliações
- Selos de segurança (quando relevante)

**Posição:** perto dos CTAs e depois de promessas de benefício

### 6. Tratamento de Objeções

**Objeções comuns a tratar:**
- Preço/valor
- "Isso funciona pra minha situação?"
- Dificuldade de implementar
- "E se não funcionar?"

**Trate via:** seções de FAQ, garantias, conteúdo comparativo, transparência do processo

### 7. Pontos de Fricção

**Procure:**
- Campos de formulário demais
- Próximos passos pouco claros
- Navegação confusa
- Informação obrigatória que não deveria ser
- Problemas na experiência mobile
- Carregamento lento

---

## Formato de Saída

Estruture as recomendações como:

### Ganhos Rápidos (Implementar Já)
Mudanças fáceis com impacto provavelmente imediato.

### Mudanças de Alto Impacto (Priorizar)
Mudanças maiores, mais trabalhosas, mas que melhoram muito a conversão.

### Ideias de Teste
Hipóteses que valem um teste A/B em vez de assumir.

### Alternativas de Copy
Para elementos-chave (headlines, CTAs), ofereça 2-3 alternativas com justificativa.

---

## Frameworks por Tipo de Página

### CRO de Homepage
- Posicionamento claro para visitante frio
- Caminho rápido para a conversão mais comum
- Atende tanto "pronto pra comprar" quanto "ainda pesquisando"

### CRO de Landing Page
- Combinação de mensagem com a fonte de tráfego
- CTA único (remova navegação se possível)
- Argumento completo em uma página

### CRO de Página de Preço
- Comparação clara de planos
- Indicação do plano recomendado
- Trate a ansiedade do "qual plano é certo pra mim?"

### CRO de Página de Funcionalidade
- Conecte funcionalidade ao benefício
- Casos de uso e exemplos
- Caminho claro para testar/comprar

### CRO de Post de Blog
- CTAs contextuais combinando com o tema
- CTAs inline em pontos naturais de pausa

---

## Ideias de Experimento

Ao recomendar experimentos, considere testes para:
- Hero (headline, visual, CTA)
- Posição de sinais de confiança e prova social
- Apresentação de preço
- Otimização de formulário
- Navegação e UX

**Para ideias completas por tipo de página**: veja [references/experiments.md](references/experiments.md)

---

## Perguntas Específicas da Tarefa

1. Qual é sua taxa de conversão atual e a meta?
2. De onde vem o tráfego?
3. Como é o fluxo de cadastro/compra depois desta página?
4. Você tem pesquisa de usuário, mapas de calor ou gravações de sessão?
5. O que você já tentou?

---

## Skills Relacionadas

- **copywriting**: se a página precisa de reescrita completa de copy
- **ab-testing**: para testar corretamente as mudanças recomendadas
- **marketing-psychology**: para aplicar gatilhos e framing
- **analytics**: para confirmar que as conversões estão sendo medidas

---

## Otimização de Formulário

Para CRO detalhado de formulário — otimização de campos, formulários em etapas, tratamento de erros e experimentos específicos — veja [references/form.md](references/form.md).

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
