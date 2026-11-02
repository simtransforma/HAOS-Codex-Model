# Contrato de exportacao integral

## Inventario e formato

As 193 pastas com SKILL.md da origem autorizada sao o inventario exigido.
Lote A cobre 97 e lote B cobre 96, sem sobreposicao. Os manifests dos owners
permanecem em exports/group-a.json e exports/group-b.json. O consolidador
normaliza caminhos em string (A) e objetos com hash (B) em exports/catalog.json.

Cada entrada consolidada registra source_folder, target_path, status, reason,
source_sha256, source_file_count, files (path/sha256), dependencies, license,
omitted_artifacts e body. O inventario explicito permite detectar origem
ausente, repetida ou substituida, em vez de contar apenas 193 arquivos arbitrarios.
O catalogo e evidencia verificavel de transporte, nao prova de runtime.

Hashes dos destinos textuais usam UTF-8 com CRLF canonicalizado para LF;
binarios conservam hash de bytes. O SHA original da fonte permanece raw e nao
e confundido com o hash portavel do destino. Isso evita falso drift em checkout
Windows; .gitattributes tambem fixa LF para texto. Testes cobrem LF/CRLF.
Na conversao dos manifests legados A/B, hashes raw LF ou CRLF sao aceitos
somente se corresponderem ao mesmo conteudo textual. O catalogo consolidado
sempre grava o hash canonical LF; alteracao de conteudo continua sendo erro.

## Fidelidade e recursos

O SHA-256 original e comparado ao SKILL.md real em modo --source. Cada arquivo
portado precisa existir dentro do repositorio e corresponder ao hash gravado.
O melhor corpo portado, inclusive referencia que preserva o core publico,
precisa reter tamanho significativo e pelo menos 25% dos tokens distintos do
procedimento original. Esse limiar anti-stub e um piso, nao uma declaracao de
equivalencia semantica: QA revisa proporcoes e adaptacoes, especialmente valores
baixos. Uma referencia nominal ou bloco generico nao comprova portabilidade.

Os 29 metodos publicos anteriores continuam presentes, com gates atuais.
Quando o nome YAML original difere da pasta, o export normaliza o name publico
e registra original_name; a validacao continua exigindo name igual a pasta.
YAML seguro suporta listas, metadata, campos citados e blocos; chaves duplicadas,
aliases, anchors, tags executaveis e campos obrigatorios ambiguos sao rejeitados.

Helper ausente, arquivo externo ou dependencia privada precisa de contrato
explicito, sem afirmar que esta instalado ou operacional. Um arquivo marcado
como embarcado precisa existir dentro da raiz. Templates sanitizados nao sao
executaveis por declaracao: .py e .json continuam sujeitos ao parsing completo.
Nenhum codigo importado e executado pelo verificador.

## Comandos

Python 3.11+ e PyYAML 6.x sao necessarios; veja scripts/model-requirements.txt.
Nao instalar dependencia sem aprovacao aplicavel. Todos os comandos abaixo sao
locais; --source e obrigatorio e nunca tem caminho privado embutido.

```sh
python -B scripts/model_exports.py --source /approved/source/skills --write
python -B scripts/model_routing.py --write
python -B scripts/model_exports.py --source /approved/source/skills
python -B scripts/model_routing.py
python -B scripts/validate_model.py
python -B -m unittest discover -s tests -v
```

O comando sem --write verifica drift. O scan continua cobrindo arquivos novos,
ignorados e binarios; caches de dependencias conhecidos nao sao percorridos.
Nenhuma falha de privacidade, links, sintaxe ou identidade e silenciada pelo
fato de o arquivo ter sido importado. A analise nao le cofre, nao executa imports,
nao altera fonte e nao faz commit, push ou publicacao.
