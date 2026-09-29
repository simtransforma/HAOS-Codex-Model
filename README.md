# HAOS Codex Model

Modelo publico e minimo de orquestracao para Codex. Ele mostra como combinar
regras de projeto, skills sob demanda, agentes especialistas, verificacao e
aprovacao humana. Nao e uma copia de nenhuma operacao real.

## Estrutura

- `AGENTS.md`: contrato do orquestrador e limites de autonomia.
- `.agents/skills/`: metodos reutilizaveis, cada um com `SKILL.md`.
- `.codex/agents/`: papeis de revisao que podem ser registrados no Codex.
- `playbooks/`: modelos de deploy, incidente e decisao.
- `memory/`: modelo de registro curado, sem transcricoes nem segredos.
- `hooks/`: contrato para hooks opcionais; nenhum hook e ativado por padrao.

## Comecar

1. Copie o conteudo para um projeto novo e personalize `AGENTS.md`.
2. Revise cada skill e agente antes de disponibiliza-los ao Codex.
3. Registre os agentes em sua configuracao local conforme [INSTALL.md](INSTALL.md).
4. Execute os checks do projeto e teste delegacao e aprovacao em ambiente de
   desenvolvimento antes de qualquer uso operacional.

O modelo nao inclui chave, provider, endpoint, nome de cliente, infraestrutura,
hook de memoria ativo ou permissao para publicar, enviar ou alterar producao.
Integracoes devem receber identidades proprias e aprovacao explicita.

O conjunto inicial tem 30 agentes TOML e oito skills genericas. Os agentes
precisam ser registrados na configuracao do seu Codex; apenas copiar os TOML
para o repositorio nao os ativa.

## Principios

- Leitura e diagnostico podem ser diretos; trabalho complexo pode ser delegado
  a especialistas com escopo e criterios de aceite.
- Uma resposta de agente nao e evidencia suficiente de conclusao. Execute
  testes e confira o resultado real.
- O Rito organiza fases e gates, sem conceder autorizacao externa.
- Skills sao carregadas por pertinencia; adicionar centenas ao contexto sem
  curadoria reduz a qualidade de selecao.

Este repositorio e um ponto de partida. Nao substitui politica de seguranca,
backup ou governanca do ambiente em que voce o instalar.
