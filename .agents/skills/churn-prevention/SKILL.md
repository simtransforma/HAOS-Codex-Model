---
name: churn-prevention
description: "Use quando o usuário quiser reduzir churn, construir fluxos de cancelamento, configurar ofertas de retenção, recuperar pagamentos falhos ou implementar estratégias de retenção. Use também quando ele mencionar 'churn', 'fluxo de cancelamento', 'offboarding', 'oferta de retenção', 'dunning', 'recuperação de pagamento', 'win-back', 'retenção', 'pesquisa de saída', 'pausar assinatura', 'churn involuntário', 'as pessoas estão cancelando', 'a taxa de churn está alta', 'como segurar os clientes' ou 'os clientes estão indo embora'. Use sempre que alguém estiver perdendo assinantes ou quiser sistemas para evitar isso. Para sequências de win-back, veja emails."
---

# Prevenção de Churn (HAOS)

Você é especialista em retenção e prevenção de churn. Seu objetivo é reduzir tanto o churn voluntário (cliente decide cancelar) quanto o involuntário (pagamento falho), com fluxos de cancelamento bem desenhados, ofertas dinâmicas de retenção, retenção proativa e estratégias de dunning.

> **Stack HAOS.** Pagamentos via **Yampi** (não Stripe). E-mail/automação via **Mautic**, mensagens via **Evolution/WhatsApp**, CRM via **Clint** e **ActiveCampaign**. No Brasil, atenção ao **CDC** (cancelamento facilitado, direito de arrependimento) e à **LGPD** (dados do cliente).

## Antes de Começar

**Verifique o contexto de marketing de produto primeiro:**
Se `${USER_PROJECT_ROOT}/.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o legado `product-marketing-context.md`), leia antes de perguntar.

Reúna este contexto (pergunte se não tiver):

### 1. Situação Atual de Churn
- Qual sua taxa de churn mensal? (Voluntário vs. involuntário se souber)
- Quantos assinantes ativos?
- Qual a receita média por cliente?
- Existe fluxo de cancelamento hoje, ou o cancelamento é instantâneo?

### 2. Cobrança & Plataforma
- Qual gateway de cobrança? (Yampi, recorrência própria, etc.)
- Intervalos: mensal, anual ou ambos?
- Suporta pausar ou rebaixar plano?
- Alguma ferramenta de retenção existente?

### 3. Dados de Produto & Uso
- Você rastreia uso de funcionalidade por usuário?
- Consegue identificar quedas de engajamento?
- Tem dados de motivo de cancelamento do passado?
- Qual sua métrica de ativação? (O que os retidos fazem que os que saem não fazem?)

### 4. Restrições
- B2B ou B2C? (Afeta o design do fluxo)
- Cancelamento autosserviço obrigatório? (O CDC favorece cancelamento fácil)
- Tom da marca no offboarding? (Empático, direto, brincalhão — conforme HAU/Edson/SIM/Editora)

---

## Como Esta Skill Funciona

Churn tem dois tipos que exigem estratégias diferentes:

| Tipo | Causa | Solução |
|------|-------|---------|
| **Voluntário** | Cliente decide cancelar | Fluxos de cancelamento, ofertas, pesquisas de saída |
| **Involuntário** | Pagamento falha | E-mails de dunning, retentativas inteligentes, atualização de cartão |

O churn voluntário costuma ser 50-70% do total. O involuntário é 30-50%, mas geralmente mais fácil de consertar.

Esta skill suporta três modos:

1. **Construir um fluxo de cancelamento** — do zero, com pesquisa, ofertas e confirmação
2. **Otimizar um fluxo existente** — analisar dados e melhorar taxa de retenção
3. **Configurar dunning** — recuperação de pagamento falho com retentativas e sequências

---

## Design do Fluxo de Cancelamento

### Estrutura do Fluxo

Todo fluxo segue esta sequência:

```
Gatilho → Pesquisa → Oferta Dinâmica → Confirmação → Pós-Cancelamento
```

**Passo 1: Gatilho** — Cliente clica em "Cancelar assinatura" nas configurações.

**Passo 2: Pesquisa de Saída** — Pergunte por que está cancelando. Isso define qual oferta mostrar.

**Passo 3: Oferta Dinâmica** — Apresente oferta direcionada ao motivo (desconto, pausa, rebaixar, etc.)

**Passo 4: Confirmação** — Se ainda quiser cancelar, confirme com clareza (mensagem de fim do período de cobrança).

**Passo 5: Pós-Cancelamento** — Defina expectativas, ofereça reativação fácil, dispare sequência de win-back.

### Design da Pesquisa de Saída

A pesquisa é a fundação. Boas categorias de motivo:

| Motivo | O que revela |
|--------|--------------|
| Caro demais | Sensibilidade a preço; pode responder a desconto ou rebaixar |
| Não uso o suficiente | Baixo engajamento; pode responder a pausa ou ajuda de onboarding |
| Falta uma funcionalidade | Lacuna de produto; mostrar roadmap ou alternativa |
| Trocando por concorrente | Pressão competitiva; entender o que oferecem |
| Problemas técnicos / bugs | Qualidade; escalar para suporte |
| Necessidade temporária / sazonal | Padrão de uso; oferecer pausa |
| Negócio fechou / mudou | Inevitável; aprenda e deixe ir com elegância |
| Outro | Coringa; inclua campo de texto livre |

**Boas práticas de pesquisa:**
- 1 pergunta, seleção única com texto opcional
- 5-8 opções no máximo (evite fadiga de decisão)
- Motivos mais comuns primeiro (revise os dados a cada trimestre)
- Não transforme em culpa
- "Ajude a gente a melhorar" funciona melhor que "Por que está saindo?"

### Ofertas Dinâmicas de Retenção

A chave: **case a oferta com o motivo.** Desconto não segura quem não usa o produto. Roadmap não segura quem não pode pagar.

**Mapa oferta-por-motivo:**

| Motivo | Oferta Principal | Oferta Reserva |
|--------|------------------|----------------|
| Caro demais | Desconto (20-30% por 2-3 meses) | Rebaixar para plano menor |
| Não uso o suficiente | Pausa (1-3 meses) | Sessão gratuita de onboarding |
| Falta funcionalidade | Prévia do roadmap + prazo | Guia de alternativa |
| Trocando por concorrente | Comparação + desconto | Sessão de feedback |
| Problemas técnicos | Escalar suporte na hora | Crédito + correção prioritária |
| Temporário / sazonal | Pausar assinatura | Rebaixar temporariamente |
| Negócio fechou | Pular oferta (respeite a situação) | — |

### Tipos de Oferta de Retenção

**Desconto**
- 20-30% por 2-3 meses é o ponto ideal
- Evite 50%+ (ensina o cliente a cancelar pra ganhar desconto)
- Limite no tempo ("Esta oferta expira ao sair desta página")
- Mostre o valor em reais economizado, não só a %

**Pausar assinatura**
- 1-3 meses no máximo (pausas longas raramente reativam)
- 60-80% dos que pausam acabam voltando
- Reativação automática com aviso por antecedência
- Mantenha dados e configurações intactos

**Rebaixar plano**
- Ofereça um plano menor em vez do cancelamento total
- Mostre o que mantém vs. o que perde
- Posicione como "ajustar seu plano" e não "rebaixar"
- Caminho fácil de volta quando quiser

**Desbloqueio/extensão de funcionalidade**
- Desbloqueie um recurso premium que não testou
- Estenda o teste de um plano superior
- Melhor para motivo "não tô tendo valor suficiente"

**Contato pessoal**
- Para contas de alto valor (top 10-20% por receita)
- Encaminhe para sucesso do cliente fazer uma ligação
- E-mail pessoal do fundador para clientes menores

### Padrões de UI do Fluxo de Cancelamento

```
┌─────────────────────────────────────┐
│  Que pena ver você indo             │
│                                     │
│  Qual o principal motivo do         │
│  cancelamento?                      │
│                                     │
│  ○ Caro demais                      │
│  ○ Não uso o suficiente             │
│  ○ Falta uma funcionalidade         │
│  ○ Trocando por outra ferramenta    │
│  ○ Problemas técnicos               │
│  ○ Temporário / não preciso agora   │
│  ○ Outro: [____________]            │
│                                     │
│  [Continuar]                        │
│  [Deixa pra lá, manter assinatura]  │
└─────────────────────────────────────┘
         ↓ (seleciona "Caro demais")
┌─────────────────────────────────────┐
│  E se a gente pudesse ajudar?       │
│                                     │
│  A gente adoraria te manter. Olha   │
│  essa oferta especial:              │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  25% off nos próximos 3 meses │  │
│  │  Economize R$XX/mês           │  │
│  │                               │  │
│  │  [Aceitar Oferta]             │  │
│  └───────────────────────────────┘  │
│                                     │
│  Ou mude para o [Plano Básico] a    │
│  R$X/mês →                          │
│                                     │
│  [Não, quero continuar cancelando]  │
└─────────────────────────────────────┘
```

**Princípios de UI:**
- Mantenha a opção "continuar cancelando" visível (sem dark patterns — o CDC exige cancelamento fácil)
- Uma oferta principal + uma reserva, não um muro de opções
- Mostre a economia específica em reais, não só percentual
- Use o nome e os dados do cliente quando possível
- Mobile-friendly (muitos cancelamentos acontecem no celular)

Para padrões detalhados por setor e gateway, veja [references/cancel-flow-patterns.md](references/cancel-flow-patterns.md).

---

## Previsão de Churn & Retenção Proativa

A melhor retenção acontece antes de o cliente clicar em "Cancelar".

### Sinais de Risco

Rastreie estes indicadores antecedentes:

| Sinal | Risco | Janela |
|-------|-------|--------|
| Frequência de login cai 50%+ | Alto | 2-4 semanas antes |
| Uso de funcionalidade-chave para | Alto | 1-3 semanas antes |
| Tickets de suporte disparam e param | Alto | 1-2 semanas antes |
| Taxa de abertura de e-mail cai | Médio | 2-6 semanas antes |
| Visitas à página de cobrança aumentam | Alto | Dias antes |
| Assentos de time removidos | Alto | 1-2 semanas antes |
| Exportação de dados iniciada | Crítico | Dias antes |
| NPS abaixo de 6 | Médio | 1-3 meses antes |

### Modelo de Health Score

Construa um health score simples (0-100) de sinais ponderados:

```
Health Score = (
  Score de login        × 0.30 +
  Score de uso          × 0.25 +
  Sentimento de suporte × 0.15 +
  Saúde de cobrança     × 0.15 +
  Score de engajamento  × 0.15
)
```

| Score | Status | Ação |
|-------|--------|------|
| 80-100 | Saudável | Oportunidade de upsell |
| 60-79 | Atenção | Check-in proativo |
| 40-59 | Em risco | Campanha de intervenção |
| 0-39 | Crítico | Contato pessoal |

### Intervenções Proativas

**Antes de a pessoa pensar em cancelar:**

| Gatilho | Intervenção |
|---------|-------------|
| Queda de uso >50% por 2 semanas | E-mail "Notamos que você não usou [recurso]. Precisa de ajuda?" |
| Perto do limite do plano | Convite de upgrade (sem bloqueio) |
| Sem login por 14 dias | E-mail de reengajamento com novidades |
| Detrator de NPS (0-6) | Follow-up pessoal em até 24h |
| Ticket sem resolver >48h | Escalação + atualização proativa |
| Renovação anual em 30 dias | E-mail de recapitulação de valor + confirmação |

---

## Churn Involuntário: Recuperação de Pagamento

Pagamentos falhos causam 30-50% de todo o churn, mas são os mais recuperáveis.

### A Pilha de Dunning

```
Pré-dunning → Retentativa inteligente → E-mails de dunning → Período de carência → Cancelamento
```

### Pré-Dunning (Prevenir Falhas)

- **Alertas de vencimento de cartão**: e-mail 30, 15 e 7 dias antes
- **Método de pagamento reserva**: peça um segundo método no cadastro
- **Atualização automática de cartão**: programas Visa/Mastercard (reduz recusas 30-50%)
- **Aviso de cobrança**: e-mail 3-5 dias antes do débito em planos anuais

### Lógica de Retentativa Inteligente

Nem toda falha é igual. Estratégia por tipo de recusa:

| Tipo de Recusa | Exemplos | Estratégia |
|----------------|----------|------------|
| Recusa branda (temporária) | Saldo insuficiente, timeout | Retentar 3-5 vezes em 7-10 dias |
| Recusa dura (permanente) | Cartão roubado, conta fechada | Não retente — peça novo cartão |
| Autenticação necessária | 3D Secure | Envie o cliente para atualizar o pagamento |

**Boas práticas de timing:**
- Retentativa 1: 24h após a falha
- Retentativa 2: 3 dias após
- Retentativa 3: 5 dias após
- Retentativa 4: 7 dias após (com escalada de e-mail de dunning)
- Após 4 retentativas: cancelar com caminho de reativação

**Dica:** retente no dia do mês em que o pagamento deu certo originalmente.

### Sequência de E-mail de Dunning

| E-mail | Timing | Tom | Conteúdo |
|--------|--------|-----|----------|
| 1 | Dia 0 (falha) | Alerta amigável | "Seu pagamento não passou. Atualize o cartão." |
| 2 | Dia 3 | Lembrete prestativo | "Lembrete rápido — atualize o pagamento pra manter o acesso." |
| 3 | Dia 7 | Urgência | "Sua conta será pausada em 3 dias. Atualize agora." |
| 4 | Dia 10 | Aviso final | "Última chance de manter sua conta ativa." |

**Boas práticas:**
- Link direto para a página de pagamento (sem login se possível)
- Mostre o que a pessoa vai perder (dados, acesso)
- Não culpe ("seu pagamento falhou", não "você falhou em pagar")
- Inclua contato de suporte
- Texto simples performa melhor que e-mail desenhado em dunning

### Benchmarks de Recuperação

| Métrica | Ruim | Médio | Bom |
|---------|------|-------|-----|
| Recuperação de recusa branda | <40% | 50-60% | 70%+ |
| Recuperação de recusa dura | <10% | 20-30% | 40%+ |
| Recuperação geral | <30% | 40-50% | 60%+ |
| Prevenção pré-dunning | Nenhuma | 10-15% | 20-30% |

Para o playbook completo de dunning, veja [references/dunning-playbook.md](references/dunning-playbook.md).

---

## Métricas & Medição

### Métricas-Chave de Churn

| Métrica | Fórmula | Meta |
|---------|---------|------|
| Churn mensal | Clientes perdidos / Clientes no início do mês | <5% B2C, <2% B2B |
| Churn de receita (líquido) | (Receita perdida - Receita de expansão) / Receita inicial | Negativo (expansão líquida) |
| Taxa de retenção do fluxo | Salvos / Total de sessões de cancelamento | 25-35% |
| Taxa de aceite de oferta | Ofertas aceitas / Ofertas mostradas | 15-25% |
| Reativação de pausa | Reativados / Total pausados | 60-80% |
| Recuperação de dunning | Recuperados / Total de pagamentos falhos | 50-60% |
| Tempo até cancelar | Dias do 1º sinal ao cancelamento | Acompanhe a tendência |

### Análise de Coorte

Segmente o churn por:
- **Canal de aquisição** — quais canais trazem clientes mais fiéis?
- **Tipo de plano** — qual plano dá mais churn?
- **Tempo de casa** — quando acontecem os cancelamentos? (30, 60, 90 dias?)
- **Motivo** — quais motivos estão crescendo?
- **Tipo de oferta** — quais ofertas funcionam por segmento?

### Testes A/B do Fluxo de Cancelamento

Teste uma variável por vez:

| Teste | Hipótese | Métrica |
|-------|----------|---------|
| Desconto (20% vs 30%) | Desconto maior retém mais | Taxa de retenção, impacto no LTV |
| Duração da pausa (1 vs 3 meses) | Pausa maior aumenta retorno | Taxa de reativação |
| Posição da pesquisa (antes vs depois da oferta) | Pesquisa primeiro personaliza a oferta | Taxa de retenção |
| Apresentação (modal vs página inteira) | Página inteira chama mais atenção | Taxa de retenção |
| Tom da copy (empático vs direto) | Empático reduz fricção | Taxa de retenção |

**Como rodar experimentos:** use a skill **ab-testing** para desenhar testes estatisticamente rigorosos. Use o GTM + analytics para acompanhar cada etapa do funil de cancelamento.

---

## Erros Comuns

- **Nenhum fluxo de cancelamento** — cancelar na hora deixa dinheiro na mesa. Até pesquisa + uma oferta retém 10-15%
- **Esconder o cancelamento** — botões escondidos geram ressentimento e avaliações ruins. O CDC favorece cancelamento fácil
- **Mesma oferta pra todo motivo** — desconto genérico não resolve "falta funcionalidade" ou "não uso"
- **Descontos fundos demais** — 50%+ ensina o cliente a cancelar-e-voltar por promoção
- **Ignorar churn involuntário** — frequentemente 30-50% do total e o mais fácil de consertar
- **Sem e-mails de dunning** — deixar falhas de pagamento cancelarem em silêncio
- **Copy de culpa** — "Tem certeza que quer nos abandonar?" prejudica a confiança
- **Não medir o LTV da retenção** — cliente "salvo" que sai em 30 dias não foi salvo
- **Pausar tempo demais** — pausas acima de 3 meses raramente reativam
- **Sem caminho pós-cancelamento** — facilite a reativação e dispare win-back

---

## Integrações de Ferramentas (Stack HAOS)

| Ferramenta | Melhor para | Onde |
|------------|-------------|------|
| **Yampi** | Cobrança/recorrência, retentativas | API (TOOLS.md) |
| **Mautic** | Sequências de dunning e retenção | Hetzner `${HAOS_PRIVATE_ROOT}` |
| **Evolution / WhatsApp** | Alertas de cobrança e win-back | Hetzner `${HAOS_PRIVATE_ROOT}` |
| **Clint CRM** | Health score, contas em risco | API (27 endpoints) |
| **ActiveCampaign** | Automação de retenção (apoio) | API |

---

## Skills Relacionadas

- **emails**: para sequências de win-back após cancelamento
- **analytics**: para configurar eventos de sinal de churn
- **ab-testing**: para testar variações do fluxo com rigor estatístico
- **marketing-psychology**: para framing das ofertas de retenção

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
