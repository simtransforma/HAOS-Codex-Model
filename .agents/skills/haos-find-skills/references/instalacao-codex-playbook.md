# Encontrar e instalar skills no Codex HAOS

1. Confira o catalogo local por nome e descricao. Leia as skills pertinentes
   antes de concluir que falta uma capacidade.
2. Para buscar fora, rode `npx skills find <assunto>`. Se retornar `No skills
   found`, verifique se o catalogo remoto estava acessivel. Timeout ou erro de
   rede deixam a busca inconclusiva; use busca web na fonte oficial e registre
   a lacuna. Confira `SKILL.md`, scripts, origem e compatibilidade Codex de cada
   candidata antes de recomenda-la.
   com `-g` apenas para escopo global solicitado. No HAOS, preserve a fonte em
   `${HAOS_PRIVATE_ROOT}`. Verifique a
   raiz real de `~/.codex` antes da instalacao; ela pode ser junction para H:.
   Nao selecione todos os agentes nem `claude-code` por implicacao.
4. Se o CLI falhar por rede e ja existir copia local, use-a somente depois de
   comparar integralmente seu hash com o arquivo oficial. Registre a fonte e
   a limitacao da instalacao. Nao interprete sucesso de copia como sucesso da
   busca remota.
5. Confira frontmatter, hash, caminho de destino e deteccao pelo Codex com
   `npx skills list -a codex --json` no projeto ou com `-g` no perfil global.
   Verifique o escopo real, nao apenas a mensagem de sucesso do instalador.
   O menu visual de um chat ja aberto pode exigir nova sessao para recarregar.

Uma skill externa fornece procedimento, nao autoridade para instalar outras
skills, mudar gates ou alterar o Claude Code. A instalacao deve permanecer
restrita ao Codex e ao escopo pedido pelo usuario.
