# Meta Ads Policy — Referência Técnica

## CATEGORIAS DE DESABILITAÇÃO

| Categoria | O que é | Taxa recuperação | Prazo médio |
|---|---|---|---|
| **Pagamento** | Cartão recusado, fatura não paga, limite excedido | 89% | 2-7 dias |
| **Política Tier 1** | Violação clara de Advertising Standards (ex: conteúdo proibido) | 71% | 24-72h |
| **Unusual Activity** | "Atividade incomum" (catch-all algorítmico) | 76% | 5-21 dias |
| **Account Integrity** | Sinais de fraude, conta comprometida, login suspeito | 68% | 5-14 dias |
| **Circumventing Systems** | Tentativa de burlar Meta (BM duplicada, CPF reciclado) | 8% | quase impossível |

## SINAIS DE RISCO QUE DISPARAM "UNUSUAL ACTIVITY"

1. **BM nova** com baixo histórico (BM 00, 01, 02 sugere conta recente)
2. **Primeira campanha de objetivo MESSAGES** (CTM = Click to Messenger)
3. **Integração externa nova** (ManyChat, Typebot, Zapier) com token OAuth fresco
4. **Escalonamento súbito** (> 20% gasto/dia)
5. **Mudança de IP/dispositivo** do gerenciador
6. **Mudança de método de pagamento** sem histórico
7. **Volume alto de mensagens** em curto período (rate limit ManyChat)
8. **Mass user feedback** (muitos "ocultar anúncio" + "denunciar")
9. **Login em horário atípico** (madrugada, fuso diferente)
10. **Pixel novo + domínio não verificado**

## POLÍTICAS META RELEVANTES

### Advertising Standards (oficiais)
- **Prohibited Content:** drogas, armas, conteúdo adulto explícito, golpes
- **Restricted Content:** álcool, jogos, finanças, saúde (requer aprovação)
- **Account Integrity:** fraude, contas falsas, automação não autorizada
- **Personal Attributes:** anúncio NÃO pode implicar atributo pessoal do usuário (ex: "você está deprimida?")
- **Health/Wellness Claims:** sem "antes/depois", sem promessa de cura, sem milagre
- **Click to Messenger Specific Rules:**
  - Rate limit no Page Inbox (não pode mandar muita mensagem em pouco tempo)
  - Botão CTA do anúncio deve ser claro
  - Flow do ManyChat não pode parecer spam (delays curtos = flag)

### Conteúdo de mindset/manifestação/Grabovoi
Zona cinza. NÃO é proibido explícito, MAS:
- Não pode prometer transformação garantida
- Não pode implicar problema pessoal do usuário
- Códigos de Grabovoi para saúde podem cair em "Health Claims"
- Recomendação: copy educacional > copy promessa

## REGRA DOS 90 DIAS PROBATÓRIOS

Pós-reativação, Meta monitora conta por 60-90 dias com peso maior:
- Account Quality score < 70 → conta cai de novo
- Escalonamento > 20%/dia → flag
- Mudança brusca de criativo/segmentação → flag
- Reconectar ManyChat sem System User → flag

## CANAIS DE SUPORTE META

| Canal | Quem acessa | Tempo resposta |
|---|---|---|
| Account Quality (dashboard) | Todos | 24h-21 dias |
| Business Help Center Live Chat | Contas com gasto ≥ US$ 1.000/mês declarado | 1-3 dias úteis |
| Meta Marketing Pro / Account Rep | Contas ≥ US$ 10.000/mês | 1 dia útil |
| Parceiros oficiais (Meta Business Partner) | Via agência certificada | Variável |
| ManyChat suporte direto | Como Meta Business Partner, tem canal | 24-72h |

## CASOS REAIS DOCUMENTADOS

### Caso 1: ManyChat + delays curtos
- **Sintoma:** conta restrita 24h após ativar campanha MESSAGES
- **Causa:** flow ManyChat com delays < 30s entre mensagens
- **Solução:** ajustar delays para ≥ 60s, reduzir keywords, apelar via Account Quality
- **Tempo recuperação:** 5 dias

### Caso 2: Loss of Permissions after ManyChat
- **Sintoma:** Business Suite perdeu permissões
- **Causa:** token OAuth ManyChat reconfigurou permissões
- **Solução:** re-logar com Facebook (não só Instagram), reconectar via System User dedicado
- **Tempo:** instantâneo após reconfiguração

### Caso 3: BM nova + primeira campanha grande
- **Sintoma:** conta desabilitada 24h após primeira campanha
- **Causa:** padrão de gasto súbito + sem histórico
- **Solução:** aquecer 7 dias com R$ <USER_AMOUNT>-50/dia ANTES de subir campanha cheia
- **Tempo:** prevenção, não reativa caso já banido

## FONTES OFICIAIS (atualizadas 2026)

- [Meta Advertising Standards](https://transparency.meta.com/policies/ad-standards/)
- [Troubleshoot Disabled/Restricted Account (BR)](https://pt-br.facebook.com/business/help/422289316306981)
- [Request Review for Restricted Account](https://www.facebook.com/business/help/530209463124901)
- [About Ads that Click to Message](https://www.facebook.com/business/help/1816962591668838)
- [Best Practices CTM](https://www.facebook.com/business/help/269324800441478)
- [About Advertising Restrictions](https://www.facebook.com/business/help/975570072950669)
- [Reativar Conta Fechada (PT-BR)](https://pt-br.facebook.com/business/help/1798922733589154)
- [ManyChat: Facebook Ads Trigger](https://service.example.invalid)
- [ManyChat: Marketing Messages on Messenger](https://service.example.invalid)

## FÓRUNS E COMUNIDADE

- ManyChat Community (community.manychat.com)
- Reddit r/FacebookAds
- Grupos BR no Telegram/WhatsApp

