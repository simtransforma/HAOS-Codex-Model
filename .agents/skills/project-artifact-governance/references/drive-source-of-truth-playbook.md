# Playbook — Drive como fonte oficial e Obsidian como indice

## Objetivo

Criar ou consolidar documentos oficiais na pasta correta do Google Drive do projeto, mantendo o Obsidian apenas como memoria e indice navegavel.

## Quando usar

- o usuario diz que tudo deve ficar na pasta oficial do projeto;
- existe um Drive central com subpastas tematicas;
- um documento foi criado localmente ou no Obsidian, mas precisa ser entregue ao cliente;
- o usuario pede checklist, relatorio, handoff, demanda criativa ou guia oficial;
- ha risco de o cliente se perder entre links, copias e fontes diferentes.

## Preflight

1. Ler o guia mestre do projeto antes de decidir o destino.
2. Identificar a pasta raiz oficial por ID ou URL verificados.
3. Listar as subpastas reais da raiz.
4. Classificar o artefato pelo uso:
   - central e governanca;
   - materiais recebidos;
   - criativos e copies;
   - trafego e tracking;
   - vendas e recuperacao;
   - apresentacoes;
   - outra categoria definida pelo projeto.
5. Pesquisar por titulo e tema para evitar duplicidade.
6. Confirmar se o documento e interno ou destinado ao cliente.

## Fluxo A — documento ainda nao existe

1. Criar o arquivo nativo adequado.
2. Inserir o conteudo completo.
3. Aplicar titulos, listas e links nativos quando suportados.
4. Mover para a subpasta oficial correta.
5. Ler o arquivo novamente e conferir conteudo.
6. Ler metadados e conferir a pasta pai.
7. Retornar apenas o link observado na resposta ou no readback.

## Fluxo B — documento existe apenas localmente ou no Obsidian

1. Tratar a copia local como fonte de conteudo, nao como destino final.
2. Pesquisar se ja existe equivalente no Drive.
3. Se existir, atualizar o oficial; se nao existir, criar um novo documento oficial.
4. Verificar conteudo e pasta pai.
5. Alterar a nota Obsidian para apontar para o link oficial.
6. Manter no Obsidian somente o resumo necessario para memoria interna.

## Fluxo C — documento oficial existe na pasta errada

1. Ler metadados e identificar todos os pais atuais.
2. Adicionar a subpasta correta.
3. Remover somente o pai que foi verificado como incorreto e deve deixar de conter o arquivo.
4. Preservar pais e compartilhamentos nao relacionados.
5. Confirmar o novo pai por readback.

## Mapeamento recomendado

| Tipo de artefato | Destino logico |
|---|---|
| Guia mestre, status, indice | Central do projeto |
| Arquivo entregue pelo cliente | Materiais do cliente |
| Pedido de criativo, copy, roteiro, aprovacao | Criativos e copies |
| Plano de campanha, tracking, QA, relatorio de midia | Trafego e tracking |
| Checkout, CRM, webhooks, recuperacao | Vendas e recuperacao |
| Deck, proposta, apresentacao | Apresentacoes |

Usar os nomes reais das pastas existentes; a tabela nao autoriza criar uma nova taxonomia sem necessidade.

## QA bloqueante

- [ ] O guia mestre foi consultado.
- [ ] A pasta raiz foi verificada.
- [ ] A subpasta foi escolhida pelo tipo do artefato.
- [ ] Nao existe duplicata equivalente.
- [ ] O arquivo oficial contem o conteudo esperado.
- [ ] O ID da pasta pai corresponde ao destino escolhido.
- [ ] O link retornado foi observado na ferramenta, nao inventado.
- [ ] O Obsidian aponta para o oficial e nao se apresenta como fonte unica.
- [ ] Nenhum segredo ou dado privado foi levado a uma area distribuivel.
- [ ] Nenhuma permissao de compartilhamento foi alterada sem autorizacao.

## Tratamento de falhas

### Arquivo criado na raiz do Drive

Mover para a subpasta correta e verificar o pai antes do fechamento.

### Pesquisa nao encontra a subpasta

Listar os filhos da pasta raiz usando o ID verificado. Nao criar outra pasta por semelhanca de nome sem confirmar a estrutura.

### Documento foi criado no Obsidian primeiro

Nao apagar a nota. Criar ou atualizar o documento oficial e converter a nota em indice com o link oficial.

### O usuario corrige o destino

Tratar a correcao como decisao autoritativa do projeto. Corrigir o artefato atual e aplicar a regra nas proximas entregas do mesmo projeto.

### Nao ha acesso de escrita ao Drive

Preparar o conteudo local, declarar `EXTERNAL_PENDING` e informar exatamente qual permissao ou conexao falta. Nao declarar que o documento esta centralizado.

## Evidencia de conclusao

O fechamento deve informar:

- titulo do arquivo;
- pasta logica de destino;
- link oficial verificado;
- se o Obsidian foi atualizado como indice;
- pendencias de acesso, compartilhamento ou aprovacao.

