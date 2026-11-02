# OAuth e lives via YouTube Data API v3

## Preflight de acesso

1. Confirmar no Google Cloud qual projeto e cliente OAuth serao usados e se a
   YouTube Data API v3 esta habilitada. Nao confundir projeto habilitado com
   conta proprietaria autorizada.
2. Solicitar consentimento somente da conta Google proprietaria do canal de
   destino. Permissoes delegadas do YouTube Studio nao funcionam nas APIs.
   Gerar URL de consentimento apenas apos validar `client_id`, redirect URI,
   `state` e escopos; nao usar OAuth Playground para guardar token operacional.
3. Para leitura, preferir `youtube.readonly` quando a operacao permitir. Para
   `liveBroadcasts.insert` e `liveStreams.insert`, a documentacao aceita
   `https://www.googleapis.com/auth/youtube` ou
   `https://www.googleapis.com/auth/youtube.force-ssl`. Pedir somente o escopo
   necessario ao fluxo aprovado e proteger o refresh token no cofre.
4. Fazer `GET /youtube/v3/channels?part=id,snippet&mine=true`. Exigir o ID
   `${USER_RESOURCE_000050}` antes de criar a live do Clube. Se vier outro
   ID, parar: o token e de outro canal. `channels.list(id=...)` publico nao
   comprova que o token pode administrar esse canal.

## Modelo de operacao

- `liveBroadcast` e o evento agendado e sua privacidade; `liveStream` e a
  entrada do encoder. Criar um broadcast por noite nao equivale a repetir o
  mesmo MP4 no FFmpeg.
- Com autorizacao e escopo corretos: consultar eventos existentes, criar
  broadcast privado de teste (`liveBroadcasts.insert`), criar ou escolher
  stream (`liveStreams.insert` ou `list`), vincular (`liveBroadcasts.bind`),
  validar ingestao/status e so entao iniciar ou transicionar para `live`.
  Encerrar o evento e verificar estado final. A implementacao deve ser
  idempotente por janela/data e nao criar eventos duplicados em retry.
- Para piloto manual pelo Studio: no canal correto, abrir **Ao vivo > Gerenciar
  > Agendar transmissao > Criar nova**, escolher **Privado** e chave dedicada.
  Nao usar a live "Top Curiosidades" nem a chave padrao. Verificar as
  opcoes de inicio/fim automatico antes de enviar RTMPS; nao clicar em iniciar
  uma live publica como teste.
- Preferir RTMPS para ingestao. A chave e credencial: nunca incluir URL RTMPS
  completa em argumentos de chat, prints ou logs. Instalar via arquivo privado
  no servidor somente com aprovacao para o destino exato.
- O encoder preparado na Hostinger pode estar instalado sem estar ativo. Antes
  de ligar, verificar estado vivo do servico, canal, evento, privacidade,
  chave dedicada, direitos do video/audio e plano de parada/rollback.

## Checklist de monetizacao e miniatura

Preferencia explicita do usuario, recebida em 01/10/2026: manter monetizacao
ativada nas lives deste projeto e preservar as opcoes de anuncios que ele ja
escolheu. Tratar como criterio de verificacao por evento, nao como prova de
configuracao atual ou de receita garantida.

1. Confirmar o canal e o evento exatos no Studio antes de conferir monetizacao.
   Nao transportar a conclusao de uma live para outra.
2. Conferir monetizacao ativada e estado salvo antes de publicar. Elegibilidade,
   configuracao padrao, controle marcado sem salvar e encoder recebendo sinal
   nao comprovam esse estado. Reabrir a configuracao salva para readback quando
   necessario e registrar somente a evidencia nao sensivel.
3. Preservar as escolhas de anuncios existentes do usuario, incluindo formato
   e frequencia quando houver esses controles. Nao redefinir essas escolhas
   durante criacao, revisao ou reutilizacao de evento. Qualquer ajuste deve
   permanecer no escopo autorizado e terminar com nova conferencia do salvo.
4. Se monetizacao estiver desativada, indisponivel ou sem evidencia suficiente,
   informar a pendencia ao main antes de publicar. Nao inferir ativacao nem
   contornar restricoes da plataforma; main verifica a UI e resolve o gate.
5. Conferir miniatura especifica para a live e coerente com titulo, video e
   audio. Verificar legibilidade em tamanho reduzido, fidelidade ao conteudo
   e ausencia de promessas de resultados, inclusive financeiros.
6. Distinguir miniatura recomendada para apresentacao editorial de requisito
   tecnico para transmitir. Nao tratar a ausencia de upload personalizado como
   impedimento tecnico sem evidencia do fluxo atual; informar o que esta salvo
   e o que permanece pendente. Criar ou enviar imagem e uma acao separada, que
   deve respeitar o escopo aprovado.

## Fontes oficiais

- https://developers.google.com/youtube/v3/live/getting-started
- https://developers.google.com/youtube/v3/docs/channels/list
- https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/insert
- https://developers.google.com/youtube/v3/live/docs/liveStreams/insert
- https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/bind
- https://support.google.com/youtube/answer/9481328?hl=pt-BR
- https://support.google.com/youtube/answer/2907883?hl=pt-BR
