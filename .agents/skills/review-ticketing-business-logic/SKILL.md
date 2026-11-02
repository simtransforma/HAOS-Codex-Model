---
name: review-ticketing-business-logic
description: "Revisar com autoriza\u00e7\u00e3o a l\u00f3gica de neg\u00f3cio de plataformas de ticketing: eventos, lotes, assentos, estoque, pre\u00e7os, cupons, checkout, pagamento, emiss\u00e3o, transfer\u00eancia, reembolso e check-in. Usar para modelar invariantes e testes seguros que detectem falhas de estado, concorr\u00eancia e autoriza\u00e7\u00e3o."
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

# Revisar lógica de ticketing

Exigir o gate de autorização do skill `assess-ticketing-security`. Trabalhar primeiro com documentação, código e ambiente de homologação.

## Método por invariantes

1. Desenhar a máquina de estados de evento, pedido, pagamento, ingresso e check-in.
2. Definir invariantes antes dos testes.
3. Mapear cada transição, ator, pré-condição e efeito colateral.
4. Testar variações somente com dados sintéticos e carga mínima.
5. Comparar estado esperado e persistido em todas as integrações.

Consultar `./references/ticketing-invariants.md` e `./references/test-matrix.md`.

## Limites

Não consumir estoque real, gerar cobrança real, validar ingresso real, acionar chargeback, inundar filas ou explorar corrida em produção. Para concorrência, usar harness local/homologação com teto aprovado.

## Saída

Entregar diagrama de estados, catálogo de invariantes, matriz ator-objeto-ação-estado, hipóteses testadas e achados com remediação transacional/idempotente.
