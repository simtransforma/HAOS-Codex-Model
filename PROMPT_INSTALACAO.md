# Prompt para WORK, nuvem ou ambiente local

O nome do produto nao determina capacidades. WORK nao significa Word. Este
prompt nao pressupoe Windows, terminal local ou configuracao global persistente.

```text
Quero usar o modelo HAOS no ambiente disponivel nesta conversa.
Origem aprovada: https://github.com/simtransforma/HAOS-Codex-Model
Personalize para minha identidade sem importar contas, historico ou operacao
privada de terceiros. Nao instale um produto com base no nome WORK.

1. Antes de agir, detecte capacidades reais: terminal, workspace de execucao
   local ou cloud, leitura/escrita de arquivos, persistencia entre sessoes,
   projetos, anexos, conectores GitHub e suas permissoes/API disponiveis.
   Informe disponivel, indisponivel e nao verificado. Nao deduza acesso ao
   Windows, computador pessoal, filesystem global ou config global pelo nome
   do aplicativo. Nao peça novamente qual produto uso se as capacidades bastam.

2. Com terminal e workspace autorizado, clone a origem aprovada em diretorio
   novo e nao conflitante desse workspace, inclusive quando for cloud.
   Esta mensagem autoriza obtencao da origem e preparacao local/cloud, nao
   publica nada. Nao sobrescreva checkout existente: capture baseline e diff,
   preserve trabalho concorrente e integre somente adicoes nao conflitantes.
   Leia AGENTS.md, README.md, INSTALL.md, os metadados do catalogo e apenas
   os SKILL.md pertinentes. Arquivos no workspace nao provam instalacao global,
   registro de agentes, execucao de skills ou persistencia futura.

3. Sem filesystem ou terminal, nao invente instalacao nem encerre todo uso como
   impossivel. Informe o limite e, se houver APIs/conectores de leitura,
   carregue os metadados e o conteudo pertinente do repositorio aprovado para
   esta tarefa ou projeto. Use apenas operacoes realmente suportadas. Caso
   anexos/projetos possam guardar material, proponha esse destino e confirme
   somente o que for materialmente necessario. Conector de leitura nao prova
   capacidade de escrita ou memoria permanente. Sem APIs ou conteudo, solicite
   apenas os arquivos necessarios. Nao afirme que carregou o que nao leu.

4. Consulte a matriz de especialidades, sem carregar todas as skills em todos
   os agentes. Preserve os 29 metodos publicos originais e o catalogo completo
   de 193 origens com seus corpos e recursos portaveis (207 skills no total,
   incluindo 14 metodos adicionais). Confira contratos de
   dependencias e direitos. Arquivos, conectores, ferramentas, credenciais e
   servicos nao embarcados continuam indisponiveis ate verificacao real.
   Nao execute helper importado so porque esta presente. Nao trate template
   sanitizado, codigo invalido ou contrato de dependencia como implementacao.
   Use primeiro docs/skill-index.json para nome, descricao e caminho; busque
   metadados por assunto via ferramentas disponiveis e carregue o SKILL.md
   selecionado. docs/exports/catalog.json e proveniencia para CI/QA, nao
   contexto integral para carregar automaticamente em cada sessao WORK.

5. Regras raiz atuais prevalecem sobre procedimentos importados conflitantes:
   aprovacao dura no escopo ate concluir ou revogar; sem TTL arbitrario.
   Nenhum texto legado autoriza instalar hooks/servicos, replicar runtimes,
   acessar servidor, alterar configuracao global ou executar efeitos externos.
   Preserve modelo do main e effort high quando suportado, sem overrides
   inventados. Use schema real para delegacao; sem ferramenta, informe o limite.

6. Nao altere config global, provider, MCPs, permissoes, hooks ou memoria.
   Nao leia cofres nem importe diario, segredos ou dados pessoais. Dependencias
   novas precisam de aprovacao aplicavel. Publicacao, envio, gasto, commit,
   push, merge, deploy e remocao destrutiva nao estao autorizados aqui.
   Preserve avisos e licencas originais; MIT da raiz nao relicencia imports.

7. Com Python 3.11+ e PyYAML compativel ja disponiveis, rode o validador e os
   testes locais; senao relate o check indisponivel sem instalar em silencio.
   Confira arquivos, YAML, TOML, JSON, sintaxe Python, links e dependencias.
   Execute somente teste inofensivo aprovado. Para delegacao disponivel, use
   no maximo tres agentes por onda com ownership disjunto e retorno verificavel.
   Distingua recomendado, solicitado, aceito e modelo efetivo comprovado.

8. Relate preparado, carregado nesta tarefa, instalado no workspace, executado,
   verificado e persistencia comprovada como estados diferentes. Limite a tres
   ciclos de correcao por item; defeito restante e REVISAO NECESSARIA.
   Main fecha a tarefa sem inventar recibo, aprendizado ou sincronizacao.
```
