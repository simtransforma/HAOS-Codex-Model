---
name: haos-model-router
description: "Recomenda modelo e effort para especialistas Codex por classe, trabalho, risco e fase, cruzando cache com allowlist do runtime; sem spawn ou alteracao global."
---

# Model Router Codex

Todos os caminhos relativos abaixo pertencem ao repo canonico
`${HAOS_PRIVATE_ROOT}`, nao ao cwd de outro projeto
nem ao cache do plugin. Execute a CLI usando esse caminho absoluto.

Aplicar `docs/MAIN_ORQUESTRACAO.md` e carregar `haos-superpowers` primeiro.
Fonte: `${USER_PROJECT_ROOT}/.codex/haos-model-routing.json`; CLI: `${USER_PROJECT_ROOT}/scripts/haos_model_router.py`.
Contrato completo, schemas e limites: `${USER_PROJECT_ROOT}/docs/MODEL_ROUTER_CODEX.md`.

## Classificar antes de delegar

- C0: pergunta direta; C1: ate cinco leituras. Main responde sem spawn e sem
  trocar modelo da sessao. Nao usar essas classes para disfarcar execucao externa.
- C2: especialidade; C3: multiplas frentes. Main apresenta plano curto, seleciona
  skills, reutiliza agente adequado quando comprovado e delega com donos disjuntos.
- Matriz: mechanical = Luna medium; routine = Sol medium; deep = Astra high;
  judgment = Astra xhigh. Arquitetura, causa raiz e seguranca sao deep.
  Estrategia, conselho, copy de alto valor e QA final sao judgment.
- Risco alto e verify: piso deep/high; acao externa e final: judgment/xhigh.
  Duvida sobe um degrau; pedido explicito superior e preservado como piso.
  Qualidade vem antes de custo; nao importar tarifas ou metas do Claude Code.

## Procedimento do main

1. Consultar o schema REAL da ferramenta de spawn na sessao. O snapshot embarcado
   registra a allowlist do schema `multi_agent_v1__spawn_agent`, inspecionado
   pelo main via `ALL_TOOLS` em 2026-10-04. E snapshot estatico de capacidades,
   nao relato do usuario nem prova de execucao. Reconfirmar o schema a cada spawn.
   Cache, TOML e config nao provam que um modelo/role esta aceito nesta sessao.
2. Executar a CLI com `python -B`, classificacao explicita e, quando atualizado,
   `--runtime-capabilities CAMINHO_JSON` com capacidades verificadas no schema.
   Nao editar modelos globais ou LLM de memoria. Nao descobrir capacidades por
   tentativas pagas. Sem schema disponivel: informar a limitacao antes do spawn.
3. Ler JSON, motivos e evidencias. `no_spawn`: resolver direto. `unavailable`:
   relatar a causa, sem fallback de familia, Terra, alias Claude ou modelo global.
   `ready`: recomendacao consistente com as fontes, nao prova de execucao.
4. Role customizado tem effort FIXO. Nunca adicionar `reasoning_effort` ao spawn
   desse role. Se insuficiente, nao carregado ou divergente do snapshot: usar
   `worker` com o effort recomendado e carregar `specialist_instructions_path`.
   Main le o TOML como TOML e incorpora `developer_instructions` no briefing;
   o caminho nao e parametro da ferramenta e nao se carrega sozinho.
5. Montar briefing com objetivo, contexto, aceite, skills e caminhos, ownership,
   limites e evidencias esperadas. Incluir `PLANO:`, `SKILLS:` e `MODELO: ... porque`.
   `spawn_parameters` e fragmento: falta o briefing e qualquer campo exigido pelo
   schema vivo. Nao passar o JSON completo como argumentos nem inventar overrides.
6. C3 usa no maximo tres agentes por onda. Usar `fork_turns=none` ou ate quatro
   somente quando o schema suportar; senao `fork_context=false` se disponivel.
   Nao inventar esses campos quando ausentes. Verificar resultado e testes antes
   de fechar; subagentes nao comitam nem fazem memoria/Evoluir independente.
7. Em C2/C3, mostrar no chat antes da delegacao `rota recomendada: classe,
   especialista, modelo/effort e motivo`. Apos a chamada real, distinguir
   `spawn aceito com parametros solicitados` de modelo efetivo comprovado;
   comunicar progresso/QA em mudancas relevantes. Se o JSON retornar
   `unavailable`, explicar a limitacao sem fallback oculto. C0/C1 nao exibem
   banner nem sao interrompidos pelo roteamento.

## Limites obrigatorios

Recomendacao nao autoriza enviar, publicar, gastar, alterar infra, push ou merge.
Nao instalar hooks DENY, nao tocar config/main/AGENTS/plugin/perfil e nao fazer
spawn a partir desta CLI. Skill nova nao prova recarga do catalogo instalado.
Pedido de effort maior que o suportado retorna unavailable; nao reduzir em silencio.
Se um pedido indicar modelo exato nao representado pelas flags de piso, resolver
essa restricao explicitamente no main; a CLI nao inventa substituicao equivalente.
Jev/TypeSafe participa automaticamente como classificador auxiliar no hook global
`haos_jev_autoroute.py`. O hook envia somente categorias fixas extraidas localmente,
nao o prompt bruto, memoria ou segredos, e devolve recomendacao consultiva.
Conferir a sugestao contra o pedido real, catalogo de agents/skills e pisos locais.
Jev nao e modelo Codex de spawn nem substitui os pisos deterministas. Em erro,
baixa confianca ou ausencia de sugestao, classificar localmente sem interromper
o pedido. Nenhuma sugestao autoriza mutacao externa.
