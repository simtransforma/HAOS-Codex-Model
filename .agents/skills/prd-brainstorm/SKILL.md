---
name: prd-brainstorm
description: "Brainstorming interativo e gera\u00e7\u00e3o de PRD estruturado para novos projetos"
author: "Skills Collection\r"
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

# PRD Brainstorm Skill

## Objetivo
Conduzir um processo de brainstorming estruturado e interativo para descoberta de produto, resultando em um PRD (Product Requirements Document) completo que serve como entrada para a skill `sprint-context-generator`.

## Referências Importantes
- [Técnicas de Brainstorming](./references/brainstorm-techniques.md) - OST, JTBD, Assumption Mapping
- [Template PRD](./references/prd-template.md) - Estrutura completa do documento
- [Guia de Tech Stacks](./references/tech-stack-guide.md) - Matriz de decisão tecnológica

---

## WORKFLOW DE 5 FASES

### FASE 1: Discovery Inicial

**Objetivo:** Entender o problema fundamental e contexto do projeto.

Faça as seguintes perguntas **uma de cada vez**, aguardando confirmação:

#### Q1: Problema
```
Qual problema você quer resolver?

Descreva a dor ou necessidade que motivou essa ideia. Seja específico:
- O que está acontecendo hoje que não funciona bem?
- Qual é o impacto desse problema?
- Com que frequência ele ocorre?
```

**Após resposta:** Resuma o problema em 1-2 frases e peça confirmação.

#### Q2: Usuários
```
Quem são os usuários afetados por esse problema?

Considere:
- Perfil demográfico (idade, profissão, localização)
- Nível técnico
- Frequência de uso esperada
- Outros produtos que usam hoje
```

**Após resposta:** Crie uma persona resumida e confirme.

#### Q3: Tipo de Projeto
```
Qual o tipo deste projeto?

[ ] Novo produto - Criar algo do zero
[ ] Nova feature - Adicionar funcionalidade a produto existente
[ ] Melhoria - Otimizar algo que já existe
[ ] Migração - Reescrever/modernizar sistema legado
[ ] Prova de conceito - Validar viabilidade técnica
```

**Após resposta:** Confirme as implicações do tipo escolhido.

#### Q4: Ideias Iniciais
```
Quais ideias de solução você já considerou?

Mesmo ideias parciais ou vagas são úteis. Compartilhe:
- Funcionalidades imaginadas
- Referências de produtos similares
- Abordagens técnicas consideradas
```

**Após resposta:** Liste as ideias e confirme entendimento.

---

### FASE 2: Brainstorming Estruturado

**Objetivo:** Aprofundar a descoberta usando técnicas profissionais de product discovery.

Aplique as 3 técnicas abaixo de forma interativa:

#### 2.1 Opportunity Solution Tree (OST)

```
Vamos construir uma Árvore de Oportunidades:

1. OUTCOME DE NEGÓCIO
   Qual resultado mensurável você quer alcançar?
   Ex: "Aumentar retenção em 20%" ou "Reduzir tempo de onboarding para 5min"

2. OPORTUNIDADES
   Que problemas/necessidades dos usuários, se resolvidos, levariam a esse outcome?
   (Liste 3-5 oportunidades)

3. SOLUÇÕES
   Para cada oportunidade, quais soluções podemos testar?
   (2-3 soluções por oportunidade)
```

**Visualize o resultado:**
```
                    [OUTCOME]
                        |
        ┌───────────────┼───────────────┐
        |               |               |
  [Oportunidade 1] [Oportunidade 2] [Oportunidade 3]
        |               |               |
    ┌───┴───┐       ┌───┴───┐       ┌───┴───┐
[Sol A] [Sol B]  [Sol C] [Sol D]  [Sol E] [Sol F]
```

Confirme a árvore antes de prosseguir.

#### 2.2 Jobs To Be Done (JTBD)

```
Agora vamos identificar os "Jobs" que os usuários precisam realizar.

Complete as frases no formato:

"Quando [SITUAÇÃO/CONTEXTO],
 eu quero [AÇÃO/CAPACIDADE],
 para que [RESULTADO DESEJADO]."

Identifique jobs em 3 categorias:

FUNCIONAIS (tarefas práticas):
- "Quando _______, quero _______, para _______."

EMOCIONAIS (como querem se sentir):
- "Quando _______, quero _______, para _______."

SOCIAIS (como querem ser percebidos):
- "Quando _______, quero _______, para _______."
```

Documente pelo menos 2 jobs por categoria.

#### 2.3 Assumption Mapping

```
Toda solução é baseada em suposições. Vamos mapeá-las:

Liste suas suposições em 3 categorias:

VALOR (o usuário quer isso?)
- Suposição 1: _______
- Suposição 2: _______

USABILIDADE (o usuário consegue usar?)
- Suposição 1: _______
- Suposição 2: _______

VIABILIDADE (conseguimos construir?)
- Suposição 1: _______
- Suposição 2: _______
```

**Priorização (matriz 2x2):**
```
              ALTO IMPACTO
                   |
    Testar    |    Testar
    Depois    |    Primeiro
              |
 BAIXA ───────┼─────── ALTA
 INCERTEZA    |    INCERTEZA
              |
    Assumir   |    Monitorar
    como OK   |    de Perto
              |
              BAIXO IMPACTO
```

Classifique cada suposição e identifique as que precisam ser testadas primeiro.

---

### FASE 3: Pesquisa de Tecnologias

**OBRIGATÓRIO: Use WebSearch para pesquisar stacks atuais.**

```javascript
// Pesquisas obrigatórias:
WebSearch("[tipo do projeto] tech stack 2024 2025")
WebSearch("[framework/linguagem considerada] vs alternatives 2025")
WebSearch("[tipo do projeto] MVP best practices")
```

#### Apresente 2 Opções Comparativas:

**OPÇÃO A: MVP Simples**
- Foco: Validação rápida, baixo custo
- Critérios: Menor curva de aprendizado, deploy rápido, fácil pivotagem
- Exemplo de stack: [baseado na pesquisa]

**OPÇÃO B: Stack Robusto**
- Foco: Escalabilidade, longo prazo
- Critérios: Performance, manutenibilidade, ecossistema maduro
- Exemplo de stack: [baseado na pesquisa]

**Tabela Comparativa:**
```
| Critério          | Opção A (MVP)    | Opção B (Robusto) |
|-------------------|------------------|-------------------|
| Tempo até MVP     | X semanas        | Y semanas         |
| Custo inicial     | $                | $$                |
| Escalabilidade    | Limitada         | Alta              |
| Curva aprendizado | Baixa            | Média/Alta        |
| Comunidade        | [Tamanho]        | [Tamanho]         |
```

**Recomendação:** Baseado no contexto do projeto (tipo, timeline, equipe), recomende uma opção com justificativa.

Peça confirmação do usuário sobre a stack escolhida.

---

### FASE 4: Consolidação

**Objetivo:** Criar um resumo completo antes de gerar o PRD.

```
📋 RESUMO DO PROJETO

PROBLEMA:
[Resumo do problema em 2-3 frases]

SOLUÇÃO:
[Descrição da solução proposta]

USUÁRIOS:
[Persona principal]

OUTCOME ESPERADO:
[Métrica de sucesso principal]

JOBS PRINCIPAIS:
1. [Job funcional mais importante]
2. [Job emocional mais importante]

SUPOSIÇÕES CRÍTICAS:
1. [Suposição de maior risco]
2. [Segunda suposição crítica]

TECH STACK ESCOLHIDA:
[Stack selecionada com justificativa]

ESCOPO MVP:
- Inclui: [features essenciais]
- Não inclui: [features para depois]
```

**Confirmação obrigatória:**
```
Este resumo está correto e completo?
Deseja ajustar algo antes de gerar o PRD final?
```

---

### FASE 5: Geração do PRD

**Após confirmação, gere o arquivo `prd.md`.**

Use o template em [references/prd-template.md](./references/prd-template.md).

#### Localização do Arquivo:
- Se existe pasta do projeto: `[projeto]/docs/prd.md`
- Se não existe: criar na raiz como `prd.md`

#### Seções Obrigatórias:
1. Metadata (projeto, versão, data, status)
2. Overview (problema, solução, objetivo)
3. Contexto (background, usuários, métricas)
4. Assumptions (valor, viabilidade, riscos)
5. Scope (in/out of scope, futuro)
6. User Stories (formato padrão + critérios)
7. Technical Stack (escolha + alternativas)
8. Success Metrics (KPIs mensuráveis)
9. Dependencies & Blockers
10. Timeline Estimado
11. Próximos Passos

#### Validação:
Execute o script de validação:
```bash
node scripts/validate-prd.js prd.md
```

#### Finalização:
```
✅ PRD gerado com sucesso: [caminho do arquivo]

📌 PRÓXIMO PASSO:
Execute /sprint-context-generator para criar o contexto técnico do sprint.

O sprint-context-generator irá:
- Importar automaticamente as informações do PRD
- Pular perguntas já respondidas
- Focar em detalhes técnicos (arquitetura, APIs, testes)
```

---

## REGRAS IMPORTANTES

### Interatividade
- **NUNCA** pule fases ou perguntas
- **SEMPRE** aguarde confirmação antes de avançar
- **SEMPRE** resuma o entendimento após cada resposta
- Se o usuário parecer confuso, ofereça exemplos

### Pesquisa
- **OBRIGATÓRIO** usar WebSearch na Fase 3
- Cite fontes quando recomendar tecnologias
- Apresente dados atualizados (2024-2025)

### Qualidade do PRD
- User Stories devem seguir formato padrão
- Métricas devem ser mensuráveis (números específicos)
- Escopo deve ser claramente definido
- Tech stack deve ter justificativa

### Integração
- O PRD deve ser compatível com sprint-context-generator
- Mantenha consistência de nomenclatura
- Inclua seção explícita de "Próximos Passos"

---

## EXEMPLOS DE INTERAÇÃO

### Exemplo: Início de Sessão
```
Usuário: /prd-brainstorm

Claude: 🧠 **PRD Brainstorm Iniciado**

Vou guiá-lo através de um processo de descoberta estruturado para criar
um PRD completo. São 5 fases:

1. Discovery Inicial - Entender o problema
2. Brainstorming - Técnicas de product discovery
3. Pesquisa Tech - Definir stack ideal
4. Consolidação - Validar entendimento
5. Geração PRD - Documento final

Vamos começar?

**FASE 1: Discovery Inicial**

Qual problema você quer resolver?

Descreva a dor ou necessidade que motivou essa ideia...
```

### Exemplo: Transição de Fase
```
Claude: Excelente! Entendi que o problema é [resumo].

Isso está correto? (sim/não/ajustar)

Usuário: sim

Claude: Perfeito! Próxima pergunta:

Quem são os usuários afetados por esse problema?...
```

---

## TROUBLESHOOTING

### Usuário muito vago
Ofereça exemplos concretos e pergunte qual se aproxima mais da ideia.

### Usuário quer pular fases
Explique o valor de cada fase. Se insistir, documente no PRD que a fase foi pulada e os riscos.

### Escopo muito grande
Sugira dividir em múltiplos PRDs ou priorizar features para MVP.

### Incerteza técnica alta
Recomende fase de spike/prova de conceito antes do desenvolvimento.

---

## CHANGELOG

- v1.0.0: Versão inicial com workflow de 5 fases
