---
name: haos-auto-brain
description: "Camada de auto-memoria que pesca aprendizados duraveis nos prompts do usuario e realimenta a memoria de longo prazo de forma barata. Use ao montar captura passiva de contexto, destilacao de memoria com 1 chamada de LLM, anti-duplicata de notas, fila de revisao/gap, ou quando quiser que um agente aprenda preferencias/regras/correcoes do usuario ao longo das sessoes sem custo alto. Inspirada nas ideias do GBrain (Garry Tan)."
---

# HAOS Auto-Brain

> **Creditos:** Inspirado nas ideias do GBrain de Garry Tan (github.com/garrytan/gbrain, MIT): ingestao automatica, `create_safety` (anti-duplicata) e gap analysis. Esta e uma reimplementacao adaptada ao stack HAOS (hooks Python + memoria markdown + um LLM barato via API compativel com OpenAI), nao o codigo do GBrain.

## O que e

O Auto-Brain e uma camada fina de auto-memoria. Ela observa os prompts que o usuario digita, separa o que e aprendizado duravel (preferencia, regra, fato sobre a pessoa/operacao, correcao) do que e efemero (tarefa pontual, pergunta, comando), e realimenta isso na memoria de longo prazo do agente, sem voce ter que pedir "lembra disso" toda vez.

O objetivo e simples: o agente fica mais alinhado a cada sessao, e isso custa quase nada, porque a captura nao usa LLM e a destilacao roda 1 chamada barata por execucao (em vez de ficar mandando tudo pra um modelo caro o tempo todo).

A ideia vem do GBrain (Garry Tan): ingerir contexto automaticamente, evitar duplicar o que ja existe (`create_safety`) e separar o que ficou ambiguo numa fila de gaps. Aqui isso foi reescrito no estilo HAOS: hooks Python + arquivos markdown como memoria, em vez de qualquer estrutura especifica do GBrain.

## As 3 pecas

### 1. Captura passiva (sem LLM, custo zero)

Um hook de "prompt submetido" faz um append de 1 linha JSON num inbox local por dia, com o prompt e uma flag `learning_candidate`. A flag e calculada por heuristica de palavras-chave (ex: "sempre", "nunca", "prefiro", "de agora em diante", "regra", "corrige") e descarta triviais ("ok", "sim", "vai") e comandos. Nada vai pra rede aqui. E um efeito colateral silencioso, dentro de `try/except`, que jamais quebra o fluxo principal.

Referencia: `reference/capture_block.py` (bloco `_is_learning_candidate` + `_capture_prompt`).

### 2. Destilador (1 chamada de LLM, com anti-duplicata)

Numa hora barata (ex: no fechamento de tarefa, ou via cron), um script le o inbox do dia, junta o indice atual da memoria + a lista de arquivos que ja existem, e faz **1** chamada a um LLM barato pedindo apenas APRENDIZADOS DURAVEIS que ainda NAO estejam na memoria. O modelo responde JSON com `learnings` (cada um com `title`, `type`, `body`, `action` CREATE/UPDATE/SKIP, `confidence`) e `gaps`.

A anti-duplicata (`create_safety`, ideia do GBrain) acontece de duas formas: mandamos a lista de arquivos existentes pro modelo no prompt, e ainda checamos no codigo antes de gravar (UPDATE so casa se o arquivo existir; o indice so ganha ponteiro novo se nao houver um).

Referencia: `reference/distiller.py`.

### 3. Fila de gap / revisao

O que veio com `confidence: low` ou como `gap` (ambiguidade, ponto a confirmar) NAO e gravado sozinho na memoria. Vai pra uma fila de revisao em markdown (checklist), pro humano confirmar ou descartar depois. So o que e claramente duravel e inequivoco (`confidence: high`) grava sozinho.

## Salvaguardas (importante)

- **Local primeiro.** A captura nunca toca a rede. A destilacao manda pro LLM SO os prompts do usuario + o indice da memoria, nunca dados sensiveis de terceiros (CRM, financeiro, PII).
- **Kill-switch.** Um arquivo-flag (ex: `.brain_off`) desliga captura E destilacao de uma vez.
- **So alta confianca grava sozinho.** O resto vira fila de revisao humana. O agente nunca "decide sozinho" sobre algo ambiguo.
- **Fail-safe.** Qualquer erro loga e sai com codigo 0; nunca derruba o hook nem o fechamento.
- **Idempotente.** Prompts ja processados ficam marcados e nao sao reanalisados (sem custo repetido).
- **Barato por design.** Captura = 0 LLM. Destilacao = 1 chamada por execucao, modelo barato, sem daemon, sem loop.
- **Sem segredos no codigo.** A chave de API e lida em runtime de uma variavel de ambiente / cofre, nunca embutida.

## Como adaptar (generico)

Os scripts em `reference/` sao genericos de proposito. Antes de usar, defina por variavel de ambiente / config:

- `HAOS_MEMORY_DIR` — pasta da sua memoria markdown (onde ficam os `.md` + o indice).
- `HAOS_BRAIN_DIR` — subpasta de trabalho do brain (inbox, fila de revisao, log, kill-switch). Default sugerido: `<HAOS_MEMORY_DIR>/_brain`.
- `OPENROUTER_API_KEY` (ou a chave do seu provedor compativel com OpenAI) — lida em runtime, nunca commitada.
- `HAOS_BRAIN_MODEL` — id do modelo barato (ex: um "flash/mini"). Opcional, tem default.

Nao assuma a estrutura interna de ninguem: a skill so precisa de uma pasta de notas markdown + um indice. O padrao de frontmatter das notas, os tipos (`user`/`feedback`/`project`/`reference`) e os gatilhos de aprendizado sao todos pontos de ajuste. Troque a heuristica de `learning_candidate` pelo vocabulario do seu usuario; troque o frontmatter pelo formato da sua memoria.

### Fluxo de instalacao tipico

1. Plugar o **bloco de captura** (`reference/capture_block.py`) no seu hook de prompt submetido.
2. Agendar o **destilador** (`reference/distiller.py`) numa hora barata (fechamento de tarefa ou cron diario). Rode com `--dry-run` primeiro pra ver o JSON sem gravar nada.
3. Conferir a **fila de revisao** de vez em quando e promover/descartar os itens de baixa confianca.
4. Kill-switch: criar o arquivo `.brain_off` no `HAOS_BRAIN_DIR` para pausar tudo.


## Adaptacao Codex HAOS

- Carregar `${HAOS_PRIVATE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
