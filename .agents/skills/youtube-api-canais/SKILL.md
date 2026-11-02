---
name: youtube-api-canais
description: "Use para inventariar canais YouTube da SIM/usuario, verificar acesso do Studio versus OAuth, configurar YouTube Data API v3 e operar lives via API com identidade e canal corretos."
---

## Contrato publico de execucao

Material de dominio portado da fonte real, nao uma instalacao de infraestrutura.
As regras do usuario e do AGENTS.md prevalecem sobre comandos e exemplos abaixo.
Publicar, enviar, gastar, alterar servidores, reiniciar, apagar, push e merge
exigem consentimento explicito para o destino e a acao. Nao executar comandos
com placeholders. Nao buscar o cofre ou ambientes do autor. Ferramentas/MCPs
citados precisam existir na instalacao do usuario; nomes nao provam acesso.
Consulte [PORTABILITY.md](PORTABILITY.md) para dependencias, recursos omitidos,
licencas e adaptacoes. Exemplos preservados nao sao prova de estado vivo.

# YouTube API e canais HAOS

## Decisoes que esta skill protege

- Ler references/canais.md (user-supplied dependency; see PORTABILITY.md) para identificar o canal pelo
  ID, nao pelo avatar, titulo de uma live ou conta Google logada. O inventario
  registra apenas canais com evidencia; nao conclua que ele lista todos os
  canais do grupo.
- Acesso de administrador no YouTube Studio permite gerenciar lives na UI,
  mas permissao delegada nao concede acesso as APIs do YouTube. Para operacoes
  privadas ou mutaveis da YouTube Data API v3, usar OAuth de uma identidade
  proprietaria do canal. Chave de API nao substitui OAuth.
- Antes de qualquer chamada mutavel, executar `channels.list` com `mine=true`
  usando o token candidato e comparar o `items[].id` com o canal de destino.
  Nao confiar apenas em sucesso no consentimento OAuth ou em `channels.list`
  consultado por `id` publico.
- Projeto Google Cloud, API habilitada, cliente OAuth, escopos e acesso ao
  canal sao verificacoes separadas. O projeto historico `sim-make` e apenas
  candidato ate conferencia no Console; nao reutilizar tokens de Drive/GTM
  como se tivessem escopo YouTube.
- Segredos ficam no cofre canonico via loader seguro: nunca incluir client
  secret, refresh/access token, cookie, chave de stream ou URL RTMPS completa
  em skill, chat, commit, log ou screenshot. Nao aceitar chave enviada pelo
  usuario no chat; orientar entrada por canal seguro.
- Criar/alterar evento, conceder OAuth, iniciar live, enviar video, instalar
  segredo no servidor e habilitar servico sao acoes externas distintas.
  Aplicar o OK explicito do usuario ao escopo aprovado e validar o canal exato.

## Monetizacao e miniatura antes de publicar

- Preferencia explicita do usuario em 01/10/2026: as lives deste projeto devem
  ter monetizacao ativada. Antes de publicar cada evento, conferir no Studio
  o estado efetivamente salvo; elegibilidade do canal ou configuracao padrao
  nao comprovam que a monetizacao daquele evento esta ativada.
- Preservar as opcoes de anuncios ja escolhidas pelo usuario. Nao substituir
  formato, frequencia ou outras escolhas por um novo padrao. Se o estado salvo
  estiver desativado, indisponivel ou nao puder ser confirmado, sinalizar a
  pendencia e resolver com o main antes de publicar; nao declarar sucesso.
- Conferir miniatura especifica da live, legivel e fiel ao conteudo, sem
  promessa de resultados. Separar esse checklist editorial de obrigatoriedade
  tecnica: nao afirmar que o upload de miniatura personalizada e requisito
  para transmitir sem verificar a exigencia aplicavel no fluxo atual.
- Aplicar o checklist de [references/live-api.md](references/live-api.md).
  Esta preferencia nao comprova estado vivo nem amplia autorizacao externa.

## Roteamento

### Fonte e verificacao de loops

- Para um video administrado pelo canal, preferir o download oficial do
  Studio quando a obtencao publica falhar. Conferir o destino Downloads
  configurado no Windows antes de concluir que o download nao ocorreu;
  em 01/10/2026 foi `${USER_WORKSPACE_ROOT}`, diferente do caminho legado em C:.
- Validar duracao, codecs, decodificacao e hash local/remoto antes do envio.
  Cada live simultanea precisa de evento, chave e instancia exclusivos.
- Comprovar pelo menos uma volta da fonte mantendo o processo de encoder;
  estar ativo por mais que a duracao, sozinho, nao demonstra retorno ao inicio.
  Separar prova do loop, recepcao Excelente, publicacao no Studio e uptime 24h.
- Nao confundir previa com publicacao: conferir `Encerrar transmissao` e a
  linha do evento em `Ao vivo agora` com a visibilidade desejada. Registrar
  timeouts do Studio como falha de verificacao, nao como falha do servidor.

- Para descobrir ou atualizar canais: usar references/canais.md (user-supplied dependency; see PORTABILITY.md)
  e comprovar `channelId`, URL e papel por fonte recente. Adicionar um canal
  somente apos verificacao; indicar `A CONFIRMAR` para ownership/API nao testados.
- Para OAuth, live agendada e RTMPS: ler
  [references/live-api.md](references/live-api.md). Consultar a documentacao
  oficial atual e Context7 antes de alterar codigo ou configuracao de API.
- Para autenticacao Google geral, combinar com `google-cloud`; para o encoder
  do piloto, consultar `deploy/youtube-live-sim/README.md` e
  `<USER_DEPENDENCY:docs/YOUTUBE_LIVE_SIM_PILOTO_2026-09-28.md>`. Estado documentado nao prova
  estado vivo: verificar Studio/API/servidor no turno da operacao.

## Fontes primarias

- [Visao geral da Live Streaming API](https://developers.google.com/youtube/v3/live/getting-started)
- [Permissoes do canal e limite para APIs](https://support.google.com/youtube/answer/9481328?hl=pt-BR)
- [Identificar canal do token com channels.list](https://developers.google.com/youtube/v3/docs/channels/list)
