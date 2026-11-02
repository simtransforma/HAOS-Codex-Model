---
name: haos-rag-corpus-oficial
description: "Prepara e valida corpus de fontes oficiais para uma RAG existente, com proveniencia, direitos, revisao de PII e readback; use em pedidos de alimentar base com documentos oficiais."
---

# Corpus Oficial para RAG

Todos os caminhos relativos nesta skill partem do repo canonico `${HAOS_PRIVATE_ROOT}`, nao do cwd nem do cache do plugin.

Trate captura, curadoria e ingestao como etapas distintas. Esta skill nao escolhe infraestrutura, cria uma RAG nova nem autoriza escrita remota.

## Escopo e fontes

1. Defina dominio, documentos candidatos, prioridade, base destinataria e finalidade de consulta.
2. Confirme que cada origem e oficial e que captura/uso pretendidos respeitam copyright, termos de acesso e restricoes tecnicas. Nao contorne login, bloqueio ou paywall.
3. Verifique texto, versao e jurisdicao na fonte. Fonte inacessivel ou conteudo ilegivel fica `NAO CAPTURADO`, com motivo; nao substitua por parafrase inventada.
4. Diferencie data de publicacao, vigencia/redacao e data real de captura. Nao declare norma vigente so por URL ou memoria.

## Manifesto e curadoria

- Mantenha por documento: titulo, URL oficial, identificador estavel/path-id, hash do conteudo, data de captura, vigencia/redacao conhecida, metodo, permissao/restricao e status.
- Preserve identidade unica por documento para evitar colisao ou sobrescrita. Compare hash e path-id antes de reingerir.
- Revise PII e material sensivel caso a caso; falso positivo de detector nao libera ingestao automaticamente.
- Escolha tags apos consultar as tags reais do conector. Nao invente taxonomia, contagens ou score threshold universal.
- Uma transcricao integral so entra se permitida pela fonte; quando nao for, armazene metadados e referencia permitidos.

## Preflight por documento

- Registre pagina ou secao de origem quando o documento for longo ou tiver varias versoes.
- Guarde URL canonica e identificador oficial, nao apenas resultado de busca.
- Compare titulo e conteudo capturado com a pagina aberta; HTTP 200 nao prova texto correto.
- Confira encoding e acentuacao em amostras PT-BR antes de calcular o hash final.
- Marque redacao historica como tal e preserve relacao com a vigente sem sobrescrever evidencias.
- Remova apenas PII cuja remocao seja permitida e nao altere o sentido da norma.
- Registre restricoes de redistribuicao e retencao; fonte oficial nao significa dominio publico automaticamente.
- Nao trate score de busca isolado como prova: confira documento retornado e trecho sustentador.
- Prepare rollback por identificador antes de qualquer reingestao que substitua chunks.
- Separe falha de captura, falha de preparo, falha de ingestao e falha de recuperacao.
- Mantenha contagens de documentos e chunks distintas; uma nao prova a outra.
- Evite ampliar o corpus com paginas relacionadas sem escopo aprovado.

## Ingestao controlada

1. Descubra e documente um conector REAL disponivel, seu contrato, destino e capacidade de dry-run. Nao copiar scripts, paths, credenciais ou procedimentos de transporte do ambiente Claude.
2. Rode dry-run e confira itens, duplicatas, PII, custos e impacto. A escrita externa exige OK explicito no escopo.
3. Ingerir somente o lote aprovado; nunca rodar sincronizacao destrutiva nem apagar corpus como atalho.
4. Faca readback por tag e por documento/path-id, comparando amostras com fonte e manifesto. Resultado vazio pede diagnostico, nao alegacao de ausencia.
5. Relate capturados, nao capturados, falhas, duplicatas, autorizacao e evidencia por destino. Sem conector real ou OK, entregue apenas corpus/manifesto e `INGESTAO PENDENTE`.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
