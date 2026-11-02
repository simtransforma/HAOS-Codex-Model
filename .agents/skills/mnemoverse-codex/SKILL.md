---
name: mnemoverse-codex
description: "Configura, valida e diagnostica o acesso do Codex ao Mnemoverse usando o cofre Master sem expor credenciais e sem alterar o Claude Code."
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

# Mnemoverse no Codex

Use esta skill quando o Codex precisar configurar, testar ou diagnosticar o
Mnemoverse, especialmente quando houver erro de chave ausente, `401`, alias
duplicado ou MCP iniciado com ambiente antigo.

## Regras fundamentais

- O `${USER_SECRET_FILE}` e a fonte de credenciais. Consulte-o por loader seguro antes de
  declarar uma chave ausente ou desistir por erro de autenticacao.
- Nunca imprima, registre, masque parcialmente, copie, versione ou grave o valor
  de uma chave.
- No PC, configurar somente o ambiente/configuracao do Codex. Na sandbox
  Hostinger do Thiago, usar exclusivamente o broker interno e o MCP de leitura;
  a chave fica root-only no broker, nunca no usuario `thiago`. Nao alterar
  Claude Code, `.claude`, claude-mem do Claude Code ou credenciais desses
  ambientes.
- Nao escolher uma chave apenas pelo nome do alias. Validar cada candidato contra
  um endpoint read-only do Mnemoverse e selecionar somente um retorno autorizado.
- Variavel recomendada no cliente MCP: `MNEMOVERSE_API_KEY`.
- Na sandbox, a variavel acima pertence somente ao broker. O MCP da sandbox
  nao recebe essa variavel e expoe apenas `memory_stats` e `memory_read`.
- Depois de alterar variavel de usuario ou configuracao MCP, reiniciar o Codex
  para que o processo do servidor MCP herde o novo ambiente.

## Fluxo minimo

1. Localizar o `${USER_SECRET_FILE}` sem mover, copiar ou imprimir o arquivo.
2. Ler os aliases candidatos em memoria.
3. Validar candidatos com `GET /api/v1/memory/stats`, usando o modo de
   autenticacao aceito pelo endpoint.
4. Gravar somente a chave selecionada na variavel de ambiente do usuario e
   referenciar essa variavel no `config.toml` do Codex.
5. Confirmar a configuracao sem exibir o valor.
6. Reiniciar o Codex quando o MCP ja estiver em execucao.
7. Testar `memory_stats` ou `memory_read`; classificar o resultado como
   `OK`, `PENDENTE_RELOAD`, `401_INVALIDA` ou `BLOQUEADO`.

## Diagnostico

- `MNEMOVERSE_API_KEY is required`: o processo MCP nao recebeu a variavel; o
  Master pode ter a chave. Verificar o Master e recarregar o Codex antes de
  concluir ausencia.
- `401`: testar os demais aliases do Master com o loader seguro. Nao substituir
  a chave por tentativa manual e nao rotacionar nada sem pedido do usuario.
- API read-only `200`, MCP ainda sem chave: a credencial esta valida, mas o
  processo MCP atual foi iniciado antes da configuracao; reiniciar o Codex.
- MCP `memory_write` so deve ocorrer depois da validacao local do aprendizado,
  com sintese redigida e sem dados sensiveis.

## Scripts do projeto

- `<USER_DEPENDENCY:scripts/install-mnemoverse-codex-safe.ps1>`: seleciona um alias valido,
  configura a variavel do usuario e o MCP do Codex.
- `<USER_DEPENDENCY:scripts/verify-mnemoverse-master-safe.ps1>`: testa aliases sem imprimir
  valores e retorna somente status por alias/modo.

## Playbook correspondente

Para o procedimento completo de preflight, validacao, reload e fechamento, use
`<USER_DEPENDENCY:playbooks/mnemoverse-codex-auth.md>` no PC. Para a sandbox Thiago, use
`<USER_DEPENDENCY:playbooks/thiago-sandbox-mnemoverse-readonly.md>`; nao aplique o instalador
Windows nem coloque a chave no usuario Linux.

## Evidencia obrigatoria

Relatorios devem registrar apenas:

- se o Master foi consultado;
- se algum alias foi validado;
- se o MCP esta configurado;
- se o processo precisa de reload;
- resultado read-only da API/MCP;
- confirmacao de que Claude Code nao foi alterado.

Nunca registrar o nome completo do cofre, o valor, prefixo, sufixo, tamanho ou
qualquer trecho da credencial.
