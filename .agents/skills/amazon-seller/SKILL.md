---
name: amazon-seller
description: "Opera o Amazon Seller Central e planeja ou implementa integrações com a Selling Partner API (SP-API), incluindo catálogo, preços, estoque, pedidos, relatórios, logística, Bling e preparação de anúncios. Use para registrar ou autorizar apps privados, diagnosticar permissões e erros SP-API, criar automações, analisar operação de marketplace ou orientar ações no Seller Central brasileiro."
---

# Amazon Seller e SP-API

## Escopo e fontes

Use esta skill para a operação da **${USER_BRAND}** na Amazon Brasil e para integrações privadas da organização. Leia as referências conforme a tarefa:

- `references/sp-api-operacao.md`: onboarding, autenticação, apps privados, APIs e segurança.
- `references/amazon-seller-br.md`: operação do Seller Central BR, Bling, anúncios e checklist de mudança.

Prefira a documentação oficial atual da Amazon. A página GitHub compartilhada no e-mail de aprovação foi migrada para o portal de documentação; não a trate como fonte técnica atual.

## Classificar antes de agir

| Pedido | Camada | Ação inicial |
|---|---|---|
| App, token, integração, pedido, catálogo, preço, estoque, relatório | SP-API | Mapear caso de uso -> operação -> papel (role) -> autorização. |
| Cadastro, oferta, frete, conta, desempenho ou recurso | Seller Central | Ler estado atual e política aplicável. |
| Sincronização fiscal/ERP | Bling + SP-API | Definir fonte de verdade, campos, frequência, idempotência e reconciliação. |
| Campanha patrocinada, lance, orçamento, relatório publicitário | Amazon Ads API | Tratar como produto separado da SP-API, com acesso e aprovação próprios. |

## Fluxo de integração privada

1. Confirmar que o objetivo atende apenas à própria organização. App privado é autoautorizado; não oferecer OAuth a terceiros nem publicar no Appstore.
2. Definir o menor conjunto de dados e operações necessário. Consultar os mapeamentos de roles antes de codificar.
4. Autorizar o app privado na conta vendedora e guardar credenciais LWA/refresh token somente em cofre ou variável de ambiente ignorada pelo Git. Nunca imprimir, colocar em planilha, chat, log, documento ou commit.
5. Implementar autenticação LWA OAuth 2.0, leitura de limites de taxa e retries com backoff. Não usar IAM/SigV4 para novas integrações: a SP-API não os requer desde 2023.
6. Validar uma operação somente leitura antes de criar mutações. Registrar ID de correlação, horário, marketplace e resposta sem PII.

## Marketplace Brasil

Usar `marketplaceId=${RESOURCE_ID}` para Brasil. Não inferir que uma API ou programa disponível nos EUA também está disponível no Brasil: confirmar a disponibilidade na documentação da operação.

## Escolher APIs pelo caso de uso

- **Catálogo e listagens:** Catalog Items, Product Type Definitions, Listings Items e Feeds. Validar schema e issues antes de publicar; preferir prévia/validação quando disponível.
- **Preço e competitividade:** Product Pricing e Product Fees. Não alterar preço automaticamente sem limite, margem mínima e aprovação configurada.
- **Pedidos e entrega:** Orders, Merchant Fulfillment, Shipping/Notifications. Minimizar PII; confirmar canal FBA/MFN antes de qualquer ação.
- **Estoque e logística:** FBA Inventory, Fulfillment Inbound, Supply Sources e Reports. Manter SKU e saldo reconciliáveis com o ERP.
- **Financeiro e BI:** Finances, Sales e Reports. Distinguir pedido, liquidação, taxa, estorno e saldo; nunca usar faturamento bruto como receita líquida.
- **Bling:** documentar mapeamento SKU/ASIN, pedido, status, rastreio, NF, estoque e exceções. Criar reconciliação em vez de sincronização cega.

## Dados restritos e segurança

- Solicitar somente os roles estritamente necessários; falta de role normalmente retorna 403.
- Tratar PII de comprador, endereço, telefone, e-mails e relatórios restritos como dados sensíveis. Para APIs legadas restritas, usar Restricted Data Token (RDT) quando exigido; para Orders API v2026-01-01, seguir a regra de roles atual da Amazon.
- Criptografar segredos e dados em trânsito/repouso, limitar acesso por função, registrar incidentes e reter dados somente pelo tempo necessário.
- Nunca copiar PII para prompts, tickets, planilhas públicas ou logs. Redigir IDs e campos sensíveis nos diagnósticos.

## Diagnóstico

Para erro de API, coletar sem segredos: endpoint/operação, versão, marketplace, HTTP status, request ID, role esperado, horário e se a chamada era sandbox ou produção. Então verificar, nesta ordem: autorização LWA, app autorizado, role, marketplace, payload/schema, versão, rate limit e status da API.

## Saída esperada

Entregar sempre: objetivo, dados acessados, APIs/roles necessários, riscos, plano de teste, aprovação necessária e reversão. Dizer claramente o que foi apenas planejado/testado e o que foi realmente executado.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
