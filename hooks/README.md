# Hooks opcionais

Esta pasta documenta um contrato. Nenhum hook e ativado por este documento;
um plano, nome de evento ou prompt nao comprova instalacao. Nao copie hooks,
paths, bancos ou permissoes de uma operacao privada.

## Antes de habilitar

Confirme versao e schema do runtime, evento suportado, owner, entrada minima,
saida, permissao, limite de tempo, tratamento de falha, deduplicacao, opt-out
e rollback. Faca merge seletivo preservando hooks gerenciados; nunca substitua
configuracao existente nem instale capturadores de memoria por padrao.

Teste sem efeitos externos: sucesso, falha, timeout, reentrada, tarefa ativa,
pedido de parada, ausencia de recibo e segredo sintetico. Ler configuracao ou
obter exit code zero nao prova execucao no evento real; confira a evidencia
correspondente sem registrar dados privados.

## Evoluir e Stop

Evoluir e a avaliacao automatica do main ao fechar a tarefa: resultado e
evidencias, aprendizado reutilizavel ou somente fechamento. Este modelo nao
implementa, por este texto, ledger, gravador de diario ou sincronizador remoto.
Subagentes nao duplicam o fechamento nem a memoria.

Se o ambiente implementar Stop, ele nao pode substituir a resposta ao usuario,
bloquear pergunta/correcao/continuacao por recibo ausente, solicitar continuacoes
automaticas ou disparar loops de encerramento. Tarefa em andamento nao e erro.
Main concilia pendencias antes de reportar; hook nao inventa sucesso nem fecha
por inferencia. Falha de observabilidade nao concede permissao para uma acao
sensivel; os gates de seguranca existentes permanecem aplicaveis.

JEV, se implementado separadamente, e consultivo e opcional. Sem API autorizada
fica desligado, com classificacao local. Nao recebe prompt bruto, memoria,
segredos ou caminhos privados, nem muda modelo, faz spawn ou autoriza rede.

Diario literal, caso explicitamente solicitado em implementacao separada, fica
privado e separado da memoria curada. Nao capturar retroativamente intervalo
recusado. Confira [seguranca](../SECURITY.md) e
[integracoes](../docs/INTEGRATIONS.md) antes de qualquer habilitacao.
