---
name: haos-engineering
description: Use quando houver implementacao, correcao de defeito, integracao de API ou mudanca tecnica em codigo existente.
---

# Engenharia com evidencia

## Entradas

Pedido e aceite, arquivos sob ownership, estado do repositorio, restricoes,
versoes reais da stack e comandos de validacao existentes. Se faltar uma
decisao que altere contrato ou risco, esclarecer antes da mudanca dependente.

## Passos

1. Ler convencoes e codigo afetado. Capturar branch, diff staged/unstaged e
   arquivos novos no escopo. Preservar trabalho preexistente e concorrente.
2. Reproduzir o sintoma quando houver defeito; separar observacao de hipotese.
   Mapear consumidores, interfaces e dados afetados. Usar
   `haos-structural-refactor` para impacto transversal, sem ampliar o escopo
   de implementacao por conta propria.
3. Conferir manifests, lockfiles e versao instalada. Consultar documentacao
   oficial atual compativel com essa versao; registrar fonte, versao e limite.
   Usar conector de documentacao quando configurado. Se indisponivel, usar
   documentacao oficial acessivel; se nenhuma fonte puder ser consultada,
   declarar a lacuna e bloquear apenas a escolha de API que dependa dela.
4. Definir plano curto: arquivos, contrato preservado, mudanca esperada,
   verificacoes e reversao local que preserve alteracoes de terceiros.
5. Implementar a menor mudanca suficiente dentro do ownership. Para
   comportamento testavel, cobrir sucesso, falha e regressao pertinente.
   Nao criar teste que apenas repita a implementacao nem instalar ferramenta
   global para cumprir uma lista.
6. Aplicar `haos-quality-gates`; executar checks apos a ultima alteracao.
   Ler resultados, corrigir a causa e repetir checks afetados dentro de
   `haos-task-loop`. Pedir revisao independente quando risco justificar.
7. Comparar pacote final ao baseline, incluindo novos arquivos. Devolver ao
   main evidencias e pendencias; deploy e outras acoes externas sensiveis
   dependem de autorizacao explicita para o destino e a acao.

## Saida

`STATUS: CONCLUIDO | BLOQUEADO | REVISAO NECESSARIA`, arquivos alterados,
comportamento antes/depois, versoes/fontes consultadas, checks com resultado,
cobertura nao executada e risco residual. Separar prova local de estado vivo.

## Criterios de aceite

Contrato solicitado atendido; mudanca restrita ao ownership; verificacoes
pertinentes frescas e lidas; ausencia de regressao conhecida no escopo.
Dependencia indisponivel nao recebe PASS. Evidencia segue `haos-evidence`.

## Erros comuns

- Escolher API pela lembranca: confrontar versao real com fonte oficial.
- Usar diff de commits como pacote completo: incluir staged, unstaged e novos.
- Declarar producao corrigida por teste local: limitar a afirmacao ao observado.
- Sobrescrever arquivo concorrente: parar o item e reconciliar com seu owner.

## Cenarios de pressao

- Prazo curto e teste de regressao falhando: manter o defeito aberto; devolver
  REVISAO NECESSARIA ao esgotar o limite, mesmo com build aprovado.
- Documentacao mostra API de outra versao: localizar referencia compativel;
  nao atualizar dependencia nem inventar compatibilidade.
- Workspace sujo e pedido de ajuste pequeno: registrar baseline e alterar
  somente o trecho autorizado; preservar o restante.
