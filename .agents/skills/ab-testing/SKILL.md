---
name: ab-testing
description: "Use quando o usuário quiser planejar, desenhar ou implementar um teste A/B ou experimento, ou construir um programa de experimentação de crescimento. Use também quando ele mencionar 'teste A/B', 'split test', 'experimento', 'testar essa mudança', 'copy de variante', 'teste multivariado', 'hipótese', 'devo testar isso', 'qual versão é melhor', 'testar duas versões', 'significância estatística', 'por quanto tempo rodar esse teste', 'experimentos de crescimento', 'velocidade de experimento', 'backlog de experimento', 'score ICE', 'programa de experimentação' ou 'playbook de experimento'. Use sempre que alguém comparar duas abordagens e quiser medir qual performa melhor. Para implementação de tracking, veja analytics. Para otimização de conversão de página, veja cro."
---

# Setup de Teste A/B (HAOS)

Você é especialista em experimentação e testes A/B. Seu objetivo é ajudar a desenhar testes que produzem resultados estatisticamente válidos e acionáveis.

> **Contexto HAOS.** A medição de testes em páginas públicas passa pelo GTM `${RESOURCE_ID}` + GA4. Para eventos customizados, acione o agente tracking-engineer.

## Avaliação Inicial

**Verifique o contexto de marketing de produto primeiro:**
Se `${USER_PROJECT_ROOT}/.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o legado `product-marketing-context.md`), leia antes de perguntar.

Antes de desenhar um teste, entenda:

1. **Contexto do Teste** — o que você quer melhorar? Que mudança está considerando?
2. **Estado Atual** — taxa de conversão base? Volume de tráfego atual?
3. **Restrições** — complexidade técnica? Prazo? Ferramentas disponíveis?

---

## Princípios Centrais

### 1. Comece com uma Hipótese
- Não só "vamos ver o que acontece"
- Previsão específica do resultado
- Baseada em raciocínio ou dados

### 2. Teste Uma Coisa
- Uma variável por teste
- Senão você não sabe o que funcionou

### 3. Rigor Estatístico
- Pré-determine o tamanho de amostra
- Não espie e pare cedo
- Comprometa-se com a metodologia

### 4. Meça o Que Importa
- Métrica primária ligada a valor de negócio
- Métricas secundárias para contexto
- Métricas de guardrail para evitar dano

---

## Framework de Hipótese

### Estrutura

```
Porque [observação/dado],
acreditamos que [mudança]
vai causar [resultado esperado]
para [público].
Saberemos que é verdade quando [métricas].
```

### Exemplo

**Fraca**: "Mudar a cor do botão pode aumentar os cliques."

**Forte**: "Porque os usuários relatam dificuldade de achar o CTA (por mapas de calor e feedback), acreditamos que deixar o botão maior e com cor contrastante vai aumentar os cliques no CTA em 15%+ para novos visitantes. Vamos medir a taxa de clique de page view até início de cadastro."

---

## Tipos de Teste

| Tipo | Descrição | Tráfego necessário |
|------|-----------|--------------------|
| A/B | Duas versões, uma mudança | Moderado |
| A/B/n | Múltiplas variantes | Maior |
| MVT | Múltiplas mudanças em combinações | Muito alto |
| Split URL | URLs diferentes por variante | Moderado |

---

## Tamanho de Amostra

### Referência Rápida

| Base | 10% Lift | 20% Lift | 50% Lift |
|------|----------|----------|----------|
| 1% | 150k/variante | 39k/variante | 6k/variante |
| 3% | 47k/variante | 12k/variante | 2k/variante |
| 5% | 27k/variante | 7k/variante | 1,2k/variante |
| 10% | 12k/variante | 3k/variante | 550/variante |

**Calculadoras:**
- [Evan Miller](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely](https://www.optimizely.com/sample-size-calculator/)

**Para tabelas detalhadas de amostra e cálculo de duração**: veja [references/sample-size-guide.md](references/sample-size-guide.md)

---

## Seleção de Métricas

### Métrica Primária
- Única métrica que mais importa
- Diretamente ligada à hipótese
- O que você usa para encerrar o teste

### Métricas Secundárias
- Apoiam a interpretação da primária
- Explicam por que/como a mudança funcionou

### Métricas de Guardrail
- Coisas que não devem piorar
- Pare o teste se ficarem muito negativas

### Exemplo: Teste de Página de Preço
- **Primária**: taxa de seleção de plano
- **Secundárias**: tempo na página, distribuição de planos
- **Guardrail**: tickets de suporte, taxa de reembolso

---

## Desenhando Variantes

### O Que Variar

| Categoria | Exemplos |
|-----------|----------|
| Headlines/Copy | Ângulo da mensagem, proposta de valor, especificidade, tom |
| Design Visual | Layout, cor, imagens, hierarquia |
| CTA | Copy do botão, tamanho, posição, número |
| Conteúdo | Informação incluída, ordem, quantidade, prova social |

### Boas Práticas
- Mudança única e significativa
- Ousada o bastante para fazer diferença
- Fiel à hipótese

---

## Alocação de Tráfego

| Abordagem | Divisão | Quando usar |
|-----------|---------|-------------|
| Padrão | 50/50 | Default para A/B |
| Conservadora | 90/10, 80/20 | Limitar risco de variante ruim |
| Rampa | Comece pequeno, aumente | Mitigação de risco técnico |

**Considerações:** consistência (o usuário vê a mesma variante ao voltar), exposição equilibrada por hora/dia da semana.

---

## Implementação

### Client-Side
- JavaScript modifica a página após o load
- Rápido de implementar, pode causar flicker
- Ferramentas: PostHog, Optimizely, VWO, Google Optimize alternativas via GTM

### Server-Side
- Variante decidida antes da renderização
- Sem flicker, exige trabalho de dev
- Ferramentas: PostHog, LaunchDarkly, Split

---

## Rodando o Teste

### Checklist de Pré-Lançamento
- [ ] Hipótese documentada
- [ ] Métrica primária definida
- [ ] Tamanho de amostra calculado
- [ ] Variantes implementadas corretamente
- [ ] Tracking verificado (GTM/GA4)
- [ ] QA feito em todas as variantes

### Durante o Teste

**FAÇA:** monitore problemas técnicos, cheque qualidade dos segmentos, documente fatores externos.

**EVITE:** espiar resultados e parar cedo, mudar variantes, adicionar tráfego de fontes novas.

### O Problema do "Espiar"
Olhar os resultados antes de atingir o tamanho de amostra e parar cedo gera falsos positivos. Pré-comprometa-se com a amostra e confie no processo.

---

## Analisando Resultados

### Significância Estatística
- 95% de confiança = p-valor < 0,05
- Significa <5% de chance de ser aleatório
- Não é garantia — só um limiar

### Checklist de Análise

1. **Atingiu a amostra?** Se não, resultado é preliminar
2. **Estatisticamente significativo?** Cheque intervalos de confiança
3. **Tamanho do efeito é relevante?** Compare ao MDE, projete o impacto
4. **Secundárias consistentes?** Apoiam a primária?
5. **Preocupações de guardrail?** Algo piorou?
6. **Diferenças por segmento?** Mobile vs. desktop? Novo vs. recorrente?

### Interpretando Resultados

| Resultado | Conclusão |
|-----------|-----------|
| Vencedora significativa | Implemente a variante |
| Perdedora significativa | Mantenha o controle, aprenda por quê |
| Sem diferença significativa | Precisa de mais tráfego ou teste mais ousado |
| Sinais mistos | Aprofunde, talvez segmente |

---

## Documentação

Documente todo teste com: hipótese, variantes (com screenshots), resultados (amostra, métricas, significância), decisão e aprendizados.

**Para templates**: veja [references/test-templates.md](references/test-templates.md)

---

## Programa de Experimentação de Crescimento

Testes individuais valem. Um programa contínuo é um ativo que compõe.

### O Loop de Experimento

```
1. Gere hipóteses (de dados, pesquisa, concorrentes, feedback de cliente)
2. Priorize com ICE
3. Desenhe e rode o teste
4. Analise com rigor estatístico
5. Promova vencedores a um playbook
6. Gere novas hipóteses dos aprendizados
→ Repita
```

### Geração de Hipóteses

| Fonte | O que procurar |
|-------|----------------|
| Analytics | Pontos de queda, páginas de baixa conversão, segmentos fracos |
| Pesquisa de cliente | Dores, confusão, expectativas não atendidas |
| Análise de concorrente | Features, mensagens ou UX que eles usam e você não |
| Tickets de suporte | Perguntas/reclamações recorrentes em fluxos de conversão |
| Mapas de calor/gravações | Onde os usuários hesitam, dão rage-click ou abandonam |
| Experimentos passados | "Perdedores significativos" revelam novos ângulos |

### Priorização ICE

Pontue cada hipótese de 1-10 em três dimensões:

| Dimensão | Pergunta |
|----------|----------|
| **Impacto** | Se funcionar, quanto move a métrica primária? |
| **Confiança** | Quão certos estamos? (Por dados, não palpite) |
| **Facilidade** | Quão rápido e barato dá pra subir e medir? |

**Score ICE** = (Impacto + Confiança + Facilidade) / 3

Rode os de maior score primeiro. Repontue mensalmente.

### Velocidade de Experimento

| Métrica | Meta |
|---------|------|
| Experimentos lançados por mês | 4-8 para a maioria |
| Taxa de vitória | 20-30% é comum em programas maduros |
| Duração média | 2-4 semanas |
| Profundidade do backlog | 20+ hipóteses na fila |
| Lift cumulativo | Ganhos compostos de todos os vencedores |

### O Playbook de Experimento

Quando um teste vence, não só implemente — documente o padrão:

```
## [Nome do Experimento]
**Data**: [data]
**Hipótese**: [a hipótese]
**Tamanho de amostra**: [n por variante]
**Resultado**: [vencedor/perdedor/inconclusivo] — [métrica primária] mudou [X%] (IC 95%: [faixa], p=[valor])
**Guardrails**: [métricas de guardrail e desfechos]
**Deltas por segmento**: [diferenças notáveis por device, segmento, coorte]
**Por que funcionou/falhou**: [análise]
**Padrão**: [insight reaproveitável]
**Aplicar a**: [outras páginas/fluxos onde o padrão pode funcionar]
**Status**: [implementado / parado / precisa de follow-up]
```

### Cadência de Experimento

**Semanal (30 min)**: revise experimentos rodando por problemas técnicos e guardrails. Não declare vencedores cedo — mas pare testes com guardrails muito negativos.

**Quinzenal**: encerre os concluídos. Analise, atualize o playbook, lance o próximo do backlog.

**Mensal (1 hora)**: revise velocidade, taxa de vitória, lift cumulativo. Reabasteça o backlog. Repriorize com ICE.

**Trimestral**: audite o playbook. Que padrões foram aplicados amplamente? Que vencedores não foram escalados? Que partes do funil estão sub-testadas?

---

## Erros Comuns

### Design do Teste
- Testar mudança pequena demais (indetectável)
- Testar coisas demais (não isola)
- Sem hipótese clara

### Execução
- Parar cedo
- Mudar coisas no meio do teste
- Não checar a implementação

### Análise
- Ignorar intervalos de confiança
- Selecionar segmentos a dedo
- Superinterpretar resultados inconclusivos

---

## Perguntas Específicas da Tarefa

1. Qual sua taxa de conversão atual?
2. Quanto tráfego esta página recebe?
3. Que mudança você considera e por quê?
4. Qual a menor melhoria que vale detectar?
5. Que ferramentas você tem para testar?
6. Já testou essa área antes?

---

## Skills Relacionadas

- **cro**: para gerar ideias de teste com base em princípios de CRO
- **analytics**: para configurar a medição do teste
- **copywriting**: para criar copy de variante

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
