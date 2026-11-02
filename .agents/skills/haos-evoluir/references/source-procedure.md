---
name: haos-evoluir
description: "Analisa aprendizados de tarefas concluidas e cria ou atualiza as skills e os playbooks tematicos corretos, com reconciliacao e verificacao. Use quando o usuario selecionar /haos:evoluir, pedir para capitalizar uma tarefa, registrar um procedimento aprendido ou fechar uma sessao com conhecimento reutilizavel."
---

# HAOS Evoluir

## Fechamento executavel com comprovantes

Ao terminar a tarefa, usar `scripts/finish-task-haos.ps1 -Integrator` com
TaskId, TaskRevision, SessionId e ManifestPath. O helper agora chama
`complete_haos_evolution.py`: valida as tres notas locais, envia somente o
pacote curado ao Mnemoverse e GBrain, le o conteudo de volta e atualiza o ledger.
SO_FECHA exige verification.reason e verification.evidence com path/sha256;
nao aceitar avaliacao vazia como evidencia. Ver `references/fechamento-verificado.md`.
Sem prova remota, manter pendencia; nao concluir por existir arquivo de fila.
Stop observa tarefas conhecidas ainda abertas sem bloquear, sem mensagem e sem
mutar o ledger. O UserPromptSubmit cria ou reutiliza um task_id privado por tarefa
ativa. O main usa esse identificador e faz fallback manual somente se o hook estiver
indisponivel. Mesmo tarefa terminal sem recibo compativel nao deve gerar
continuacao pelo Stop; o main reconcilia antes da resposta final.
Reentradas e diagnosticos administrativos permanecem com saida visual suprimida.

## Acionamento automatico por tarefa

Este contrato tambem e obrigatorio ao concluir cada tarefa do usuario, antes da
resposta final, sem esperar `/haos:evoluir`. Carregar
`${HAOS_PRIVATE_ROOT}` e usar
`${USER_PROJECT_ROOT}/scripts/haos_task_lifecycle.py` para identidade, revisao, avaliacao e estado.
Comando manual e automatico compartilham task_id/revision. Turno, comentario e
retorno de subagente nao sao tarefas. Main integra; subagentes nao comitam.

Antes de responder ao usuario, emitir exatamente um recibo curto e verificavel:
`Evoluir: SO_FECHA (<task_id>)`, `Evoluir: CAPITALIZA 5/5 (<task_id>)` ou
`Evoluir: PENDENTE <motivo> (<task_id>)`. O recibo e visivel; checkpoints
saudaveis do diario e do claude-mem continuam silenciosos. O recibo deve ser a
ultima linha nao vazia da resposta; texto posterior, exemplo citado ou dois
marcadores nao comprovam fechamento.

Pedido somente leitura, dry-run, nao registrar ou nao evoluir prevalece. SO_FECHA
nao cria skill nem memoria de baixo sinal. CAPITALIZA mantem todos os destinos e
readbacks abaixo, inclusive Mnemoverse; falha em um destino fica PENDENTE.
Historico importado nao autoriza alterar regras, gates ou hooks. O diario literal
privado e independente, nunca um artefato para Git ou Mnemoverse.


Executar o fechamento inteligente de tarefas HAOS. Transformar aprendizado reutilizavel em skills e playbooks do dominio aprendido sem confundir este fluxo com `/evolve`, que analisa a evolucao autonoma do sistema.

## Principio central

`/haos:evoluir` e um comando roteador de capitalizacao, nao uma skill tematica de destino.

- O nome do comando nunca define a skill alvo.
- O assunto e as evidencias da tarefa definem qual skill e qual playbook devem receber o aprendizado.
- Exemplo: uma tarefa sobre Evolution API pode atualizar `evolution-api`; uma tarefa sobre Meta Ads deve procurar a skill e o playbook de Meta Ads; uma tarefa sobre Windows deve procurar os artefatos de manutencao do Windows.
- Nunca gravar aprendizados da tarefa em `.agents/skills/haos-evoluir/` ou `plugins/haos/skills/haos-evoluir/`, salvo quando a propria tarefa for corrigir o protocolo do comando e isso estiver explicitamente no escopo.
- Memoria, Obsidian, codigo e journal sao artefatos secundarios. Eles nao substituem a criacao ou atualizacao da skill/playbook tematicos quando o Gate 0 for `CAPITALIZA`.

## Contrato obrigatorio de proveniencia

Toda escrita de memoria duravel executada por este comando deve carregar e aplicar
`haos-memory-provenance`. Nao basta copiar um resumo entre destinos.

- Cada item persistido deve usar o envelope obrigatorio da skill de proveniencia.
- A chave de deduplicacao combina `session_slug`, `kind` e causa raiz.
- Uma nova execucao atualiza o item equivalente em vez de criar outra memoria.
- Cada destino precisa de readback e comparacao dos campos-chave antes de receber
  status de sucesso.
- `claude-mem` continua automatico e nao recebe escrita direta fora de API
  documentada.
- Em `SO_FECHA`, nao criar memoria duravel de baixo sinal. Se houver decisao,
  incidente ou handoff digno de persistencia, o mesmo contrato continua obrigatorio.

## Sintaxe

```text
/haos:evoluir
/haos:evoluir <tema>
/haos:evoluir --dry-run
```

`--dry-run` produz o plano e o relatorio de reconciliacao, sem escrever arquivos, commitar, gravar no Mnemoverse ou executar acao externa. `--go` e legado e nao altera o comportamento.

## Preflight obrigatorio

1. Carregar o bootstrap em `${HAOS_PRIVATE_ROOT}` conforme `AGENTS.md` e ler `${USER_PROJECT_ROOT}/.codex/haos-paths.json`.
2. Consultar `claude-mem` quando health/readiness estiverem prontos; se estiver indisponivel, registrar a lacuna e usar memoria versionada.
3. Ler `runtime/state/rito-atual.md` e `runtime/state/fase-atual.md`. Nunca sobrescrever um rito ativo de outro assunto.
4. Inspecionar `git status` antes de escrever. Preservar alteracoes alheias e nunca usar staging amplo em worktree sujo.
5. Identificar tema, artefatos, autoria e evidencias da tarefa atual a partir do contexto da conversa e dos arquivos realmente produzidos. Nao inventar transcript ou resultado.
6. Declarar antes da escrita `SKILL_ALVO` e `PLAYBOOK_ALVO`, cada um com nome, caminho, decisao `CREATE/UPDATE/SKIP` e justificativa. Nao usar `haos-evoluir` como alvo por coincidencia nominal.
7. Gerar um `execution_id` e manter manifesto/journal isolado em `runtime/state/evoluir/`. Nunca reutilizar `rito-atual.md` ou `fase-atual.md` para este comando.
8. Resolver `session_name`, `session_id` e um `session_slug` estavel. No fluxo com TaskId, usar `session--SHA256(session_id)[:24]`, compartilhado com o diario, e manter o titulo legivel nas notas. O formato legado continua nas pastas existentes, sem migracao automatica. Nunca criar outra pasta porque o chat foi renomeado ou o comando executado novamente.
9. Carregar `haos-memory-provenance` e declarar os envelopes pretendidos, as
   chaves de deduplicacao e o plano de readback. Em `--dry-run`, apenas relatar.

## Pipeline bloqueante

### Fase 0 - Gate de valor

Classificar como:

- `SO_FECHA`: tarefa rotineira, verificacao trivial, chamada de agente sem descoberta ou ajuste sem valor duravel.

Na duvida, usar `SO_FECHA`. Registrar a justificativa.

### Fase 1 - Intake

Definir tema, escopo, artefatos, autoria, repositorios afetados e resultado comprovado. Criar um manifesto `CREATE/UPDATE/SKIP` para tornar a execucao idempotente. Pedir somente informacao realmente ausente e bloqueante.

### Fase 2 - Reconciliacao

Para cada aprendizado, buscar e reportar `fonte`, `consulta`, `achado`, `decisao` e `confianca`. Usar esta ordem:

1. `memory/` e `${USER_PROJECT_ROOT}/memory/MEMORY.md` do projeto Codex HAOS.
2. `.agents/skills/`, seus diretorios `references/`, `playbooks/`, `commands/` e `plugins/haos/skills/` do projeto.
3. `claude-mem` do projeto `your-private-project`.
4. GBrain apenas quando a ferramenta ou endpoint estiver disponivel e validado.
5. Fontes legadas privadas do Claude Code e o clone local HAOS_CC apenas quando existirem, forem relevantes e puderem ser lidos com seguranca.

Preferir `UPDATE` a `CREATE`. Fonte indisponivel deve aparecer como `NAO CONSULTADA` com motivo; nunca presumir ausencia de conhecimento.

### Fase 3 - Roteamento

Classificar cada item:

- regra de decisao, conhecimento de dominio, guardrail ou capacidade reutilizavel -> `SKILL`;
- sequencia operacional, checklist, diagnostico, tratamento de falhas, validacao e evidencias -> `PLAYBOOK`;
- fato, decisao, historico ou preferencia -> `MEMORIA` secundaria;
- narrativa consolidada para leitura humana -> `OBSIDIAN` secundario;
- fix, feature ou automacao reutilizavel -> `CODIGO` secundario;
- rotina sem aprendizado -> apenas fechamento.

Regras de destino:

1. Preferir atualizar a skill tematica existente.
2. Para procedimento exclusivo da skill, usar `.agents/skills/<skill>/references/<tema>-playbook.md` e referenciar o arquivo em `SKILL.md`.
3. Para procedimento transversal, usar `playbooks/<tema>.md`.
4. Criar uma nova skill somente quando nenhuma skill existente possuir o dominio.
5. Criar ou atualizar playbook sempre que o aprendizado contiver passos executaveis, preflight, troubleshooting, gates ou validacao. Uma nota solta em memoria nao basta.
6. O manifesto pode marcar `SKILL=SKIP` ou `PLAYBOOK=SKIP` apenas com justificativa verificavel.

### Fase 4 - Gate de escopo

Classificar como `PRIVADO` ou `DISTRIBUIVEL`.

Tratar como privado qualquer segredo, identificador de conta, dado pessoal, caminho sensivel, IP, host interno, configuracao de producao, informacao de cliente ou detalhe que aumente risco operacional. Nunca copiar o mapa completo de recursos para artefato distribuivel. Segredo nunca entra em memoria, skill, log, Obsidian ou commit.

### Fase 5 - Validacao previa

Antes de escrever, validar destino, formato, duplicidade, links pretendidos, frontmatter e escopo Git. Se o artefato equivalente ja existir, atualizar em vez de duplicar. Bloquear a execucao se `SKILL_ALVO` ou `PLAYBOOK_ALVO` apontar para o comando roteador sem que o tema seja o proprio protocolo de capitalizacao.

### Fase 6 - Escrita serializada

Escrever localmente nesta ordem:

1. skill tematica;
2. playbook tematico e o link correspondente na skill;
3. codigo secundario, quando aplicavel;
4. memoria individual;
5. narrativa consolidada dentro do projeto, pronta para espelho humano;
6. indice `MEMORY.md` por ultimo;
7. log append-only de reconciliacao, quando aplicavel.
8. pasta duravel da sessao em `memory/sessions/<session_slug>/`, mantendo resumo, decisoes, aprendizados, artefatos, pendencias, manifesto e historico append-only em `evolucoes/`.
9. `provenance.yaml` na pasta da sessao, contendo somente envelopes sanitizados
   dos itens duraveis realmente persistidos.

Nunca criar indice apontando para artefato ainda inexistente. A persistencia no Mnemoverse acontece somente depois da validacao local e recebe apenas uma sintese redigida. Em `--dry-run`, nao escrever nada nem gravar no Mnemoverse.

### Fase 7 - Persistencia documental e Mnemoverse

Depois que os artefatos locais forem validados, completar as camadas de memoria
sanitizadas nesta ordem:

Antes da primeira escrita, executar o contrato `haos-memory-provenance`. Para
cada item duravel, preencher e validar:

```yaml
session_slug: nome-estavel-da-sessao
scope: projeto-ou-sistema
kind: decisao | aprendizado | procedimento | incidente | handoff
summary: fato-compacto-e-sanitizado
source: caminho-relativo-ou-evidencia
observed_at: ISO-8601
confidence: confirmed | inferred | pending
supersedes: id-ou-null
```

Buscar equivalencia por `session_slug`, `kind` e causa raiz antes de criar. Se
houver registro anterior, atualizar ou marcar `supersedes`; nao duplicar.

1. memoria local em `your-private-project/memory/sessions/<session_slug>/`;
2. memoria global em `HAOS_Memory/sessions/<session_slug>/`;
3. espelho humano em `Obsidian/HAOS-Codex-Xtreme3/01-Sessoes/<session_slug>/`;
4. commit local seletivo no repo `your-private-project`;
5. commit local seletivo no repo `HAOS_Memory`;
6. fila sanitizada de ingestao do GBrain Codex em `memory/inbox/evoluir/<session_slug>/`;
7. sintese duravel no Mnemoverse via `mcp__mnemoverse__memory_write`.

Depois de cada escrita, reler o destino e comparar pelo menos `session_slug`,
`kind`, `summary`, `source`, `confidence` e a referencia de supersessao. Sem
readback verificavel, o destino fica `PENDENTE`, mesmo que a chamada de escrita
tenha retornado sucesso tecnico.

Obsidian e os repositorios de memoria sao destinos autorizados do fechamento do
comando. Runtimes de servidor, Claude Code, HAOS_CC, Hetzner, OpenClaw, Hermes,
Google Drive e demais destinos continuam fora do escopo.

Regras dos espelhos e repositorios:

- copiar somente narrativa e memoria sanitizadas, nunca dumps, transcripts,
  segredos, dados pessoais, hosts, IPs ou inventarios internos;
- em worktree sujo, usar staging seletivo por lista de artefatos desta execucao;
- commit local nos dois repositorios e parte obrigatoria do fechamento quando o escopo estiver isolado;
- remote ausente, caminho ausente ou falha de autenticacao gera `PENDENTE` apenas
  para aquele destino.

Depois das camadas locais e dos espelhos sanitizados, salvar no Mnemoverse uma
unica sintese duravel e redigida da evolucao, usando
`mcp__mnemoverse__memory_write` quando a ferramenta estiver disponivel.

Regras da gravacao:

1. Usar o dominio `haos:evolucao` e conceitos curtos do tema.
2. Gravar somente aprendizado reutilizavel, decisao, causa/mitigacao, procedimento resumido, validacao e caminhos relativos dos artefatos criados.
3. Remover segredos, tokens, chaves, `.env`, dados pessoais, dados de clientes, dumps, transcripts completos, IPs, hosts, inventarios internos e caminhos absolutos sensiveis.
4. Nao usar `memory_delete`, `memory_delete_domain` ou salas compartilhadas como parte automatica do fechamento.
5. Registrar no relatorio o retorno real: `GRAVADO`, `FILTRADO` ou `PENDENTE`. Se o MCP estiver indisponivel ou falhar, nao inventar sucesso; o fechamento local continua valido e a pendencia deve ser declarada.

Esta gravacao redigida no Mnemoverse e uma camada adicional de memoria. Nao
atualizar, copiar ou subir nada para runtimes de servidor, HAOS_CC, Hetzner,
OpenClaw, Hermes, Claude Code ou Google Drive.

O claude-mem e automatico por hooks e deve ser apenas verificado. Ele nao faz
commit, Obsidian ou HAOS_Memory. O GBrain legado do Claude Code nao e automatico
para Codex e nao deve ser reapontado; o comando cria uma fila Codex sanitizada e
so declara `INGERIDO` quando uma integracao Codex for realmente executada e
validada.

### Fase 8 - Fechamento Git e espelhos

1. Executar auditoria de segredos.
2. Validar o diff.
3. Adicionar somente os arquivos produzidos pela tarefa atual.
4. Espelhar a narrativa sanitizada no Obsidian.
5. Adicionar seletivamente os artefatos no GitHub do projeto Codex.
6. Adicionar seletivamente a memoria sanitizada em `HAOS_Memory/sessions/<session_slug>/`.
7. Criar commits locais seletivos nos dois repositorios quando o escopo estiver isolado.

Usar `${USER_PROJECT_ROOT}/scripts/finish-task-haos.ps1` somente quando o worktree estiver limpo ou quando todo o escopo que ele adicionara pertencer comprovadamente a tarefa atual. Em worktree sujo, usar staging seletivo e registrar o fechamento sem capturar mudancas alheias.

### Fase 9 - Verificacao e relatorio

Provar, conforme aplicavel:

- arquivos existem;
- frontmatter parseia;
- skill passa no validador;
- playbook existe, possui passos acionaveis e esta ligado pela skill quando for especifico dela;
- links locais resolvem;
- indice aponta para artefatos existentes;
- auditoria de segredos passou;
- diff/staging contem apenas o escopo atual;
- commit local existe, quando solicitado;
- memoria local atualizada;
- Obsidian retornou `ATUALIZADO` ou `PENDENTE`;
- GitHub Codex retornou `COMMITADO`, `PUSH_FEITO` ou `PENDENTE`;
- GitHub global retornou `COMMITADO`, `PUSH_FEITO` ou `PENDENTE`;
- persistencia Mnemoverse retornou `GRAVADO`, `FILTRADO` ou `PENDENTE`;
- `provenance.yaml` contem envelopes validos, sanitizados e sem duplicatas;
- deduplicacao foi demonstrada por chave e decisao `CREATE/UPDATE/SKIP`;
- readback foi executado por destino, ou a impossibilidade foi marcada `PENDENTE`;
- nenhuma rotina de runtime externo, merge, deploy ou publicacao foi executada.

Se qualquer prova falhar, usar `STATUS: REVISAO NECESSARIA` ou `STATUS: BLOQUEADO`; nunca declarar sucesso parcial como conclusao total.

## Relatorio minimo

```text
STATUS: LOCAL_COMPLETE | EXTERNAL_PENDING | CONCLUIDO | REVISAO NECESSARIA | BLOQUEADO
EXECUTION_ID: ...
SESSION_NAME: ...
SESSION_ID: ...
SESSION_SLUG: ...
TEMA: ...
GATE_0: CAPITALIZA | SO_FECHA
RECONCILIACAO: fonte -> achado -> UPDATE/CREATE
SKILL_ALVO: nome -> caminho -> CREATE/UPDATE/SKIP -> motivo
PLAYBOOK_ALVO: nome -> caminho -> CREATE/UPDATE/SKIP -> motivo
MANIFESTO: CREATE/UPDATE/SKIP por artefato
ARTEFATOS: caminhos
VALIDACAO: checks e resultados
MEMORIA_LOCAL: ATUALIZADA | PENDENTE
OBSIDIAN: ATUALIZADO | PENDENTE
GITHUB_CODEX: COMMITADO | PUSH_FEITO | PENDENTE
GITHUB_GLOBAL: COMMITADO | PUSH_FEITO | PENDENTE
MNEMOVERSE: GRAVADO | FILTRADO | PENDENTE | NAO_APLICAVEL
GBRAIN_CODEX: QUEUED | INGERIDO | PENDENTE
PROVENIENCIA: VALIDADA | PENDENTE | NAO_APLICAVEL
DEDUPLICACAO: chave -> CREATE | UPDATE | SKIP
READBACK: destino -> VALIDADO | PENDENTE
PENDENCIAS: ...
```

## Stop rules

- Nunca bloquear ou emitir feedback por existir tarefa `running/reopened`; pergunta,
  correcao e continuacao do usuario tem prioridade e recebem resposta normal.
- Stop nao solicita continuacao por recibo ausente, inclusive em tarefa terminal;
  o main reconcilia antes da resposta final, sem deixar o hook disputar o chat.
- Nao substituir reconciliacao por "nao encontrei" sem busca demonstravel.
- Nao atualizar `haos-evoluir` apenas porque o comando executado se chama evoluir.
- Nao relatar "Skill Evolution atualizada". Informar o nome tecnico e o caminho exatos da skill tematica, por exemplo `evolution-api`.
- Nao usar memoria, journal ou Obsidian como substituto de skill/playbook quando houver aprendizado operacional reutilizavel.
- Nao sobrescrever contradicao antiga; marcar o registro anterior como superado e ligar as versoes.
- Nao tocar `your-private-project` salvo quando o tema envolver OpenClaw/Hetzner.
- Nao executar alteracao externa fora das camadas de memoria autorizadas e do
  push explicitamente aprovado.
- Nao atualizar ou subir artefatos em runtimes de servidor, Claude Code, Hetzner,
  OpenClaw, Hermes, Google Drive ou qualquer outro destino fora da memoria.
- Nao tratar marcador tecnico, pergunta `Y/n` ou silencio como aprovacao humana.
- Nao declarar memoria salva apenas porque a escrita retornou sucesso; exigir
  readback e comparacao dos campos-chave.
- Nao criar nova memoria quando a mesma causa raiz ja estiver registrada para a
  sessao; atualizar ou ligar por `supersedes`.
- Nao expor, imprimir, memorizar ou commitar segredos.

## Referencias

- `${HAOS_PRIVATE_ROOT}`
- `${HAOS_PRIVATE_ROOT}`
- `${HAOS_PRIVATE_ROOT}`
- `${HAOS_PRIVATE_ROOT}`
- `${HAOS_PRIVATE_ROOT}`
