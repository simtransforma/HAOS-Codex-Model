# Readback remoto do Evoluir

1. Registrar tarefa e revisao antes do trabalho; nao criar uma tarefa por turno.
2. Validar fontes, hashes e revisao independente antes de capitalizar.
3. O integrador grava e rele os tres destinos locais antes do transporte remoto.
4. Mnemoverse usa o dominio HAOS existente. Buscar por igualdade do pacote curado
   na listagem recente paginada; usar busca semantica apenas como complemento.
5. Marcar tentativa antes do envio com identidade de tarefa, revisao e conteudo.
   Falha ambigua exige readback; nunca reenviar cegamente nem reescrever para
   contornar rejeicao por duplicidade ou relevancia.
6. GBrain usa a instancia compartilhada, namespace Codex e leitura de
   `compiled_truth`. `isError=true` nunca comprova sucesso.
7. Recibos precisam corresponder a tarefa, revisao e payload. Fila local nao
   equivale a ingestao; somente readback permite declarar o destino concluido.
8. SO_FECHA exige evidencia verificavel sem inventar aprendizado. Tarefa
   running/reopened passa silenciosamente, sem bloqueio ou feedback.
   Stop nao solicita continuacao, inclusive para tarefa terminal sem recibo
   compativel; o main reconcilia o fechamento antes da resposta final.

Stop ocorre depois da resposta registrada: nao corrige retroativamente uma
afirmacao falsa. O main continua obrigado a fechar antes da resposta final.
Vetos de registro, dry-run e somente leitura permanecem prioritarios.

O diario literal continua privado. Apenas sintese curada vai aos repositorios,
Obsidian, Mnemoverse e GBrain. Commit local nao equivale a push. claude-mem com
health pronto pode continuar com backlog e rate limiting; avaliar separadamente.
