---
name: active-prospecting
description: "Pesquisa, qualifica e adiciona novas contas B2B a uma base comercial. Use para crescer uma lista de prospecção, montar uma lista de empresas ou instituições por ICP e região, enriquecer dados públicos, identificar canais de contato institucionais, pontuar leads e registrar fontes e datas sem inventar dados ou disparar mensagens."
---

# Prospecção ativa

Encontre contas novas com evidência pública, priorize as que cabem no ICP e entregue uma fila comercial pronta para abordagem humana.

## Fluxo obrigatório

1. Defina oferta, ICP, região, categoria, volume e critério de prioridade. Se o pedido usar uma base existente, derive a hipótese do cabeçalho e das melhores contas; declare a hipótese antes de escrever.
2. Faça backup e leia o esquema, as chaves de deduplicação, as validações e a lista de não contato antes da coleta.
3. Pesquise fontes em camadas: diretórios e associações setoriais, sites oficiais, páginas institucionais e, por último, perfis públicos como pista.
4. Para cada candidato, confirme nome, categoria, cidade/UF e URL oficial. Procure apenas e-mail, telefone e formulário que estejam expostos publicamente pela organização.
5. Compare com a base por e-mail, telefone, domínio e nome normalizado. Mescle somente por chave forte; encaminhe semelhanças para revisão.
6. Registre sempre fonte, data de coleta, status de validação, score, prioridade e próxima ação.
7. Insira somente os registros com identidade suficiente na base ativa; envie os de evidência fraca para revisão.
8. Releia as células gravadas e valide filtros, tabela, listas suspensas, fórmulas e clipping.

## Pontuação

Use `references/playbook.md` para critérios e score. Como padrão:

- `A — alta`: ICP forte, fonte oficial e canal público pronto ou conta estratégica;
- `B — média`: ICP confirmado e fonte oficial, mas canal ainda a completar;
- `C — baixa`: fit parcial ou pouca acionabilidade;
- `D — revisar/arquivar`: identidade ou evidência insuficiente.

## Regras de dados

- Não invente e-mail, telefone, decisor, cidade, porte ou relação comercial.
- Não trate domínio ativo como caixa de e-mail validada.
- Não faça coleta de dados privados, login, contorno de bloqueio ou disparo automático.
- Respeite opt-out, `Não contatar` e LGPD; use dados institucionais e públicos.
- Preserve origem, URL da fonte e data da verificação.

## Entrega

Em uma planilha existente, reutilize as colunas e validações já aprovadas. Para cada lote, registre no log: fonte, filtro aplicado, candidatos coletados, duplicados removidos, registros incluídos, pendências e data.

Leia [references/playbook.md](references/playbook.md) antes de pesquisar ou criar um lote novo.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
