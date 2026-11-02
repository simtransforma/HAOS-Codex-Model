---
name: lovable-session-ops
description: "Operar projetos Lovable usando a sess\u00e3o j\u00e1 autenticada do navegador, com edi\u00e7\u00e3o manual quando os cr\u00e9ditos de IA acabarem, valida\u00e7\u00e3o de build/preview e publica\u00e7\u00e3o somente ap\u00f3s autoriza\u00e7\u00e3o expl\u00edcita. Use para editar, criar rotas, remover componentes, corrigir responsividade, manter tracking e publicar projetos Lovable."
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

# Operação Lovable com sessão persistente

## Objetivo

Executar alterações no projeto Lovable autenticado do usuário sem pedir login, OAuth ou créditos novamente sem verificar o estado atual.

## Ordem obrigatória

1. Classificar o projeto antes de operar: projetos do workspace SIM usam o conector MCP Lovable existente; projetos HAU e de clientes usam o navegador local já autenticado no perfil correto. Não tentar conectar contas HAU ao MCP do SIM.
2. Reutilizar o navegador já aberto e a aba do projeto. Listar abas; se houver uma aba Lovable autenticada, reivindicá-la. Não abrir outro perfil nem pedir login.
3. Ler o estado atual do projeto: rota, preview, arquivos e botão Publish. Não confiar em mensagens antigas do chat como prova de estado.
4. Consultar se há créditos antes de enviar mensagens ao agente. Se `0 credits remaining`, não clicar em Upgrade, Buy once ou Auto top-up.
5. Se houver créditos, usar o agente somente para alterações bem especificadas. Se não houver, usar a aba Files > Code e editar manualmente.
6. Nunca alterar a V1 para criar a V2. Criar uma rota/arquivo separado e preservar URLs, UTMs, IDs de tracking, preços e componentes de checkout.
   Antes de enviar qualquer imagem ao projeto, aplicar o fluxo obrigatório de compressão e desempenho abaixo. Vale para todas as páginas novas e revisões.
7. Rodar build/typecheck local quando houver cópia local do projeto. No Lovable, aguardar o preview atualizar e verificar a rota alterada.
8. Publicar somente com OK explícito do usuário para esta alteração. Antes de publicar, verificar que não há alterações não relacionadas, que a V1 continua intacta e que a opção nativa **Hide Lovable badge** está ativada.
9. Após publicar, abrir a URL pública com cache-buster, testar desktop e 320/375/430px, validar CTA, checkout, WhatsApp, tracking, ausência do selo Lovable e ausência de vídeo quando solicitado.

## Ocultar o selo Lovable — padrão obrigatório

Regra explícita de usuario em 2026-09-25: todo projeto deve usar **Hide Lovable badge = ON** antes da publicação, salvo instrução explícita contrária para aquele projeto.

- Conferir projeto e workspace e ler o estado atual da configuração nativa. Ativar se estiver desligada; preservar se já estiver ligada. Não clicar no toggle sem verificar seu estado.
- Usar a configuração nativa. Não substituir por CSS, remoção de DOM ou outro artifício de ocultação.
- Incluir a conferência no gate de publicação e na revisão de projetos existentes. Um screenshot do usuário prova o estado capturado, não o estado atual nem uma alteração feita pelo agente.
- Após publicar, conferir a ausência do selo na URL canônica pública, em desktop e mobile e nas rotas entregues. Registrar separadamente a configuração observada e a verificação pública.
- Se faltar acesso à configuração ou houver limitação de plano, registrar a pendência sem declarar sucesso. Não comprar créditos nem alterar plano sem autorização específica.

## Roteamento de contas

- `SIM`: manter e reutilizar o conector MCP Lovable já autenticado no workspace SIM.
- `HAU/clientes`: operar pelo navegador local autenticado na conta proprietária do projeto.
- Não interpretar `403`, projeto ausente ou workspace inesperado no MCP como inexistência do projeto; primeiro tratar como possível identidade OAuth errada.
- Não criar aliases MCP adicionais por tentativa e erro. O OAuth do Lovable pode rejeitar registro dinâmico de cliente (`invalid_client_metadata`); nesse cenário, aplicar o fluxo de navegador local.
- Nunca misturar edição, histórico ou publicação entre contas. Confirme nome do projeto e workspace antes de qualquer alteração.

## Edição manual sem créditos

- Use Files para localizar `src/App.tsx`, a página alvo e os componentes envolvidos.
- Para criar uma rota, adicione o import e a `<Route>` em `src/App.tsx` e crie o arquivo da página na pasta `src/pages`.
- Cole o conteúdo completo no editor, salve, aguarde o status de build e só então abra Preview.
- Não use o chat para pedir a mesma alteração quando o saldo for zero; isso apenas abre o modal de compra e não altera o código.
- Se a árvore de arquivos travar, preserve o projeto, registre o bloqueio e use a cópia local para preparar o patch; não substitua outra rota como atalho.

## Tracking e checkout

- Preservar `data-checkout-link="true"`, eventos Meta/GA4/GTM/Clarity, UTMs recebidas e links Zenie existentes.
- Nunca trocar o domínio de checkout, preços ou IDs sem instrução específica.
- Validar que a barra fixa não cobre CTA principal e que o botão de atendimento mantém o WhatsApp oficial do projeto.

## Imagens comprimidas e desempenho — padrão obrigatório

Regra solicitada por usuario em 2026-09-24: preparar e comprimir imagens **antes do upload** em todas as páginas. Corrigir um projeto existente pelo agente Lovable é permitido; não adiar a preparação dos próximos projetos para depois da construção.

1. Inventariar os originais e o uso: dimensões, bytes, transparência, largura renderizada e posição na página. Preservar os originais; criar derivados identificáveis e registrar origem, formato, dimensões e tamanho antes/depois. Compressão técnica não autoriza redesenhar, gerar, cortar ou omitir itens do produto.
2. Redimensionar para os tamanhos efetivamente usados em mobile e desktop, considerando DPR sem ampliar a fonte. Comprimir fotos e artes raster em WebP ou AVIF quando compatível; preservar alpha e usar formato sem perdas quando necessário para texto fino, logotipo ou qualidade. SVG já otimizado não exige conversão raster. Não escolher uma versão maior que o original sem motivo comprovado.
3. Comparar visualmente os derivados antes do upload: produto inteiro, códigos, cheque, caneta, rostos, cores e transparência legíveis. Ajustar qualidade/resolução por imagem; não impor percentual fixo que destrua detalhes. Imagem já otimizada pode ser mantida se a comparação documentar que nova compressão piora a qualidade ou aumenta o peso.
4. Enviar os derivados aprovados, não os arquivos brutos. Usar `srcset`/`sizes` ou `picture` com tamanhos e formatos adequados; fundos CSS também precisam de versão por viewport. Confirmar `currentSrc` e bytes realmente transferidos no navegador, evitando baixar desktop e mobile juntos.
5. Declarar dimensões ou proporção para reservar espaço. Aplicar carregamento tardio somente abaixo da dobra; imagem LCP ou conteúdo visual prioritário deve carregar imediatamente. Usar prioridade/preload apenas para recursos críticos comprovados; quando o briefing exigir vídeo primeiro, evitar disputa com esse player.
6. Medir antes/depois nas mesmas rotas, viewport, rede, CPU e estado de cache: bytes de imagens e recursos próprios, requisições e LCP/CLS; adicionar diagnóstico de JavaScript/fontes/terceiros conforme o gargalo observado. Registrar ferramenta e limitações; não apresentar redução de bytes como percentual de ganho de velocidade nem medição de laboratório como Core Web Vitals de usuários reais.
7. Preservar conteúdo, UTMs, consentimento, formulários, checkout, pixels e player. Não remover integrações, adiar sua função ou trocar vídeo só para melhorar uma nota. Se terceiros limitarem o resultado, separar esse custo das melhorias nos recursos próprios.
8. Antes de publicar, verificar build, qualidade visual desktop/mobile, ausência de overflow e regressões. Depois da publicação autorizada, conferir domínio canônico, derivados servidos, MIME/tamanho/cache e layout. Encerrar com evidência do resultado real, sem prometer nota ou velocidade não medida.

## Lições operacionais consolidadas

- Após publicar, conferir a URL canônica antes de promover integrações servidor a servidor. O endereço `lovable.app` pode redirecionar para domínio já vinculado. Em chamadas autenticadas configuradas sem redirects, testar o verificador diretamente na URL canônica e alterar somente esse campo, seguido de readback e teste público do formulário. Ver seção 10 do playbook de release.
- Em QA de vídeo, registrar licença, manifesto, segmentos e erro do decodificador separadamente. Um erro de codec no navegador automatizado não prova defeito de domínio ou licença; respostas HTTP corretas também não comprovam reprodução. Não trocar IDs ou mídia por inferência.

- Para aceitar uma CTA fixa de atendimento no mobile, não basta encontrar o link no DOM: confirme `aria-hidden=false`, retângulo inteiro dentro da viewport e clique que resulte no domínio de WhatsApp esperado. Repita em 320, 375, 390 e 430 px e em uma dobra com checkout visível.
- `safe-area-inset-bottom` pode empurrar a CTA para fora da viewport. Prefira espaçamento que preserve o retângulo clicável ou calcule a altura do dock; o critério é a área clicável ficar totalmente visível sem cobrir o botão de checkout.
- Com saldo zero, o caminho confiável é Files > Code: localizar o arquivo real, usar o editor de código, substituir o conteúdo completo, salvar, aguardar o build e publicar somente no gate autorizado. Chat, cards antigos e API podem não refletir o estado live.
- Após publicar, validar a URL pública com cache-buster e o bundle live. Status de preview ou mensagem histórica não é evidência de publicação.
- No navegador local, o fluxo comprovado é: abrir o projeto correto, usar `Ctrl+K` > `Code`, editar o arquivo real, salvar com `Ctrl+S`, confirmar novo item de histórico de edição, abrir Preview, publicar no gate autorizado e validar a URL pública.
- O fluxo manual pelo editor de código pode continuar disponível quando o projeto está sem créditos de IA. Créditos e permissão de edição/publicação são estados diferentes e devem ser verificados separadamente.

## Gate de equivalência visual e release

- Apresentação, wireframe, pacote local, screenshot de candidato e mensagem do agente não comprovam que o conceito foi implementado. Para cada conceito, nomeie separadamente `SOLICITADO`, `LOCAL`, `PREVIEW` e `LIVE` e registre a evidência de cada estado.
- Aceite visual e autorização de publicação são gates independentes. Um candidato pode estar visualmente aprovado e continuar bloqueado para deploy; um OK para publicar não corrige candidato divergente.
- Antes da edição, crie uma allowlist explícita de arquivos, literais, assets e comportamentos que podem mudar. O diff fora da allowlist bloqueia o release até remoção ou decisão do usuario.
- Identifique cada candidato por uma tupla imutável: `concept_id + reference_sha256 + candidate_sha + screenshot_set`. O release manifest e o readback live devem apontar para a mesma tupla/SHA.
- Antes de publicar um redesign, monte um contrato de preservação para copy, rotas, API, UTMs, tracking e integrações. Revise o diff final contra esse contrato e remova qualquer inserção não solicitada antes do deploy.
- QA responsivo deve testar largura e altura, não somente breakpoints. Em páginas de conversão, meça também os marcos semânticos da primeira dobra: primeiro campo/CTA e elementos visuais essenciais inteiros dentro da viewport.
- `object-fit: cover` e ausência de overflow não provam composição correta. Quando um personagem, produto, telefone, player ou selo for essencial, registre seu retângulo e margens nas viewports críticas; use art direction, `object-position`, `contain` ou camada separada conforme necessário.
- Todo hotfix visual reabre a matriz mínima desktop/mobile e exige readback da URL pública com cache-buster. Um conserto restrito por breakpoint precisa provar que as classes fora desse breakpoint permaneceram inalteradas.
- Em QA de formulário conectado, prefira validação estrutural, interceptação ou simulação local sem envio real. Não gere lead, e-mail, card ou POST externo apenas para comprovar layout.
- QA live de layout é `GET/HEAD-only` por padrão. Interceptor/proxy não sobrevive por presunção: depois de todo reload, navegação ou nova página, reafirme e teste que a guarda está armada antes de qualquer interação potencialmente mutável.
- Perfis Chromium de QA são efêmeros, ficam fora do repositório e usam diretório temporário dedicado. Não abra, versione, reutilize como evidência nem remova um perfil residual sem confirmar o alvo e o gate de limpeza.
- Deck, PDF ou apresentação podem documentar o trabalho, mas nunca fecham o caminho crítico de implementação, QA e publicação.

Procedimento completo: [Playbook de redesign visual e release](references/lovable-visual-redesign-release-playbook.md).

## Segurança e comunicação

- Não revelar tokens, cookies, senhas ou conteúdo de sessão.
- Não comprar créditos, fazer upgrade, enviar mensagens, publicar ou alterar produção sem autorização explícita.
- Se o usuário já autorizou a publicação da alteração atual, não pedir autorização novamente; apenas confirmar o escopo antes do clique final.
- Ao reportar bloqueio, dizer exatamente: saldo de créditos, ação que continua disponível manualmente e o que falta para concluir.

## Critérios de aceite

- Rota solicitada abre no preview e na URL pública.
- Build/typecheck sem erro.
- V1 permanece funcional e sem regressão.
- Mobile sem overflow horizontal.
- Imagens otimizadas antes do upload, com comparação de peso/qualidade; variantes corretas confirmadas na rede e desempenho verificado no escopo afetado.
- Checkout/UTM/tracking preservados.
- Hide Lovable badge ativado na configuração nativa e ausência do selo confirmada no domínio público em desktop/mobile.
- Publicação confirmada por botão/URL pública, nunca por inferência de uma mensagem antiga.

## Referências

- [Playbook de roteamento SIM e HAU](references/lovable-multi-account-routing-playbook.md)
- [Playbook de redesign visual e release](references/lovable-visual-redesign-release-playbook.md)
