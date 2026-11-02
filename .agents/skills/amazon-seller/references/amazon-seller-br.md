# Amazon Seller Brasil — operação e integrações

## Limites de decisão


## Bling

Antes de ativar qualquer integração, documentar:

| Domínio | Fonte de verdade | Controles mínimos |
|---|---|---|
| SKU/ASIN e cadastro | Amazon para ASIN; ERP para SKU interno | Tabela de mapeamento única e validação de duplicidade. |
| Estoque | Definir um único mestre por SKU | Reserva, estoque de segurança e reconciliação diária. |
| Pedidos | Amazon como origem de pedido | Idempotência por ID do pedido e logs sem PII. |
| NF e rastreio | ERP/logística | Validar canal de fulfillment antes de enviar atualização. |
| Financeiro | Amazon settlements/Finances | Conciliar taxas, estornos e liquidação, não só pedidos. |

Começar com leitura/reconciliação; só então propor sincronização unidirecional e, por último, mutações bidirecionais com fila, retry seguro e rollback.

## Anúncios Amazon

A SP-API não é a Amazon Ads API. Campanhas, Sponsored Ads, lances, orçamento e relatórios publicitários usam a Amazon Ads API/console e têm acesso/aplicação próprios. Não assumir que a aprovação da SP-API concede esse acesso.


Fonte: https://advertising.amazon.com/about-api

## Checklist antes de mutar produção

1. Confirmar conta, marketplace BR e ambiente.
2. Confirmar role, autorização e operação exata.
3. Gerar prévia com itens afetados e impacto comercial.
4. Definir limite, idempotência, monitoramento e rollback.
6. Executar lote pequeno, validar resposta e reconciliar no Seller Central.
