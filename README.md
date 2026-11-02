# HAOS Codex Model

Modelo publico de orquestracao para Codex: regras de projeto, skills sob demanda,
papeis especialistas e verificacao com aprovacao humana. Conteudo generico e
portavel, sem configuracao de operacao privada. Nao e um servico gerenciado,
instalador automatico ou distribuicao do Superpowers upstream.

## Comecar

Leia [AGENTS.md](AGENTS.md) e [INSTALL.md](INSTALL.md) antes de copiar arquivos.
O [prompt de instalacao](PROMPT_INSTALACAO.md) delimita uma instalacao local
conservadora. Uma interface de chat ou GPT Work sem filesystem e ferramentas
locais nao instala este modelo: pode analisar o material e preparar um plano.

O caminho de descoberta de skills e agentes varia conforme runtime, versao,
camadas de configuracao e confianca do projeto. Versoes recentes do Codex tambem
descobrem agentes em `.codex/agents/`; registro explicito continua sendo uma
opcao conservadora. Nenhuma dessas formas dispensa diagnostico e teste real.
Veja fontes oficiais e procedimento no [INSTALL.md](INSTALL.md).

## Mapa

| Local | Conteudo |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Contrato resumido e gates |
| [docs/MAIN_ORQUESTRACAO.md](docs/MAIN_ORQUESTRACAO.md) | Plano, delegacao, revisao e fechamento |
| [docs/CAPABILITIES.md](docs/CAPABILITIES.md) | Entregue, conceitual e opcional, sem confundir ativacao |
| [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) | Fronteiras das integracoes opcionais |
| `.agents/skills/` | Metodos locais, com `SKILL.md` por skill |
| `.codex/agents/` | Definicoes TOML de papeis, sujeitas ao schema instalado |
| `.codex/skill-routing.json` | Catalogo e associacoes declarativas de skills e papeis |
| `playbooks/` | Checklists reutilizaveis |
| `memory/` | Estrutura de memoria curada, nao diario de conversas |
| [hooks/README.md](hooks/README.md) | Contrato opcional, nao ativacao de hooks |
| [SECURITY.md](SECURITY.md) | Segredos, consentimento e relato de incidentes |
| [CHANGELOG.md](CHANGELOG.md) | Historico das mudancas documentadas |

## Validacao local

Na raiz deste checkout, com Python 3.11 ou superior e sem dependencias externas:

```sh
python -B scripts/validate_model.py
python -B -m unittest discover -s tests -v
```

O validador confere estrutura, referencias locais, matriz e candidatos sensiveis;
a suite testa esse comportamento. Isso nao comprova modelo efetivo, instalacao,
skills executadas, delegacao, hooks ou integracoes em funcionamento. O aceite
do runtime tem checks separados no [INSTALL.md](INSTALL.md).

## Operacao

Perguntas simples recebem resposta direta. Trabalho substantivo usa contexto e
evidencias, plano proporcional, catalogo de metadados, skills selecionadas e
especialistas disponiveis. Ondas tem no maximo tres agentes com owners
disjuntos; revisao e independente. Loops sao finitos e defeitos nao viram sucesso
por falta de tentativas. O Rito preserva suas 13 fases e gates.

Modelos sao escolhidos por capacidade e schema real, sem IDs universais. JEV e
opcional e fica desligado sem API autorizada. Evoluir e um fechamento conceitual
do main, nao promessa de captura, hook Stop ou sincronizacao de memoria.

Permissao local nao autoriza deploy, publicacao, envio, gasto, push ou merge.
Um OK externo explicito permanece valido no escopo ate concluir ou revogar,
sem renovacao por tempo; ampliacao material pede nova confirmacao.

O catalogo efetivo vem dos arquivos presentes e do diagnostico do ambiente,
nao de contagens promocionais. Conectores, autenticacao, bibliotecas externas e
testes operacionais nao sao implicados pela documentacao. Este modelo nao
substitui politica de seguranca, backup ou governanca do usuario.
