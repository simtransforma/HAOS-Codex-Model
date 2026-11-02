# Fechamento verificado do Evoluir

1. Main registra tarefa estavel e revisao, nao uma tarefa por chamada ou turno.
2. Validar entrega e evidencia. CAPITALIZA atualiza skill/playbook do dominio;
   SO_FECHA verifica sem fabricar conhecimento. Evidence e um arquivo existente
   sanitizado com SHA256, acompanhado do motivo da verificacao.
3. Gerar manifesto curado e chamar finish-task-haos.ps1 com -Integrator.
4. O helper verifica repo local, HAOS_Memory e Obsidian e executa os conectores
   remotos. O completer registra avaliacao e conclui o ledger apenas quando
   todos os destinos requeridos estiverem confirmados.
5. Mnemoverse: usar somente chave validada carregada em memoria; conferir o
   conteudo EXATO por memory/recent paginado. Busca semantica por hash pode
   omitir uma memoria que foi gravada. Nao usar contagem como comprovante.
6. GBrain: respeitar URL e bearer do perfil Codex, namespace codex/evoluir,
   campo compiled_truth e isError. Nao iniciar instancia ou banco separados.
7. Repeticao usa a mesma tarefa/revisao e compara conteudo antes de escrever.
   Tentativa Mnemoverse ambigua nao pode ser reenviada cegamente. Marcador inclui
   tarefa, revisao e conteudo; nova revisao nao herda bloqueio da anterior.
8. Stop deixa todas as respostas passarem em silencio e nunca substitui a
   pergunta do usuario. Recibo terminal ausente ou incompativel e verificado
   pelo main antes da resposta final, sem continuacao do hook. Waiting/blocked
   e pendencias remotas nao iniciam loops. Veto, leitura e subagentes prevalecem.

## Manifesto aprovado e notas de fechamento

O manifesto-base pode ter sido avaliado antes do integrador. Nesse caso,
`assess_closure` aceita somente as tres notas locais da mesma sessao, preserva
artefatos, revisao, gate e review originais e exige os cinco destinos. Nao apagar
o ledger nem criar outra identidade de sessao para contornar imutabilidade.
O manifesto final fica persistido antes da tentativa remota, permitindo retomada
com a mesma tarefa/revisao. Erros do integrador devem manter causa objetiva,

Separar execucao controlada dos hooks de disparo nativo pelo aplicativo. Um
checkpoint lido durante o turno nao comprova o Stop que ainda nao ocorreu.
Fonte arquivada pode ser reconciliada pelo diario somente apos validar a mesma
identidade e continuidade; preservar offsets, lacunas e opt-outs existentes.

## Limites operacionais

- Stop ocorre depois da resposta registrada; nao desfaz texto exibido.
- Regra automatica nao prova captura integral; relatar estado vivo do diario.
- Diario historico sem fonte completa nao pode ser reconstruido por invencao.
- Health claude-mem e observacao enfileirada nao comprovam sumarizacao pelo LLM.
- MCP nativo com ambiente antigo pode exigir recarga; o conector do fechamento
  usa credencial em memoria e nao depende da recarga desse processo antigo.
- Commit local nao e push. Publicacao GitHub continua separada e autorizada.
- Nada deste procedimento instala ou altera configuracao no Claude Code.
