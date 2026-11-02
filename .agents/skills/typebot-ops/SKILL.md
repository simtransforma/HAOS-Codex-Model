---
name: typebot-ops
description: "Diagnosticar, manter e recuperar Typebot self-hosted em Docker, incluindo Builder, Viewer, PostgreSQL, MinIO, login, magic link e drift entre compose, .env e ambiente efetivo. Use quando o Typebot abre mas o login falha, mostra erro generico, nao envia acesso, perde bots ou apresenta falhas de banco. Nao use para desenhar fluxos conversacionais."
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

# Typebot Ops

Operar o Typebot self-hosted com preservacao de bots, usuarios, arquivos e
configuracao. Comecar em modo somente leitura; SSH, restart, recreate, banco ou
qualquer mudanca externa exigem OK explicito do usuario.

## Invariantes

1. Estado desejado nao prova estado efetivo. Compare `.env` e compose atuais com
   o ambiente carregado em cada container, sem imprimir valores sensiveis.
2. Builder e Viewer devem apontar para o mesmo banco e schema canonicos, salvo
   arquitetura documentada que prove o contrario.
3. Container `running`, rota HTTP 200 e tela de login aberta nao provam que
   autenticacao, Prisma, SMTP ou banco estao funcionais.
4. Antes de recriar um servico, validar o banco de destino e registrar contagens
   nao sensiveis de usuarios e bots para comparacao posterior.
5. Corrigir somente o componente causal. Nao reiniciar banco, Viewer, MinIO ou
   stack inteira quando o drift estiver restrito ao Builder.
6. Nunca imprimir URLs completas de banco, variaveis de ambiente, tokens,
   cookies, e-mails, senhas ou links de magic login.

## Roteamento

- Login, magic link, erro generico, Prisma ou divergencia de banco: ler
  [references/login-database-drift-playbook.md](references/login-database-drift-playbook.md).
- Backup, restore ou disaster recovery do host: usar a skill `backup-hetzner`.
- Criacao e conteudo dos bots: tratar como trabalho de produto/conversacional,
  fora desta skill operacional.

## Saida minima

Relatar causa comprovada, escopo alterado, backup/rollback, componentes
preservados e evidencias finais. Diferenciar `corrigido tecnicamente` de
`login humano confirmado`: o segundo depende de o usuario concluir OAuth ou
abrir o magic link mais recente.
