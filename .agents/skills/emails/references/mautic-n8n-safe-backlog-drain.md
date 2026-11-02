# Drenagem segura de backlog n8n–Mautic

Use este playbook quando uma régua de e-mail possui backlog antigo, reservas
órfãs, execuções interrompidas ou risco de duplicação. O procedimento é
fail-closed: uma tentativa ambígua nunca volta automaticamente para a fila.

## Invariantes

- A identidade idempotente combina contato normalizado, régua e etapa.
- `accepted` é imutável durante reparo e rollback.
- `attempting` nunca é reenviado por idade; primeiro precisa ser reconciliado no
  Mautic.
- Só é recuperável automaticamente o `reserved` sem `contact_id`, sem `sent_at`
  e com lease expirado.
- Compra, DNC, oposição, consentimento e regras de saída são reavaliados no JIT
  antes do POST.
- Um erro antes do POST não prova envio; um timeout depois do POST também não
  prova ausência de envio.

## 1. Congelar e medir

1. Desabilite novos claims e suspenda apenas os triggers envolvidos.
2. Aguarde execuções ativas terminarem.
3. Capture workflow/version, crons, função de claim, controle, estados do
   dispatch, elegíveis vencidos e quota/reputação SES.
4. Habilite retenção de execuções com erro durante a recuperação.
5. Preserve backup privado do workflow e das funções; nunca grave credenciais no
   artefato de evidência.

Não use contagem de campanha, dashboard ou quota SES como prova de causa. Separe
capacidade do provedor, gargalo do workflow e falha de uma API JIT.

## 2. Reconciliar estados

### `attempting`

Para cada tentativa, procure `email_stats` por `contact_id`, `email_id` e janela
temporal estreita em torno do claim:

- exatamente um registro não falho: promover para `accepted` e avançar a etapa;
- nenhum registro: manter para revisão, pois o ponto exato da interrupção precisa
  ser provado;
- mais de um registro ou falha: `manual_review`.

Nunca converta `attempting` em `reserved` apenas porque passou tempo.

### `reserved`

Reclaim somente quando:

- `contact_id IS NULL`;
- `sent_at IS NULL`;
- lease superior ao limite operacional;
- enrollment continua elegível;
- chave idempotente permanece a mesma.

Se o enrollment deixou de ser elegível, preserve o estado terminal canônico da
máquina local, sempre sem envio. Por exemplo: consentimento, DNC, oposição ou
estado obsoleto podem resultar em `blocked_jit`, enquanto compra pode usar um
estado terminal próprio como `cancelled_purchase`. A transação deve exigir
cardinalidade exata e registrar um checkpoint agregado.

## 3. Endurecer dependências JIT

- Prefira fonte local/canônica já atualizada por webhooks a uma terceira consulta
  remota redundante por lead.
- Remover uma consulta redundante só é seguro quando compra e consentimento
  continuam cobertos por fontes independentes verificadas.
- Em APIs externas necessárias, use batching conservador, timeout explícito,
  retries limitados e espera entre tentativas.
- HTTP 429 ou 5xx antes do POST do Mautic mantém o item em `reserved`; não marque
  como aceito.
- Pare o bulk diante de novo erro de execução ou `attempting` órfão.

## 4. Liberar em ondas

1. Canário de 5.
2. Canário de 50.
3. Canário de 100.
4. Bulk somente depois dos três canários completos e sem ambiguidade.

Cada onda valida:

- quantidade reivindicada;
- quantidade bloqueada no JIT;
- quantidade aceita no Mautic;
- zero duplicata;
- nenhuma tentativa pendente após a execução;
- duração menor que o intervalo do trigger ou concorrência explicitamente
  dimensionada.

Dimensione o bulk por vazão sustentável da cadeia inteira, não só pelo limite do
SES. Inclua CRM, DWH, Mautic e qualquer API externa.

## 5. Watchdog

O watchdog registra apenas agregados sem PII e deve:

- parar/congelar em novo erro de execução;
- parar/congelar em `attempting` sem execução ativa;
- tolerar falha curta do próprio observador sem confundi-la com falha da
  produção;
- nunca reiniciar cegamente após timeout de observação;
- manter quota SES acima do backlog mais headroom;
- restaurar o cron normal somente após zero backlog e janela estável.

Se o observador perder acesso, consulte a fonte viva antes de reiniciar ou
congelar. Processo de monitoramento encerrado não prova que o workflow parou.

## 6. Critério de zero e restauração

O catch-up termina quando, no mesmo checkpoint:

- execuções ativas = 0;
- `attempting` = 0;
- `reserved` pendente = 0;
- `requeued` = 0;
- elegíveis vencidos sem dispatch = 0.

Depois:

1. congele novamente;
2. observe o ledger por pelo menos dez minutos;
3. exija fingerprint estável;
4. marque o run como `complete`;
5. restaure agenda, cron comercial e controle;
6. faça readback do workflow ativo.

Novos cadastros surgidos após a restauração pertencem à cadência normal e não
reabrem o backlog histórico, desde que seus timestamps e gatilhos confirmem essa
origem.

## 7. Prova final de entrega única

Para todos os dispatches `accepted`, faça uma reconciliação em massa com
`email_stats` usando `contact_id`, `email_id` e janela temporal:

- total aceito = total com exatamente um `email_stats`;
- ausentes = 0;
- múltiplos = 0;
- falhos = 0.

Também prove no ledger:

- `count(*) = count(distinct dispatch_key)`;
- no PostgreSQL, `count(*) = count(distinct (identity_hash, lane, step))`;
- bloqueados não possuem `sent_at`;
- o workflow voltou aos crons normais;
- a conta SES está habilitada e saudável.

Aceite técnico e `email_stats` não garantem colocação na caixa de entrada. O
relatório deve separar aceite Mautic/SMTP de inbox placement.

## Stop rules

- Não retry de estado ambíguo.
- Não ampliar audiência durante reparo.
- Não relaxar compra, DNC, consentimento ou oposição para zerar contador.
- Não usar DELETE/TRUNCATE como limpeza de fila.
- Não restaurar cron enquanto houver reserva segura ou elegível vencido sem
  dispatch.
- Não imprimir e-mails, telefones, tokens, cookies ou credenciais na evidência.
