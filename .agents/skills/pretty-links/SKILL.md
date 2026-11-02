---
name: pretty-links
description: "Criar e operar links de rastreio Pretty Links no WordPress do usuario.club, com slug OPACO, UTM por canal e tracking (pixel Meta + GA4). Use SEMPRE que a tarefa for \"cria um pretty link\", \"encurta esse link\", \"link de rastreio\", \"slug do pretty links\", \"link pro disparo\", \"link pro tiktok do usuario\", \"link da FPV369\", \"qual slug usar\", ou quando alguem pedir um link curto do usuario.club pra colocar em anuncio, WhatsApp, SMS, bio ou QR code. Tambem aciona implicitamente quando uma campanha precisa de um link rastreavel e atribuivel. NAO crie o slug antes de propor e receber OK do usuario: slug e decisao de seguranca comercial, nunca pode vazar a estrategia.\n"
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

# pretty-links

Cria links de rastreio Pretty Links (usuario.club) com slug opaco, UTM por canal e os pixels certos, sem quebrar a atribuicao nem vazar estrategia. Plugin: Pretty Links Pro Executive v3.6.22 no WordPress de usuario.club. Credenciais WP/Pixel/GA4 no ${USER_SECRET_FILE} (ler por nome de variavel, nunca colar valor).

## Regra de ouro: o slug e OPACO (inegociavel)

O slug e a parte da URL que o lead VE (vai em SMS, WhatsApp, e-mail, bio, QR code, anuncio). Ele NUNCA pode revelar a estrategia comercial: oferta, tier, desconto, etapa de funil.

- **Title (admin, privado):** nome legivel interno, no formato `[{Canal}] {nome interno}`. Pode ter "Pre Oferta", "Bolsa Social", "Cancelamento". So o usuario e o HAOS veem.
- **Slug (URL publica):** opaco, neutro, sem leitura comercial. Esse e o que sai pro mundo.

### Processo obrigatorio (sempre, antes de criar)
1. Receber do usuario o nome interno (Title) e o destino.
2. **HAOS propoe o slug opaco** (1, no maximo 2 opcoes).
3. Esperar **OK do usuario**.
4. So entao criar.

Nao criar antecipando, nao improvisar slug "legivel".

### Termos que VAZAM (proibido no slug publico)
"Pre", "Pre-Oferta", "Pre-Venda"; "Oferta", "Desconto", "Promo"; "Vaga-Perdida", "Resgate", "Cancelamento", "Win-Back"; "Comercial", "SDR", "Fechamento"; "Bolsa-Social", "Bolsa-Parcial"; "Boleto", "24x", "12x", "Parcelado"; tier nominal ("Prata", "Ouro", "Diamante", "VIP", "Premium"); etapa de funil ("Topo", "Meio", "Fundo", "MOFU", "BOFU"); nome de campanha sensivel ou produto interno nao lancado.

### Padroes de slug opaco (bons)
- Data + numero: `live-080626-369`, `evento-150626-1`
- Codigo curto neutro: `r369`, `kit-azul`, `quiz-2`
- Versao A/B: nome-base + `-a` / `-b` / `-v2`
- Iniciais + sequencia: `nc-01`, `pd-03`

### Validacao antes de entregar a lista (pro usuario ou pro usuario)
Reler cada slug: deixa adivinhar a oferta? o tier? o desconto? repete o nome interno do funil? Se sim, reescrever. So libera quem passa no filtro. **Slugs antigos ficam como estao** (sem rename retroativo) e NAO se menciona slug antigo renomeado em doc, chat ou commit: referir por post_id ou Title interno.

## Tracking padrao (todos os links)

| Campo | Valor |
|---|---|
| `redirect_type` | `metarefresh` (NAO usar `pixel`, bugado no 3.6.22) |
| `track_me` | ON |
| `param_forwarding` | ON |
| `nofollow` | ON |
| `sponsored` | ON |

A pagina intermediaria (metarefresh) injeta, via Global Head Scripts do plugin, o **Pixel Meta `${USER_RESOURCE_000023}`** e o **GA4 `${USER_RESOURCE_000022}`**. Dispara no clique, antes do redirect, sem perder atribuicao.

**Quirk do 3.6.22:** a tela de edicao mostra dois `selected` no `<select name="redirect_type">` (`307` e `metarefresh`). O efetivo e `metarefresh` (validado por curl no front). Nao tentar "consertar" essa exibicao.

## Workflow tecnico (criacao/edicao, inclusive em massa)

### Superficies e diagnostico

- A API REST do WordPress funcionar **nao prova** que existe uma API REST para os registros reais do Pretty Links. Na versao 3.6.22, auditar as rotas em `/wp-json/` antes de concluir.
- Criar somente um post do CPT `pretty-link` nao basta: o destino e as opcoes do redirect vivem no modelo/tabelas internas do plugin.
- Os metodos legados XML-RPC `prli.*` podem estar registrados e, ainda assim, responder que XML-RPC nao esta habilitado. O controlador do plugin consulta uma opcao propria, `enable_xmlrpc`; essa falha nao significa que o XML-RPC padrao do WordPress esteja desligado.
- App Password do WordPress pode autenticar REST/XML-RPC, mas nao transforma o formulario autenticado do `wp-admin` em API.

### Ordem de execucao

1. Preferir o navegador ja autenticado no `wp-admin`, usando uma aba normal e ativa.
2. Se a automacao direta do navegador nao estiver disponivel, usar cookies + nonce e replicar o formulario completo por POST.
3. Usar os metodos XML-RPC `prli.*` somente se a opcao propria do plugin tiver sido habilitada com revisao de seguranca e OK explicito do usuario.

### Fluxo pelo navegador autenticado

1. Reabrir a lista do Pretty Links em uma aba normal do WordPress e obter uma referencia atual da aba.
2. Evitar paginas de extensao/suspensao de abas: uma UI `chrome-extension://` pode bloquear a automacao. Acordar ou navegar uma aba normal antes de continuar.
3. Preencher Title, destino completo com UTM, slug aprovado, `redirect_type=metarefresh`, categoria/tag e todos os checkboxes do tracking padrao.
4. Publicar primeiro um link piloto; validar o front antes de continuar o lote.
5. Em lote, respeitar intervalo minimo de 1,5 segundo entre operacoes.
6. Referencias de aba podem ficar obsoletas entre turnos. Reenumerar as abas e usar o identificador atual quando ocorrer erro de handle/stale tab.

### Fallback por cookies + nonce

1. Abrir usuario.club logado no Chrome.
2. Pela extensao "Get cookies.txt LOCALLY", exportar no formato Netscape.
3. Salvar apenas em arquivo temporario local, fora do repositorio.
4. Fazer POST em `wp-admin/post.php` replicando TODOS os campos do formulario do Pretty Links, incluindo nonces e hidden inputs.

### Cuidados aprendidos na marra
- **Checkbox ausente no POST = WP grava OFF.** Enviar sempre todos os checkboxes que devem ficar ON (track_me, param_forwarding, nofollow, sponsored).
- **Mod_Security** do host bloqueia UA generico tipo "Mozilla/5.0". Mandar UA completo de browser real.
- **Urlencode** caracteres especiais: `%` vira `%25`, `@@` vira `%40%40`. Sem isso o WAF derruba.
- Ler o `prli_url` da edit page sempre com **HTML-unescape** (`&amp;` vira `&`) antes de reusar como destino.
- **Rate limit operacional: 1,5s entre operacoes.** Mais rapido, o WAF derruba.
- Sessao wp-admin expira: se comecar a redirecionar (302) pra login, regenerar o cookies.txt.
- O aviso do WordPress "Conexao perdida" ou um formulario recarregado nao prova falha. Se o front publico e a leitura administrativa confirmarem o registro, considerar a criacao bem-sucedida.

### QA autoritativo do redirect

- Para `metarefresh`, o comportamento esperado e **HTTP 200 com meta refresh no HTML**, nao um header `Location` 30x.
- Extrair o destino do meta refresh e aplicar HTML-unescape antes de comparar (`&amp;` deve virar `&`).
- Confirmar o destino/ASIN esperado e todas as UTMs hardcoded.
- Testar `param_forwarding` acrescentando um parametro descartavel na URL curta e conferindo se ele aparece no destino renderizado.
- Em lote, registrar os `post_id` por leitura administrativa autenticada (por exemplo, `wp.getPosts`) e cruzar com Title e slug.
- A validacao publica do redirect tem precedencia sobre avisos transitórios da interface, mas nao substitui a verificacao de Title/slug/post_id no admin.

## Saida esperada

- Antes de criar: a proposta de slug opaco (1 a 2 opcoes) + Title interno + destino com UTM do canal, aguardando OK.
- Depois de criar: confirmacao com Title, slug publico, destino, canal (categoria+tag), redirect_type efetivo (metarefresh) e a URL final `usuario.club/{slug}`. Validar no front o HTTP 200 e o destino extraido do meta refresh; nao exigir `Location` em redirects `metarefresh`. Nunca declarar "criado" sem conferir o redirect real.
- Em lote: tabela com Title, slug, destino e post_id. Slug sempre passou no filtro anti-vazamento. Zero em-dash no texto.

## Referencias operacionais

- [Playbook de diagnostico da API, criacao pelo navegador e QA](references/pretty-links-api-browser-playbook.md)

