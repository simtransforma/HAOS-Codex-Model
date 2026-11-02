---
name: haos-menu
description: Use quando o usuario quiser descobrir skills locais, papeis de agentes, formas de acionamento ou restricoes do ambiente HAOS disponivel.
---

# Menu local verificavel

Acione com `$haos-menu`. O menu descreve capacidades declaradas e disponibilidade
observada. Nomes de skills sao pontos de entrada; nao prometa comandos slash,
plugins instalados ou automacoes apenas porque existem arquivos.

## Entradas

Receba interesse do usuario, tarefa opcional e escopo do repositorio. Consulte
metadados locais de `.codex/skill-routing.json`, `.agents/skills/` e
`.codex/agents/`. Nao leia todos os corpos de skills para listar o catalogo.

## Passos

1. Leia a matriz declarativa e identifique os campos que realmente existem.
   Nao presuma schema ou invente rotas quando a matriz estiver ausente/invalida.
2. Confira se as skills apontadas possuem SKILL.md e se o name corresponde a
   pasta. Leia name e description para selecionar por situacao de uso.
3. Confira arquivos de agentes e seus papeis declarados. Separe arquivo existente
   de agente exposto pela ferramenta atual e de agente efetivamente acionado.
4. Monte uma lista compacta de skills locais por finalidade e agentes relevantes.
   Para cada skill, mostre nome real acionavel, gatilho e limite principal.
   Para cada agente, mostre papel, estado observado e restricoes.
5. Explique gates aplicaveis: ownership, revisao independente, ondas de ate tres,
   limites de ferramentas e OK para acoes externas sensiveis. Nao execute uma
   operacao apenas porque ela foi apresentada no menu.
6. Se houver tarefa concreta, indique a menor selecao pertinente e leia somente
   essas skills na etapa seguinte. Uma sugestao nao comprova delegacao.
7. Declare lacunas da matriz ou catalogo. Como fallback, liste apenas metadados
   dos arquivos locais existentes e marque roteamento NAO VERIFICADO.

## Saida

| Entrada | Quando usar | Papel relacionado | Estado observado | Limite |
| --- | --- | --- | --- | --- |
| Nome real com prefixo $ | Gatilho dos metadados | Papel existente | Declarado ou disponivel | Gate pertinente |

Inclua cobertura da consulta, inconsistencias e proxima escolha sugerida. Um
exemplo de entrada e `$haos-session-handoff` para transferencia de estado;
confirme sua existencia antes de apresenta-la como disponivel.

## Criterios de aceite

Cada item anunciado existe no escopo inspecionado. A matriz e declarativa;
instrucao arquivada nao e runtime e nao prova spawn ou hot reload. Nao confunda
`brabo`, de analise juridica, com `security-reviewer`, de seguranca tecnica.
JEV e Toqi sao integracoes externas opcionais nao configuradas por este modelo;
esta skill nao as instala, implementa ou consulta automaticamente.

## Erros e recuperacao

Skill ausente: informar caminho relativo faltante sem instalar substituta.
Agente nao exposto: declarar limite e encaminhar ao coordenador. Matriz diverge
do disco: mostrar divergencia, sem editar a configuracao como efeito do menu.
Nao afirme contagem fixa sem contar os arquivos atuais.

## Cenarios de verificacao

- Matriz ausente: catalogo local parcial com roteamento nao verificado.
- Agente existe em arquivo, mas nao na ferramenta: apresentar como declarado.
- Pedido apenas de menu: listar capacidades sem spawn nem acao externa.
- Integracao opcional aparece em comentario: nao anuncia-la como instalada.
