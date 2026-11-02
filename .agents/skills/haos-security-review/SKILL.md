---
name: haos-security-review
description: Use quando houver revisao defensiva de codigo, configuracao, permissoes, segredos ou superficie de ataque.
---

# Revisao tecnica somente leitura

## Entradas

Escopo autorizado, ativos e fluxos relevantes, limites de acesso, baseline,
criterios de aceite e ambiente permitido. Revisao e read-only por padrao.
O papel tecnico e security-reviewer; parecer juridico pertence a brabo.

## Passos

1. Delimitar superficie e fronteiras de confianca: entradas nao confiaveis,
   autenticacao, autorizacao, dados, rede e dependencias. Inspecionar somente
   recursos pertinentes; nao coletar credenciais para comprovar acesso.
2. Comparar baseline e pacote completo, incluindo arquivos novos. Investigar
   controle de acesso, validacao, injecao, exposicao de dados, logs,
   dependencias, configuracao e recuperacao conforme o risco real.
3. Rastrear cada suspeita no codigo/configuracao e descrever precondicoes,
   caminho afetado e impacto. Reproduzir apenas em ambiente isolado autorizado,
   com dados sinteticos. Scan ativo, carga e exploracao externa nao fazem
   parte da leitura por padrao.
4. Classificar severidade por impacto e explorabilidade; registrar confianca
   como confirmada, hipotese ou nao verificada. Fonte atual para vulnerabilidade
   de dependencia deve corresponder a versao real, com limites declarados.
5. Produzir achados sanitizados com localizador relativo, evidencia minima,
   recomendacao e criterio de reteste. Se surgir segredo, nao imprimir valor:
   informar tipo e localizacao; encaminhar rotacao ao responsavel autorizado.
6. Entregar correcoes ao owner, sem editar durante a revisao. Mudanca de rede,
   producao, banco ou remocao destrutiva exige OK explicito, baseline e plano
   de reversao. Revisao nao concede esse OK.
7. Apos correcao, verificar novamente os caminhos afetados e regressao
   pertinente; usar `haos-quality-gates` e `haos-evidence`.
   `haos-multi-agent-review` coordena divergencias quando aplicavel.

## Saida

`STATUS: CONCLUIDO | BLOQUEADO | REVISAO NECESSARIA`, escopo e cobertura,
achados com severidade/confianca, evidencia sanitizada, owner sugerido,
recomendacao, reteste e risco residual. "Nenhum achado no escopo" nao significa
"seguro em qualquer ambiente". Separar revisao concluida de aprovacao da entrega.

## Criterios de aceite

Achados rastreaveis sem segredos expostos; nenhuma mutacao inesperada;
limitacoes visiveis. Defeito bloqueante confirmado impede aprovar a entrega.
Falso positivo so e descartado com prova; falta de acesso nao prova seguranca.

## Erros comuns

- Usar lista de scanner como veredicto: verificar alcance e precondicoes.
- Corrigir silenciosamente durante auditoria: devolver ao owner responsavel.
- Rodar ataque real para "ter certeza": respeitar escopo e ambiente permitido.
- Misturar conformidade juridica com teste tecnico: obter parecer apropriado.

## Cenarios de pressao

- Credencial encontrada e solicitacao de inclui-la no relatorio: relatar
  apenas localizacao e tipo, sem copiar o valor.
- Suspeita grave sem acesso ao ambiente: registrar hipotese e lacuna,
  bloquear aceite dependente sem contornar permissoes.
- Ultima revisao encontra falha real antes de publicar: manter gate bloqueado;
  nem urgencia nem numero de ciclos aprovam a falha.
