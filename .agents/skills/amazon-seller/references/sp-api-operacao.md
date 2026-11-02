# SP-API — referência operacional

## Estado confirmado em 25/07/2026

O perfil da ${USER_BRAND} foi aprovado como **desenvolvedor privado** com acesso global de marketplace às roles solicitadas. Isso libera o registro de um cliente de app, mas não cria nem autoriza automaticamente um aplicativo em produção.

## Conceitos

- **Perfil de desenvolvedor:** aprovação organizacional e de roles.
- **App client:** cliente registrado no Solution Provider Portal/Developer Central.
- **App privado:** atende somente a própria organização e usa autoautorização; não é app público/OAuth para terceiros.
- **LWA:** Login with Amazon; OAuth 2.0 gera os tokens usados pela SP-API.
- **Refresh token:** segredo durável usado para obter access tokens; manter fora de Git e de logs.
- **RDT:** token curto para operações restritas/PII quando a API o exige.

## Registro de aplicativo

1. Entrar no Solution Provider Portal com usuário principal.
2. Acessar **Develop Apps** e escolher **Add new app client**.
3. Preencher tipo, finalidade, roles e marketplaces estritamente necessários.
4. Validar em sandbox quando houver suporte e executar chamada de leitura em produção somente após aprovação.
5. Autoautorizar o app privado na conta vendedora e custodiar credenciais de modo seguro.

Não registrar app com escopo genérico, não solicitar dados que o fluxo não usa e não expor LWA client secret ou refresh token.

## Autorização e roles

Uma operação precisa de pelo menos uma das roles listadas na documentação; operações restritas podem exigir role geral e role restrita. Mapear operação e tipo de Report/Feed/Notification antes de pedir alteração no perfil. Falhas por escopo normalmente retornam `403`.

Para PII, aplicar minimização. Em operações legadas restritas, gerar RDT com `Tokens API.createRestrictedDataToken` e enviar o RDT no cabeçalho `x-amz-access-token`. A Orders API v2026-01-01 migra o acesso a PII para roles; confirmar a versão adotada antes de implementar.

## Implementação robusta

- Usar a versão de API mais recente compatível e monitorar release notes/deprecações.
- Respeitar `x-amzn-RateLimit-Limit`, paginação e limites por app/conta.
- Aplicar retry exponencial apenas para falhas transitórias; não repetir mutações sem chave de idempotência ou reconciliação.
- Guardar logs sem PII e com request ID, operação, horário, marketplace, status e correlação interna.
- Separar credenciais sandbox/produção e negar acesso em menor privilégio.

## Fontes oficiais

- Registro de aplicação: https://developer-docs.amazon.com/sp-api/docs/registering-your-application
- Visão de onboarding: https://developer-docs.amazon.com/sp-api/docs/onboarding-overview
- Registro privado: https://developer-docs.amazon.com/sp-api/docs/register-as-a-private-developer
- Roles e mapeamentos: https://developer-docs.amazon.com/sp-api/docs/role-mappings
- Marketplaces: https://developer-docs.amazon.com/sp-api/docs/marketplace-ids
- Dados restritos: https://developer-docs.amazon.com/sp-api/docs/authorization-with-the-restricted-data-token
- FAQ: https://developer-docs.amazon.com/sp-api/docs/general-faq
- Suporte: https://developer.amazonservices.com/support

O guia GitHub informado na aprovação redireciona para a nova documentação: https://developer-docs.amazon.com/sp-api/docs/what-is-the-selling-partner-api
