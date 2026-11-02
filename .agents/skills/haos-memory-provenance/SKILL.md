---
name: haos-memory-provenance
description: Use quando o main preparar persistencia curada, reconciliar duplicatas ou verificar escrita e readback de conhecimento duravel.
---

# Proveniencia e escrita reconciliavel

## Entradas

Candidato comprovado, origem e evidencia, destinos habilitados, autorizacao,
opt-outs e identidade existente. Subagente prepara candidato; main persiste.
No-memory, read-only ou dry-run impedem escrita; respeitar tambem restricoes
de consulta. Nao instalar memoria nem criar hook para preencher campos.

## Envelope

Campos obrigatorios por item, com null explicito quando a regra permitir:

| Campo | Contrato |
| --- | --- |
| record_id | Identidade estavel do item; reutilizar ao atualizar |
| scope | Projeto ou dominio ao qual a afirmacao se aplica |
| kind | decisao, aprendizado, procedimento, incidente ou handoff |
| summary | Conteudo curado e sanitizado, sem transcricao literal |
| origin | Tipo e nome generico da fonte da observacao |
| locator | Caminho relativo e secao, ou identificador exato da fonte |
| observed_at | Momento real da observacao em ISO-8601 com fuso |
| confidence | confirmed, inferred ou pending; com justificativa |
| supersedes | Identidade/revisao superada, ou null para item inicial |
| task_id / revision | Identidade da tarefa se disponivel, ou null com motivo |
| dedupe_key | Chave estavel de scope, kind e causa raiz normalizada |
| content_hash | Resumo criptografico do conteudo canonico sanitizado |

O localizador precisa permitir reencontrar a prova sem revelar segredos.
Registro inferred/pending nunca deve ser promovido a fato confirmado por
simples repeticao. Se observed_at da evidencia for desconhecido, declarar
a lacuna e resolver antes de persistir como confirmada.

## Passos

1. Confirmar valor e autorizacao com `haos-evoluir`. Remover segredos, dados
   pessoais desnecessarios, caminhos internos sensiveis e raciocinio privado.
   Validar campos e definicao estavel da causa raiz.
2. Buscar equivalentes por dedupe_key e identidade em cada destino permitido.
   Busca semantica vazia nao prova ausencia; preferir leitura exata.
   Nao usar titulo da sessao ou numero de tentativa como chave.
3. Escolher CREATE se ausencia comprovada; SKIP se conteudo identico; UPDATE
   para novo conteudo do mesmo item. Se substituir afirmacao antiga, ligar
   supersedes e preservar historico. Conflito nao resolvido fica PENDENTE.
4. Serializar escritas por item/destino. Reutilizar identidade e hash em
   tentativas da mesma revisao; nao gerar outro id para contornar timeout.
   Mudanca de conteudo exige nova revisao explicita.
5. Escrever apenas nos destinos habilitados e autorizados. Disabled recebe
   DESABILITADO, nao falha. Guardar recibo sanitizado com destino, operacao,
   identidade/revisao, hash pretendido e resultado realmente retornado.
6. Fazer readback por destino e comparar identidade, scope, kind, summary,
   origin, locator, confidence, supersedes e hash. Se o destino nao guardar
   hash, recalcular a partir do conteudo lido no mesmo formato canonico.
   SKIP exige leitura que comprove equivalencia.
7. Em timeout ou retorno ambiguo, consultar identidade/recibo e reconciliar:
   conteudo igual permite confirmar; diferente exige resolver conflito;
   ausencia comprovada permite nova tentativa controlada. Sem prova suficiente,
   manter PENDENTE e nao reenviar cegamente.
8. Main consolida estados. Falha parcial preserva destinos ja confirmados;
   fila local, filtro, resposta de escrita e health nao substituem readback.

## Saida

Envelope sanitizado e quadro por destino: habilitacao, autorizacao, operacao,
id/revisao, hash, resultado, readback, diferencas e proximo passo.
Estados: VALIDADO, PENDENTE ou DESABILITADO; dry-run informa NAO EXECUTADO.

## Criterios de aceite

Origem rastreavel, dedupe demonstrada, supersessao preservada e readback exato
em cada destino exigido. Sem identidade remota suficiente para reconciliar,
nao afirmar persistencia. Esta skill nao concede permissao de escrita externa.

## Erros comuns

- Confundir sucesso tecnico com salvo: comparar o registro lido.
- Mudar id depois de timeout: investigar o id original antes de repetir.
- Atualizar contradicao apagando historia: usar supersedes e preservar versoes.

## Cenarios de pressao

- Timeout apos escrita possivelmente concluida: procurar pelo id e hash;
  sem resposta conclusiva, manter PENDENTE.
- Sessao foi renomeada e candidato reaparece: a dedupe_key continua estavel;
  SKIP ou UPDATE apos leitura, sem duplicar.
- Um destino confirma e outro falha: preservar o primeiro e relatar pendencia
  apenas no segundo; nao apagar prova nem simular sucesso global.
