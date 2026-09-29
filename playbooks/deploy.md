# Playbook de deploy

## Preflight

- Defina mudanca, destino, owner e autorizacao explicita.
- Confira branch, diff, testes, backup, dependencia e saude atual.
- Registre criterio de sucesso, janela e observabilidade.

## Execucao

- Aplique somente o escopo aprovado.
- Registre comandos e resultados sem segredos.
- Pare em erro inesperado; nao altere controles para "fazer passar".

## Pos-deploy

- Verifique a versao no destino e o fluxo funcional.
- Compare indicadores e logs ao baseline.
- Documente resultado, risco residual e decisao de manter ou reverter.

## Rollback

- Use procedimento especifico do servico, previamente testado.
- Preserve dados criados depois do baseline; nao restaure snapshot antigo
  sobre trabalho novo sem aprovacao e analise de perda.
