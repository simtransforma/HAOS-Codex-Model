# Capacidades e limites

Este mapa distingue artefatos do modelo, contratos textuais e integracoes.
Nao e inventario de ferramentas ativas no computador do usuario. Descubra o
catalogo pelos metadados presentes e pelo diagnostico do runtime, sem contagens
fixas que fiquem desatualizadas ou prometam cobertura inexistente.

## Artefatos verificaveis

| Artefato | O que entrega | O que nao comprova |
| --- | --- | --- |
| [AGENTS.md](../AGENTS.md) | Regras de projeto e gates | Aplicacao infalivel pelo modelo |
| [MAIN_ORQUESTRACAO](MAIN_ORQUESTRACAO.md) | Contrato de plano, ondas, revisao e fechamento | Scheduler ou ferramenta de spawn |
| `.agents/skills/` | Skills locais com nome, descricao e procedimento | Carregamento de todas ou execucao automatica |
| `.codex/agents/` | Definicoes de papeis em TOML | Aceitacao pelo schema ou agente ativo |
| `.codex/skill-routing.json` | Catalogo e associacoes por papel/rota | Motor de dispatch ou slash commands instalados |
| `playbooks/` | Checklists de trabalho | Procedimento executado ou ambiente configurado |
| `memory/` | Estrutura para conhecimento curado | Captura de chats, memoria remota ou sync |
| [INSTALL.md](../INSTALL.md) e [prompt](../PROMPT_INSTALACAO.md) | Procedimento de instalacao local seletiva | Produto instalado por um chat sem filesystem |
| [hooks/README.md](../hooks/README.md) | Requisitos para hooks opcionais | Hook, ledger ou Stop ativados |
| `scripts/validate_model.py` e `tests/` | Validador offline e suite unittest | Modelo efetivo ou execucao ponta a ponta no runtime |

## Catalogo por pertinencia

O export integral cobre 193 origens e preserva os 29 metodos publicos anteriores.
A contagem da uniao e calculada dos arquivos, sem predeterminar os overlaps.
Veja [cobertura integral](../playbooks/capabilities.md),
[contrato do export](EXPORT_CONTRACT.md) e
[direitos dos imports](THIRD_PARTY_NOTICES.md). A matriz e reconstruida por CLI
dos frontmatters reais para as especialidades dos 34 papeis, nao por broadcast.

As skills locais incluem roteamento (`haos-router`), fases (`haos-rito-v2`),
ondas (`haos-execution-waves`), evidencia (`haos-evidence`), engenharia
(`haos-engineering`), memoria curada (`haos-memory`), seguranca
(`haos-security-review`) e isolamento opcional (`haos-worktree`). Consulte os
frontmatters reais para selecao e a matriz local para associacoes por papel.

O catalogo inclui tambem pesquisa (`haos-deep-research`), alegacoes e fontes
(`haos-claim-verification`, `haos-source-quality-auditor`), capacidade consultiva
(`haos-model-router`), fechamento e proveniencia (`haos-evoluir`,
`haos-memory-provenance`), transferencia e importacao (`haos-session-handoff`,
`haos-session-dump`, `haos-dump-import`) e adaptacao de metodos
(`haos-superpowers`). O core original e preservado; procedimentos importados
mantem proveniencia e termos proprios. Nenhum deles e conector autenticado.

Os papeis TOML cobrem especialidades como produto, engenharia, dados, criativo,
automacao e revisao. O nome do arquivo nao garante credencial profissional,
ferramenta de dominio ou modelo particular. Instalacao e descoberta variam por
versao e camada; [INSTALL.md](../INSTALL.md) explica autodiscovery recente e
registro explicito conservador. Prova de delegacao exige chamada e retorno.

## Contratos, nao engines

- Rito: 13 fases na skill publica correspondente, com gates e evidencia.
- Modelos por capacidade: politica textual; nao implica roteador executavel,
  benchmark, ID fixo ou garantia de modelo efetivo.
- Evoluir automatico: skill de avaliacao do main; nao implica gravador, ledger,
  sincronizador, commit ou hook de fechamento instalado.
- Adaptacao Superpowers: fronteiras de uso opcional; upstream nao incluido por
  esta documentacao. A matriz local associa metodos, nao instala o upstream.
- JEV e demais conectores: opcionais e separados; sem API autorizada, JEV
  permanece desligado e o main classifica localmente.

## Validacao e manutencao

Antes de afirmar uma capacidade, confira arquivo, formato, schema, catalogo
carregado, chamada real e resultado conforme o nivel alegado. Checks estaticos
nao provam comportamento do agente nem integracao ponta a ponta. Uma nova
definicao nao prova recarga de sessao aberta. Sem teste, marque `NAO TESTADO`.

Confira [integracoes opcionais](INTEGRATIONS.md). Este pacote nao entrega
credenciais, endpoints privados, operacao pessoal ou conectores autenticados.

Na raiz do checkout completo, execute os checks offline com Python 3.11+ e
PyYAML 6.x disponivel (scripts/model-requirements.txt):

```sh
python -B scripts/validate_model.py
python -B -m unittest discover -s tests -v
```

O resultado corresponde ao pacote lido naquele momento. A suite testa o
validador; nenhum PASS estatico comprova agente carregado, modelo efetivo,
delegacao, hook, entrega externa ou ausencia infalivel de segredos.
