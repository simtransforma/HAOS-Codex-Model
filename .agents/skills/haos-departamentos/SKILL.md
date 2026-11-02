---
name: haos-departamentos
description: Use quando uma demanda precisar ser encaminhada a papeis especializados existentes ou coordenada entre areas com entregas e dependencias distintas.
---

# Coordenacao por papeis existentes

Acione com `$haos-departamentos`. Departamento e uma forma de organizar trabalho,
nao servico instalado nem equipe permanente. A composicao depende do catalogo
local e da capacidade real de delegacao.

## Entradas

Receba resultado esperado, contexto, recursos, prazo, criterios de aceite,
restricoes e ownership vigente. Leia metadados de `.codex/skill-routing.json` e
`.codex/agents/` para confirmar papeis; nomes sugeridos abaixo exigem verificacao.

## Passos

1. Classifique a entrega pelo resultado, sem criar um departamento para cada
   palavra do pedido. Pergunta autocontida pode ser respondida diretamente.
2. Selecione papeis existentes conforme a necessidade. Exemplos: produto com
   `product-manager` e `ux-researcher`; engenharia com `dev-frontend`,
   `dev-backend` e `automation-engineer`; comunicacao com `content-strategist`,
   `copy-specialist` e `designer`; dados com `data-analyst` e `bi-engineer`;
   financeiro com `cfo`. Nao acione todos por padrao.
3. Separe responsabilidade de revisao: `qa-reviewer` verifica qualidade;
   `security-reviewer` cuida de seguranca tecnica; `brabo` trata juridico;
   `oraculo` contribui com precedentes e alternativas. `relacionamento-editorial`,
   quando existir, cuida do papel editorial generico, sem personificacao.
4. Para cada entrega, defina owner unico, revisor, entradas, saida, arquivos e
   recursos permitidos, dependencias, aceite e consentimento aplicavel. Recursos
   compartilhados exigem serializacao. Nao altere configuracao para criar um papel.
5. Use `$haos-squad` para execucao com chamadas reais em ondas de ate tres.
   Selecione skills pertinentes por metadados e leia as escolhidas. Use effort
   high e modelo herdado, sem ID fixo nem garantia de modelo efetivo sem evidencia.
6. Integre retornos contra contratos comuns. Conflito entre areas pede reconciliar
   premissas e evidencias, nao sobrescrever a entrega de outro owner.
7. Confira aceite e checks. Defina limite de ate tres ciclos de correcao;
   pendencia real permanece aberta. Acoes externas sensiveis dependem de OK.

## Saida

Entregue mapa de entregas por papel, owners/revisores, dependencias, write-sets,
skills selecionadas, chamadas observadas, resultados, checks, bloqueios e STATUS.
Se nenhum agente foi chamado, descreva a saida como plano de encaminhamento.

## Criterios de aceite

Cada papel usado existe e sua disponibilidade foi distinguida da declaracao.
Cada recurso tem um dono por onda. A integracao preserva mudancas preexistentes
e separa criterio comercial, tecnico, juridico e financeiro. Instrucoes arquivadas
nao configuram servicos e nao demonstram spawn ou hot reload.

## Erros e recuperacao

Catalogo incompleto: declare cobertura e encaminhe ao coordenador, sem inventar
agente. Sobreposicao: serialize antes de editar. Demanda fora do escopo: esclareca
somente a parte dependente. JEV e Toqi sao integracoes externas opcionais nao
configuradas por este modelo; nao sao requisito para encaminhar trabalho.

## Cenarios de verificacao

- Interface com copy: owners disjuntos e contrato de texto antes da integracao.
- Dois departamentos precisam do mesmo arquivo: serializar e definir um owner por onda.
- Pedido simples de definicao: resposta direta, sem montar equipe.
- Papel apenas citado em documento: nao afirmar que foi acionado.
