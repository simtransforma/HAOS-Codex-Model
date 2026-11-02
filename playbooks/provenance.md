# Proveniencia e readback

## Fontes e transformacao

Este modelo usa requisitos autorizados do mantenedor e sinteses originais de
conceitos de orquestracao, verificacao, pesquisa e conhecimento. O inventario
[capacidades](capabilities.md) separa uso conceitual, dependencias opcionais e
exclusoes. Inventario nominal nao prova leitura integral, paridade funcional,
licenca ou configuracao de uma ferramenta.

Arquivos privados foram apenas fontes de consulta: nenhum diario, cliente,
endpoint, chave, caminho operacional, voz proprietaria ou configuracao viva e
destino de distribuicao. Materiais terceiros nao foram embarcados; adaptadores
nao incluem upstream. Para adicionar conteudo terceiro, documentar licenca e
atribuicao antes de copiar. Sem direitos claros, excluir o conteudo.

## Envelope

Usar haos-memory-provenance. O [schema de template](../memory/templates/provenance.schema.json)
e seu [exemplo inativo](../memory/templates/provenance.example.json) nao comprovam persistencia.
Para um registro real: identidade estavel,
escopo, tipo, resumo, fonte/localizador, observacao, confianca, chave idempotente e
supersedes distinguem fato de inferencia e revisao de duplicata.

No-memory, read-only e dry-run impedem persistencia conforme o escopo pedido.
Destinos sao cadastrados explicitamente; nao criar conta, servico, API ou espelho.

## Algoritmo operacional

1. Sanitizar antes de gravar ou transmitir. Nunca duplicar o dado bruto para log.
2. Buscar equivalente por identidade, escopo, tipo e causa raiz.
3. Se equivalente e mesmo conteudo: no-op e readback, sem nova memoria.
4. Se mudou: atualizar sob revisao ou criar supersessao explicita, sem apagar historia.
5. Escrever somente em destino habilitado e autorizado.
6. Ler pelo identificador exato e comparar campos/conteudo da revisao.
7. Registrar recibo por destino: verified, pending, disabled ou not_applicable.

Resposta aceita, fila criada, health ou similaridade semantica nao provam
persistencia exata. Timeout e resultado ambiguo exigem reconciliacao por ID/chave
antes de reenviar. Disabled nao e pending; falha de destino habilitado nao apaga
os readbacks validos dos demais.

## Fechamento

Main classifica valor e verifica escopo, artefato, proveniencia, validacao e
readback dos destinos habilitados. SO_FECHA nao exige aprendizado; CAPITALIZA
somente sobre conteudo novo confirmado; PENDENTE explica lacuna comprovada.
Sem servico configurado, o fechamento local permitido nao fica dependente dele.
Nenhum marcador textual faz sync, commit, push ou ingestao automaticamente.
