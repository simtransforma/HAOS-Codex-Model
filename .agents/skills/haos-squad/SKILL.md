---
name: haos-squad
description: Use quando uma tarefa autorizada puder ser dividida em entregas independentes com especialistas, ownership disjunto e integracao verificavel.
---

# Squad com responsabilidade delimitada

Acione com `$haos-squad`. Uma squad existe quando ha chamadas reais a agentes e
retornos observados. Plano, arquivo de papel ou lista de nomes nao prova spawn.

## Entradas

Receba objetivo, plano vigente, evidencias, baseline, criterios de aceite,
dependencias, ownership e autorizacoes. Consulte catalogo local e capacidade de
delegacao antes de prometer paralelismo. Nao delegue pergunta simples por ritual.

## Passos

1. Divida o trabalho em unidades com saida verificavel. Mapeie dependencias;
   coloque na mesma onda apenas unidades independentes. Use ate tres agentes
   por onda, respeitando tambem o limite real da ferramenta.
2. Atribua owner unico por arquivo ou recurso e revisor distinto quando aplicavel.
   Write-sets devem ser disjuntos; caminhos compartilhados ou dependencia incerta
   exigem serializacao. Preserve baseline sujo e trabalho de outros agentes.
3. Prepare briefing com objetivo, contexto minimo, fontes pertinentes, read_files,
   write_files, recursos, saida, aceite, checks, skills e caminhos, dependencias,
   riscos, limite de ciclos e evidencia de autorizacao atual quando necessaria.
   Diga explicitamente que outros agentes trabalham em areas disjuntas e que
   suas mudancas nao podem ser revertidas.
4. Acione a ferramenta real com effort high e modelo herdado, sem ID fixo.
   Use somente parametros suportados. Se a ferramenta nao puder representar
   a configuracao requerida, declare a limitacao; nao degrade em silencio.
   Informe solicitado, aceito e efetivamente observado como estados distintos.
5. Cada executor atua apenas no ownership, le skills pertinentes e devolve prova.
   Sem delegacao recursiva, commit, push, merge, memoria independente ou acao
   externa fora do consentimento. Bloqueio deve incluir tentativa e lacuna,
   sem expandir a area de escrita por conta propria.
6. Integre depois dos retornos: confira diff contra baseline, arquivos novos,
   interacoes e checks. Use `$haos-multi-agent-review` para revisao independente
   pertinente. O coordenador resolve sobreposicoes antes de nova escrita.
7. Encaminhe correcoes ao owner original ou reatribua explicitamente apos parar
   o anterior. Limite a tres ciclos com hipotese nova e verificacao fresca.
   Defeito restante resulta em REVISAO NECESSARIA; dependencia real, BLOQUEADO.
8. Pare no aceite ou bloqueio. Nao deixe agentes ocultos, loops ou promessa de
   trabalho futuro sem acompanhamento. Revogacao interrompe a parte afetada.

## Saida

Cada executor retorna STATUS: CONCLUIDO, BLOQUEADO ou REVISAO NECESSARIA;
arquivos/recursos; mudancas; checks e resultados; pendencias; riscos residuais.
O coordenador entrega quadro de ondas, chamadas e retornos observados, integracao,
aceite e limites. Modelo pedido nao prova modelo efetivo; arquivo nao prova hot reload.

## Criterios de aceite

Todas as unidades possuem owner, resultado verificavel e integracao concluida.
Nenhum arquivo recebeu escrita concorrente autorizada a dois donos. Checks
planejados nao aparecem como executados. Aprovacao de plano nao autoriza por
si so publicacao, gasto ou outra acao externa sensivel fora do escopo aprovado.

## Erros e recuperacao

Ferramenta indisponivel: entregar plano/handoff e declarar ausencia de delegacao.
Timeout: consultar estado do agente, nao presumir conclusao nem duplicar executor
no mesmo recurso. Diff inesperado: reconciliar com owner e baseline antes de editar.
Nao instalar integracoes ou alterar servicos para simular capacidade de squad.

## Cenarios de verificacao

- Quatro entregas independentes: dividir em ondas respeitando teto de tres.
- Dois write-sets se cruzam: serializar antes do spawn ou redefinir ownership.
- Retorno diz pronto sem check: verificar aceite e manter pendencia explicita.
- Ferramenta nao retorna modelo efetivo: registrar somente configuracao solicitada.
