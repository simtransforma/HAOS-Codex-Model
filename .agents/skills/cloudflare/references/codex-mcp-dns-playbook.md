---
title: Cloudflare MCP no Codex — autenticação e DNS idempotente
status: active
last_validated: 2026-09-14
scope: cloudflare-mcp-dns
---

# Cloudflare MCP no Codex

## Quando usar

Use este procedimento quando o Codex precisar ler ou alterar DNS pela conexão oficial da Cloudflare. Alterações continuam sujeitas ao gate de aprovação externa do HAOS.

## Princípio operacional

Quatro estados são independentes:

1. plugin instalado;
2. servidor MCP configurado;
3. OAuth autenticado;
4. ferramentas carregadas na sessão atual.

Não inferir um estado a partir de outro.

## Autenticação

1. Verifique se o MCP usa `https://mcp.cloudflare.com/mcp`.
2. Faça o login OAuth com uma versão atual do Codex CLI.
3. Se um CLI antigo falhar no callback com `missing required issuer`, trate como incompatibilidade do cliente e tente novamente com a versão atual; não conclua que a conta está inválida.
4. Reinicie o aplicativo ou abra uma nova tarefa para renovar o catálogo de ferramentas.
5. Faça uma leitura inofensiva para validar identidade e escopo antes de propor mutação.

## Alteração DNS idempotente

1. Pesquise no próprio MCP a operação e o schema atuais.
2. Resolva a zona pelo nome, sem copiar identificadores permanentes para o artefato.
3. Consulte o hostname exato e registre apenas a contagem e o estado necessários à decisão.
4. Interrompa se houver conflito de tipo, duplicidade inesperada ou destino divergente sem autorização explícita.
5. Com aprovação vigente:
   - zero correspondências: criar;
   - uma correspondência equivalente: não alterar;
   - uma correspondência divergente e identificada: atualizar;
   - múltiplas correspondências: bloquear para revisão.
6. Releia o registro e confirme sucesso na resposta.
7. Faça verificação independente de DNS e da camada de aplicação, incluindo HTTPS quando aplicável.

## Evidência mínima de conclusão

- autorização explícita vinculada à mudança;
- leitura anterior do hostname;
- resposta de mutação bem-sucedida ou prova de idempotência;
- readback do estado final;
- resolução DNS externa;
- resposta HTTPS esperada, quando houver aplicação web.

## Privacidade e segurança

Memórias e relatórios devem guardar somente o procedimento e o resultado abstrato. Não persistir tokens, senhas, IDs da conta/zona/registro, IPs de origem, cookies, inventário de hosts ou detalhes internos do painel.

## Diagnóstico rápido

| Sintoma | Hipótese provável | Próxima ação |
|---|---|---|
| Skill disponível, ferramentas ausentes | Plugin instalado sem conexão autenticada | Conferir URL do MCP e login OAuth |
| OAuth volta com erro de emissor | CLI antigo incompatível com o callback | Repetir com CLI atual |
| Login concluído, ferramentas ainda ausentes | Catálogo da sessão está antigo | Reiniciar aplicativo/tarefa |
| API confirma alteração, site não responde | DNS/TLS/origem ainda não convergiu | Validar DNS e HTTPS externamente |

## Critério de atualização

Revalidar este playbook quando mudar a versão do Codex CLI, o endpoint oficial do MCP ou o contrato das ferramentas Cloudflare.
