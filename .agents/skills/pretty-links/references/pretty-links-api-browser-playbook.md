---
title: Pretty Links - API, navegador autenticado e QA
date: 2026-08-24
status: active
---

# Pretty Links: API, navegador autenticado e QA

## Objetivo

Executar criacao e diagnostico de Pretty Links com evidencia verificavel, sem confundir a API do WordPress com a camada de persistencia do plugin e sem expor credenciais.

## Pre-flight obrigatorio

1. Confirmar Title interno, destino e UTM.
2. Propor slug opaco e obter OK explicito do usuario antes da criacao.
3. Confirmar que o usuario esta logado no WordPress em uma aba normal do navegador.
4. Fechar ou acordar abas suspensas por extensao; nao automatizar a partir de `chrome-extension://`.
5. Consultar cada URL curta antes da criacao. Um slug novo deve estar livre; em caso de colisao, parar e propor outro.

## Arvore de diagnostico da API

1. Consultar `/wp-json/` e verificar se a REST API geral do WordPress responde.
2. Enumerar as rotas e procurar namespace/endpoints do Pretty Links. Ausencia de rota significa que REST geral ativa nao oferece CRUD dos links do plugin.
3. Consultar `system.listMethods` no XML-RPC padrao e separar os metodos WordPress dos metodos `prli.*`.
4. Se `prli.api_version` responder que XML-RPC nao esta habilitado, verificar o controlador do plugin. Na versao 3.6.22, ele consulta `get_option('enable_xmlrpc')`, uma opcao propria do Pretty Links.
5. Nao concluir que o XML-RPC do WordPress esta desligado se `wp.getPosts` ou outros metodos padrao funcionam.
6. Nao criar apenas o CPT `pretty-link`: a URL de destino e as opcoes vivem nas tabelas/modelos internos do plugin.
7. Classificar o resultado:
   - REST WordPress ativa, sem REST Pretty Links: usar navegador/formulario.
   - XML-RPC WordPress ativo, `prli.*` bloqueado: gate interno do plugin.
   - Sessao wp-admin ativa: fluxo preferencial pelo navegador.
   - Sessao expirada: renovar login/cookies antes de executar.

## Criacao pelo navegador autenticado

1. Enumerar as abas atuais e selecionar uma aba normal do `wp-admin`.
2. Abrir `Pretty Links > Add New`.
3. Preencher:
   - Title interno aprovado;
   - Target URL completa com UTM;
   - Pretty Link/slug aprovado;
   - redirect type `metarefresh`;
   - categoria e tag do canal;
   - `track_me`, `param_forwarding`, `nofollow` e `sponsored` ligados.
4. Publicar um piloto e validar o front.
5. Somente depois continuar o lote, com pelo menos 1,5 segundo entre operacoes.
6. Se a referencia da aba ficar obsoleta, reenumerar as abas; nao insistir em handle antigo.

## Fallback por formulario HTTP

1. Exportar cookies da sessao autenticada para arquivo temporario fora do repositorio.
2. Ler o formulario atual e capturar nonces, hidden inputs e valores efetivos.
3. Reenviar o formulario completo com User-Agent realista e encoding correto.
4. Enviar explicitamente todos os checkboxes que precisam permanecer ligados.
5. Aplicar HTML-unescape ao destino lido antes de reutiliza-lo.
6. Se houver 302 para login, renovar a sessao. Se houver bloqueio do WAF, revisar User-Agent, encoding e ritmo.

## Falhas comuns

| Sintoma | Diagnostico | Acao |
|---|---|---|
| UI de extensao aberta | automacao bloqueada por pagina `chrome-extension://` | acordar/navegar uma aba normal |
| handle de aba invalido | referencia ficou obsoleta | reenumerar abas e usar a referencia atual |
| "Conexao perdida" apos publicar | aviso do editor pode ser transitorio | validar URL publica e readback administrativo |
| formulario vazio apos publicar | navegacao/reload nao prova rollback | verificar redirect e post_id antes de repetir |
| 302 para login | sessao expirada | renovar login/cookies |
| slug existente | colisao real | parar e obter novo slug aprovado |
| 403/WAF | request, encoding ou ritmo rejeitado | revisar UA, urlencode e intervalo de 1,5s |

## QA autoritativo

Para cada link:

1. Fazer GET na URL curta.
2. Para `metarefresh`, esperar HTTP 200 e localizar o destino no elemento meta refresh do HTML.
3. Fazer HTML-unescape do destino antes da comparacao.
4. Confirmar dominio/destino, identificador do produto e todas as UTMs esperadas.
5. Acrescentar `?qa_forward=1` a URL curta e confirmar que o parametro foi encaminhado ao destino.
6. Fazer readback administrativo e registrar Title, slug e post_id.
7. So declarar sucesso se o redirect publico e o registro administrativo forem coerentes.

## Opcoes futuras de automacao

- Um endpoint REST customizado pode autenticar a requisicao e chamar a funcao interna `prli_create_pretty_link`, preservando o modelo oficial do plugin.
- Os metodos legados `prli.*` podem ser avaliados se o gate proprio do plugin for habilitado deliberadamente.
- Qualquer alteracao de configuracao, endpoint ou seguranca em producao exige revisao e OK explicito do usuario.

Nunca registrar cookies, nonces, senhas, tokens ou valores do cofre em logs, memoria, documentacao ou Git.
