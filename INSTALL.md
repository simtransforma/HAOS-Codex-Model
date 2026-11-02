# Instalacao local conservadora

Este procedimento e manual e seletivo. Nao substitui `config.toml`, `AGENTS.md`,
hooks, credenciais, memorias ou politicas existentes. O
[prompt pronto](PROMPT_INSTALACAO.md) delimita o mesmo escopo.

## 1. Identificar o ambiente

Confirme runtime, versao instalada, raiz do projeto, filesystem, shell e
ferramentas realmente disponiveis. "GPT Work" ou um chat no navegador nao
demonstram acesso local. Sem filesystem local autorizado, nao tente instalar:
entregue diagnostico e instrucoes, com `BLOQUEADO` para a instalacao dependente.
Nao instale um produto chamado GPT Work nem invente CLI, API ou acesso local.

Capture branch, diff staged/unstaged e arquivos novos antes de agir. Registre
um baseline e selecione somente arquivos necessarios. Preserve trabalho
concorrente. Consulte [AGENTS.md](AGENTS.md), [README.md](README.md), schemas e
fontes oficiais compativeis com a versao instalada antes de alterar config.

## 2. Preparar os arquivos

Escolha um destino local aprovado. Compare o conteudo existente antes de copiar.
Integre regras de `AGENTS.md` sem apagar instrucoes locais. Skills ficam em
`.agents/skills/<nome>/SKILL.md`; revise metadados e leia apenas as selecionadas.
Nas versoes atuais de referencia, a descoberta busca `.agents/skills` do cwd
ate a raiz do repositorio. Confira a raiz, os conflitos de nome e o diagnostico
da sua versao; arquivo presente nao prova skill carregada ou executada.

Copie apenas papeis necessarios de `.codex/agents/`. Nao sobrescreva skills,
papeis ou memoria existentes. Um conflito exige merge preservador ou decisao
objetiva do usuario. `memory/` e estrutura opcional: nao importe historico nem
ative captura de conversas. Nao copie configuracoes pessoais ou hooks de outro
ambiente. Nenhuma credencial e necessaria para ler estes documentos.

## 3. Descobrir ou registrar agentes

Versoes recentes do Codex tambem fazem autodiscovery dos TOML em
`.codex/agents/`, por camada de configuracao. Isso nao vale automaticamente
para toda versao, schema de arquivo ou projeto sem confianca. Verifique as
definicoes requeridas, warnings e schema multi-agent da sessao instalada.
Nao prometa que os TOML deste modelo serao aceitos sem esse diagnostico.

Quando necessario, use registro explicito como fallback conservador no
`config.toml` local aplicavel. Exemplo generico, a adaptar ao caminho e schema
da instalacao; nao e um comando de instalacao:

```toml
[agents.qa-reviewer]
description = "Revisao independente de qualidade e testes"
config_file = "/caminho/absoluto/projeto/.codex/agents/qa-reviewer.toml"
```

Faca merge da tabela, sem duplicar um papel ja existente. Preserve provider,
modelo principal, MCPs, permissoes, hooks e demais papeis. Na referencia atual,
caminhos relativos de `config_file` sao resolvidos a partir do `config.toml`
que os declara; um caminho absoluto adaptado evita ambiguidade entre camadas.
Nao substitua a configuracao inteira nem habilite recursos nao solicitados.

Use modelos por capacidade e parametros permitidos. Para papeis novos, effort
`high` e o padrao HAOS quando suportado; um papel pode fixar seu proprio effort.
Nao invente override de spawn, ID de modelo ou reducao silenciosa. Sem suporte,
declare o limite. Alterar TOML nao prova recarga em uma sessao ja aberta.

## 4. Validar de verdade

Na raiz do checkout completo do modelo, com Python 3.11 ou superior:

```sh
python -B scripts/validate_model.py
python -B -m unittest discover -s tests -v
```

Esses comandos sao offline e usam a biblioteca padrao. Validam o pacote e o
validador, nao demonstram agente, modelo efetivo ou integracao executada.
Uma instalacao seletiva ainda exige os checks do destino abaixo; nao copie
arquivos extras nem altere config apenas para simular um aceite completo.

1. Leia o diff completo contra baseline, incluindo arquivos novos da instalacao.
2. Valide TOML e frontmatter das skills com ferramentas disponiveis, e confirme
   os caminhos. Registre checks indisponiveis; nao instale validadores em silencio.
3. Confira diagnostico de config, catalogo de skills, agentes e schema real de
   delegacao. Warnings e rejeicoes precisam de explicacao, nao supressao.
4. Execute uma tarefa local inofensiva usando uma skill selecionada; confirme
   pelo artefato e pelo check que o procedimento foi aplicado.
5. Se houver delegacao real, chame um papel para uma leitura limitada, receba
   seu retorno e confira-o independentemente. Sem ferramenta, informe
   `DELEGACAO NAO TESTADA`; listar um agente nao equivale a executa-lo.
6. Distinga modelo/effort pedido, aceito e efetivo observado. Reavalie apenas a
   configuracao alterada se a versao exigir nova sessao ou recarga suportada.
7. Relate instalado localmente, carregado, executado e verificado como estados
   diferentes. Plano ou texto de hook nao comprova instalacao nem ativacao.

Nao teste publicacao, envio, producao ou integracoes pagas como parte deste
aceite. Integra-se cada servico depois, por escopo proprio e autorizacao.

## 5. Rollback e limites

Remova ou reverta somente as adicoes desta instalacao contra o baseline, apos
comparar o estado atual. Preserve alteracoes concorrentes; rollback destrutivo
ou alcance incerto exige confirmacao. Nao use reset amplo, remocao recursiva
indiscriminada ou copia integral de backup sobre config modificada por terceiros.

Nenhum hook, memoria remota, provider, LLM auxiliar, JEV, broker, RAG ou rede e
configurado por este texto. Veja [integracoes](docs/INTEGRATIONS.md) e
[hooks](hooks/README.md). Nao declare sincronizacao ou novo conteudo remoto sem
push autorizado e readback pelo integrador.

## Fontes oficiais

Consultadas em 2026-11-02; os links `main` sao moveis, nao garantia de suporte
na versao instalada. Compare o codigo/schema da release usada:

- [Loader de papeis e autodiscovery por camada](https://github.com/openai/codex/blob/main/codex-rs/agent-roles/src/loader.rs).
- [Schema de configuracao e registro de papeis](https://github.com/openai/codex/blob/main/codex-rs/config/src/config_toml.rs).
- [Raizes de descoberta de skills](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs).
