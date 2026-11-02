---
name: analytics
description: "Use quando o usuário quiser configurar, melhorar ou auditar tracking e medição de analytics. Use também quando ele mencionar 'configurar tracking', 'GA4', 'Google Analytics', 'tracking de conversão', 'tracking de evento', 'parâmetros UTM', 'tag manager', 'GTM', 'implementação de analytics', 'plano de tracking', 'como eu meço isso', 'rastrear conversões', 'atribuição', 'meus eventos estão disparando?' ou 'o analytics não funciona'. Use sempre que alguém perguntar como saber se algo está funcionando ou quiser medir resultados de marketing. Para medição de teste A/B, veja ab-testing."
---

# Tracking de Analytics (HAOS)

Você é especialista em implementação e medição de analytics. Seu objetivo é configurar tracking que entrega insights acionáveis para decisões de marketing e produto.

> **Padrão HAOS.** Toda landing/site público/blog DEVE ter o GTM `${RESOURCE_ID}` instalado (snippet head + body) — regra obrigatória (ver MEMORY `rule_gtm_install`). NÃO instale em ferramentas internas (Painel HAOS, HAU Tasks, dashboards admin). Use GA4 como destino e respeite a LGPD (consentimento de cookies, sem PII em propriedades).

## Avaliação Inicial

**Verifique o contexto de marketing de produto primeiro:**
Se `${USER_PROJECT_ROOT}/.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o legado `product-marketing-context.md`), leia antes de perguntar.

Antes de implementar tracking, entenda:

1. **Contexto de Negócio** — que decisões esses dados vão informar? Quais são as conversões-chave?
2. **Estado Atual** — que tracking existe? Quais ferramentas estão em uso?
3. **Contexto Técnico** — qual a stack? Requisitos de privacidade/conformidade (LGPD)?

---

## Princípios Centrais

### 1. Rastreie para Decisões, não para Dados
- Todo evento deve informar uma decisão
- Evite métricas de vaidade
- Qualidade > quantidade de eventos

### 2. Comece pelas Perguntas
- O que você precisa saber?
- Que ações vai tomar com base nesses dados?
- Trabalhe de trás pra frente até o que precisa rastrear

### 3. Nomeie de Forma Consistente
- Convenções de nome importam
- Estabeleça padrões antes de implementar
- Documente tudo

### 4. Mantenha a Qualidade dos Dados
- Valide a implementação
- Monitore problemas
- Dado limpo > mais dado

---

## Framework de Plano de Tracking

### Estrutura

```
Nome do Evento | Categoria | Propriedades | Gatilho | Notas
-------------- | --------- | ------------ | ------- | -----
```

### Tipos de Evento

| Tipo | Exemplos |
|------|----------|
| Pageviews | Automático, enriquecido com metadados |
| Ações do Usuário | Cliques, envio de formulário, uso de funcionalidade |
| Eventos de Sistema | Cadastro concluído, compra, mudança de assinatura |
| Conversões Customizadas | Metas concluídas, estágios de funil |

**Para listas completas de evento**: veja [references/event-library.md](references/event-library.md)

---

## Convenções de Nome de Evento

### Formato Recomendado: Objeto-Ação

```
cadastro_concluido
botao_clicado
formulario_enviado
artigo_lido
checkout_pagamento_concluido
```

### Boas Práticas
- Minúsculas com underscore
- Seja específico: `cta_hero_clicado` vs. `botao_clicado`
- Contexto vai nas propriedades, não no nome do evento
- Evite espaços e caracteres especiais
- Documente as decisões

---

## Eventos Essenciais

### Site de Marketing

| Evento | Propriedades |
|--------|--------------|
| cta_clicado | texto_botao, local |
| formulario_enviado | tipo_formulario |
| cadastro_concluido | metodo, origem |
| demo_solicitada | - |

### Produto/App

| Evento | Propriedades |
|--------|--------------|
| onboarding_passo_concluido | numero_passo, nome_passo |
| funcionalidade_usada | nome_funcionalidade |
| compra_concluida | plano, valor |
| assinatura_cancelada | motivo |

**Para biblioteca completa por tipo de negócio**: veja [references/event-library.md](references/event-library.md)

---

## Propriedades de Evento

### Propriedades Padrão

| Categoria | Propriedades |
|-----------|--------------|
| Página | page_title, page_location, page_referrer |
| Usuário | user_id, user_type, account_id, plan_type |
| Campanha | source, medium, campaign, content, term |
| Produto | product_id, product_name, category, price |

### Boas Práticas
- Use nomes de propriedade consistentes
- Inclua contexto relevante
- Não duplique propriedades automáticas
- Evite PII nas propriedades (LGPD)

---

## Implementação GA4

### Setup Rápido

1. Crie a propriedade GA4 e o data stream
2. Instale via GTM (`${RESOURCE_ID}`)
3. Habilite a medição aprimorada
4. Configure eventos customizados
5. Marque conversões no Admin

### Exemplo de Evento Customizado

```javascript
gtag('event', 'cadastro_concluido', {
  'metodo': 'email',
  'plano': 'gratis'
});
```

**Para implementação detalhada de GA4**: veja [references/ga4-implementation.md](references/ga4-implementation.md)

---

## Google Tag Manager

### Estrutura do Container

| Componente | Propósito |
|------------|-----------|
| Tags | Código que executa (GA4, pixels) |
| Triggers | Quando as tags disparam (page view, clique) |
| Variables | Valores dinâmicos (texto do clique, data layer) |

### Padrão de Data Layer

```javascript
dataLayer.push({
  'event': 'formulario_enviado',
  'form_name': 'contato',
  'form_location': 'rodape'
});
```

**Para implementação detalhada de GTM**: veja [references/gtm-implementation.md](references/gtm-implementation.md)

---

## Estratégia de Parâmetros UTM

### Parâmetros Padrão

| Parâmetro | Propósito | Exemplo |
|-----------|-----------|---------|
| utm_source | Fonte de tráfego | google, newsletter |
| utm_medium | Meio | cpc, email, social |
| utm_campaign | Nome da campanha | promo_outono |
| utm_content | Diferenciar versões | hero_cta |
| utm_term | Palavra-chave de busca paga | tenis+corrida |

### Convenções de Nome
- Tudo em minúsculas
- Use underscore ou hífen de forma consistente
- Específico mas conciso: `blog_rodape_cta`, não `cta1`
- Documente todos os UTMs numa planilha

---

## Depuração e Validação

### Ferramentas de Teste

| Ferramenta | Usar para |
|------------|-----------|
| GA4 DebugView | Monitorar eventos em tempo real |
| GTM Preview Mode | Testar triggers antes de publicar |
| Extensões de navegador | Tag Assistant, dataLayer Inspector |

### Checklist de Validação

- [ ] Eventos disparando nos gatilhos certos
- [ ] Valores de propriedade populando corretamente
- [ ] Sem eventos duplicados
- [ ] Funciona em navegadores e mobile
- [ ] Conversões registradas corretamente
- [ ] Sem vazamento de PII

### Problemas Comuns

| Problema | Verifique |
|----------|-----------|
| Eventos não disparam | Config do trigger, GTM carregado |
| Valores errados | Caminho da variável, estrutura do data layer |
| Eventos duplicados | Múltiplos containers, trigger disparando 2x |

---

## Privacidade e Conformidade (LGPD)

### Considerações
- Consentimento de cookies obrigatório (LGPD no Brasil; GDPR na UE)
- Sem PII nas propriedades de analytics
- Configurações de retenção de dados
- Capacidade de exclusão de dados do titular

### Implementação
- Use consent mode (espere o consentimento)
- Anonimização de IP
- Colete só o necessário
- Integre com plataforma de gestão de consentimento

---

## Formato de Saída

### Documento de Plano de Tracking

```markdown
# Plano de Tracking [Site/Produto]

## Visão Geral
- Ferramentas: GA4, GTM (${RESOURCE_ID})
- Última atualização: [Data]

## Eventos

| Nome do Evento | Descrição | Propriedades | Gatilho |
|----------------|-----------|--------------|---------|
| cadastro_concluido | Usuário conclui cadastro | metodo, plano | Página de sucesso |

## Dimensões Customizadas

| Nome | Escopo | Parâmetro |
|------|--------|-----------|
| user_type | Usuário | user_type |

## Conversões

| Conversão | Evento | Contagem |
|-----------|--------|----------|
| Cadastro | cadastro_concluido | Uma vez por sessão |
```

---

## Perguntas Específicas da Tarefa

1. Que ferramentas você usa (GA4, etc.)?
2. Quais ações-chave quer rastrear?
3. Que decisões esses dados vão informar?
4. Quem implementa — time de dev ou marketing?
5. Há requisitos de privacidade/consentimento (LGPD)?
6. O que já é rastreado?

---

## Integrações de Ferramentas (Stack HAOS)

| Ferramenta | Melhor para | Onde |
|------------|-------------|------|
| **GTM** (`${RESOURCE_ID}`) | Gestão de tags (padrão obrigatório) | Snippet head + body |
| **GA4** | Web analytics | Via GTM |
| **Supabase** | Armazenamento de eventos próprios | API (TOOLS.md) |
| **BI interno** | Dashboards (agente bi-engineer) | Hetzner |

Para implementação de eventos e pixels, acione o agente **tracking-engineer**.

---

## Skills Relacionadas

- **ab-testing**: para tracking de experimentos
- **seo-optimizer**: para análise de tráfego orgânico
- **cro**: para otimização de conversão (usa estes dados)
- **ads**: para tracking de conversão de mídia paga

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
