---
name: mautic-email-design
description: "Criar e revisar e-mails HTML no Mautic para usuario, SIM, usuario e usuario, preservando o padr\u00e3o aprovado de arte editorial, narrativa, assinatura e rodap\u00e9. N\u00e3o configura infraestrutura ou campanhas por si s\u00f3."
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

# Mautic: padrão editorial usuario/SIM

Use para novas peças ou revisões de conteúdo HTML no Mautic desta marca. O padrão nasceu dos pilotos usuario/usuario aprovados pelo usuario em setembro de 2026. Não imponha essa identidade a outras marcas nem trate a aprovação do padrão como permissão de envio.

## Fontes e composição

- Copy: carregar `usuario-burger-copy` e suas referências pertinentes.
- Layout: `haos-design` + `impeccable`; acabamento preserva o piloto aprovado.
- Arte raster: GPT Imagens integrado com `imagegen`. Cada mensagem precisa de uma cena própria, não só recorte ou troca de cor do mesmo master.
- Procedimento de produção e QA: [playbook](references/producao-e-qa.md).
- Referência canônica no repo: `<USER_DEPENDENCY:docs/ritos/email-remarketing-presente-20260915/redesign-v4/>`. Consultar `copy-prototypes.json`, `render_prototypes.py` e `<USER_DEPENDENCY:assets/usuario-e01-usuario-claro.png>`/`<USER_DEPENDENCY:assets/usuario-e01.png>` antes de alterar esse padrão.

## Identidade aprovada

usuario: fotografia humana cinematográfica, preto quente, dourado e marfim. Tipografia editorial com destaque serifado. Cena ligada ao conflito específico do e-mail, sem futurismo.

usuario: arte clara, acolhedora, marfim/azul suave/ouro, texto azul profundo. Não copiar o visual escuro do usuario nem reintroduzir silhuetas sombrias, orbes ou POWER FIELD. Usar retrato de usuario apenas com referência real fornecida, preservando identidade; personagens ilustrativos não são participantes ou depoimentos reais.

A referência de rosto não obriga repetir a mesma pose em todos os headers. Variar gesto, enquadramento e expressão preservando identidade; manter a primeira arte aprovada. Quando houver ingresso online, apresentar as duas modalidades desde o header e início da copy: desejo pelo presencial sem excluir quem participa à distância. Verificar cartões e FAQ completos antes de citar benefícios; não prometer equivalência de técnicas quando a página for contraditória.

## Narrativa

Uma função dominante por mensagem: cena concreta, tensão reconhecível, reflexão, mecanismo específico do produto e próximo passo. Em storytelling, os pilotos usam aproximadamente 300–420 palavras; ajustar ao conteúdo, sem preencher com repetição. Assunto e pré-header complementares. Não inventar biografia, resultados, prazos, escassez ou equivalência de ingressos. 'Último e-mail da sequência' não significa 'cupom expira hoje'.

## Layout e CTA

- Coluna de até 640px; 24px laterais no celular; corpo 18px/30px.
- HTML de tabela com estilos inline e fontes de fallback. Hero responsivo com altura automática, sem recorte obrigatório.
- CTA principal é botão HTML real, dourado, alto contraste, texto maiúsculo legível. Não colocar o único CTA dentro da imagem.
- Texto essencial e oferta também em HTML/plainText, preservando entendimento com imagens bloqueadas.
- Variar cenas e argumentos; manter coerência de marca, leitura e rodapé. Não redesenhar tudo quando o pedido for um ajuste pontual.

## Assinatura e rodapé fixos

1. Assinatura original preta transparente, em área clara, aproximadamente 230px de largura. Não recriar com fonte e não acrescentar nome digitado abaixo.
2. Logo abaixo, seis ícones PNG transparentes: Instagram, Facebook, X, LinkedIn, Pinterest e WhatsApp. Mesmo tom `#282521`, ícone de 24px, alvo de 44px. WhatsApp por último, não em fileira separada.
3. Abaixo, texto em uma linha alinhado à esquerda: `Precisa de ajuda? Fale com o suporte`, link `https://service.example.invalid`.
4. Razão social e CNPJ aprovados, Termos/Privacidade, `{webview_url}` e `{unsubscribe_url}`. Não esconder nem invalidar o descadastro.
5. Não incluir `São usuario - SP` no rodapé desse padrão. A cidade em informações factuais do evento é independente e deve permanecer quando pertinente.

Ativos base: assinatura e cinco redes em `redesign-v3/assets/`; WhatsApp monocromático em `redesign-v4/assets/icon-whatsapp-mono.png`. Preservar os originais. Referências locais precisam virar URLs públicas verificadas antes de publicação, sem vazamento de paths privados.

## Operação separada de design

Não alterar IDs, público, tags, cadência, DNC, UTMs, cupons ou condições de saída ao trocar copy/arte. No projeto presente/trilha, Mautic e automações de e-mail usam Hostinger; Clint/Lovable e monitoramento Assiny/Lia ficam no n8n Hetzner. Essa divisão é histórica do projeto, não prova de estado vivo. Verificar a fonte real antes de operação.

Produção exige aprovação do escopo, backup/readback e canário; aprovação visual não autoriza reenvio em massa. Aceitação SMTP ou email_stats não prova entrega na caixa de entrada. Falha ambígua de envio exige reconciliação antes de repetir.
