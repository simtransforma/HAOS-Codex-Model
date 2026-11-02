---
name: feedback-interpreter
description: "Transforma feedbacks brutos de clientes em prompts perfeitos e estruturados para o Lovable. Use esta skill sempre que o usuário colar um feedback de cliente (\"o cliente falou que...\", \"o cliente reclamou de...\", \"precisa mudar X segundo o feedback\", \"o cliente quer isso diferente\"), pedir para transformar ou interpretar feedback em prompt para o Lovable, ou quando houver um texto vago, emocional ou incompleto de cliente que precisa virar instrução técnica. Também aciona em: \"converte esse feedback\", \"transforma esse feedback em prompt\", \"o que eu mando pro Lovable com base nisso\", \"interpreta esse feedback\". Nunca pule esta skill quando houver feedback de cliente — ela garante prompts de alta qualidade e evita perdas na tradução entre o que o cliente disse e o que o Lovable vai executar.\n"
---

# Feedback Interpreter

Decodifica feedbacks vagos, emocionais ou incompletos e os transforma em prompts modulares, precisos e prontos para o `send_message` do Lovable MCP.

Leia `references/prompt-patterns.md` quando precisar de padrões detalhados por tipo de mudança.
Leia `references/examples.md` para ver transformações reais antes/depois.

---

## Fluxo de Execução

### 1. Classificar o Feedback

Leia o feedback e mapeie cada ponto para uma categoria:

| Categoria | Sinal no feedback | Escopo |
|-----------|-------------------|--------|
| **Visual** | "ficou feio", "não gostei do visual", "parece estranho" | cores, espaçamento, tipografia, layout, ícones |
| **Funcional** | "não funciona", "tá errado", "não faz nada" | comportamento de botões, dados, fluxos, validações |
| **UX/Fluxo** | "confuso", "difícil", "muitos passos" | navegação, ordem de elementos, quantidade de cliques |
| **Conteúdo** | "texto errado", "nome errado", "falta info" | labels, títulos, placeholders, mensagens de erro |
| **Feature nova** | "quero adicionar", "falta um X", "e se tivesse" | novo componente, seção, integração |

### 2. Decodificar Intenção Implícita

Feedbacks vagos escondem pedidos concretos. Traduza:

- **"Ficou feio"** → identifique o elemento mais provável (botão? fundo? card?) e proponha ajuste específico
- **"Não gostei das cores"** → qual contexto? (CTA, fundo, texto, status?) → sugira ajuste alinhado à paleta existente
- **"Está confuso"** → onde está o atrito? (formulário longo? botão escondido? fluxo não intuitivo?)
- **"Quero igual ao [X]"** → extraia o padrão de design implícito (layout, hierarquia, cores)
- **"Mais profissional"** → remover elementos decorativos, aumentar espaçamento, tipografia mais limpa

Se o feedback tiver **menos de 2 pontos identificáveis**, faça no máximo **2 perguntas de esclarecimento** antes de montar o prompt.

### 3. Montar o Prompt para Lovable

Use a estrutura modular abaixo. Inclua **apenas as seções com mudanças reais**.

```markdown
## Contexto
[Estado atual — o que existe hoje que precisa mudar. 1-2 frases.]

## Mudanças solicitadas

### Visual
- [elemento específico] → [ajuste específico]
- Ex: "Botão primário da hero section" → "mudar de #3B82F6 para #1D4ED8, aumentar padding para py-4 px-8"

### Funcional
- [ação] deve [comportamento esperado]
- Ex: "Ao clicar em Salvar" deve "exibir toast de confirmação e redirecionar para /dashboard"

### Conteúdo
- [elemento] → [novo texto]
- Ex: "Label do campo email" → "Endereço de e-mail"

### Feature nova
- [descrição concisa do que adicionar e onde]

## Critérios de aceitação
- [ ] [resultado visível e verificável pelo cliente]
```

**Regras de qualidade do prompt:**
- Cada mudança deve ter **elemento + ajuste** (nunca só um dos dois)
- Medidas visuais em unidades concretas (`px`, `rem`, classes Tailwind)
- Comportamentos funcionais com **trigger → resultado** (`ao clicar X → acontece Y`)
- Máximo 1 feature nova por prompt (se houver mais, dividir em prompts separados)

### 4. Entregar

Sempre entregar em 3 partes:

1. **Diagnóstico** (2-3 bullets) — o que o feedback realmente pede, traduzido do vago para o técnico
2. **Prompt pronto** — em bloco de código Markdown, pronto para colar no `send_message` do Lovable
3. **Nível de confiança:**
   - ✅ Feedback claro — prompt fiel ao pedido
   - ⚠️ Inferências feitas — liste o que foi assumido para o usuário validar antes de enviar

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
