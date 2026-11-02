# Invariantes de ticketing

- Estoque disponível nunca fica negativo e cada assento só pertence a uma reserva ativa.
- Reserva expirada não conclui compra sem nova confirmação de estoque e preço.
- Total cobrado corresponde a itens, taxas, descontos e moeda validados no servidor.
- Cupom respeita evento, lote, usuário, período, limite e número de usos.
- Pedido pago emite exatamente os ingressos devidos; callback repetido é idempotente.
- Reembolso válido não excede o valor elegível nem restaura benefício duas vezes.
- Transferência exige propriedade, consentimento e revoga o token anterior quando aplicável.
- QR/barcode não revela segredo reutilizável; check-in válido ocorre no máximo uma vez.
- Organizador só administra seus eventos; operador só acessa o tenant/portão autorizado.
- Exportações e relatórios aplicam a mesma autorização da interface principal.
- Webhook tem autenticidade, proteção contra replay e reconciliação segura.
- Cancelamento preserva trilha de auditoria e não deixa credencial ativa órfã.
