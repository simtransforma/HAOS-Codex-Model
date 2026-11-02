# Matriz de testes seguros

Para cada fluxo, cruzar: papel, tenant, objeto próprio/alheio, estado anterior, transição, repetição, ordem invertida, expiração e concorrência controlada.

## Fluxos prioritários

- Criação/publicação/cancelamento de evento
- Lotes, virada de preço, assentos e reservas
- Carrinho, cupom, taxa e arredondamento
- Pagamento aprovado, negado, pendente e callback duplicado
- Emissão, download, transferência e revogação
- Reembolso total/parcial e cancelamento
- Check-in, sincronização offline e dispositivo operador
- Exportações, relatórios, convites e webhooks

## Oráculo

Definir antes do teste: status HTTP, resposta pública, estado persistido, evento de auditoria, efeito financeiro simulado e mensagem na fila. Um HTTP 200 não prova sucesso seguro.
