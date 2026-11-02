# Playbook — ciclo de vida de refresh token Google OAuth

## Objetivo

Diagnosticar e corrigir expiracao recorrente de refresh tokens Google sem confundir
modo Testing, revogacao comum e controle de sessao/RAPT. Aplicavel a integracoes de
Drive, Docs, Sheets, GTM, GA4, Search Console e n8n.

## Guardrails

- Nunca imprimir client secret, refresh token, access token, authorization code,
  cookie, URL de consentimento completa ou conteudo do cofre.
- Confirmar somente presenca, resultado booleano, categoria de erro e status HTTP.
- Alterar consent screen, credencial remota, workflow ou infraestrutura somente com
- Fazer backup e readback antes de trocar referencias de credencial no n8n.
- Nao prometer token eterno. Documentar os eventos que ainda podem revoga-lo.

## Arvore de diagnostico

1. Trocar o refresh token por access token em chamada segura, sem imprimir payload.
2. Classificar o resultado:
   - `invalid_grant` + `invalid_rapt`: suspeitar de reautenticacao/controle de sessao;
   - `invalid_grant` + revogado/expirado: verificar senha, revogacao, inatividade e
     limite de tokens;
   - access token obtido, mas API retorna `403`: verificar escopo/permissao, nao
     rotacionar automaticamente.
3. Inspecionar o tipo de audiencia do aplicativo:
   - `Externo + Testing`: refresh token pode expirar em 7 dias;
   - `Interno`: a regra de 7 dias nao se aplica;
   - `Externo + Em producao`: a regra de 7 dias nao se aplica, mas outras causas
     continuam validas.
4. Inspecionar os escopos efetivamente devolvidos pelo token. Se houver
   `https://www.googleapis.com/auth/cloud-platform` em um token operacional, tratar
   como acoplamento indevido e candidato a `invalid_rapt`.

## Regra de arquitetura

Separar duas credenciais:

| Credencial | Uso | Escopos/identidade |
|---|---|---|
| OAuth operacional | Drive, Docs, Sheets, GTM, GA4, Search Console | somente escopos das APIs necessarias |
| Infraestrutura GCP | Cloud Resource Manager, Service Usage, Billing, Cloud Run etc. | service account/ADC ou OAuth separado com menor privilegio |

Nunca adicionar `cloud-platform` ao token operacional apenas por conveniencia. Essa
mistura faz automacoes de negocio herdarem a politica de sessao do Google Cloud.

## Rotacao segura do token operacional

1. Mapear consumidores atuais e preservar o estado ativo/inativo dos workflows.
2. Gerar nova autorizacao com:
   - `access_type=offline`;
   - `prompt=consent` apenas na rotacao que precisa devolver novo refresh token;
   - somente escopos operacionais necessarios;
   - sem `include_granted_scopes=true` quando o objetivo for remover um escopo antigo,
     pois a concessao incremental pode reincorporar `cloud-platform`.
3. Trocar o authorization code no listener local e salvar o refresh token somente no
   cofre aprovado.
4. Validar o refresh imediatamente e afirmar apenas:
   - access token recebido;
   - tempo de expiracao do access token;
   - booleans por familia de escopo;
   - `cloud-platform=false` para a credencial operacional.

## Propagacao no n8n

1. Listar os workflows consumidores e salvar backup individual.
2. Criar uma nova credencial criptografada; nao hardcodar token em node ou JSON.
3. Alterar somente a referencia da credencial nos nodes alvo.
4. Fazer readback de cada workflow e confirmar que a referencia mudou.
5. Restaurar/preservar o estado ativo anterior; ativacao e desativacao sao endpoints
   separados do `PUT` do workflow.
6. Rodar smoke test descartavel de renovacao OAuth.
7. Rodar um segundo smoke test na API de negocio realmente usada, por exemplo Sheets.
8. Remover workflow/dado temporario e auditar execucoes recentes por erro.

## Validacao final

- [ ] Refresh grant retorna HTTP 200 e access token sem imprimir segredo.
- [ ] Drive/Docs/Sheets respondem conforme o escopo esperado.
- [ ] GTM/GA4/Search Console respondem quando fizerem parte da credencial.
- [ ] `cloud-platform` esta ausente do token operacional.
- [ ] Todos os consumidores n8n apontam para a nova credencial.
- [ ] Estados ativos/inativos foram preservados.
- [ ] Smoke test de renovacao passou.
- [ ] Smoke test da API de negocio passou.
- [ ] Nenhum segredo entrou em log, diff, memoria ou relatorio.

## Falhas e tratamento

- Se o novo token ainda trouxer `cloud-platform`, verificar se a URL de autorizacao
  manteve `include_granted_scopes=true` ou se o escopo ainda esta na lista solicitada.
- Se o consentimento nao devolver refresh token, confirmar `access_type=offline` e
  usar `prompt=consent` somente nessa nova concessao.
- Se a conta for Interna, nao mudar para Externa para "corrigir expiracao" sem prova;
  isso amplia superficie e nao resolve `invalid_rapt`.
- Se infraestrutura GCP parar apos a separacao, configurar a credencial de
  infraestrutura apropriada em vez de recolocar `cloud-platform` no token operacional.

## Limites de longevidade

Mesmo fora do modo Testing, um refresh token ainda pode ser invalidado por revogacao
manual, troca de senha em cenarios aplicaveis, seis meses sem uso, excesso de tokens
emitidos ou politicas administrativas. A meta e eliminar expiracao recorrente causada
pela arquitetura, nao declarar eternidade.

## Referencias oficiais

- Google Cloud — Token types: https://cloud.google.com/docs/authentication/token-types
- Google Cloud — Reauthentication: https://cloud.google.com/docs/authentication/reauthentication
- Google Cloud — Session controls: https://cloud.google.com/access-context-manager/docs/session-controls-for-reauthentication
- Google OAuth 2.0 — Expiration: https://developers.google.com/identity/protocols/oauth2#expiration
