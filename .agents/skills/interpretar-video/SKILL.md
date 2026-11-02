---
name: interpretar-video
description: "Interpretar o CONTEUDO de um arquivo de video ou audio local (o que aparece nas telas e/ou o que e falado), ja que o modelo nao \"assiste\" video nem \"ouve\" audio direto. Faz duas coisas com ffmpeg + Whisper (transcricao local da OpenAI): (1) extrai FRAMES do video em imagens pra o modelo LER as telas/cliques; (2) extrai o AUDIO e transcreve com Whisper pra o modelo LER a narracao. Use SEMPRE que o usuario mandar um video/audio (.mp4 .mov .mkv .webm .m4a .mp3 .ogg .wav) e pedir pra \"ver\", \"assistir\", \"interpretar\", \"entender\", \"transcrever\", \"resumir\", \"o que ele fala/mostra\", \"documentar o processo do video\", \"transformar o video em passo a passo\", ou anexar um arquivo de midia esperando que o modelo entenda o conteudo. Tambem quando um processo/tutorial chega como screencast (gravacao de tela) e precisa virar manual. NAO use pra criar/editar video (isso e videomaker) nem pra baixar video da web (isso e firecrawl/yt)."
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

# Interpretar video / audio local (ffmpeg + Whisper)

O modelo NAO abre um `.mp4`/`.mp3` e "entende". O truque: **quebrar a midia em coisas que o modelo
LE** — imagens (frames) e texto (transcricao). Esta skill tem os comandos prontos, validados no
Windows do usuario (ffmpeg 8.x + openai-whisper 20250625 ja instalados; Python `py -3`).

## Regra de decisao (o que extrair)

Antes de tudo, veja se a midia tem AUDIO e/ou VIDEO — isso decide o caminho:

```bash
ffprobe -v error -show_entries stream=index,codec_type,codec_name,width,height -of default=nw=1 "ARQUIVO"
```

- So `codec_type=video`, sem audio -> **gravacao de tela muda**. So extrair frames e LER.
- So `codec_type=audio` (ou .mp3/.m4a) -> **so transcrever** com Whisper.
- Tem os dois -> **frames + transcricao** (o caminho completo; junte os dois pra entender o video).

Duracao (pra dimensionar quantos frames):
```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "ARQUIVO"
```

## 1) Extrair FRAMES (ler as telas / o que e mostrado)

Use um scratchpad, nao a pasta do usuario. 1 frame a cada N segundos:

```bash
mkdir -p "SCRATCH/frames"
ffmpeg -y -i "ARQUIVO" -vf "fps=1/2,scale=1200:-1" -q:v 4 "SCRATCH/frames/f_%02d.jpg" -loglevel error
```

- `fps=1/2` = 1 frame a cada 2s (bom p/ screencast de processo). Video curto e cheio de cliques:
  use `fps=1/1.5`. Video longo/estatico: `fps=1/4` ou `1/5` pra nao gerar frames demais.
- `scale=1200:-1` = largura 1200px (legivel, arquivo leve). Nao passar de ~1400 (custo de leitura).
- `-q:v 4` = qualidade JPEG boa. Numeros DUPLO digito no nome (`%02d`) pra ordenar certo.

Depois LEIA os frames com a ferramenta Read (varios de uma vez, em ordem). Estrategia esperta:
leia primeiro os SALTEADOS (f_01, f_04, f_07, f_10...) pra pegar a sequencia geral, e so entao
os intermediarios das partes que importam. Reconstrua a acao quadro a quadro (qual tela, o que foi
digitado/clicado, o que mudou entre um frame e o outro).

Se precisar de um instante EXATO (ex.: pegar o segundo 12.5 nitido):
```bash
ffmpeg -y -ss 12.5 -i "ARQUIVO" -frames:v 1 -q:v 2 "SCRATCH/frame_12s.jpg" -loglevel error
```

## 2) Transcrever AUDIO (ler o que e falado) — Whisper

Extrai o audio em WAV 16kHz mono (formato que o Whisper gosta) e transcreve em PT-BR:

```bash
ffmpeg -y -i "ARQUIVO" -vn -ac 1 -ar 16000 "SCRATCH/audio.wav" -loglevel error
py -3 -m whisper "SCRATCH/audio.wav" --language Portuguese --model small --output_format txt --output_dir "SCRATCH" --fp16 False
```

- Modelos por custo/qualidade: `tiny` (rapido, ruim) < `base` < `small` (bom equilibrio, PADRAO) <
  `medium` (melhor, mais lento) < `large` (top, pesado). Audio ruim/sotaque forte -> suba pra `medium`.
- `--fp16 False` evita o warning de FP16 em CPU. Saida vai em `SCRATCH/audio.txt` — LEIA com Read.
- Formatos com timestamp: `--output_format srt` (util pra casar fala com o frame daquele minuto).
- Primeira execucao baixa o modelo (~460MB no `small`); depois fica em cache.

Alternativa mais rapida (se instalada): `faster-whisper` (mesmos modelos, 3-4x mais rapido).
Instalar so se o Whisper padrao estiver lento demais: `py -3 -m pip install faster-whisper`.

## 3) Sintetizar

Junte os dois: a transcricao diz O QUE a pessoa explica; os frames mostram ONDE ela clica. Entregue
o resultado no formato que o usuario pediu (resumo, passo a passo, manual). Se for virar manual com
telas, os frames-chave ja servem de print (ver skill de montar PDF, se houver). SEMPRE cite o que
viu na fonte (VBA): "no frame f_07 ele preenche o CFOP", nao "acho que ele preenche".

## Pegadinhas (validadas em producao 08/07/2026)

- **Video de tela do WhatsApp costuma vir SEM audio** (so `codec_type=video`). Rode o `ffprobe` de
  streams ANTES — se tentar extrair audio de um video mudo, o ffmpeg da "Output file does not
  contain any stream". Nesse caso e so frames.
- **Nao jogar frames/audio na pasta do usuario** — usar o scratchpad da sessao.
- **Nome dos frames com `%02d`/`%03d`** senao `f_10` vem antes de `f_2` na ordem alfabetica.
- **ffmpeg e Whisper JA estao instalados** no PC do usuario (ffmpeg no PATH; `py -3 -m whisper`). Se
  faltar em outra maquina: ffmpeg via winget/gyan.dev; `py -3 -m pip install openai-whisper`.
- Windows: os comandos rodam no Bash tool (Git Bash). Caminho com espaco -> sempre entre aspas.

