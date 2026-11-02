# Playbook Lovable — roteamento SIM e HAU

## Decisão operacional

| Origem do projeto | Canal padrão | Regra |
|---|---|---|
| SIM | MCP Lovable existente | Usar apenas para projetos visíveis no workspace SIM autenticado. |
| HAU e clientes | Navegador local autenticado | Reutilizar a sessão da conta proprietária do projeto e operar no painel Lovable. |

Não tentar transformar o MCP do SIM em conector multi-conta durante uma entrega. Se o
projeto HAU não aparecer no MCP, seguir pelo navegador local.

## Preflight

1. Identificar se o projeto pertence ao SIM ou à HAU/cliente.
2. Confirmar nome do projeto, workspace e domínio público.
3. Verificar se a sessão correta já está aberta no navegador local.
4. Ler o estado live: rota, preview, histórico, arquivos e publicação pendente.
5. Confirmar o escopo autorizado. Publicação continua sendo alteração sensível.

## Fluxo HAU/cliente pelo navegador local

1. Reutilizar a aba autenticada do projeto; não abrir outro perfil por padrão.
2. Abrir `Ctrl+K` e selecionar `Code`.
3. Localizar o arquivo e a rota reais antes de editar.
4. Aplicar a menor alteração suficiente e salvar com `Ctrl+S`.
5. Confirmar que surgiu um novo item no histórico de edição do Lovable.
6. Abrir Preview e validar a rota alterada.
7. Com autorização explícita vigente, abrir Publish e executar `Publish changes`.
8. Aguardar a conclusão e testar a URL pública com cache-buster.
9. Validar desktop, mobile, CTAs, checkout, WhatsApp, tracking e preservação de UTMs.

## Fluxo SIM pelo MCP

1. Confirmar que a identidade e o workspace retornados pelo conector são do SIM.
2. Listar ou consultar o projeto antes de qualquer escrita.
3. Se o projeto esperado não aparecer ou houver `403`, interromper a escrita e conferir
   se o projeto é HAU/cliente; não assumir que ele foi removido.
4. Usar o MCP apenas dentro das permissões e do workspace confirmados.
5. Publicar somente com autorização explícita e validar a URL pública depois.

## Falhas conhecidas e recuperação

- `invalid_client_metadata` ao adicionar outro MCP Lovable: o registro dinâmico OAuth
  foi rejeitado. Remover a entrada parcial e usar o navegador local para HAU/clientes.
- `403` no projeto: provável divergência entre conta OAuth e proprietária do projeto.
  Conferir identidade/workspace antes de pedir novo login ou concluir que não há acesso.
- `0 credits remaining`: não comprar créditos. Usar Files/Code se a edição manual estiver
  disponível e validar build/preview normalmente.
- Alteração salva mas não aparece no site: confirmar histórico, Preview, Publish e URL
  pública com cache-buster; mensagem antiga do chat não comprova deploy.

## Evidência mínima de conclusão

- Projeto e workspace corretos confirmados.
- Arquivo/rota alterados identificados.
- Histórico registra a edição.
- Preview aprovado.
- Publicação autorizada e concluída, quando aplicável.
- URL pública testada com resultado comportamental, não apenas visual.

## Segurança

- Não registrar cookies, tokens, senhas ou e-mails de login neste playbook.
- Não comprar créditos, trocar plano ou publicar sem autorização.
- Não copiar sessão entre contas nem usar o MCP do SIM em projetos HAU/clientes.
