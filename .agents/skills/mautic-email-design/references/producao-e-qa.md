# Produção e QA do e-mail editorial

## Preparar

1. Retomar checkpoint e distinguir artefatos locais da versão publicada. Registrar IDs/rotas de destino a preservar.
2. Ler piloto aprovado e feedback mais recente. Antes de criar skill nova, buscar padrão existente em skills/playbooks; atualizar este padrão por evidência, não preferências inferidas.
3. Definir uma função, assunto, pré-header, cena, CTA e URL por mensagem. Copy pronta antes de produzir o hero definitivo.
4. Congelar assinatura, ícones, rodapé e tokens. Mudanças de conteúdo não devem alterar automações.

## Produzir

5. Escrever narrativa que dependa do produto. Cena ilustrativa não é depoimento. Usar urgência baseada em fato ou decisão presente, sem vencimento fictício.
6. Gerar uma arte específica por mensagem com GPT Imagens; inspecionar referências e resultado. Arquivar prompt e origem, copiar ativo ao projeto e manter versão anterior.
7. Renderizar HTML responsivo e plainText. Preservar cabeçalho aprovado e variar apenas o que atende à função da mensagem.
8. Construir UTMs com parser de URL; manter o cupom como parâmetro separado. Não concatenar segundo `?` nem perder os parâmetros existentes.

## Validar

- Inventário: quantidade de e-mails, IDs e cenas distintos; não chamar dois pilotos de sequência completa.
- Copy: grafia PT-BR, mecanismo, assunto coerente, preços e condições sustentados; ausência de comentários internos/POWER FIELD/marcadores pendentes.
- Links: CTA principal correto por etapa, cupom e UTMs intactos; redes e suporte corretos; tokens Mautic preservados.
- Assets: todos carregam, sem recortes indevidos, identidade de usuario fiel à referência; assinatura original e WhatsApp no tom comum.
- Layout: conferir desktop e 390px (320px se necessário), corpo/CTA legíveis, sem overflow, suporte em uma linha, rodapé sem nome digitado e sem cidade.
- HTML abaixo do limite de corte do cliente; piloto é inferior a 80KB. Não usar imagem base64 inline ou paths locais em produção.
- Capturar evidência da versão realmente renderizada. Detector estático não substitui a inspeção visual.

## Publicar apenas quando em escopo autorizado

9. Ler versão viva e comparar com baseline; não sobrescrever divergência desconhecida. Backup dos campos que serão alterados.
10. Fazer upload de ativos aprovados em destino público adequado, validar HTTP/conteúdo e renderizar URLs remotas.
11. Atualizar somente os campos aprovados (HTML/plainText/assunto/pré-header). Readback exato antes de afirmar publicação.
12. Teste apenas para destinatário autorizado; registrar template/horário/recibo. Não confundir aceitação com entrega; não reenviar cegamente após timeout.
13. Preservar DNC, supressão por compra e atribuição; não reiniciar a régua nem resetar estágio do lead para validar estética.

## Evidência e evolução

Fonte de aprovação: pedido do usuario sobre pilotos v4, assinatura e exclusão da cidade; checkpoint `<USER_DEPENDENCY:docs/ritos/email-remarketing-presente-20260915/redesign-v4/checkpoint.md>`. Registrar evolução com task_id/revision existente, proveniência e readback por destino. Nunca converter pendência de 12 peças, publicação ou entrega em sucesso por haver plano.
