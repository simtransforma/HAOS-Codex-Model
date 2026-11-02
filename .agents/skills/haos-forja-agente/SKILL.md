---
name: haos-forja-agente
description: "Cria ou integra um agente HAOS no Codex com papel, TOML e roteamento verificaveis; use quando o usuario pedir novo especialista, conselheiro ou agente."
---

# Forja de Agente Codex

Todos os caminhos relativos nesta skill partem do repo canonico `${HAOS_PRIVATE_ROOT}`, nao do cwd nem do cache do plugin.

Crie um papel operacional verificavel no repositorio HAOS Codex. Um SKILL.md descreve procedimento; um agente e perfil de execucao em `.codex/agents/<slug>.toml`.

## Escopo

1. Feche o mandato literal: slug sem colisao, oficio em verbos, entradas, saidas, limites, departamento ou conselho e relacao com agentes vizinhos.
2. Leia pelo menos dois TOML locais pertinentes e os consumidores reais do agente. Verifique nomes, schema e campos aceitos no runtime atual; nao transplante frontmatter ou paths Claude.
3. Consulte `haos-model-router` e `${USER_PROJECT_ROOT}/.codex/haos-model-routing.json` para recomendacao; confirme IDs/roles no schema vivo. Papel novo sem suporte explicito usa `worker` com as instrucoes do TOML no briefing, se a ferramenta permitir.
4. Defina instrucoes especializadas claras, ferramentas pelo menor privilegio e limites de escalonamento. Nao conceda permissao externa por implicacao.

## Integracao

- Registre onde o repo realmente roteia esse papel: catalogo de agentes, router/matriz, comando e skill somente quando cada mecanismo existir e fizer parte do escopo autorizado.
- Atualize referencias e invocacoes que tornem o papel descobrivel, sem editar arquivos fora do ownership da tarefa. Se o escopo nao incluir um registro necessario, reporte integracao parcial.
- Conselho requer contrato explicito de participacao e voto no fluxo real; nao presuma que TOML sozinho altera o conselho.
- Nao imponha bump de versao, worktree, commit ou push por ritual. Subagentes nao fazem memoria ou commits independentes.

## Conteudo minimo do agente

- Declare missao, tarefas dentro e fora do escopo, entradas necessarias e entrega esperada.
- Delimite quando consultar outro especialista e quem decide em caso de conflito.
- Especifique evidencias que o agente deve devolver ao main, nao apenas uma conclusao.
- Evite instrucoes absolutas que conflitem com plataforma, pedido atual ou consentimento HAOS.
- Use exemplos locais pequenos para o TOML, preservando campos ja comprovados pelo parser.
- Nao replique todo o catalogo de skills no perfil; liste apenas as pertinentes ao oficio.
- Para papel que toca producao ou dados sensiveis, descreva gate e comportamento somente leitura antes do OK.
- Se o agente substituir outro papel, explicite migracao e compatibilidade; nao desative o antigo implicitamente.
- Se o nome colidir com marca, produto ou papel existente, resolva a ambiguidade antes de criar arquivos.
- Evite paths de perfil pessoal, alias de modelos Claude e referencias que nao existem no checkout Codex.
- Use defaults do runtime quando o campo opcional nao for necessario; nao invente schema.
- Mantenha o perfil conciso o bastante para ser carregado integralmente na invocacao.

## Validacao

- Parseie TOML com parser real, confira slug, campos, paths e ausencia de segredos.
- Valide JSON/YAML de registros alterados e referencias reais no repo.
- Teste o roteamento/invocacao no runtime disponivel; arquivo existente ou hook sugerindo papel nao prova que houve spawn.
- Se schema ou ferramenta de spawn estiver indisponivel, declare a lacuna e limite o aceite a validacao estatica.
- Entregue arquivos, teste executado e o que ainda precisa de recarga ou prova viva. Nao altere Claude Code.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
