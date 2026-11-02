---
name: haos-structural-refactor
description: "Detecta arquivos de codigo grandes ou complexos, confirma risco estrutural no codigo real e produz um plano de refatoracao incremental; use implicitamente em pedidos para identificar god files, dividir arquivos extensos, reduzir responsabilidades misturadas, planejar extracao de modulos ou avaliar refatoracao estrutural sem confundir tamanho com divida tecnica."
---

# HAOS Structural Refactor

Operar em `AUDIT` por padrao. Tratar o tamanho apenas como sinal de triagem: um
arquivo acima do teto e candidato a inspecao, nao prova de divida tecnica.

## Descoberta deterministica

Resolva `<skill-dir>` como o diretorio que contem este `SKILL.md` e execute o
scanner empacotado a partir dali. Nao presuma que o workspace atual e o repo
canonico do HAOS:

```powershell
python "<skill-dir>/scripts/scan_structural_risk.py" <root> --max-lines 350 --format markdown
```

Usar `--format json` para consumo estruturado e `--output <arquivo>` para gravar
somente o relatorio solicitado. O scanner nunca altera os arquivos analisados e
nao exibe seu conteudo.

## AUDIT

1. Obter ground truth fresca: estado do worktree, manifests, estrutura, comandos
   oficiais de teste e arquivos candidatos. Preservar alteracoes preexistentes.
2. Rodar o scanner e inspecionar cada candidato no codigo real. Avaliar mistura de
   responsabilidades, coesao, fan-in/fan-out, contratos publicos, estado
   compartilhado, cobertura e historico de mudancas. Nao concluir risco pelo
   numero de linhas isolado.
3. Carregar `haos-quality-gates` para definir baseline e validacoes da stack.
4. Carregar `haos-execution-waves` para ownership, dependencias, ondas e
   evidencias. Usar `haos-multi-agent-review` quando houver revisao delegada.
5. Usar Graphify por `haos-graphify-code-map` somente quando o impacto for
   transversal, houver contratos compartilhados ou a arquitetura estiver
   desconhecida. Confirmar toda relacao apontada no codigo.
6. Entregar candidatos priorizados, evidencias, costuras naturais, plano por
   ondas, testes previstos e risco residual. Permanecer read-only.

Costuras naturais incluem fronteiras de dominio, adaptadores de I/O, parsing,
validacao, persistencia, apresentacao e componentes com estado independente.
Extrair por essas fronteiras; nao dividir apenas para atingir uma contagem menor.

## APPLY

Entrar em `APPLY` somente quando o usuario pedir implementacao. Refatoracao ampla,
transversal ou com varios modulos exige primeiro baseline e plano e, depois, OK

1. Revalidar ground truth e baseline imediatamente antes de editar.
2. Preservar API publica, comportamento observavel e compatibilidade, salvo mudanca
   de contrato explicitamente aprovada.
3. Executar no maximo tres unidades independentes por onda, com ownership exclusivo
   e write-sets disjuntos. Serializar arquivos ou recursos compartilhados.
4. Testar cada unidade apos a mudanca e rodar os gates de integracao da onda.
5. Designar revisor diferente do owner, em modo somente leitura. O revisor nao
   corrige o trabalho revisado.
6. Proibir commit por subagente. Nao fazer commit, push, merge, deploy ou outra
   acao externa sem autorizacao aplicavel.
7. Interromper a onda se contratos quebrarem, testes regredirem, a costura se
   mostrar artificial ou o worktree divergir de forma relevante.

## Saida minima

```text
STATUS: AUDIT CONCLUIDO | APPLY CONCLUIDO | REVISAO NECESSARIA | BLOQUEADO
ESCOPO:
BASELINE:
CANDIDATOS E EVIDENCIAS:
COSTURAS NATURAIS:
ONDAS E OWNERSHIP:
VALIDACOES:
RISCO RESIDUAL:
```
