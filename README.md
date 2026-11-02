# HAOS Codex Model

Modelo publico de orquestracao para Codex: regras de projeto, skills sob demanda,
papeis especialistas e verificacao com aprovacao humana. Conteudo generico e
portavel, sem configuracao de operacao privada. Nao e um servico gerenciado,
instalador automatico ou distribuicao do Superpowers upstream.

## Comecar

Leia [AGENTS.md](AGENTS.md) e [INSTALL.md](INSTALL.md) antes de copiar arquivos.
O [prompt de instalacao](PROMPT_INSTALACAO.md) delimita uma instalacao local
conservadora por capacidades. WORK/cloud pode oferecer workspace executavel
sem Windows local. Sem filesystem, conectores/APIs podem carregar conteudo
pertinente; isso nao comprova instalacao global nem persistencia.

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

Na raiz deste checkout, com Python 3.11+ e PyYAML 6.x ja disponiveis:

A dependencia de validacao esta fixada em [requirements-validator.txt](requirements-validator.txt)
(PyYAML 6.0.3). O CI instala esse arquivo no ambiente isolado do job; nenhuma
instalacao global no computador e necessaria ou implicada.

```sh
python -B scripts/validate_model.py
python -B scripts/model_routing.py
python -B -m unittest discover -s tests -v
```

O validador confere estrutura, referencias locais, matriz e candidatos sensiveis;
a suite testa esse comportamento. Isso nao comprova modelo efetivo, instalacao,
skills executadas, delegacao, hooks ou integracoes em funcionamento. O aceite
do runtime tem checks separados no [INSTALL.md](INSTALL.md).

## Catalogo completo e direitos

O pacote transporta 193 pastas de origem com procedimentos reais e recursos
portaveis, preservando os 29 metodos publicos anteriores. A uniao possui
207 skills: as 193 origens e 14 metodos adicionais. A [cobertura](playbooks/capabilities.md) aponta para inventario,
hashes, corpos portados, dependencias e motivos concretos de omissoes.
Os 34 agentes recebem skills por especialidade, nao todas para todos.
Consulte o [indice compacto](docs/skill-index.json) e leia apenas procedimentos
selecionados. O catalogo de proveniencia e para CI/QA, nao para carregar em
WORK a cada sessao. Busca local: `python -B scripts/model_routing.py --search tema`.

MIT da raiz cobre somente contribuicoes originais do modelo. Imports mantem
autoria e termos proprios; licenca desconhecida nao e licenca permissiva nem
exclusao automatica. Veja [avisos](docs/THIRD_PARTY_NOTICES.md).

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
