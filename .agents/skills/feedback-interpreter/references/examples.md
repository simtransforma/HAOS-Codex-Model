# Exemplos — Feedback Bruto → Prompt Lovable

---

## Exemplo 1: Feedback Visual Vago

**Feedback do cliente:**
> "Não gostei das cores do site, tá muito apagado, queria algo mais vibrante"

**Diagnóstico:**
- Visual — paleta atual percebida como sem energia
- Provavelmente afeta: botões CTA, headers, elementos de destaque
- Não afeta: conteúdo, funcionalidade

**Prompt gerado:**
```markdown
## Contexto
A paleta atual usa tons neutros/pastel que passam impressão de pouca energia.
Precisamos aumentar o contraste e vibração dos elementos de destaque.

## Mudanças solicitadas

### Visual
- Botão CTA principal → mudar para tom mais saturado (ex: de `bg-blue-400` para `bg-blue-600`)
- Títulos das seções → aumentar peso para `font-bold` e usar cor mais escura (`text-gray-900`)
- Seção hero → adicionar gradiente de fundo mais presente (ex: `from-blue-600 to-indigo-700`)
- Manter elementos secundários com a paleta atual para não sobrecarregar

## Critérios de aceitação
- [ ] Botão CTA tem contraste visual claro em relação ao fundo
- [ ] Hero section transmite energia e destaque imediato
```

**Nível de confiança:** ⚠️ Inferências feitas — assumi que "vibrante" se refere à intensidade dos CTAs e hero. Se o cliente quis mudar a paleta inteira, especifique quais seções.

---

## Exemplo 2: Feedback Funcional Claro

**Feedback do cliente:**
> "O botão de cadastro não faz nada quando eu clico"

**Diagnóstico:**
- Funcional — botão sem ação conectada
- Provavelmente: falta handler de submit ou navegação

**Prompt gerado:**
```markdown
## Contexto
O botão "Cadastrar" na página de registro não executa nenhuma ação ao ser clicado.

## Mudanças solicitadas

### Funcional
- Botão "Cadastrar" deve, ao ser clicado:
  1. Validar campos obrigatórios (nome, email, senha)
  2. Exibir spinner de loading durante o processamento
  3. Em sucesso: exibir toast "Cadastro realizado!" e redirecionar para /dashboard
  4. Em erro: exibir mensagem de erro inline abaixo do campo correspondente

## Critérios de aceitação
- [ ] Clicar no botão executa a ação de cadastro
- [ ] Usuário recebe feedback visual durante o loading
- [ ] Erros de validação são exibidos de forma clara
```

**Nível de confiança:** ✅ Feedback claro

---

## Exemplo 3: Feedback Misto + Vago

**Feedback do cliente:**
> "Preciso que o dashboard fique mais profissional e que dê pra ver o total de vendas em destaque"

**Diagnóstico:**
- Visual — "mais profissional" → menos decoração, mais espaço, tipografia limpa
- Feature nova — card com total de vendas em destaque
- Dois pontos distintos — podem ser tratados num único prompt pois são relacionados

**Prompt gerado:**
```markdown
## Contexto
O dashboard atual precisa de refinamento visual e de um elemento de destaque
para a métrica principal (total de vendas).

## Mudanças solicitadas

### Visual
- Remover elementos decorativos excessivos (bordas coloridas, sombras pesadas)
- Aumentar espaçamento interno dos cards para `p-6`
- Tipografia dos títulos de seção → `text-sm font-medium text-muted-foreground uppercase tracking-wide`
- Fundo dos cards → `bg-white` com `shadow-sm` (sutil)

### Feature nova
- Adicionar card de destaque no topo do dashboard com:
  - Título: "Total de Vendas"
  - Valor principal em `text-3xl font-bold`
  - Variação percentual vs. período anterior (verde se positivo, vermelho se negativo)
  - Posição: primeiro card, largura total ou 1/2 da grid

## Critérios de aceitação
- [ ] Dashboard transmite aparência limpa e profissional
- [ ] Total de vendas é o primeiro dado que o usuário vê
- [ ] Variação de performance é visualmente clara
```

**Nível de confiança:** ⚠️ Inferências feitas — assumi que "profissional" = visual mais clean. Dados do total de vendas assumidos como já existentes no backend.

---

## Exemplo 4: Feedback de Conteúdo

**Feedback do cliente:**
> "O texto do botão tá errado, precisa falar 'Solicitar Orçamento' e não 'Comprar Agora'"

**Diagnóstico:**
- Conteúdo — label de botão incorreto
- Simples e direto

**Prompt gerado:**
```markdown
## Contexto
O texto do botão CTA principal está incorreto para o contexto do negócio.

## Mudanças solicitadas

### Conteúdo
- Botão CTA principal (hero section) → "Comprar Agora" → "Solicitar Orçamento"
- Verificar se há outros botões com texto "Comprar Agora" e atualizar também

## Critérios de aceitação
- [ ] Nenhum botão exibe "Comprar Agora"
- [ ] CTA principal exibe "Solicitar Orçamento"
```

**Nível de confiança:** ✅ Feedback claro
