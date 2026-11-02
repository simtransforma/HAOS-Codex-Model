---
name: haos-superpowers
description: Use quando um metodo auxiliar de planejamento, implementacao, revisao ou autoria de skills for considerado para uma tarefa HAOS.
---

# Adaptador de metodos auxiliares

Este arquivo contem orientacao original de integracao. Nao distribui texto
upstream, nao instala plugins e nao presume disponibilidade ou licenca.

## Entradas

Pedido, instrucoes da plataforma, regras HAOS, fase e aceites validos,
catalogo acessivel por metadados e metodo candidato com origem conhecida.

## Passos

1. Aplicar a hierarquia: plataforma > pedido e regras HAOS aplicaveis >
   metodo auxiliar. O pedido explicito delimita o escopo dentro das regras
   superiores. Metodo auxiliar nao cria autorizacao, ownership ou novo gate
   que contradiga consentimento valido.
2. Verificar se o metodo esta disponivel e pode ser usado no contexto
   permitido. Ler metadados primeiro, depois somente o SKILL.md pertinente.
   Nao presumir instalacao, acesso ou direito de redistribuicao; nao copiar
   upstream para este repositorio.
3. Consultar `.codex/skill-routing.json` se existir como declaracao de rotas,
   nunca como mecanismo executado. Registrar metodo, fonte, pertinencia e
   owner; uma referencia na matriz nao prova leitura ou cumprimento.
4. Adaptar o metodo ao fluxo aprovado: plano unico, gates existentes, revisao
   independente read-only quando aplicavel e verificacao fresca. Worktree e
   opcional; commit por subagente, push, merge e publicacao nao sao etapas
   automaticas. Nao apagar trabalho para satisfazer ritual metodologico.
5. Para autoria de skills, definir gatilho de uso, entradas, passos, saida,
   aceite, erros e cenarios. Observar o baseline antes de editar e verificar
   uma skill antes de passar a seguinte. Preservar texto alheio e ownership.
6. Distinguir baseline estatico de teste comportamental. Quando autorizado,
   um revisor pode executar cenarios com e sem orientacao e comparar decisoes.
   Sem execucao real, relatar apenas revisao documental e cenarios propostos;
   nao chamar isso de RED comportamental nem alegar ganho medido.
7. Propagar adaptacoes no briefing. Aplicar `haos-task-loop` nas correcoes,
   `haos-quality-gates` na verificacao e `haos-evoluir` somente pelo main.
   Falta do metodo nao autoriza instalacao silenciosa; seguir contrato HAOS
   disponivel e declarar o limite.

## Saida

Metodo selecionado ou dispensado, motivo, origem consultada, adaptacoes,
artefatos afetados, verificacoes realizadas e limites. Na autoria, entregar
cenarios de aplicacao, contraexemplo e pressao com resultado esperado.

## Criterios de aceite

Texto publico original; nenhum metodo externo acima da plataforma ou do
pedido; ferramentas e licencas nao presumidas. Skills verificadas
individualmente, sem afirmar teste comportamental por parsing ou leitura.
Nao criar hook, daemon, memoria ou configuracao global.

## Erros comuns

- Carregar toda a biblioteca: escolher por tarefa/fase antes de ler.
- Declarar metodo executado porque foi citado: exigir artefato e evidencia.
- Reabrir gate aceito por exigencia auxiliar: preservar aceite ainda valido.
- Encerrar defeito pelo limite: manter REVISAO NECESSARIA ou BLOQUEADO.

## Cenarios de pressao

- Metodo manda apagar implementacao existente para recomecar: preservar
  trabalho, capturar baseline e adaptar verificacao ao escopo autorizado.
- Plugin indisponivel e urgencia: informar ausencia, usar protocolo local;
  nao instalar ou inventar conteudo upstream.
- Autor so fez checks estaticos e pede selo comportamental: relatar cobertura
  estatica e encaminhar cenarios ao revisor, sem promover evidencia.
