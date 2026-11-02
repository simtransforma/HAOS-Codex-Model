# Playbook: login do Typebot e drift de banco

Use quando a interface do Typebot abre, mas o login retorna erro generico,
OAuth falha, o magic link nao e enviado ou a sessao nao e criada.

## Resultado esperado

- identificar a camada causal antes de alterar producao;
- preservar banco, bots, usuarios e arquivos;
- aplicar a menor correcao reversivel;
- provar autenticacao, banco e integridade separadamente.

## 1. Preflight

1. Confirmar o hostname canonico e o host que executa o stack.
2. Obter OK explicito antes de SSH, restart, recreate ou mudanca remota.
3. Registrar estado dos containers, reinicios, health e imagem efetiva.
4. Nao imprimir valores de `.env` ou `docker inspect`. Expor somente presenca e
   metadados seguros, como host e nome do banco sem usuario ou senha.
5. Se houver risco de migracao, drop ou volume, validar backup recente usando
   `backup-hetzner` antes de prosseguir.

## 2. Diagnostico em camadas

### Rota e Auth.js

Validar separadamente:

- pagina de login;
- `/api/auth/providers`;
- `/api/auth/session`;
- `/api/auth/csrf`.

HTTP 200 aqui prova apenas que a aplicacao responde. Ainda e necessario ler os
logs do Builder no instante da tentativa.

### Logs do Builder

Filtrar logs recentes e higienizar e-mails, URLs, tokens e credenciais. Procurar:

- `PrismaClientInitializationError`;
- `Can't reach database`;
- `relation ... does not exist` ou `table ... does not exist`;
- `AdapterError` e `SessionTokenError`;
- `EmailSignInError`, `EAUTH`, `535`, SMTP e Nodemailer;
- erros OAuth e callback URL.

### Estado desejado versus efetivo

Comparar, sem revelar segredos:

1. origem de `DATABASE_URL` no compose;
2. destino sanitizado no `.env` atual;
3. destino sanitizado carregado no Builder;
4. destino sanitizado carregado no Viewer;
5. redes Docker efetivas dos tres componentes: Builder, Viewer e banco.

Arquivos corretos com container antigo indicam drift de runtime. Nao alterar a
rede para tornar acessivel um banco errado apenas porque ele aparece no erro.

### Banco e integridade

Antes da correcao, consultar o banco que o `.env` atual declara como canonico:

- conexao `SELECT 1`;
- existencia do schema esperado;
- contagem de tabelas;
- contagem de bots e usuarios.

Registrar somente contagens. Nao listar dados pessoais, nomes de bots ou linhas.

## 3. Matriz de decisao

| Evidencia | Causa provavel | Acao |
|---|---|---|
| Builder e Viewer usam o mesmo banco, mas nao ha TCP/DNS | rede ou banco indisponivel | reparar a dependencia de rede/banco com rollback |
| `.env` e Viewer usam banco canonico, Builder usa outro | container obsoleto | recriar somente o Builder a partir do compose atual |
| Banco responde, mas `User`/`Typebot` nao existem | banco ou schema errado | nao migrar; corrigir o destino efetivo |
| Banco e schema passam, mas SMTP retorna `535`/`EAUTH` | transporte de e-mail | validar provedor e credencial sem trocar banco |
| Magic link passa, Google falha | OAuth isolado | revisar client, redirect URI e callback canonico |

## 4. Correcao de container obsoleto

1. Criar backup privado, modo restrito, do compose e do `.env`.
2. Validar que o `.env` canonico conecta e contem as tabelas e contagens
   esperadas.
3. Executar `docker compose config -q`.
4. Recriar apenas o Builder, sem dependencias e sem pull implicito:

```bash
docker compose up -d --no-deps --force-recreate typebot-builder
```

5. Confirmar que o ambiente efetivo do novo Builder aponta para o mesmo destino
   do Viewer.
6. Confirmar que nenhuma rede temporaria de diagnostico permaneceu no compose ou
   nos containers.

Se a validacao pre-recreate falhar, parar. Nao tentar corrigir dados ou executar
migration automaticamente.

## 5. Validacao final

Provar todos os itens:

- Builder e Viewer `running`;
- ambos usam o banco canonico;
- conexao TCP e consulta SQL funcionam;
- contagens de bots e usuarios permanecem iguais ao precheck;
- compose valido;
- pagina de login, providers e session respondem;
- zero novo erro Prisma/Auth.js/SMTP no recorte posterior;
- um unico canario de magic link retorna a rota de `verify-request`, sem imprimir
  token, URL completa ou destinatario.

O clique no link ou OAuth e um gate humano. Informar ao usuario para usar apenas o
link mais recente; nao declarar login humano concluido sem essa confirmacao.

## 6. Rollback

- Manter o backup ate uma janela de observacao satisfatoria.
- Se o Builder novo nao iniciar, restaurar o compose anterior e recriar somente
  o Builder.
- Nao restaurar banco ou volume para um problema comprovadamente restrito a
  configuracao efetiva do container.

## Evidencia de fechamento

Entregar: causa raiz, diferenca desejado/efetivo, servico recriado, contagens
antes/depois, endpoints testados, erros recentes, caminho privado de rollback e
qualquer gate humano restante.
