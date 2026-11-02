# Memoria curada

Guarde aqui somente procedimentos, decisoes, incidentes e aprendizados
confirmados. Para cada registro, inclua data, fonte, escopo, evidencias e
responsavel pela aprovacao. Remova identificadores pessoais e segredos.

Sessoes brutas, dumps e arquivos de ambiente ficam fora deste repositorio.
Uma ferramenta de memoria externa so esta ativa depois de configurada e
testada no seu ambiente; nao declare sincronizacao por presuncao.

## Templates inativos

- [Schema de proveniencia](templates/provenance.schema.json).
- [Exemplo ficticio](templates/provenance.example.json).

O schema descreve somente um template: template=true, active=false,
confidence=pending e nenhum destino configurado. Identidades, observacao,
dedupe e hash ficam null no exemplo, sem fabricar prova de persistencia.
Nao e um validador de registro operacional pronto para gravacao.

Antes de persistir um item real em destino autorizado, cumprir os campos e gates
de haos-memory-provenance: origem verificavel, momento real, identidade estavel,
dedupe e readback por destino. Nao habilitar servicos para preencher o template.
Zero destinos nao e capitalizacao 0/0; exemplos nao contam como memoria salva.

O [schema de estado do Rito](../workspace/runtime/state/rito.schema.json) e seu
[exemplo inativo](../workspace/runtime/state/rito.example.json) mantem as 13 fases
not_started, gates pending, sem identidade, evidencias ou aprovacao. Copiar ou
validar esses JSON nao cria tarefa, avanca fase, instala hook ou ativa runtime.
