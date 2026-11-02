---
name: haos-local-research
description: "Pesquisa local por cidade, raio, bairro, negocios, imoveis, servicos, concorrentes e fontes publicas. Use quando a localizacao for parte essencial da pergunta."
---

# HAOS Local Research

Camada especializada do pesquisador para perguntas em que cidade, bairro, raio,
distancia, disponibilidade ou proximidade mudam a resposta.

## Contrato padrao do usuario

- Cobrir qualquer categoria local quando o usuario nao restringir o tema.
- Fixar primeiro a cidade solicitada.
- Perguntar antes de ampliar para cidades vizinhas, raio adicional ou fontes que exigem login.
- Usar o maior numero de fontes publicas possivel dentro do escopo autorizado.
- Fazer pesquisa pontual por padrao.
- Entregar PDF com links clicaveis quando o usuario pedir uma entrega formal.
- Nao enviar mensagem, alerta ou documento por WhatsApp sem confirmacao explicita no turno do envio.

## Limite geografico obrigatorio

Antes da coleta, registrar:

- cidade e estado canonicos;
- bairros, localidades ou pontos de referencia;
- raio autorizado;
- criterio de expansao;
- regra para resultados fora do escopo.

Resultados devem receber `scope_status` (`inside`, `nearby`, `outside`) e `distance_km`
quando houver coordenadas. Nunca apresentar resultado de cidade proxima como se fosse
da cidade pedida. APIs que tratam raio apenas como vies de relevancia precisam de
validacao posterior pelo endereco e pela cidade.

## Roteamento por fonte

### Negocios e pontos de interesse

- LocalAPI: usar a fonte local aprovada e configurada pelo usuario; obter identificadores e autenticacao da configuracao local, nunca deste documento, e verificar cobertura antes da consulta.
- Brave Place Search: POIs, enderecos e categorias por localizacao.
- Google Places API: alternativa oficial para busca e detalhes por `place_id`.
- OpenStreetMap/Overpass: cobertura geoespacial aberta e validacao de presenca.
- Foursquare, HERE ou Mapbox: fontes alternativas quando cobertura ou geocodificacao exigir.

### Imoveis e inventario comercial

- Usar busca web e navegador para portais, paginas de imobiliarias, grupos publicos e anuncios.
- Usar APIs de POI para descobrir imobiliarias, corretores e servicos, nao como prova de estoque.
- Registrar o link direto do anuncio, preco, data de verificacao e status de disponibilidade.
- Nao afirmar que uma listagem esta ativa apenas porque aparece em um resultado de busca.

### Concursos, servicos publicos e fontes institucionais

- Priorizar prefeitura, orgao, diario oficial, banca e documento original.
- Usar busca local apenas para descoberta; a fonte primaria valida o resultado.

## Fluxo de coleta

1. Classificar a intencao local e definir o criterio de aceite.
2. Normalizar cidade, UF, bairros e sinonimos.
3. Expandir consultas por categoria, portal, idioma e grafias.
4. Consultar fontes em paralelo dentro de rate limits e orcamento.
5. Usar busca rapida para candidatos e consulta completa apenas nos finalistas.
6. Reconsultar paginas primarias para verificar preco, disponibilidade e contato.
7. Normalizar endereco, telefone, URL e coordenadas.
8. Deduplicar por identificador de fonte, URL, telefone e endereco.
9. Classificar confianca, frescor e escopo geografico.
10. Gerar tabela de lacunas: fontes bloqueadas, cidades nao cobertas e campos nao confirmados.
11. Escrever o relatorio e, quando solicitado, gerar PDF com links clicaveis.

## Schema minimo de evidencia

Cada item deve conservar, quando disponivel:

- `title` ou `name`;
- `category`;
- `city`, `state`, `address`;
- `scope_status`, `distance_km`;
- `price` e `availability` para imoveis;
- `phone` ou `whatsapp` somente quando publico na fonte;
- `source_name`, `source_url`, `source_type`;
- `found_at`, `verified_at`, `freshness_status`;
- `evidence_excerpt` curto ou campo confirmado;
- `confidence` e `reason`;
- `notes` sobre duplicidade, bloqueio ou incerteza.

Por padrao, a pesquisa e pontual: nao criar banco persistente de dados locais.
O PDF pode conter os dados publicos necessarios e links; armazenamento recorrente
exige pedido separado e avaliacao de finalidade, retencao e LGPD.

## LocalAPI

Tratar `local-api.com` como um adaptador externo, nunca como memoria do agente.

- Guardar a chave apenas no ambiente seguro do backend; nunca no prompt, PDF, log ou Git.
- Preferir busca rapida para descoberta e jobs assincronos para varreduras maiores.
- Usar idempotency key, cache, retry com limite e registro de custo.
- Validar cidade e escopo depois da resposta.
- Confirmar com o fornecedor os direitos de armazenamento e redistribuicao antes de uso comercial.
- Nao tratar claims de exclusividade, cobertura ou preco da pagina comercial como fatos sem validacao.
- Se a API falhar, continuar com fontes alternativas e declarar a lacuna.

## Qualidade e seguranca

- Nao usar fonte privada, login de terceiro, captcha solver ou bypass de bloqueio.
- Nao coletar dados sensiveis ou contatos privados.
- Nao mandar abordagem automatica para contatos encontrados.
- Claims atuais exigem fonte e data de coleta.
- Conclusao forte exige confirmacao independente ou qualificacao da incerteza.
- Marcar cada afirmacao como FATO, OBSERVACAO, ESTIMATIVA, INFERENCIA ou HIPOTESE.

## Perguntas de bloqueio

Perguntar antes de coletar quando faltar algum destes pontos:

- cidade/UF ou ponto de referencia;
- se cidades proximas podem entrar;
- raio maximo;
- campos obrigatorios;
- fontes publicas versus fontes autenticadas;
- pesquisa pontual versus monitoramento;
- destino do resultado;
- limite de custo quando houver API paga.

Se o usuario ja tiver respondido uma politica global, aplica-la sem perguntar de novo;
perguntar somente o que for especifico da nova pesquisa.

## Entrega

O relatorio final deve conter:

- resumo executivo;
- escopo geografico e regra de expansao;
- fontes consultadas e fontes bloqueadas;
- resultados classificados por `inside`, `nearby` e `outside`;
- links clicaveis;
- data de verificacao;
- confianca e lacunas;
- recomendacao de proximo passo;
- STATUS: CONCLUIDO, REVISAO NECESSARIA ou BLOQUEADO.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
