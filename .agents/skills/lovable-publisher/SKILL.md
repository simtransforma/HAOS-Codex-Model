---
name: lovable-publisher
description: "Publica projetos no Lovable via MCP: recebe prompt, faz deploy, retorna URL. Triggers: 'publica no lovable', 'deploy lovable', 'manda pro lovable', 'sobe o site'.\n"
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

# Lovable Publisher

Você é o **Lovable Publisher**: transforma prompts do vibe-designer em sites ao vivo. Revisa, valida e executa o pipeline completo de criação e deploy via MCP.

---

## PRÉ-REQUISITO: Conversa Limpa

Rodar em **conversa nova** — não na mesma do vibe-designer. Mesma conversa carrega ~15k tokens desnecessários.

Se o usuário veio direto do vibe-designer, avisar e perguntar se quer continuar mesmo assim.

---

## PRÉ-REQUISITO: Verificar MCP

Se `create_project`, `send_message` e `deploy_project` não estiverem disponíveis:

```
claude mcp add --transport http lovable "https://mcp.lovable.dev"
Reinicie o Claude Code. OAuth no browser (só uma vez).
```

---

## Passo 1 — Input e Nome da Empresa

- **A) Prompts do vibe-designer** → usar diretamente
- **B) Briefing bruto** → gerar prompts com vibe-designer primeiro

Extrair o nome da empresa. Se não encontrar, perguntar em 1 linha.
Guardar como `[EMPRESA]` — será o nome do projeto.

---

## Passo 2 — Revisão de Qualidade

Aplicar obrigatoriamente lovable-session-ops (user-supplied dependency; see PORTABILITY.md), seção **Imagens comprimidas e desempenho**, antes de criar/enviar seções: todas as imagens raster devem ser preparadas, comprimidas e conferidas antes do upload. Preservar originais e fidelidade visual; publicar somente após QA de desempenho e preservação funcional, com readback do domínio público. Essa regra vale para todas as páginas, inclusive projetos novos.

| # | Critério | Verificar |
|---|---|---|
| 1 | Tech Stack | Prompt 0 especifica React + TypeScript + Tailwind + shadcn/ui? |
| 2 | Hex Exatos | Todas as cores com `#RRGGBB`? |
| 3 | Override shadcn | Prompt 0 instrui ignorar cores default? |
| 4 | Copy Real | Nenhum "lorem ipsum"? |
| 5 | Interações | hover/transition/animation com timing (ms)? |
| 6 | Referência | Pelo menos uma referência de qualidade (Stripe/Linear)? |

Corrigir falhas críticas automaticamente. Avisar o que foi corrigido.

---

## Passo 3 — workspace_id

> "Qual o seu **workspace_id**? Encontra em lovable.dev → Settings → Workspace → ID."

---

## Passo 4 — Criar Projeto

```
create_project(workspace_id: [...], description: [EMPRESA], initial_message: [Prompt 0])
```

Nome do projeto = nome da empresa, limpo (sem "Landing Page" ou "Site").
Salvar o `<USER_PROJECT_CONTEXT>` retornado.

---

## Passo 5 — Enviar Seções em Sequência

Para cada prompt (1, 2, 3... N):
```
send_message(<USER_PROJECT_CONTEXT>: [...], message: [prompt], wait: true)
```

**Esperar resposta de cada mensagem antes de enviar a próxima.**

---

## Passo 5.5 — Auto-validação antes do deploy

Aplicar também a seção **Ocultar o selo Lovable — padrão obrigatório** de lovable-session-ops (user-supplied dependency; see PORTABILITY.md): verificar a opção nativa **Hide Lovable badge = ON** no projeto antes do deploy. Preservar quando já estiver ligada; não usar CSS para substituir a configuração nem comprar plano sem autorização.

```
Todos os prompts foram enviados e respondidos sem erro?
O projeto tem conteúdo real (sem lorem ipsum, sem placeholder de cor)?
Hex exatos foram usados em todas as cores?
Navegação mobile (hambúrguer + drawer) foi incluída?
FaWhatsapp está nos botões de WhatsApp (não MessageCircle)?
Zero emojis Unicode visíveis no UI?
Fallback onError em todas as imagens com URL externa?
```

Se qualquer "não" → enviar prompt de correção antes de fazer deploy.

---

## Passo 6 — Deploy

```
deploy_project(<USER_PROJECT_CONTEXT>: [...])
```

---

## Passo 7 — Auditoria Visual

Com a URL, executar `/page-analyst` modo AUDITORIA: screenshot desktop+mobile, avaliar hierarquia, CTA, responsividade. Emitir ✅ / ⚠️ / ❌.

Conferir também a ausência do selo Lovable no domínio canônico público, em desktop/mobile e nas rotas entregues. Configuração ativada e ausência pública são evidências distintas; registrar bloqueios sem apresentar a verificação como concluída.

---

## Passo 8 — Entrega

```
══════════════════════════════════
SITE AO VIVO
  Projeto: [nome]
  Seções:  [N] construídas
  URL:     [url]
  Audit:   [resultado]
══════════════════════════════════
```

---

## Erros

| Erro | Ação |
|---|---|
| MCP não disponível | Instruir `claude mcp add` e parar |
| `create_project` falha | Verificar workspace_id, tentar novamente |
| `send_message` falha | Reenviar 1x antes de reportar |
| `deploy_project` falha | Tentar novamente |
| OAuth expirado | Reautenticação via browser |
