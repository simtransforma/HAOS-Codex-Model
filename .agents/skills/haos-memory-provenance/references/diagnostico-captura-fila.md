# Diagnostico de captura e filas de memoria

## Preflight

1. Confirmar o runtime Codex isolado, seu processo, bundle e banco antes de
   reiniciar. Nao alterar a instalacao Claude Code nem o servico GBrain compartilhado.
2. Verificar saude, readiness e integridade SQLite em snapshot consistente.
   Esses resultados nao comprovam processamento de todas as mensagens.
3. Separar fila pending/processing, itens concluidos, observacoes e resumos.
   Comparar snapshots com horario. Fila menor pode resultar de exclusao, nao
   apenas sucesso; inspecionar os caminhos de finalizacao antes de inferir.

## Diario privado

Executar, na raiz canonica, a CLI read-only:

```powershell
python -B scripts/haos_journal/diagnostics.py --config .codex/haos-paths.json --session-id SESSION_ID --dry-run
```

- `historical_gap` registra o inicio prospectivo, nao uma falha atual de leitura.
- `sequence` conta segmentos Markdown, nao mensagens capturadas.
- `gaps` e cumulativo; nao atribuir causas antigas sem evidencia individual.
- Em `SYNC_LIMITADO`, captura ativa e fonte validada, usar o sync existente em
  lotes limitados. Comparar offset, generation, backlog e contadores apos cada lote.
- Parar se houver divergencia, veto, ausencia de progresso ou fonte invalida.
  Nunca usar from-start, limpar gaps ou reativar opt-out para aparentar cobertura.
- Eventos internos conhecidos ficam excluidos; schema desconhecido gera marcador
  de lacuna sem persistir seu payload. Diario literal nunca vai a Git ou APIs.

## Provider e fila operacional

1. Diferenciar autenticacao, limite individual da chave, saldo e limite upstream.
   Uma chave aceita sem teto individual nao prova saldo nem capacidade disponivel.
2. HTTP 429 exige serializacao, backoff e Retry-After; HTTP 402 indica restricao
   de credito/orcamento. Nao trocar chave/modelo, ampliar gasto ou repetir chamadas
   indefinidamente para testar.
3. Diagnostico usa somente categorias permitidas. Nunca imprimir corpo bruto,
   excecao contendo credencial ou cofre. Loader seguro precede alegacao de chave ausente.
4. Antes de retomar backlog, auditar os caminhos de abort, quota, shutdown e
   finalizacao. Nao remover pendencias sem confirmacao de processamento duravel.
5. Protecao deve ser exclusiva do runtime Codex, ter testes com dados sinteticos,
   patch reproduzivel, build separado e rollback. Nao compartilhar alteracoes com Claude.
6. Endpoint que retorna contadores nao equivale a endpoint de recuperacao.
   Replay historico exige escopo limitado, deduplicacao, backup consistente e
   controle de custo; nao iniciar drenagem ilimitada de fila antiga.

### Padrao Codex para 429 recorrente no OpenRouter

1. Pausar somente o worker isolado e provar que a porta `37778` fechou.
2. Copiar `claude-mem.db`, WAL e SHM para backup local, registrar SHA-256 e nao
   copiar `settings.json` ou arquivos de segredo.
3. Identificar se o `429` e da conta, do OpenRouter ou do provedor upstream com
   diagnostico sanitizado. Health verde e chave aceita nao eliminam rate limit.
4. A tentativa de rede pode respeitar `Retry-After`, mas o esgotamento precisa
   encerrar o gerador com hard stop. Nunca devolver a mesma linha para um respawn
   automatico ilimitado.
5. Preservar a linha sem confirmacao em `pending`. Para backlog anormal, copiar
   tudo para uma tabela de quarentena na mesma transacao, conferir contagens e so
   entao retirar da fila ativa.
6. Manter o modelo escolhido como principal. Fallback precisa ser explicito,
   ordenado e registrado; ele serve para indisponibilidade/rate limit, nao para
   trocar silenciosamente a decisao de modelo.
7. Reconstruir apenas o bundle do worker Codex. Nao executar sync, instalador ou
   build que publique artefatos na instalacao do Claude Code.
8. Validar com um canario sintetico: fila volta a zero, observacao aparece no
   SQLite, log informa o modelo realmente usado e a auditoria retorna integridade
   `ok`. Backlog antigo deve ser quarentenado, nao apagado para melhorar o painel.

### Resposta individual maior que a janela do modelo

1. Nunca permitir que o truncamento transforme uma conversa valida em
   `messages=[]`. A mensagem mais recente deve continuar representada.
2. Recortar somente a janela curada enviada ao LLM. Preservar o evento bruto no
   armazenamento operacional para auditoria, reparo e nova extracao.
3. Para uma mensagem individual gigante, manter cabeca e cauda com marcador
   explicito de omissao. Aplicar limite proprio, menor que o limite total da
   conversa, para reservar capacidade de resposta do modelo.
4. Testar separadamente: funcao de truncamento, bundle ativo e canario semantico.
   Uma entrada repetitiva sem informacao pode produzir observacao vazia mesmo
   quando o transporte esta correto; isso nao prova falha de persistencia.
5. Se o canario vivo encontrar `429`, registrar a evidencia estrutural do recorte
   e manter a persistencia ponta a ponta como pendente. Nao confundir rate limit
   do provedor com regressao para payload vazio.
6. Nao drenar backlog grande automaticamente. Replay pode gerar custo, deve ser
   serializado, deduplicado e autorizado pelo owner.

## Aceite

Separar evidencias de codigo, ativacao viva, captura prospectiva e historico.
Timeout ou exit code zero de um runner nao substitui o veredito do revisor.
Fechar o Evoluir com readback por destino e registrar qualquer pendencia real;
nao chamar memoria integralmente recuperada quando houver lacunas nao verificadas.
