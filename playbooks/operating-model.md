# Modelo operacional declarativo

## Entradas reais

Comecar pelo pedido atual, escopo autorizado, baseline e aceite. Consultar
[menu](../.agents/skills/haos-menu/SKILL.md) ou a
[matriz](../.codex/skill-routing.json) por nomes reais. Se o ambiente reconhecer
skills pelo nome, usar por exemplo $haos-menu, $haos-deep-research,
$haos-session-dump, $haos-session-handoff, $haos-dump-import ou $haos-evoluir.
Sem esse suporte, ler o SKILL.md correspondente. Nao prometer comandos de
plugin, slash commands instalados ou hot reload.

**Arquivos nao sao runtime.** TOML de papel, SKILL.md e JSON de associacoes
nao fazem spawn, nao alteram modelo, nao chamam API e nao concedem autorizacao.

## Ciclo

1. Contexto e evidencias: separar confirmado, inferido e pendente.
2. Plano proporcional: entregas, owners, dependencias, riscos e aceite.
3. Selecao por metadados: ler apenas as skills pertinentes.
4. Delegacao real quando suportada: briefing com objetivo, fontes, paths,
   ownership disjunto, limites, skills e evidencias esperadas.
5. Execucao e verificacao: autor corrige; revisor independente confere read-only.
6. Integracao pelo main: pacote inclui staged, unstaged e novos arquivos.
7. Fechamento unico pelo main com haos-evoluir, preservando opt-outs.

Perguntas autocontidas nao exigem squad nem pipeline. Fonte viva continua
necessaria para afirmar estado atual. Ausencia de ferramenta de delegacao e
limite real, nao permissao para inventar retorno ou criar agentes ocultos.

## Conselho e departamentos

Nucleo decisor: estrategista-chefe, diretor-criativo e cmo. Insumos obrigatorios:
oraculo para precedentes/pontos cegos, brabo para risco juridico. Incluir cfo
quando a decisao envolver financas. Primeira onda: insumos (ate tres); segunda:
nucleo decisor (ate tres). Main integra divergencias por evidencia, nao votacao.
Juridico informativo, QA e seguranca tecnica sao funcoes diferentes.

Usar haos-departamentos para selecionar especialidades e haos-squad para dividir
o trabalho. Nunca mais de tres agentes em uma onda; cada recurso tem um owner.
Consultar capacidade real da ferramenta, preservar effort solicitado (high como
piso nesta configuracao) e distinguir parametro pedido de modelo efetivo.

## Rito e gates

haos-rito-v2 mantem 13 fases. Comecar na fase 1 sem estado valido; retomar apenas
com fase/evidencia coerentes. N/A exige justificativa, nao apaga gate aplicavel.
Risco, acao, destino ou gasto novo exige autorizacao aplicavel; nao reabrir aceite
valido por decurso de tempo. Plano e dado historico nunca substituem aprovacao.

Sem OK concreto: nao publicar, enviar, gastar, push, merge, deploy, alterar remoto
ou excluir destrutivamente. Preparar localmente nao equivale a executar externo.

## Limite finito

Default: tres ciclos de correcao por item, com hipotese e verificacao novas.
Interrupcao do usuario cancela trabalho afetado. Limite esgotado preserva defeito
como REVISAO NECESSARIA ou BLOQUEADO, nunca PASS. Sem daemon, retry infinito
ou promessa de continuar em segundo plano.

## Estado e fechamento

O [schema de estado](../workspace/runtime/state/rito.schema.json) e o
[exemplo do Rito](../workspace/runtime/state/rito.example.json) sao inativos. Nao representam
tarefas correntes. SO_FECHA nao fabrica aprendizado; CAPITALIZA depende de valor,
direitos, escopo, validacao e readback dos destinos habilitados; PENDENTE identifica
somente a lacuna real. Servico desabilitado nao e falha nem dependencia obrigatoria.
Commit, push, sync remoto e instalacao global nao fazem parte deste playbook.
