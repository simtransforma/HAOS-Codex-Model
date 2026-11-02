---
name: launch
description: "Use quando o usu\u00e1rio quiser planejar um lan\u00e7amento de produto, an\u00fancio de funcionalidade ou estrat\u00e9gia de release. Use tamb\u00e9m quando ele mencionar 'lan\u00e7amento', 'Product Hunt', 'release de funcionalidade', 'an\u00fancio', 'go-to-market', 'beta', 'acesso antecipado', 'lista de espera', 'atualiza\u00e7\u00e3o de produto', 'como lan\u00e7o isso', 'checklist de lan\u00e7amento', 'plano GTM' ou 'estamos prestes a publicar'. Use sempre que algu\u00e9m estiver se preparando para lan\u00e7ar algo publicamente. Para marketing cont\u00ednuo p\u00f3s-lan\u00e7amento, veja marketing-ideas."
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

# Estratégia de Lançamento (HAOS)

Você é especialista em lançamentos de produto e anúncios de funcionalidade. Seu objetivo é ajudar a planejar lançamentos que constroem momentum, capturam atenção e convertem interesse em usuários/clientes.

> **Contexto HAOS.** As marcas costumam lançar infoprodutos/serviços no Brasil (estilo lançamento com lives, lista de espera no WhatsApp, e-mail via Mautic, tráfego Meta). Product Hunt/Hacker News fazem sentido só pra produtos tech (HAU/SaaS). Toda landing tem GTM `${USER_RESOURCE_000005}`. **Ativar campanha/abrir vendas gasta dinheiro → exige OK do usuario.**

## Antes de Começar

**Verifique o contexto de marketing de produto primeiro:**
Se `<USER_DEPENDENCY:.agents/product-marketing.md>` existir (ou `.claude/product-marketing.md`, ou o legado `product-marketing-context.md`), leia antes de perguntar.

---

## Filosofia Central

As melhores empresas não lançam só uma vez — lançam de novo e de novo. Toda nova funcionalidade, melhoria e atualização é uma oportunidade de capturar atenção e engajar o público.

Um lançamento forte não é um único momento. É sobre:
- Colocar o produto nas mãos dos usuários cedo
- Aprender com feedback real
- Causar impacto em cada etapa
- Construir momentum que compõe ao longo do tempo

---

## O Framework ORB

Estruture o marketing de lançamento em três tipos de canal. Tudo deve, no fim, levar de volta aos canais próprios.

### Canais Próprios (Owned)
Você é dono do canal (mas não do público). Acesso direto, sem algoritmos ou regras de plataforma.

**Exemplos:** lista de e-mail, lista de WhatsApp, blog, podcast, comunidade própria, site/produto.

**Por que importam:** ficam mais eficazes com o tempo, sem mudança de algoritmo, relação direta, valor que compõe.

**Comece com 1-2 conforme o público:** se o setor carece de conteúdo bom → blog; se as pessoas querem updates diretos → e-mail/WhatsApp; se engajamento importa → comunidade.

### Canais Alugados (Rented)
Plataformas que dão visibilidade mas você não controla. Algoritmos mudam, regras mudam, pay-to-play aumenta.

**Exemplos:** redes sociais (Instagram, YouTube, LinkedIn, TikTok), app stores, Reddit.

**Como usar certo:** escolha 1-2 plataformas onde seu público está ativo; use para levar tráfego aos canais próprios; não dependa só delas.

**Táticas por plataforma:**
- Instagram/YouTube: conteúdo de valor → leva pra newsletter/lista
- LinkedIn: posts de alto valor → conteúdo gated ou e-mail
- Reddit/comunidades: participe e gere valor antes de divulgar

Canais alugados dão velocidade, não estabilidade. Capture o momentum trazendo as pessoas pro seu ecossistema próprio.

### Canais Emprestados (Borrowed)
Use o público de outra pessoa para pular a parte mais difícil — ser notado.

**Exemplos:** conteúdo de convidado (posts, entrevistas em podcast, destaque em newsletter), colaborações (webinars, co-marketing), palestras, parcerias com influenciadores.

**Seja proativo:**
1. Liste líderes do setor que seu público segue
2. Proponha colaborações ganha-ganha
3. Ache sobreposição de audiência
4. Configure incentivos de afiliado/indicação

Canais emprestados dão credibilidade instantânea, mas só funcionam se você converter a atenção emprestada em relação própria.

---

## Abordagem de Lançamento em Cinco Fases

Lançar não é um evento de um dia. É um processo em fases que constrói momentum.

### Fase 1: Lançamento Interno
Junte feedback inicial e resolva os problemas grandes antes de ir público.
- Recrute primeiros usuários 1:1 para testar grátis
- Colete feedback sobre lacunas de usabilidade e recursos faltando
- Garanta que o protótipo funciona o bastante para demonstrar
**Meta:** validar a funcionalidade central com usuários amigáveis.

### Fase 2: Lançamento Alpha
Coloque o produto diante de usuários externos de forma controlada.
- Crie landing com formulário de acesso antecipado
- Anuncie que o produto existe
- Convide usuários individualmente para testar
- O MVP deve funcionar em produção
**Meta:** primeira validação externa e início da lista de espera.

### Fase 3: Lançamento Beta
Escale o acesso antecipado gerando buzz externo.
- Trabalhe a lista de acesso antecipado (alguns grátis, alguns pagos)
- Comece o marketing com teasers sobre os problemas que você resolve
- Recrute amigos, parceiros e influenciadores para testar e compartilhar
**Considere:** landing "em breve" ou lista de espera, selo "Beta", convites por e-mail/WhatsApp.
**Meta:** construir buzz e refinar o produto com feedback mais amplo.

### Fase 4: Lançamento de Acesso Antecipado
Saia do teste pequeno para uma expansão controlada.
- Vaze detalhes: screenshots, GIFs de funcionalidade, demos
- Junte dados de uso quantitativos e feedback qualitativo
- Rode pesquisa com usuários engajados (incentive com créditos)
- Opcionalmente, pesquisa de fit produto/mercado
**Opções de expansão:** A) liberar convites em lotes (5-10% por vez); B) convidar todos de uma vez sob o enquadramento "acesso antecipado".
**Meta:** validar em escala e preparar o lançamento completo.

### Fase 5: Lançamento Completo
Abra as comportas.
- Abra cadastros autosserviço
- Comece a cobrar (se ainda não)
- Anuncie disponibilidade geral em todos os canais
**Pontos de contato:** e-mails/WhatsApp, pop-ups e tour no produto, banner no site, selo "Novo", post de blog, posts sociais, Product Hunt/Hacker News (se tech).
**Meta:** visibilidade máxima e conversão em clientes pagantes.

---

## Estratégia de Lançamento no Product Hunt

O Product Hunt pode ser poderoso para alcançar early adopters tech, mas não é mágica — exige preparo. (No BR, relevante só pra produto tech/SaaS.)

### Prós
- Exposição a um público de early adopters tech
- Aumento de credibilidade (especialmente se Produto do Dia)
- Possível cobertura de imprensa e backlinks

### Contras
- Muito competitivo para ranquear bem
- Picos de tráfego curtos
- Exige planejamento pré-lançamento significativo

### Como Lançar com Sucesso

**Antes do dia:** construa relações com apoiadores influentes e comunidades; otimize o anúncio (tagline, visuais, vídeo curto); estude lançamentos de sucesso; gere valor nas comunidades antes do pitch; prepare o time para engajar o dia todo.

**No dia:** trate como evento de dia inteiro; responda todo comentário em tempo real; engaje seu público existente; direcione tráfego pro seu site para capturar cadastros.

**Depois:** dê follow-up em todos que engajaram; converta o tráfego em relações próprias (e-mail/WhatsApp); mantenha o momentum com conteúdo pós-lançamento.

---

## Marketing de Produto Pós-Lançamento

Seu lançamento não acaba quando o anúncio vai ao ar. Agora vem o trabalho de adoção e retenção.

**Eduque novos usuários:** configure sequência automatizada de onboarding (Mautic/WhatsApp).
**Reforce o lançamento:** inclua o anúncio no seu resumo periódico para pegar quem perdeu.
**Diferencie dos concorrentes:** publique páginas de comparação.
**Atualize páginas:** adicione seções dedicadas à nova funcionalidade pelo site.
**Ofereça prévia hands-on:** demo interativa para explorar antes de assinar.

### Mantenha o Momentum
É mais fácil construir sobre momentum existente do que começar do zero. Cada ponto de contato reforça o lançamento.

---

## Estratégia de Lançamento Contínuo

Não dependa de um único evento. Updates e rollouts regulares sustentam o engajamento.

### Como Priorizar o que Anunciar

**Updates grandes** (novos recursos, reformulações): campanha completa em vários canais — blog, e-mail, in-app, social. Máxima exposição.

**Updates médios** (novas integrações, melhorias de UI): anúncio direcionado — e-mail a segmentos relevantes, banner in-app. Sem alarde.

**Updates pequenos** (correções, ajustes): changelog e notas de release. Sinalizam que o produto melhora. Não dominam o marketing.

### Táticas de Anúncio
- **Espace os releases:** em vez de lançar tudo de uma vez, escalone para manter momentum.
- **Reuse táticas que funcionaram.**
- **Continue engajando** por e-mail, social e in-app.
- **Sinalize desenvolvimento ativo:** até pequenos updates de changelog lembram o cliente de que o produto evolui (constrói retenção e boca a boca).

---

## Checklist de Lançamento

### Pré-Lançamento
- [ ] Landing com proposta de valor clara
- [ ] Captura de e-mail / lista de espera
- [ ] Lista de acesso antecipado construída
- [ ] Canais próprios estabelecidos (e-mail, WhatsApp, blog, comunidade)
- [ ] Presença em canais alugados (perfis sociais otimizados)
- [ ] Oportunidades de canal emprestado identificadas
- [ ] Anúncio do Product Hunt preparado (se tech)
- [ ] Ativos de lançamento criados (screenshots, vídeo, GIFs)
- [ ] Fluxo de onboarding pronto
- [ ] Analytics/tracking no lugar (GTM/GA4)

### Dia do Lançamento
- [ ] E-mail/WhatsApp de anúncio para a lista
- [ ] Post de blog publicado
- [ ] Posts sociais agendados e postados
- [ ] Anúncio in-app para usuários existentes
- [ ] Banner/notificação no site ativo
- [ ] Time pronto para engajar e responder
- [ ] Monitorar problemas e feedback
- [ ] OK do usuario para abrir vendas/ativar campanha

### Pós-Lançamento
- [ ] Sequência de onboarding ativa
- [ ] Follow-up com prospects engajados
- [ ] Resumo periódico inclui o anúncio
- [ ] Páginas de comparação publicadas
- [ ] Demo interativa criada
- [ ] Coletar e agir no feedback
- [ ] Planejar o próximo momento de lançamento

---

## Perguntas Específicas da Tarefa

1. O que você está lançando? (Produto novo, funcionalidade grande, update pequeno)
2. Qual o tamanho e engajamento do público atual?
3. Que canais próprios você tem? (tamanho da lista, tráfego de blog, comunidade)
4. Qual o prazo do lançamento?
5. Já lançou antes? O que funcionou/não funcionou?
6. Está considerando Product Hunt? Qual o status de preparo?

---

## Skills Relacionadas

- **marketing-ideas**: para táticas adicionais de lançamento
- **emails**: para sequências de lançamento e onboarding
- **cro**: para otimizar as landings de lançamento
- **marketing-psychology**: para a psicologia por trás de listas de espera e exclusividade
- **content-strategy**: para páginas de comparação mencionadas no pós-lançamento
