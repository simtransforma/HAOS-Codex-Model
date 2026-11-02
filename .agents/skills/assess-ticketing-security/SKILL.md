---
name: assess-ticketing-security
description: "Planejar e conduzir avaliações autorizadas de segurança em plataformas web e APIs de ticketing, incluindo escopo, modelagem de superfície, autenticação, autorização, sessões, integrações e validação segura. Usar quando houver autorização escrita e um alvo de ingressos, eventos, checkout, bilheteria ou controle de acesso."
---

# Avaliar segurança de ticketing

## Gate obrigatório

Antes de qualquer interação com o alvo, exigir: proprietário, autorização escrita, hosts/APIs incluídos, ambiente, janela, contas de teste, limites de taxa, contatos de emergência e ações proibidas. Sem isso, produzir apenas plano, checklist ou análise local.


## Fluxo

1. Registrar o escopo e a regra de parada usando `references/scope-and-safety.md`.
2. Mapear atores, ativos, fluxos, integrações e fronteiras de confiança.
3. Criar matriz endpoint x papel x objeto x estado.
4. Priorizar testes passivos e contas sintéticas.
5. Validar uma hipótese por vez com a menor requisição possível.
6. Parar ao encontrar acesso não autorizado, PII, instabilidade, efeito financeiro ou saída do escopo.
7. Registrar evidência mínima, impacto, causa provável, remediação e reteste.

## Cobertura

Consultar `references/knowledge-base.md` para controles e fontes. Cobrir autenticação, recuperação, sessão, autorização por objeto e função, APIs, upload/exportação, webhooks, pagamentos, filas, caches, rate limiting, configuração, dependências e observabilidade.

Para lógica de compra, inventário, ingresso e check-in, acionar também `review-ticketing-business-logic`.

## Saída

Entregar escopo validado, mapa de ataque, matriz de testes, diário de execução, achados reproduzíveis sem segredos e plano de correção. Separar claramente confirmado, indício e não testado.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
