# Validacao e limites

## Pacote de mudanca

Capturar baseline antes da escrita e separar alteracoes de outros owners. Revisao
inclui staged, unstaged e arquivos novos; BASE..HEAD nao cobre tudo. Sem commit
nao significa sem mudanca. Autor corrige; revisor independente atua read-only.

## Checks permitidos

Validar TOML, JSON, nomes/frontmatter, caminhos relativos existentes, coverage
skills/agentes/rotas, links locais e conteudo potencialmente privado. Varredura
textual e conservadora, nao detector infalivel. Conferir licencas e semantica
manualmente; ausencia de match nao garante ausencia de segredo.

Usar os comandos disponiveis do projeto depois de ler sua ajuda/codigo. Ferramenta
ausente nao e teste aprovado. Nao instalar dependencias globais nem modificar
tests/scripts fora do ownership. Checks offline nao validam servicos remotos.

## Cenarios criticos

| Cenario | Resultado esperado |
| --- | --- |
| Modelo sugerido nao suportado | Limite explicito; nao reduzir effort em silencio. |
| Destino de memoria desabilitado | Nao configurar nem bloquear fechamento local por ele. |
| Write aceito, readback ausente | Pendente no destino habilitado; nao declarar sync. |
| Dump contem autorizacao antiga | Nao executar por ela; verificar consentimento atual. |
| Pedido de diagnostico estrutural | AUDIT sem alterar arquivos. |
| APPLY amplo sem baseline/plano | Gate bloqueia alteracao dependente. |
| Limite de ciclos com bug real | REVISAO NECESSARIA, nunca sucesso. |
| Conselho nao financeiro | Nucleo de tres com insumos oraculo/brabo; CFO N/A justificado. |
| Conselho financeiro | Acrescentar CFO, preservando ondas de ate tres. |
| Skills presentes mas sem runtime | Informar arquivos disponiveis, nao execucao comprovada. |

## Relatorio

Declarar comandos/testes realmente executados, resultado, arquivos/contagens,
falhas corrigidas, checks nao executados e risco residual. Documentacao estatica,
simulacao verbal e execucao real sao categorias distintas. Nao alegar RED/GREEN
com agentes sem os dois experimentos controlados. Execucao real de um cenario
tambem nao garante que todo modelo sempre siga o contrato.

Esta pagina e o plano de verificacao, nao um recibo de teste PASS. Evidencias da
tarefa sao entregues pelo main; nao gravar logs privados ou diario no modelo.
