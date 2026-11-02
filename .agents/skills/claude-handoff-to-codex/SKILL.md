---
name: claude-handoff-to-codex
description: "Converte um handoff/dump Markdown exportado do Claude Code para um handoff operacional do Codex/HAOS e prepara a retomada da tarefa na sessao atual. Use quando o usuario trouxer um MD de handoff/session summary/dump do Claude Code e quiser continuar a tarefa no Codex."
---

# Claude Handoff -> Codex

Esta skill adapta um handoff de sessao vindo do Claude Code para uso seguro no Codex/HAOS e, por padrao, prepara a retomada operacional na sessao atual.

## Quando usar

Use quando o usuario fornecer:

- um arquivo `.md` com resumo completo de uma sessao do Claude Code;
- um dump bruto deterministico de transcript do Claude Code;
- um handoff de projeto criado fora do Codex;
- um pedido como "converter handoff do Claude para Codex", "continuar aqui no Codex", "trazer essa sessao para ca".

## Regras obrigatorias

2. Ler o arquivo de origem completo antes de converter.
3. Nunca copiar valores de segredos, tokens, cookies, chaves, senhas ou `.env` para o handoff convertido.
4. Manter nomes de variaveis de ambiente quando uteis, mas sem valores.
5. Converter caminhos, comandos e rotinas para o contexto Codex/HAOS quando aplicavel.
6. Registrar explicitamente o que depende de Claude Code e precisa de equivalente Codex.
8. O resultado deve ser um handoff novo em `${USER_PROJECT_ROOT}/memory/handoffs/`, nao uma edicao destrutiva do arquivo original.
9. Depois de converter, ler o handoff convertido e preparar a retomada, salvo quando o usuario pedir apenas conversao ou usar `--no-resume`.

## Entrada esperada

```text
/haos:importar-handoff ${HAOS_PRIVATE_ROOT}
/haos:handoff-codex ${HAOS_PRIVATE_ROOT} --project ${HAOS_PRIVATE_ROOT}
```

Tambem aceita dumps brutos, por exemplo:

```text
```

Se nenhum projeto for informado, inferir nesta ordem:

1. caminho citado dentro do handoff;
2. workspace atual;
3. `${HAOS_PRIVATE_ROOT}` para tarefas do proprio HAOS.

## Workflow

### 1. Bootstrap

- Carregar HAOS quando a tarefa mencionar HAOS, Rito, agentes, Mega Brain, memoria, seguranca, deploy, servidor ou producao.
- Consultar `claude-mem` isolado se estiver pronto.
- Ler `session-handoff` como skill complementar quando for continuar a tarefa apos converter.

### 2. Inspecao do handoff original

Identificar e registrar:

- projeto e objetivo;
- branch e estado Git se houver;
- arquivos criticos;
- ferramentas usadas;
- comandos executados;
- decisoes;
- pendencias;
- bloqueios;
- acoes externas sensiveis ja feitas ou pendentes;
- referencias especificas a Claude Code, `.claude`, MCPs, agentes ou hooks.

Se o arquivo for um dump bruto, nao copiar a transcricao inteira por padrao. Gerar um indice operacional compacto com:

- metadados de parsing;
- janela temporal;
- ferramentas e volume;
- arquivos tocados;
- comandos executados;
- subagentes spawnados;
- secoes de continuidade como `O QUE FAZER`;
- aprendizados/pegadinhas quando existirem.

Manter o caminho do dump original como fonte detalhada. Usar copia integral somente se o usuario pedir explicitamente ou se o script for rodado com `-IncludeFullDump`.

### 3. Sanitizacao

Remover ou mascarar:

- valores de variaveis em `.env`;
- tokens, API keys, cookies, JWTs e bearer tokens;
- chaves privadas;
- URLs assinadas;
- credenciais de banco/SSH;
- qualquer bloco marcado como segredo.

Escrever no handoff convertido apenas:

- nome da variavel;
- onde ela deve existir;
- finalidade operacional;
- status `valor omitido por seguranca`.

### 4. Adaptacao Claude -> Codex

Converter:

- `.claude/handoffs` -> `${USER_PROJECT_ROOT}/memory/handoffs`;
- instrucoes "Claude Code" -> "Codex", quando forem sobre o runtime atual;
- hooks/comandos Claude -> comandos HAOS/Codex equivalentes, ou marcar `EQUIVALENTE A DEFINIR`;
- memoria Claude -> memoria tripla HAOS quando aplicavel;
- agentes Claude -> `.codex/agents/*.toml` ou skills HAOS, quando houver equivalencia.

Nao converter referencias documentais historicas quando elas forem parte da explicacao do que aconteceu.

### 5. Geracao do handoff Codex

Criar um novo arquivo:

```text
memory/handoffs/YYYY-MM-DD-HHMMSS-claude-to-codex-<slug>.md
```

O arquivo deve conter:

- metadados da conversao;
- resumo operacional;
- diferencas Claude/Codex;
- arquivos e comandos relevantes;
- pendencias e gates;
- proximas acoes para a nova sessao Codex;
- secoes de seguranca;
- conteudo convertido/sintetizado do handoff original.

### 6. Validacao

Antes de concluir:

- validar que o arquivo convertido existe;
- procurar padroes de segredo no arquivo gerado;
- validar que nao houve escrita no arquivo original;
- se houver script, rodar o modo de validacao dele;
- reportar caminho do handoff convertido e primeiro passo recomendado.

### 7. Retomada Codex

Depois da validacao, carregar o handoff convertido e montar a retomada:

1. Extrair projeto alvo, branch, arquivos criticos, comandos, pendencias, bloqueios e proximas acoes.
2. Validar existencia do projeto alvo e estado Git quando o projeto existir localmente.
3. Classificar cada proxima acao:
   - `PODE_EXECUTAR_LOCAL`: leitura, analise, edicao local dentro do projeto autorizado, validacao local.
   - `EQUIVALENTE_CODEX_A_DEFINIR`: ferramenta exclusiva Claude Code sem equivalente Codex confirmado.
   - `BLOQUEADO`: falta arquivo, login, permissao, repo ou informacao essencial.
4. Iniciar pela primeira acao `PODE_EXECUTAR_LOCAL`.

## Script recomendado

Use o script local quando existir:

```powershell
powershell -ExecutionPolicy Bypass -File "${HAOS_PRIVATE_ROOT}" -InputPath "<handoff.md>"
```

Com projeto explicito:

```powershell
powershell -ExecutionPolicy Bypass -File "${HAOS_PRIVATE_ROOT}" -InputPath "<handoff.md>" -ProjectPath "${HAOS_PRIVATE_ROOT}"
```

Para manter o dump inteiro dentro do handoff convertido:

```powershell
powershell -ExecutionPolicy Bypass -File "${HAOS_PRIVATE_ROOT}" -InputPath "<dump.md>" -IncludeFullDump
```

## Saida esperada

Responder com:

- arquivo gerado;
- origem lida;
- itens convertidos;
- itens marcados como pendentes;
- evidencia de sanitizacao;
- contexto carregado para retomada;
- primeira acao executada ou gate exato que impede execucao.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
