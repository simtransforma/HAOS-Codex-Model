---
name: haos-multi-agent-review
description: "Revisao HAOS em ondas, com revisores somente leitura, deduplicacao de achados, owner unico por arquivo e verificacao fresca."
---

# HAOS Multi-Agent Review

Use em mudancas com risco relevante, varios modulos ou mais de uma especialidade.
Para mudanca pequena, um revisor adequado basta.

## Contrato

1. Registre objetivo, escopo, criterios de aceite e baseline.
2. Onda de revisao: no maximo tres revisores, todos `read-only`, cada um com um
   eixo distinto. Revisores nao corrigem arquivos.
3. Cada achado deve conter severidade `P0` a `P3`, arquivo/local, evidencia,
   impacto e correcao proposta.
4. O orquestrador consolida, remove duplicatas e resolve contradicoes usando
   evidencia, nunca maioria de votos.
5. Onda de correcao: no maximo tres executores com write-sets disjuntos. Cada
   arquivo tem um unico owner por onda.
6. O revisor final nao pode ser o owner da correcao que valida.
7. Rode novamente os checks que provam cada claim antes de concluir.

## Fingerprint de achado

Use uma chave estavel:

```text
<regra>|<arquivo>|<simbolo-ou-linha>|<sintoma>
```

Achados com a mesma causa raiz viram um item consolidado. Preserve todas as
evidencias relevantes e indique quando os revisores discordarem.

## Saida minima

```text
STATUS: APROVADO | AJUSTES NECESSARIOS | BLOQUEADO
ESCOPO REVISADO:
BASELINE:
ACHADOS P0-P3:
CORRECOES APLICADAS:
VERIFICACAO FRESCA:
RISCO RESIDUAL:
```

Alteracao externa, push, merge, publicacao, envio, gasto ou remocao destrutiva
