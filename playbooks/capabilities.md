# Capacidades e cobertura integral

A entrega inclui as 193 pastas de origem, sem curadoria reduzida a 29.
Os 29 metodos publicos anteriores sao preservados; a uniao contem mais de
193 skills por incluir metodos publicos sem pasta equivalente na origem.

## Evidencia

O [indice compacto](../docs/skill-index.json) e a entrada para descoberta por
metadados. O catalogo completo abaixo e evidencia de CI/QA, nao carga automatica
de contexto em WORK. Abra somente os procedimentos pertinentes.

- [Catalogo consolidado](../docs/exports/catalog.json): cada origem, destino,
  status, motivo, arquivos e hashes, dependencias, direitos e corpo portado.
- [Contrato do export](../docs/EXPORT_CONTRACT.md): normalizacao A/B, verificacao
  anti-stub e limites da evidencia.
- [Matriz](../.codex/skill-routing.json): especialidades dos 34 papeis, geradas
  dos frontmatters reais; catalogo declarativo, nao runtime de execucao.

`ported_full` significa transporte do procedimento e recursos disponiveis;
`adapted_private_config` informa sanitizacao ou adaptacao portavel. Nenhum
status implica integracao, credencial, servico ou helper executado.
Omissao de arquivo exige motivo individual concreto, nunca "fora do escopo"
ou mera ausencia de licenca. Dependencia nao embarcada exige contrato e bloqueia
apenas a acao que depende dela. Código Python/JSON invalido falha no gate.

## Ambiente e direitos

WORK/cloud pode oferecer workspace executavel sem acesso ao computador local.
Sem filesystem, conectores/APIs podem carregar conteudo sob demanda, mas nao
demonstram instalacao global nem persistencia. Ver o
[prompt por capacidades](../PROMPT_INSTALACAO.md).

Conteudo fornecido foi autorizado para exportacao. Isso nao inventa licenca
permissiva de terceiros nem apaga restricoes reais. Avisos originais permanecem
sob seus termos; veja [direitos e avisos](../docs/THIRD_PARTY_NOTICES.md).
MIT da raiz e limitada ao codigo/documentacao originais do modelo.

As regras raiz prevalecem sobre procedimentos legados: sem TTL de consentimento,
replicacao automatica de runtimes, ativacao de hooks, acesso a servidor ou nova
permissao externa. Toqi/JEV, memoria remota, browsers, LLMs, APIs e servicos sao
dependencias opcionais, nao instaladas nem autorizadas por este pacote.
