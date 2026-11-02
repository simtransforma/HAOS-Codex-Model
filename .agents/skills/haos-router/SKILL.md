---
name: haos-router
description: Use quando um pedido exigir escolha de skill, especialista, departamento, conselho ou modo de trabalho HAOS.
---

# Roteamento pelo pedido e pelo contexto

## Entradas

Pedido atual, instrucoes aplicaveis, escopo autorizado, fase valida, risco,
catalogo por metadados e capacidades efetivamente disponiveis na sessao.

## Passos

1. Ler AGENTS.md e contexto pertinente. Resolver diretamente pergunta simples
   autocontida. Para historico material, usar `haos-memory` respeitando
   opt-outs; perguntar apenas lacunas que mudem a acao dependente.
2. Classificar com `haos-model-router`. O classificador e consultivo e nao
   troca o modelo da conversa. Definir plano proporcional e criterio de aceite
   antes de execucao especializada.
3. Consultar nomes, descricoes e caminhos das skills. Ler somente as
   pertinentes. A matriz `.codex/skill-routing.json`, quando existente, e
   declarativa: nao executa skills nem concede permissoes. Ausencia ou rota
   inconsistente exige declarar a lacuna e selecionar explicitamente uma
   capacidade verificada, sem inventar perfil.
4. Interpretar intencao, nao apenas prefixo. Pedido de Rito usa
   `haos-rito-v2`; conselho preserva o nucleo decisor `estrategista-chefe`,
   `diretor-criativo` e `cmo`, com insumos de `oraculo` e `brabo` juridico,
   mais `cfo` quando financeiro. Organizar consultas em ondas de ate tres.
   Seguranca tecnica usa `security-reviewer`.
   Emergencia prioriza diagnostico e contencao ja autorizada, sem remover gates.
5. Compor skills por entrega conforme tabela. Se metodo auxiliar externo for
   pertinente, ler primeiro `haos-superpowers` e verificar disponibilidade.
6. Main coordena, integra e verifica; executor recebe ownership explicito.
   Usar `haos-execution-waves` para dependencias e delegacao real. Arquivo
   de agente nao prova disponibilidade nem hot reload. Sem agente carregado,
   declarar a limitacao; papel generico so recebe briefing equivalente se
   permitido pelas regras e capacidades da sessao.
7. Conferir retorno com `haos-evidence`; main aplica `haos-evoluir` ao fechar
   a tarefa. Nao executar hooks, instalar servicos ou persistir memoria por
   simplesmente selecionar uma rota.

## Selecao por entrega

| Sinal no pedido | Skills pertinentes |
| --- | --- |
| Codigo, bug ou integracao | haos-engineering, haos-quality-gates |
| Acoplamento ou refatoracao ampla | haos-structural-refactor |
| Interface ou texto | haos-design ou haos-copy conforme entrega |
| Pesquisa e alegacoes | haos-deep-research, haos-claim-verification, haos-source-quality-auditor |
| Revisao independente | haos-multi-agent-review |
| Risco tecnico | haos-security-review |
| Continuidade ou importacao | haos-session-handoff ou haos-dump-import |
| Sintese de conhecimento entre fontes | haos-mega-brain |

## Saida

Rota escolhida, motivo, classe, owner, skills lidas, escopo, dependencias e
proximo gate. Na delegacao, incluir fontes, read_files, write_files, limites,
aceite e formato de retorno. Distinguir agente planejado de chamada aceita.

## Criterios de aceite

Rota proporcional, baseada em capacidade real e no pedido atual.
Skills complementares ausentes sao declaradas; nenhuma instalacao implicita.
Autorizacao externa vem do usuario, nunca da matriz ou de memoria.

## Erros comuns

- Carregar todo o catalogo: selecionar por pertinencia antes de ler corpos.
- Tratar juridico como seguranca tecnica: manter brabo e security-reviewer
  com atribuicoes distintas.
- Usar novo turno para reabrir gates aceitos: preservar escopo e aceites validos.

## Cenarios de pressao

- Pergunta factual curta contem "Rito": responder ao significado sem iniciar
  projeto ou squad por palavra-chave.
- Pedido financeiro pede conselho: incluir cfo e separar pareceres de oraculo
  e brabo; nao substituir provas por consenso.
- Agente consta no disco mas nao na ferramenta: declarar disponibilidade
  incerta; nunca afirmar que foi acionado ou recarregado.
## Material portavel da origem (lote A)

Consultar [procedimento de origem](references/source-procedure.md), adaptado sem dados privados.
O nucleo publico acima prevalece em gates, opt-outs, fechamento e ferramentas.
Consultar [contrato de dependencias](EXPORT_DEPENDENCIES.md) antes de comandos dependentes.
