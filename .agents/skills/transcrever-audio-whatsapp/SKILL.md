---
name: transcrever-audio-whatsapp
description: "Transcrever em massa os audios (mensagens de voz / PTT) de uma conversa de WhatsApp e montar a leitura cronologica do que foi conversado, usando Evolution API para baixar a midia e Whisper LOCAL para transcrever (custo ZERO, nada sai da maquina). Use quando o usuario pedir \"transcreve os audios da conversa\", \"o que o fulano falou no audio\", \"le a conversa do whatsapp com fulano\", \"entende o que foi combinado nesses audios\", \"me resume os audios do grupo X\". LEITURA APENAS: esta skill nunca responde nem envia mensagem. Validada em producao 01/08/2026 com 85 audios transcritos (77 numa conversa + 8 em outra)."
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

# Transcrever audios de conversa de WhatsApp (Evolution API + Whisper local)

O modelo nao "ouve" audio. Para entender o que foi combinado numa conversa cheia de mensagem de
voz, e preciso baixar cada audio e transcrever. Este e o procedimento validado, com custo **zero**
(Whisper roda local, nao ha chamada de API paga).

## (a) Quando usar

Gatilhos na linguagem do usuario:
- "transcreve os audios da conversa com o fulano"
- "o que o fulano falou no audio"
- "le a conversa do whatsapp com fulano"
- "entende o que foi combinado nesses audios"
- "me resume o que rolou nesse grupo, tem varios audios"
- "puxa o historico dessa conversa e me diz o que ficou definido"

Skills vizinhas (nao confundir):
- `interpretar-video` -> arquivo local de video/audio ja em disco (frames + Whisper). Use aquela se
  o arquivo ja esta na maquina e nao ha WhatsApp no meio.
- `evolution-api` -> referencia geral dos endpoints da Evolution. Use como fonte dos endpoints.
- Esta skill aqui e o **fluxo ponta a ponta**: achar o chat, puxar o historico, baixar N audios,
  transcrever e montar a leitura cronologica.

## (b) Pre-requisitos

| Item | Como verificar |
|---|---|
| Evolution API no ar | `GET {EVOLUTION_API_URL}/instance/fetchInstances` responde 200 |
| Instancia do WhatsApp **conectada** | estado `open` na resposta acima |
| Whisper local instalado | `py -3 -m whisper --help` (modelo `medium` foi suficiente) |
| ffmpeg no PATH | `ffmpeg -version` (o Whisper usa) |
| Python 3 | `py -3 --version` |

**Credenciais (por NOME de variavel do ${USER_SECRET_FILE}, nunca o valor):**
- `EVOLUTION_API_URL`
- `EVOLUTION_API_KEY` (header `apikey`)
- nome da instancia usado nas rotas

> Credencial de Evolution e **por instancia**. Se der 401 numa instancia e 200 noutra, e isso.

## (c) Passo a passo (comandos reais)

### Passo 0 - Carregar credencial SEM vazar em log

**NUNCA use `source` no ${USER_SECRET_FILE} em bash.** Ja vazou linha de credencial em log de sessao.
Parser Python silencioso:

```python
# load_env.py
import os, re, pathlib
P = pathlib.Path(r"${USER_WORKSPACE_ROOT}")
ENV = {}
for line in P.read_text(encoding="utf-8", errors="ignore").splitlines():
    m = re.match(r'^\s*([A-Z0-9_]+)\s*=\s*(.*)$', line)
    if m:
        ENV[m.group(1)] = m.group(2).strip().strip('"').strip("'")
BASE = ENV["EVOLUTION_API_URL"].rstrip("/")
KEY  = ENV["EVOLUTION_API_KEY"]
INST = "<nome-da-instancia>"
# NUNCA print(KEY). Nem em debug.
```

### Passo 1 - Achar o chat: CHECAR OS DOIS JIDs

🔴 **Pegadinha numero 1 da skill.** O mesmo contato pode existir com **dois** identificadores:
- `user-000046@account.example.invalid` (o telefone)
- `NNNNNNNNNNNN@lid` (identificador interno novo do WhatsApp)

**A conversa VIVA costuma estar no `@lid`, enquanto o chat do telefone esta morto (vazio ou so
mensagem antiga).** Quem checa so o telefone conclui errado que "nao tem audio nenhum".

```python
import json, urllib.request
def post(path, body):
    req = urllib.request.Request(f"{BASE}{path}", method="POST",
        data=json.dumps(body).encode(),
        headers={"apikey": KEY, "Content-Type": "application/json",
                 "User-Agent": "HAOS/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=120))

chats = post(f"/chat/findChats/{INST}", {})
alvo = "9999"  # pedaco do numero ou do nome
for c in (chats if isinstance(chats, list) else chats.get("data", [])):
    jid = c.get("remoteJid") or c.get("id") or ""
    if alvo in jid or alvo in str(c.get("pushName", "")):
        print(jid, "|", c.get("pushName"))
```

Anote **os dois** JIDs que aparecerem e siga com os dois no passo 2. So descarte um depois de ver
que ele nao tem mensagem.

### Passo 2 - Puxar o historico

```python
msgs = post(f"/chat/findMessages/{INST}", {
    "where": {"key": {"remoteJid": JID}},
    "limit": 1000
})
lista = msgs.get("messages", {}).get("records", msgs if isinstance(msgs, list) else [])
audios = [m for m in lista if "audioMessage" in (m.get("message") or {})]
print(f"total mensagens: {len(lista)} | audios: {len(audios)}")
```

**Guarde `len(audios)` agora.** Esse e o denominador da verificacao final.

### Passo 3 - Baixar a midia de cada audio

```python
import base64, pathlib, time
OUT = pathlib.Path("scratch/audios"); OUT.mkdir(parents=True, exist_ok=True)
falhas = []
for i, m in enumerate(sorted(audios, key=lambda x: x.get("messageTimestamp", 0)), 1):
    mid = m["key"]["id"]
    dest = OUT / f"{i:03d}_{mid}.ogg"
    if dest.exists():
        continue
    try:
        r = post(f"/chat/getBase64FromMediaMessage/{INST}",
                 {"message": {"key": m["key"]}, "convertToMp4": False})
        dest.write_bytes(base64.b64decode(r["base64"]))
    except Exception as e:
        falhas.append((i, mid, str(e)[:160]))
    time.sleep(0.4)
print("baixados:", len(list(OUT.glob('*.ogg'))), "| falhas:", len(falhas))
for f in falhas: print("FALHA", f)
```

### Passo 4 - Transcrever com Whisper LOCAL (custo zero)

```bash
py -3 -m whisper "scratch/audios/001_XXXX.ogg" \
  --language Portuguese --model medium \
  --output_format txt --output_dir "scratch/transcricoes" --fp16 False
```

Em lote:

```bash
for f in scratch/audios/*.ogg; do
  py -3 -m whisper "$f" --language Portuguese --model medium \
     --output_format txt --output_dir scratch/transcricoes --fp16 False
done
```

`medium` foi suficiente nos 85 audios. `small` erra mais nome proprio; `large` demora muito sem
ganho relevante para conversa de negocio em PT-BR.

### Passo 5 - Montar a leitura cronologica

Ordene por `messageTimestamp`, converta para **BRT (UTC-3)** e identifique o autor por
`key.fromMe` (true = usuario/nos, false = o contato). Formato de entrega:

```
[01/08 09:14 BRT] Fulano: <transcricao>
[01/08 09:16 BRT] usuario: <transcricao>
[01/08 09:31 BRT] Fulano: [AUDIO NAO TRANSCRITO - midia expirada no servidor do WhatsApp]
```

Texto digitado (`conversation` / `extendedTextMessage.text`) entra na mesma linha do tempo, senao a
conversa fica sem sentido.

## (d) Verificacao com evidencia

Antes de entregar, declarar os tres numeros:

```
Audios na conversa .....: N   (contagem do passo 2)
Audios transcritos .....: M   (arquivos .txt gerados)
Audios que falharam ....: N-M (lista com id e motivo)
```

```bash
ls scratch/audios/*.ogg | wc -l
ls scratch/transcricoes/*.txt | wc -l
```

**Se `M < N`, a entrega DIZ isso explicitamente**, com a lista de quais falharam e por que.
Entregar transcricao "completa" sem bater a contagem e declaracao falsa.

Referencia de escala validada: **85 audios** (77 numa conversa + 8 em outra), 01/08/2026, custo R$ <USER_AMOUNT>## (e) Pegadinhas e anti-padroes

1. 🔴 **`@lid` vs telefone.** Ja explicado no passo 1. Checar SEMPRE os dois JIDs. "Nao achei audio"
   olhando um JID so nao e "nao tem audio".
2. 🔴 **Midia antiga EXPIRA no servidor do WhatsApp.** `getBase64FromMediaMessage` devolve
   `400 Failed to fetch stream`. Nao ha conserto pelo lado da API: o arquivo nao existe mais no CDN
   do WhatsApp. **NUNCA preencher audio nao transcrito com suposicao ou com "provavelmente ele
   falou sobre X".** Declarar qual falhou e por que. Inventar conteudo de audio e o pior erro
   possivel nesta skill, porque a transcricao vira base de decisao.
3. **Whisper erra nomes proprios do nosso contexto.** Corrigir manualmente no texto final:
   | Whisper escreve | Correto |
   |---|---|
   | "Triga do Dinheiro" | **Trilha do Dinheiro** |
   | "Jean" / "Jan" | **usuario** |
   | "Laira" | **Layra** |
   | "Graboide" / "Grabovói" | **Grabovoi** |
   Passar um dicionario de substituicao no fim, e revisar nomes novos que aparecerem.
4. 🔴 **NUNCA use `source` no ${USER_SECRET_FILE} em bash.** Ja vazou linha de credencial em log de sessao.
   Usar o parser Python silencioso do passo 0. E nunca `print` de chave, nem em debug.
5. **Gravacao de reuniao (Zoom e afins) pode vir contaminada.** Ja apareceu audio de TV alheio no
   fim do arquivo, que o Whisper transcreve como se fosse a reuniao. **Cortar na despedida** ("entao
   e isso, valeu, ate mais") e descartar o resto.
6. **Nao transcreva com API paga.** Whisper local resolve e custa zero. API de audio so com OK
   nominal do usuario (regra de API paga).
7. **`sleep` entre downloads.** Rajada de `getBase64FromMediaMessage` na Evolution derruba a
   sessao. 0,3 a 0,5s entre chamadas.
8. **Audio de grupo tem varios autores.** Usar `key.participant` (nao `remoteJid`) para saber quem
   falou. Sem isso a transcricao atribui tudo ao grupo.

## (f) Rollback

**Nao ha passo destrutivo.** A skill e **LEITURA APENAS**:
- nunca responde, nunca envia mensagem, nunca marca como lida, nunca apaga nada;
- o unico efeito colateral e arquivo em `scratch/` (audios `.ogg` e `.txt`).

"Rollback" = apagar a pasta de scratch:

```bash
rm -rf scratch/audios scratch/transcricoes
```

Os `.ogg` contem conversa privada. **Apagar o scratch ao terminar** e nunca commitar essa pasta.

## Creditos

usuario Marco Menegussi Scaglianti.


## Adaptacao Codex HAOS

- Carregar `${USER_WORKSPACE_ROOT}` e o bootstrap HAOS antes de operar.
- Tratar nomes de ferramentas exclusivos do Claude como intencao; usar a ferramenta equivalente disponivel no Codex.
- Usar `/haos:*` para roteamento visual; `@` permanece reservado a plugins e mencoes do Codex.
- Nao executar push, deploy, publicacao, mensagem, gasto, servidor ou infraestrutura externa sem OK explicito do usuario.
- Nunca ler ou registrar segredos fora da necessidade estrita da tarefa.
