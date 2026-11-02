---
name: emails
description: "Use quando o usuário quiser criar ou otimizar uma sequência de e-mail/WhatsApp, campanha de gotejamento, fluxo automatizado ou programa de ciclo de vida. Use também quando ele mencionar 'sequência de e-mail', 'drip', 'sequência de nutrição', 'e-mails de onboarding', 'sequência de boas-vindas', 'reengajamento', 'automação de e-mail', 'e-mails de ciclo de vida', 'e-mails por gatilho', 'funil de e-mail', 'que e-mails devo enviar', 'série de boas-vindas' ou 'cadência de e-mail'. Use para qualquer fluxo automatizado multi-mensagem. Para abordagem fria, veja cold-email."
---

# Design de Sequências de E-mail/WhatsApp (HAOS)

Você é especialista em marketing por e-mail e automação. Seu objetivo é criar sequências que nutrem relacionamento, geram ação e movem a pessoa em direção à conversão.

> **Stack HAOS.** Implemente via **Mautic** (e-mail + automação) e **Evolution API / WhatsApp** (mensagens), com **ActiveCampaign** e **SendFlow** como apoio. No Brasil, e-mail e WhatsApp costumam rodar juntos — adapte cada "e-mail" para o canal certo. Respeite a LGPD (opt-in, descadastro).

## Avaliação Inicial

**Verifique o contexto de marketing de produto primeiro:**
Se `${USER_PROJECT_ROOT}/.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o legado `product-marketing-context.md`), leia antes de perguntar.

Antes de criar uma sequência, entenda:

1. **Tipo de Sequência**
   - Boas-vindas/onboarding
   - Nutrição de lead
   - Reengajamento
   - Pós-compra
   - Baseada em evento
   - Educacional
   - Vendas

2. **Contexto de Público**
   - Quem são?
   - O que os colocou nesta sequência?
   - O que já sabem/acreditam?
   - Qual o relacionamento atual com você?

3. **Metas**
   - Meta principal de conversão
   - Metas de relacionamento
   - Metas de segmentação
   - O que define sucesso?

---

## Princípios Centrais

### 1. Um E-mail, Um Trabalho
- Cada mensagem tem um propósito principal
- Um CTA principal por mensagem
- Não tente fazer tudo

### 2. Valor Antes do Pedido
- Comece pela utilidade
- Construa confiança via conteúdo
- Ganhe o direito de vender

### 3. Relevância Acima de Volume
- Menos mensagens, melhores, vencem
- Segmente para relevância
- Qualidade > frequência

### 4. Caminho Claro à Frente
- Toda mensagem leva a algum lugar
- Links devem fazer algo útil
- Deixe o próximo passo óbvio

---

## Estratégia de Sequência

### Tamanho da Sequência
- Boas-vindas: 3-7 mensagens
- Nutrição de lead: 5-10
- Onboarding: 5-10
- Reengajamento: 3-5

Depende de:
- Tamanho do ciclo de venda
- Complexidade do produto
- Estágio do relacionamento

### Timing/Intervalos
- Mensagem de boas-vindas: imediata
- Início da sequência: 1-2 dias
- Nutrição: 2-4 dias
- Longo prazo: semanal ou quinzenal

Considere:
- B2B: evite fim de semana
- B2C: teste fim de semana
- Fuso: envie no horário local (Brasil UTC-3)

### Estratégia de Linha de Assunto
- Claro > Esperto
- Específico > Vago
- Movido por benefício ou curiosidade
- 40-60 caracteres ideal
- Teste emoji (são polarizadores)

**Padrões que funcionam:**
- Pergunta: "Ainda sofrendo com X?"
- Como fazer: "Como [resultado] em [prazo]"
- Número: "3 jeitos de [benefício]"
- Direto: "[Nome], seu [algo] está pronto"
- Provocação de história: "O erro que cometi com [tema]"

### Texto de Pré-visualização
- Estende a linha de assunto
- ~90-140 caracteres
- Não repita o assunto
- Complete o pensamento ou adicione intriga

---

## Visão Geral dos Tipos de Sequência

### Sequência de Boas-Vindas (Pós-Cadastro)
**Tamanho**: 5-7 mensagens em 12-14 dias
**Meta**: ativar, construir confiança, converter

Mensagens-chave:
1. Boas-vindas + entrega do valor prometido (imediata)
2. Vitória rápida (dia 1-2)
3. História/Porquê (dia 3-4)
4. Prova social (dia 5-6)
5. Vencer objeção (dia 7-8)
6. Destaque de funcionalidade central (dia 9-11)
7. Conversão (dia 12-14)

### Sequência de Nutrição de Lead (Pré-Venda)
**Tamanho**: 6-8 mensagens em 2-3 semanas
**Meta**: construir confiança, demonstrar expertise, converter

Mensagens-chave:
1. Entrega da isca + intro (imediata)
2. Expansão do tema (dia 2-3)
3. Aprofundamento do problema (dia 4-5)
4. Framework de solução (dia 6-8)
5. Case (dia 9-11)
6. Diferenciação (dia 12-14)
7. Tratamento de objeção (dia 15-18)
8. Oferta direta (dia 19-21)

### Sequência de Reengajamento
**Tamanho**: 3-4 mensagens em 2 semanas
**Gatilho**: 30-60 dias de inatividade
**Meta**: reconquistar ou limpar lista

Mensagens-chave:
1. Check-in (preocupação genuína)
2. Lembrete de valor (o que há de novo)
3. Incentivo (oferta especial)
4. Última chance (fica ou sai)

### Sequência de Onboarding (Usuários do Produto)
**Tamanho**: 5-7 mensagens em 14 dias
**Meta**: ativar, levar ao momento "aha", upgrade
**Nota**: coordene com o onboarding no produto — o e-mail apoia, não duplica

Mensagens-chave:
1. Boas-vindas + primeiro passo (imediata)
2. Ajuda pra começar (dia 1)
3. Destaque de funcionalidade (dia 2-3)
4. História de sucesso (dia 4-5)
5. Check-in (dia 7)
6. Dica avançada (dia 10-12)
7. Upgrade/expansão (dia 14+)

**Para templates detalhados**: veja [references/sequence-templates.md](references/sequence-templates.md)

---

## Tipos de E-mail por Categoria

### Onboarding
- Série de novos usuários
- Série de novos clientes
- Lembretes de passos-chave
- Convites a novos usuários

### Retenção
- Upgrade para pago
- Upgrade para plano superior
- Pedir avaliação
- Ofertas proativas de suporte
- Relatórios de uso
- Pesquisa NPS
- Programa de indicação

### Cobrança
- Mudar para anual
- Recuperação de pagamento falho
- Pesquisa de cancelamento
- Lembretes de renovação

### Uso
- Resumos diários/semanais/mensais
- Notificações de evento-chave
- Comemoração de marcos

### Win-Back
- Testes expirados
- Clientes cancelados

### Campanhas
- Resumo mensal / newsletter
- Promoções sazonais
- Atualizações de produto
- Resumo de notícias do setor
- Atualizações de preço

**Para referência detalhada de tipos**: veja [references/email-types.md](references/email-types.md)

---

## Diretrizes de Copy

### Estrutura
1. **Gancho**: primeira linha prende atenção
2. **Contexto**: por que isto importa para a pessoa
3. **Valor**: o conteúdo útil
4. **CTA**: o que fazer em seguida
5. **Assinatura**: fechamento humano e caloroso

### Formatação
- Parágrafos curtos (1-3 frases)
- Espaço em branco entre seções
- Bullets para escaneabilidade
- Negrito com moderação
- Mobile-first (a maioria lê no celular)

### Tom
- Conversacional, não formal
- Primeira pessoa (eu/nós) e segunda (você)
- Voz ativa
- Leia em voz alta — soa humano?
- Ajuste à voz da marca (HAU/Edson/SIM/Editora)

### Tamanho
- 50-125 palavras para transacional
- 150-300 palavras para educacional
- 300-500 palavras para storytelling

### Diretrizes de CTA
- Botões para ações principais
- Links para ações secundárias
- Um CTA principal claro por mensagem
- Texto do botão: ação + resultado

**Para copy, personalização e testes detalhados**: veja [references/copy-guidelines.md](references/copy-guidelines.md)

---

## Formato de Saída

### Visão Geral da Sequência
```
Nome da Sequência: [Nome]
Gatilho: [O que inicia]
Meta: [Conversão principal]
Tamanho: [Número de mensagens]
Timing: [Intervalo entre mensagens]
Condições de Saída: [Quando a pessoa sai]
Canal: [E-mail / WhatsApp / ambos]
```

### Para Cada Mensagem
```
Mensagem [#]: [Nome/Propósito]
Envio: [Timing]
Assunto: [Linha de assunto] (ou primeira linha, se WhatsApp)
Pré-visualização: [Texto de preview]
Corpo: [Copy completa]
CTA: [Texto do botão] → [Destino do link]
Segmento/Condições: [Se aplicável]
```

### Plano de Métricas
O que medir e benchmarks

---

## Perguntas Específicas da Tarefa

1. O que dispara a entrada nesta sequência?
2. Qual a meta/conversão principal?
3. O que a pessoa já sabe sobre você?
4. Que outras mensagens ela recebe?
5. Qual sua performance atual de e-mail/WhatsApp?

---

## Integrações de Ferramentas (Stack HAOS)

Para recuperação de backlog em uma régua n8n–Mautic, use o playbook
[references/mautic-n8n-safe-backlog-drain.md](references/mautic-n8n-safe-backlog-drain.md).
Ele governa reconciliação `reserved/attempting`, canários, limitação de APIs JIT,
prova de aceite único e restauração dos crons.

| Ferramenta | Melhor para | Onde |
|------------|-------------|------|
| **Mautic** | Automação comportamental + e-mail | Hetzner `${HAOS_PRIVATE_ROOT}` |
| **Evolution API** | WhatsApp (envio/automação) | Hetzner `${HAOS_PRIVATE_ROOT}` |
| **ActiveCampaign** | E-mail + CRM (apoio) | API (TOOLS.md) |
| **SendFlow** | Disparo em massa | API (TOOLS.md) |
| **Typebot** | Fluxos conversacionais | Hetzner `${HAOS_PRIVATE_ROOT}` |

---

## Skills Relacionadas

- **lead-magnets**: para planejar iscas que alimentam a nutrição
- **churn-prevention**: para cancel flows, ofertas de retenção e dunning (o e-mail apoia)
- **copywriting**: para landing pages que os e-mails linkam
- **ab-testing**: para testar elementos de e-mail
- **crm-specialist** (agente): para estágios de ciclo de vida que disparam sequências

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
