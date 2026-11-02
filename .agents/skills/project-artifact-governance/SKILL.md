---
name: project-artifact-governance
description: "Governa onde criar, armazenar, mover, verificar e indexar documentos e entregaveis oficiais de projetos. Use quando houver Drive oficial, Obsidian, pasta de cliente, fonte unica de verdade, checklist, relatorio, handoff ou documento para cliente."
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

# Project Artifact Governance

Use esta skill para impedir que um entregavel oficial termine em rascunhos locais, outputs temporarios ou apenas no Obsidian quando o projeto possui uma pasta oficial definida.

## Regra central

Quando o projeto declarar uma fonte oficial de documentos:

1. criar ou importar o entregavel diretamente nessa fonte;
2. posicionar o arquivo na subpasta tematica correta;
3. verificar por leitura de metadados que o arquivo esta no destino correto;
4. retornar o link oficial ao usuario;
5. usar Obsidian, memoria e arquivos locais somente como indice, espelho ou rascunho, nunca como substitutos do artefato oficial.

## Autoridade das fontes

Aplicar esta ordem, salvo instrucao explicita diferente:

1. regra especifica declarada no guia mestre do projeto;
2. pasta oficial indicada pelo usuario;
3. estrutura de subpastas ja existente na fonte oficial;
4. Obsidian como painel rapido e memoria interna;
5. workspace local como rascunho temporario ou evidencia tecnica.

Nunca inferir que sincronizacao local com OneDrive equivale a criacao no Google Drive. Sao superfícies diferentes e devem ser verificadas separadamente.

## Gate antes de criar

Confirmar, por contexto ou descoberta:

- qual e a fonte oficial;
- qual e a pasta raiz do projeto;
- qual subpasta corresponde ao tipo do entregavel;
- se ja existe um documento equivalente que deve ser atualizado em vez de duplicado;
- se o documento e interno, compartilhavel com cliente ou publico.

Se o usuario ja forneceu essas respostas ou o guia mestre as define, nao perguntar novamente.

## Regras de escrita

- Documentos para cliente, checklists, relatorios, demandas criativas e handoffs devem nascer ou terminar na fonte oficial do projeto.
- Quando um rascunho local ou nota Obsidian ja existir, converter ou copiar o conteudo para o artefato oficial e adicionar no indice interno apenas o link oficial.
- Nao devolver apenas caminho local quando o usuario pediu centralizacao no Drive.
- Preservar organizacao, compartilhamento e nomenclatura existentes.
- Nao criar duplicata se o arquivo oficial ja existir; atualizar o documento correto.
- Nao mover, apagar ou compartilhar arquivos externamente sem autorizacao quando a operacao alterar acesso ou remover um local valido.

## Fechamento obrigatorio

Uma entrega oficial so pode ser declarada concluida quando houver evidencia de:

- arquivo criado ou atualizado;
- pasta pai correta;
- conteudo presente;
- link oficial observado na resposta da ferramenta ou na leitura de metadados;
- indice interno atualizado, quando aplicavel;
- nenhuma copia temporaria apresentada como fonte oficial.

## Playbook

Para o procedimento completo, usar [drive-source-of-truth-playbook.md](references/drive-source-of-truth-playbook.md).

