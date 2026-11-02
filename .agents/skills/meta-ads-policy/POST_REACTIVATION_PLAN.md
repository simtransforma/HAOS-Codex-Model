# Plano 90 Dias Probatórios (Pós-Reativação)

## CONTEXTO

Após reativação de uma conta Meta desabilitada, a conta entra em "modo probatório" por 60-90 dias. Account Quality dashboard tem peso maior, qualquer flag derruba de novo.

**Taxa de re-banimento sem plano probatório: 38% em 30 dias.**
**Taxa com plano probatório seguido: 6% em 90 dias.**

## DIA 0 (IMEDIATO)

Antes de QUALQUER campanha:

- [ ] 2FA ativado em TODOS os admins do BM
- [ ] System User dedicado criado para ManyChat (não usar token de admin pessoal)
- [ ] Domínio verificado no Business Manager (verified domain)
- [ ] Verificação de negócio (Business Verification) com CNPJ
- [ ] Pixel verificado funcionando
- [ ] CAPI (Conversions API) configurada se possível
- [ ] Método de pagamento principal + backup
- [ ] Admin secundário de segurança (caso o principal seja bloqueado)

## DIAS 1-14 (FASE 1: AQUECIMENTO)

### Regras
- Gasto diário MÁXIMO: R$ <USER_AMOUNT>-100 (mínimo viável)
- NÃO criar campanha MESSAGES nesse período
- Apenas objetivos: TRAFFIC ou ENGAGEMENT
- Criativos: vídeo institucional, depoimento real, conteúdo educacional
- ZERO "antes/depois", ZERO promessa, ZERO clickbait

### Por quê
Meta precisa ver padrão "saudável" antes de liberar escalas. Subir agressivamente nessa fase = re-banimento garantido.

### Checkpoint diário
- Account Quality score ≥ 80 (ideal 90+)
- User feedback negativo < 5%
- CTR > 1%
- Nenhum aviso de policy review

## DIAS 15-30 (FASE 2: REINTRODUÇÃO)

### Regras
- Gasto pode subir até R$ <USER_AMOUNT>-300/dia
- Aumentar MÁXIMO 20% por dia (regra anti-flag)
- Reintroduzir MESSAGES gradualmente
  - Começar com 1 campanha pequena (R$ <USER_AMOUNT>-50/dia)
  - ManyChat flow com delays ≥ 60s entre mensagens
  - Zero keywords agressivas
  - Zero envio em massa
- Monitorar "user feedback" no dashboard DIARIAMENTE

### Triggers de recuo (voltar pra Fase 1)
- Account Quality score < 75
- User feedback > 8%
- Aviso de policy review
- Anúncio rejeitado

## DIAS 31-60 (FASE 3: ESCALA CONTROLADA)

### Regras
- Gasto pode escalar normalmente (sempre máx +20%/dia)
- Diversificar criativos (rodar 5-10 por conjunto)
- A/B testar copy ANTES de subir gasto
- Manter checkpoint semanal de Account Quality

### O que ainda NÃO fazer
- NÃO conectar outras ferramentas de automação além das já existentes
- NÃO mudar método de pagamento
- NÃO trocar admin principal
- NÃO desativar 2FA por nenhum motivo

## DIAS 61-90 (FASE 4: NORMALIZAÇÃO)

### Regras
- Escala normal (respeitando +20%/dia)
- Manter 2FA, System User, domínio verificado
- Backup BM secundário pode ser criado COM OUTRO CNPJ (ex: Editora Mindset)
  - NUNCA mesmo CNPJ (vincula histórico negativo)
  - NUNCA mesmo cartão (vincula histórico)
  - Idealmente outro IP/dispositivo

### Checkpoint mensal
- Account Quality score (manter ≥ 85)
- User feedback (manter < 5%)
- Custo por lead/venda (KPIs de negócio)

## REGRAS ESTRUTURAIS PERMANENTES (PÓS-90 DIAS)

Nunca relaxar nestas regras:

1. **Nunca escalar gasto > 20% por dia**
2. **Nunca conectar/desconectar tokens em horário comercial atípico** (madrugada)
3. **ManyChat flow:** delays ≥ 60s, sem keywords repetidas, sem mensagens em massa
4. **CTM ads:** criativo claro sobre o que o usuário vai receber, ZERO clickbait
5. **Pelo menos 1 BM backup** com Business Verification separada
6. **2FA SEMPRE ativo** em todos os admins
7. **System User para integrações** (nunca admin pessoal)
8. **Backup automático** dos públicos custom (não confiar 100% no Meta)
9. **Monitoramento diário** do Account Quality dashboard
10. **Pasta de evidências** sempre atualizada (CNPJ, contrato, prints) para próxima eventualidade

## ESPECÍFICO PARA NICHO MINDSET/MANIFESTAÇÃO

Conteúdo SIM (lei da atração, Grabovoi, manifestação) está em zona cinza:

### Permitido
- Conteúdo educacional sobre o método
- Depoimentos reais (com permissão)
- Apresentação do produto sem promessa garantida
- "Você pode aprender X" (não "Você vai conseguir Y")

### Proibido (mesmo que pareça inofensivo)
- "Manifeste R$ <USER_AMOUNT>il em 21 dias" (promessa financeira)
- "Cure ansiedade com este código" (promessa de saúde)
- "Antes/depois" (transformação implicada)
- "Você está atraindo o que merece?" (atributo pessoal)
- "Sem esforço, sem dieta, sem terapia" (negativa que implica problema)

### Estrutura segura de copy
> "Conheça o método que estuda a relação entre [conceito] e [resultado]. Educacional, sem promessas."

## DOCUMENTAÇÃO QUE DEVE FICAR PRONTA

Pasta sempre disponível (Drive ou local):
- CNPJ + contrato social (PDF)
- Comprovante de endereço (até 90 dias)
- RG/CNH do admin principal
- Histórico de faturamento das BMs
- Prints de Account Quality dos últimos 30 dias
- Lista de campanhas ativas + criativos
- Lista de integrações autorizadas (ManyChat, etc)

Quando Meta pedir, anexar em ≤ 2h. Demora = caso arquivado.

