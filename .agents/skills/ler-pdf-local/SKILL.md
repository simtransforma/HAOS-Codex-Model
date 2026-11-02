---
name: ler-pdf-local
description: "Ler o conteudo de um PDF na maquina Windows local do usuario, incluindo PDF que e IMAGEM (print de tela, scan, sem camada de texto). Use quando o usuario pedir \"le esse PDF\", \"o que diz esse PDF\", \"extrai o texto desse PDF\", \"resume esse PDF\", \"esse PDF nao abre\", \"print salvo em PDF\", \"comprovante em PDF\", \"nota fiscal em PDF\", \"documento escaneado\", ou quando a tool Read nativa falhar num PDF com erro de pdftoppm, ou quando o MCP PDF Tools (render_pdf_page) falhar com erro de canvas/napi-rs. Cobre os dois casos: PDF com texto (extracao direta e rapida) e PDF-imagem (sem texto, precisa renderizar pagina como PNG e ler visualmente). Nasceu de uma pegadinha que ja custou tempo 3 vezes nesta maquina."
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

# Ler PDF local (Windows, maquina do usuario)

Skill de infraestrutura local. Responde: "como eu leio o conteudo deste PDF
nesta maquina, sem perder tempo tentando caminhos que ja sao sabidos como
quebrados?"

## a. Quando usar

- usuario manda um PDF (ou da o caminho de um) e pede pra ler, resumir, extrair
  texto ou dado.
- O PDF e um print de tela, scan de documento, comprovante ou nota fiscal
  salvos como PDF (candidato forte a ser PDF-imagem, sem camada de texto).
- A tool `Read` nativa falhou no PDF com erro mencionando `pdftoppm`.
- O MCP PDF Tools (`render_pdf_page`) falhou com erro mencionando `canvas` ou
  `@napi-rs`.
- Duvida se o PDF tem texto selecionavel ou e so imagem: comece pelo passo 1
  desta skill, ele responde isso de forma barata.

## b. Pre-requisitos

- Python instalado na maquina local (`py` ou `python` no PATH).
- Lib `pymupdf` (pacote do modulo `fitz`). Instalar se faltar:
  ```
  py -m pip install pymupdf
  ```
  ou, se `py` nao existir no PATH:
  ```
  pip install pymupdf
  ```
  Lib gratuita e inocua (so leitura/renderizacao de PDF, sem rede).
- **ATUALIZACAO 30/07/2026:** `poppler-utils` (pdftoppm), AWS CLI e
  `tesseract` OCR foram instalados nesta maquina via winget. Isso significa
  que a partir de uma SESSAO NOVA do Claude Code (a sessao que estava aberta
  no momento da instalacao herdou o PATH antigo e nao os enxerga), a tool
  `Read` nativa volta a ser um caminho valido para PDF. Mesmo assim, PyMuPDF
  continua sendo o caminho recomendado para PDF-IMAGEM (ver secao e): e
  self-contained, nao depende de o PATH ter propagado, e ja era o caminho
  provado nesta skill. Nao e obrigatorio instalar `tesseract`/`pytesseract`
  para o fluxo padrao desta skill (Read de imagem ja resolve), mas agora
  esta disponivel como opcao para quem precisar de OCR programatico (ex.:
  extrair texto de PDF-imagem em lote, sem leitura visual turno a turno).

## c. Passo a passo

### Passo 1: tentar extrair texto primeiro (rapido)

Use o MCP PDF Tools com o caminho absoluto do arquivo:

```
mcp__PDF_Tools_-_Fill__Sign__Merge__Split__Extract__read_pdf_content
  path: "<caminho absoluto do PDF>"
```

Se o retorno vier com `text_found: true` e texto de verdade no corpo, acabou:
use esse texto direto, nao precisa de mais nada.

### Passo 2: se o texto veio vazio, o PDF e imagem

Sinal claro: `text_found: false`, ou `text_length: 0`, ou `char_count: 0`.
Isso significa que o PDF nao tem camada de texto (e um print de tela, um
scan, ou uma imagem colada num PDF). Va direto para o passo 3. NAO tente os
dois caminhos da secao e, eles estao quebrados nesta maquina.

### Passo 3: renderizar as paginas como PNG com PyMuPDF e ler com o Read

Rode um script Python que abre o PDF com `fitz` (PyMuPDF) e salva cada
pagina como PNG no scratchpad da sessao (nunca na pasta do projeto):

```python
import fitz, sys, os

pdf = sys.argv[1]       # caminho absoluto do PDF
outdir = sys.argv[2]    # pasta de scratchpad da sessao

doc = fitz.open(pdf)
base = os.path.splitext(os.path.basename(pdf))[0]
for i, page in enumerate(doc, 1):
    pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5))  # zoom ~2.5x, boa leitura
    out = os.path.join(outdir, f"{base}_p{i}.png")
    pix.save(out)
    print(out, os.path.getsize(out))
```

Rode assim (exemplo, adapte caminhos):

```
python script.py "${USER_WORKSPACE_ROOT}" "${USER_WORKSPACE_ROOT}"
```

O zoom `fitz.Matrix(2.5, 2.5)` equivale a renderizar em ~180 DPI (o PDF
nasce a 72 DPI), suficiente pra texto de print ficar legivel. Se o texto
ainda sair pequeno demais na imagem, suba o fator (3.0, 3.5).

### Passo 4: ler o PNG com a tool Read

Depois de gerado o PNG, chame a tool `Read` nativa apontando pro caminho do
PNG (nao do PDF). O Read le imagem visualmente e o conteudo do print fica
legivel, inclusive texto dentro da imagem. Se o PDF tiver varias paginas,
leia um PNG por pagina.

## d. Verificacao

- O(s) arquivo(s) PNG existem no scratchpad e tem tamanho maior que zero
  (o proprio script imprime o caminho e o tamanho em bytes; confirme com
  `ls -la` ou equivalente se quiser reforcar).
- A tool `Read` no PNG retorna o conteudo visual da pagina (texto do print
  legivel na resposta), nao um erro.
- Se o Read no PNG vier ilegivel (imagem cortada, resolucao baixa), refaca o
  passo 3 com zoom maior antes de desistir.

## e. Pegadinhas e anti-padroes (NAO fazer)

Nesta maquina, dois caminhos que PARECEM obvios para PDF-imagem ESTAVAM
QUEBRADOS quando esta skill nasceu (30/07/2026, manha) e ja custaram tempo 3
vezes antes dela existir. **ESTADO CORRIGIDO EM 30/07/2026 (tarde):**

1. **Tool `Read` nativa direto no PDF-imagem.** Falhava com erro
   `pdftoppm is not installed` (poppler-utils nao estava instalado nesta
   maquina). **CORRIGIDO:** poppler-utils foi instalado via winget na tarde
   de 30/07/2026 (`pdftoppm -v` responde v25.07.0). Se o erro
   `pdftoppm is not installed` ainda aparecer, NAO e porque a dependencia
   sumiu, e porque a sessao atual do Claude Code herdou o PATH de antes da
   instalacao (o PATH do registro do Windows ja tem o binario, mas so
   sessoes novas enxergam). Nesse caso, nao adianta insistir no Read nativo
   dentro da mesma sessao: va direto pro PyMuPDF (passo 3), que resolve na
   hora sem depender de PATH nenhum. Numa sessao nova, o Read nativo deve
   voltar a funcionar direto no PDF, inclusive PDF-imagem.
2. **MCP PDF Tools `render_pdf_page`.** Falha com erro
   `Cannot find native binding @napi-rs/canvas-win32-x64-msvc` (o binding
   nativo do canvas usado por esse plugin esta quebrado nesta maquina).
   **CONTINUA QUEBRADO**, isso nao mudou em 30/07. Nao use.

O sinal de que voce esta diante de um PDF-imagem e o `text_found: false` (ou
`text_length`/`char_count` zerado) no retorno do passo 1. Quando ver esse
sinal, va direto pro PyMuPDF (passo 3) como caminho robusto e imediato. Se
estiver numa sessao nova e quiser testar o Read nativo direto no PDF antes
(agora que poppler existe), pode funcionar, mas PyMuPDF continua sendo o
fallback garantido sem depender de PATH ter propagado. Nao insista no MCP
`render_pdf_page` (item 2), esse continua provado quebrado.

OCR (`pytesseract`/`tesseract`): ate 30/07/2026 de manha NAO estava
instalado nesta maquina. Foi instalado via winget na tarde de 30/07/2026
(`tesseract` v5.4.0), entao agora e uma opcao disponivel para quem precisar
de OCR programatico em lote. Para o fluxo padrao desta skill (ler um PDF, um
comprovante, uma nota fiscal) continua NAO sendo necessario: a tool `Read`
de imagem ja le o conteudo visual direto, sem precisar de OCR separado. So
recorra a tesseract se o caso for extracao de texto em lote sem leitura
visual turno a turno.

## f. Rollback

Nao se aplica. Esta skill e so leitura (extrair texto, renderizar PNG,
ler imagem): nao apaga, nao sobrescreve nem modifica o PDF original. O
unico artefato criado e o PNG temporario no scratchpad da sessao, que e
descartavel por natureza.

## g. Creditos

Autor: dev-backend (HAOS) para usuario Marco Menegussi Scaglianti. 30/07/2026.
Atualizado 30/07/2026 (tarde): poppler-utils, AWS CLI e tesseract instalados
via winget nesta maquina, ver secoes b e e.


## Adaptacao Codex HAOS

- Carregar `${USER_WORKSPACE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nao executar push, deploy, publicacao, mensagem, gasto, servidor ou infraestrutura externa sem OK explicito do usuario.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.
