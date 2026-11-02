---
name: run-security-assessment-playbooks
description: "Selecionar e executar playbooks autorizados de avalia\u00e7\u00e3o de seguran\u00e7a web/API com gates, baixa intrus\u00e3o, coleta de evid\u00eancia, triagem, comunica\u00e7\u00e3o e reteste. Usar em prepara\u00e7\u00e3o, execu\u00e7\u00e3o controlada ou resposta a achados de uma plataforma online, especialmente ticketing."
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

# Executar playbooks de avaliação

Sem autorização e escopo completos, executar somente o playbook de preparação. Para qualquer alvo real, exigir OK explícito do usuario no turno antes da interação externa.

## Seleção

- Preparação e threat model: `./references/01-preparacao.md`
- Avaliação web/API controlada: `./references/02-avaliacao.md`
- Achado crítico e contenção: `./references/03-achado-critico.md`
- Relatório, correção e reteste: `./references/04-relato-reteste.md`

Usar `./assets/finding-template.md` para achados. Aplicar as regras de parada de `assess-ticketing-security`.

## Disciplina

Registrar cada ação antes/depois, manter taxa mínima, não ampliar escopo por descoberta, redigir segredos/PII e distinguir scanner, hipótese e validação manual.
