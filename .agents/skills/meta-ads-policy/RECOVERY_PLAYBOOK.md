# Recovery Playbook — Conta Meta Desabilitada

## FLUXO COMPLETO (passo a passo)

### Passo 0: NÃO FAZER (próximas 24h)

❌ NÃO criar BM nova em paralelo (circumvention = banimento permanente do CNPJ)
❌ NÃO trocar método de pagamento agora
❌ NÃO remover/trocar admin da BM
❌ NÃO falar do caso publicamente marcando Meta
❌ NÃO rodar campanhas agressivas em outras contas da mesma BM
❌ NÃO desconectar/reconectar ManyChat durante análise

### Passo 1: Coleta de evidências (15 min)

Antes de clicar em "Solicitar análise", reunir:
- [ ] Screenshot da tela de desabilitação (motivo + data + ativos afetados)
- [ ] Screenshot do Account Quality dashboard
- [ ] ID da conta de anúncios
- [ ] CNPJ + contrato social em PDF
- [ ] Comprovante de endereço (até 90 dias)
- [ ] Documento do admin principal (RG/CNH)
- [ ] Print da campanha que disparou o flag (estrutura, copy, criativo)
- [ ] Confirmação que ManyChat aparece como app autorizado

### Passo 2: Apelação formal (5 min)

1. Acessar Business Manager → Qualidade da Conta (Account Quality)
2. Selecionar conta desabilitada
3. Clicar em "Solicitar análise" / "Request Review"
4. Colar texto de apelação (ver `APPEAL_TEMPLATES.md`)
5. Submeter UMA vez
6. Salvar screenshot do envio com timestamp

### Passo 3: Aguardar (24h a 21 dias)

- **Categoria "Unusual Activity":** janela típica 5-21 dias
- **Não enviar segunda apelação antes de 72h**
- **Não criar outros casos em paralelo**
- **Monitorar email do admin principal e BM notifications**

### Passo 4: Se aprovado

Pular para `POST_REACTIVATION_PLAN.md` (90 dias probatórios)

### Passo 5: Se negado (1ª vez)

1. Aguardar 72h adicionais
2. Abrir chat com suporte Meta Business (Ajuda > Falar com Representante)
3. Usar mesmo texto da apelação como base
4. Em paralelo: abrir ticket ManyChat (user-000010@account.example.invalid)
   - Mencionar ID da conta
   - Mencionar que campanha MESSAGES integrada disparou flag
   - Pedir confirmação de que integração é legítima (eles são Meta Business Partner)
5. Após receber protocolo do ManyChat, abrir segunda apelação anexando

### Passo 6: Se negado (2ª vez)

1. NÃO insistir mais pelo dashboard padrão (canal fecha após 2 apelações)
2. Acionar parceiro Meta certificado no Brasil
   - Agências com selo Meta Business Partner Premier
   - Têm canal interno de escalação
3. Custo típico: R$ <USER_AMOUNT>-2.000 por recuperação
4. Taxa de sucesso adicional: ~50%

### Passo 7: Se negado (3ª vez)

1. Aceitar a perda da conta
2. NÃO usar mesmo CNPJ/CPF para nova BM (circumvention permanente)
3. Migrar para CNPJ secundário (ex: Editora Mindset em vez de SIM)
4. Cartão de crédito DIFERENTE
5. IP/dispositivo DIFERENTE
6. Esperar 90 dias antes de tentar

## REGRAS DE OURO

1. **Janela de 24h vale 74% sucesso. Janela de 7 dias vale 31%.** Apele HOJE.
2. **Uma apelação por vez.** Spammar reseta a fila.
3. **Inglês > PT-BR** para fila internacional (mais rápida).
4. **130-170 palavras** no texto. Não mais.
5. **Zero vitimismo, zero acusação.**
6. **Documentação pronta em 2h** se Meta pedir. Demora = caso arquivado.
7. **Pós-reativação: 90 dias probatórios.** Sem isso, cai de novo em 2 semanas.

## ESCALAÇÃO POR GASTO

| Gasto mensal declarado | Canal disponível |
|---|---|
| < US$ 100 | Apenas Account Quality + email |
| US$ 100-1.000 | + Chat Business Help (lento) |
| US$ 1.000-10.000 | + Chat Live Help (prioritário) |
| ≥ US$ 10.000 | + Meta Marketing Pro / Account Rep |

## CHECKPOINT: O QUE O REVIEWER VAI VERIFICAR

Antes de aprovar reativação, reviewer Meta checa:
1. CNPJ ativo e regular
2. Domínio verificado no BM
3. 2FA em todos os admins
4. System User configurado (se BM business)
5. Pixel ativo, sem eventos suspeitos
6. Histórico de pagamento limpo
7. User feedback nas últimas campanhas (taxa de "ocultar" e "denunciar")
8. Padrão de gasto coerente (sem picos)
9. Conexão ManyChat / Zapier autorizada via System User (não admin pessoal)

Se TODOS verdes → reativação. Se 2+ vermelhos → negação.

