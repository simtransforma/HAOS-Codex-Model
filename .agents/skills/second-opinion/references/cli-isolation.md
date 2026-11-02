# Playbook: revisores independentes no Windows

## Preflight comum

Usar apenas material selecionado e sanitizado. Nao enviar Master, transcript
integral, memoria pessoal ou diff amplo de outras tarefas. Resolver os pins de
models.json e verificar o help da versao instalada antes de executar.
Evidencia documental/local de um ID nao prova permissao na conta.

Criar pasta local exclusiva da revisao, fora do repo e das pastas de habilidades,
sob a area privada Codex-Data/reviews. Nao criar tarefa na sidebar. Reutilizar
autenticacao apenas pelos mecanismos suportados, sem copiar arquivos de segredo.
Nenhum comando abaixo foi executado para inferencia ao instalar esta skill.

## GPT Astra

Codex CLI 0.154.0 confirmou --ignore-user-config, --ephemeral, --sandbox read-only,
--skip-git-repo-check, --model e --output-last-message. Fixar gpt-6-astra e
model_reasoning_effort=max. Nunca usar resume, fork ou o historico desta conversa.

Usar CWD vazio e --ignore-user-config, desativar hooks, plugins, memories, apps,
multi_agent, shell_tool, unified_exec, browser_use, browser_use_external,
computer_use, in_app_browser, image_generation e workspace_dependencies por
flags da invocacao, sem alterar defaults globais. Desligar web_search por
configuracao da invocacao. Nao carregar MCP do projeto.

**Limite importante:** --skip-git-repo-check so dispensa a checagem Git.
--ignore-user-config nao prova que AGENTS global foi ignorado. Isolamento aqui
significa contexto novo sem historico, memoria ou pareceres anteriores, com
ferramentas indisponiveis e escopo somente leitura; nao e uma VM.
Conferir os eventos de inicio para contexto/ferramentas efetivos antes de declarar
isolamento. Se houver contexto herdado alem das regras estaticas de seguranca,
interromper: nao produzir um parecer dito independente.

Nao copiar auth.json para tentar contornar isso. Uma home totalmente isolada
requer autenticacao propria suportada; ausencia dessa autenticacao e pendencia,
nao motivo para reutilizar o historico do main ou outro modelo.

## Claude Fable 5.1

Claude Code 2.1.247: preferir nova invocacao -p --safe-mode --tools ""
--disable-slash-commands --strict-mcp-config --no-chrome
--no-session-persistence --output-format json --model claude-fable-5-1
--effort max. Safe mode preserva autenticacao suportada e desliga personalizacoes.
Nao passar --fallback-model e nao alterar os arquivos do Claude Code.

--bare e diferente: ignora OAuth/keychain e exige autenticacao API propria.
Nao forcar --bare sobre login de assinatura ja autorizado. Conferir modelo
principal efetivo nos metadados, nao confundir chamadas auxiliares com o parecer.

## Gemini

Gemini CLI 0.57.0 possui gemini-3.1-pro-preview; e o candidato documental atual,
nao garantia permanente de topo ou de acesso na conta. Verificar catalogo oficial
e modelos acessiveis e passar -m explicitamente, sem auto/Flash/Lite por omissao.

Usar GEMINI_CLI_HOME exclusivo, config de sistema explicita, tools.core vazio,
hooks e MCP vazios, sem extensoes e politica deny de todas as ferramentas.
Modo plan nao substitui deny. Material sanitizado via stdin; sem --yolo.
Nao copiar arquivos de credencial para a home. API pode receber a chave do
Master somente no ambiente do processo, por loader seguro.

## Kimi

Kimi Code 0.39.0: candidato de maior capacidade k3, alias local kimi-code/k3.
O default observado kimi-code/kimi-for-coding nao e o K3. Passar --model com o
alias resolvido. Conferir esforco max suportado, sem modificar o config global.
Consultar documentacao/catalogo antes da proxima revisao: melhor disponivel pode mudar.

Fornecer agente exclusivo com tools: [] e subagents: [], skills-dir vazio e
configuracao da invocacao sem hooks/MCP. Home exclusiva somente com autenticacao
suportada, nunca copiando credenciais existentes. -p recebe prompt como argumento,
nao por stdin; validar limite de tamanho antes de executar. Se material exceder,
usar transporte de entrada documentado na versao instalada ou declarar limite,
nao habilitar leitura irrestrita para resolver tamanho.
-p tem aprovacao automatica e nao aceita --plan: o bloqueio real e remover as
ferramentas, nao uma promessa no prompt.

## Verificacao e fechamento

Conferir modelo solicitado, resolvido e efetivo, codigo de saida, ferramentas
efetivas e hash do material. Em erro/timeout, relatar revisao parcial; nao
substituir modelo silenciosamente nem afirmar quatro revisores por tres respostas.
O main consolida e verifica; so ele executa Evoluir. Modelo configurado nao e
modelo testado. Falha de autenticacao deve consultar o Master antes de desistir.

Fontes: help local de cada CLI; [Codex](https://github.com/openai/codex);
[Claude Fable](https://service.example.invalid);
[Gemini](https://service.example.invalid);
[Kimi](https://service.example.invalid).
