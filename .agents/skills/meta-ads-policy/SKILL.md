---
name: meta-ads-policy
description: "Especialista em pol\u00edticas Meta Ads, restri\u00e7\u00f5es de conta, recupera\u00e7\u00e3o (Request a Review) e preven\u00e7\u00e3o de banimento. Ativar SEMPRE que aparecer \"conta desabilitada\", \"atividade incomum\", \"ad account disabled\", \"policy violation\", \"request a review\", \"ManyChat + Meta restricted\", \"Click to Messenger ban\", \"BM nova\", ou qualquer assunto de Account Quality, Business Integrity, CTM ads, ou apela\u00e7\u00e3o Meta."
author: "HAOS / Gian Marco"
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

# Meta Ads Policy & Recovery Specialist

Especialista em políticas Meta (Facebook + Instagram Ads), restrições de conta, recuperação via Request a Review e prevenção de banimento.

## QUANDO ATIVAR

Ative esta skill em QUALQUER um destes cenários:
- Conta de anúncios desabilitada/restrita/suspensa
- Aviso de "Atividade Incomum" (Unusual Activity)
- Apelação pelo botão "Solicitar análise" / Request a Review
- Campanha rejeitada por política
- Integração ManyChat ou Typebot trazendo flag
- Criação de nova BM (Business Manager novo)
- Subir primeira campanha de objetivo MESSAGES (Click to Messenger)
- Mudança brusca de escala (escalonamento > 20%/dia)
- Configuração de System User, 2FA, verificação de domínio, verificação de negócio
- Compliance review pré-publicação de anúncio em nicho sensível (mindset, manifestação, saúde, finanças)

## PRINCÍPIOS CENTRAIS

1. **Janela 24h é ouro.** Apelação em ≤24h tem 74% de sucesso. Em ≥7 dias, cai pra 31%.
2. **Uma apelação por vez.** Nunca spammar. Spam reseta a fila.
3. **NUNCA criar BM nova em paralelo.** Meta classifica como circumvention = banimento permanente do CNPJ, CPF e cartão.
4. **Texto curto vence textão.** 130-170 palavras, 3 parágrafos, profissional.
5. **Inglês > português** na fila internacional (mais rápida), MAS PT-BR também funciona quando reviewer brasileiro pega o caso.
6. **Compliance demonstrado** vale mais que vitimismo. Mencione que conhece as políticas.

## REGRAS ABSOLUTAS DE COMUNICAÇÃO

- ZERO travessão "—" (em-dash). Regra global HAOS.
- ZERO vitimismo ("por favor me ajude desesperadamente")
- ZERO acusação à Meta ("isso é injusto")
- ZERO ameaças ("vou processar")
- ZERO referência a outras contas suas
- ZERO links externos antes de pedirem
- ZERO repetir a mesma apelação 3 vezes

## CONTEÚDO DA SKILL

Esta skill carrega 3 arquivos de referência sob demanda:

| Arquivo | Quando ler |
|---|---|
| `REFERENCE.md` | Políticas oficiais Meta + categorias de banimento + taxas de recuperação |
| `RECOVERY_PLAYBOOK.md` | Passo a passo de recuperação (Account Quality → Request Review → Chat) |
| `APPEAL_TEMPLATES.md` | Templates de texto de apelação (PT-BR e EN) por categoria |
| `POST_REACTIVATION_PLAN.md` | Plano 90 dias probatórios pós-reativação |

Leia o arquivo relevante ao contexto antes de responder. Não responda de memória.

## DELEGAÇÃO HAOS

Esta skill é usada principalmente por:
- `@traffic-master` (estratégia geral de mídia paga)
- `@media-buyer` (execução tática, mudanças em campanha)
- `@compliance-officer` (revisão pré-publicação de anúncio sensível)
- `@copy-specialist` (escrever texto de apelação)

Quando ativada via main, delegar a tarefa específica ao agente correspondente acima.

## VALIDAÇÃO ANTES DE ENTREGAR

Antes de retornar qualquer texto (apelação, copy de anúncio, mensagem ao reviewer):
1. Validar zero "—" no output
2. Validar tamanho (130-170 palavras para apelação)
3. Validar tom (profissional, sem emoção)
4. Validar estrutura (3 parágrafos: legitimidade + fato + compliance)
5. Validar idioma adequado ao canal (EN para fila internacional, PT-BR como backup)

## FONTES OFICIAIS

- Meta Advertising Standards: https://transparency.meta.com/policies/ad-standards/
- Troubleshoot Disabled Account (PT-BR): https://pt-br.facebook.com/business/help/422289316306981
- Request a Review: https://www.facebook.com/business/help/530209463124901
- About Ads that Click to Message: https://www.facebook.com/business/help/1816962591668838
- Best Practices CTM: https://www.facebook.com/business/help/269324800441478

Ver `REFERENCE.md` para lista completa de fontes.

