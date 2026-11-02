# Prompt de instalacao local

O texto abaixo e generico e pode ser usado por qualquer usuario. A autorizacao
alcanca somente a instalacao local delimitada, nao integracoes ou publicacao.

```text
Quero instalar o modelo publico HAOS Codex no meu ambiente local, preservando
minhas configuracoes e arquivos. Personalize para minha identidade sem importar
identidade, caminhos, contas ou operacao de quem publicou o modelo.
Origem publica: https://github.com/simtransforma/HAOS-Codex-Model

1. Detecte o ambiente real: runtime e versao, ferramentas, raiz do projeto,
   acesso autorizado a filesystem local e shell. Nao presuma que GPT Work ou
   um chat de navegador tenha esses recursos, nem instale um produto com esse
   nome. Se houver apenas browser ou faltar acesso local, informe BLOQUEADO
   para instalar e entregue o plano. Nao simule instalacao com texto ou links.

2. Leia README.md, INSTALL.md e AGENTS.md dessa origem antes de instalar.
   Esta mensagem ja autoriza leitura/download do repositorio publico indicado
   e clone para um destino local novo verificado; nao exija outro OK para a
   mesma origem e acao. Confira que o destino nao existe ou esta vazio e nao
   sobreponha checkout existente. Se faltar o destino ou houver conflito real,
   pergunte somente pelo que falta. Sem acesso as fontes, informe a lacuna.
   Nao procure fontes privadas, cofre, dados pessoais, clientes ou memorias
   alheias. O clone apenas prepara a fonte; nao comprova a instalacao.

3. Alem da obtencao da fonte acima, autorizo apenas adicoes locais nao
   conflitantes no destino aprovado. Se faltar o destino, pergunte por ele. Capture
   baseline, branch, diffs e novos arquivos; preserve alteracoes concorrentes.
   Faca plano curto dos arquivos e checks. Nao substitua AGENTS.md, config,
   hooks, skills, agentes ou memoria existentes. Para integrar um conflito,
   apresente diff seletivo e obtenha decisao antes da escrita conflitante.

4. Consulte metadados das skills disponiveis e leia somente as pertinentes.
   Confira a versao do runtime e documentacao/schema oficiais atuais. Skills
   podem ser descobertas de .agents/skills do cwd ate a raiz do repositorio;
   agentes podem ter autodiscovery em .codex/agents por camada nas versoes
   recentes. Nao universalize isso: confira diagnostico e schema da sessao.

5. Se precisar registrar papel explicitamente, proponha merge minimo de
   [agents.nome] com description e config_file compativeis com a versao.
   Preserve provider, modelo principal, MCPs, permissoes, hooks e papeis atuais.
   Um config_file de exemplo precisa ser adaptado ao destino local real.
   Nao sobrescreva config inteira, nao invente flags, overrides ou IDs de
   modelo. Novos papeis usam effort high quando suportado, sem reduzir em
   silencio. Nao prometa heranca ou modelo efetivo sem evidencia do runtime.

6. Copie apenas artefatos necessarios e nao conflitantes. Nao importe diario
   ou historico, nao ative hooks/captura de memoria, JEV ou conectores, nao
   altere politicas de seguranca nem instale dependencias sem novo OK.
   Nao publique, envie mensagens, gaste, comite, faca push/merge/deploy ou
   remocao destrutiva. O OK desta tarefa dura no escopo ate concluir ou revogar;
   mudanca material de acao, destino, risco ou gasto exige nova confirmacao.

7. Verifique diff e links, frontmatter e TOML com ferramentas disponiveis,
   caminhos, diagnostico de configuracao e catalogo carregado. Execute tarefa
   local inofensiva com uma skill selecionada e confira o resultado real.
   Se houver ferramenta de delegacao, chame um agente para leitura delimitada,
   receba o retorno e revise independentemente; ate tres por onda, com owners
   disjuntos. Sem ferramenta, declare DELEGACAO NAO TESTADA. Nao invente spawn.
   Distinga parametros recomendados, solicitados, aceitos e modelo efetivo.

8. Use no maximo tres ciclos de correcao e verificacao por item. Defeito
   restante e REVISAO NECESSARIA, nao sucesso. Relate arquivos adicionados ou
   integrados, checks e resultados, nao testados, conflitos e rollback seletivo.
   Diferencie preparado, instalado, carregado, executado e verificado. Plano,
   TOML ou texto de hook nao comprovam instalacao. Nao declare novo conteudo
   remoto sem push autorizado e readback pelo integrador.

9. Main avalia Evoluir ao encerrar, sem inventar aprendizado ou identificador
   de tarefa. Memoria curada exige autorizacao, proveniencia e readback; diario
   literal continua privado. Este prompt nao autoriza persistencia de memoria.
   Stop nao substitui minhas perguntas, correcoes ou continuacoes nem bloqueia
   a conversa por falta de recibo. Apresente STATUS, evidencias e limites reais.
```
