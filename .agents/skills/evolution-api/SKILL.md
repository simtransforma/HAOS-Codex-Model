---
name: evolution-api
description: "Procedimento especializado de evolution-api; consultar requisitos e evidencias antes de executar."
---

# Evolution API (WhatsApp do grupo, Hetzner)

Como mandar mensagem, disparar alerta e operar instâncias de WhatsApp pela Evolution API da casa, sem errar o número de alerta nem o header de auth. INTERNA: cita infra, container, instância e número reais. NÃO vai pro repo público HAOS_CC.

> Antes de qualquer operação no servidor (restart, troubleshooting de container), carregue a skill `haos-hetzner-map`. Esta skill cobre o USO da API, não a manutenção do daemon Docker.

---

## Arquitetura

- A Evolution API é a **camada de WhatsApp de todo o grupo** (SIM / ${USER_BRAND} / HAU / Editora). Toda mensagem ou alerta de WhatsApp do HAOS passa por aqui.
- Roda no **Hetzner** (`example.invalid`) em dois containers Docker:
  - `evolution`: a API REST em si (o que você chama).
  - `evolution-manager`: painel web de gestão das instâncias (parear QR code, ver status, criar/apagar instância pela UI).
- Exposta via Traefik em `https://service.example.invalid` (base pública da API). Só 22/80/443 são públicas no servidor; a porta interna do container é loopback/rede Docker.
- Banco próprio no Postgres do Hetzner: `evolution` (entra no backup geral diário). O monitor `wa-monitor` (container + DB `wa_monitor`) consome a MESMA instância para notificar eventos de Meta Ads.
- Multi-instance: já roda com mais de um número possível. Cada número conectado é uma **instância** nomeada.

---

## Autenticar

- **Base URL:** variável `EVOLUTION_API_URL` do MASTER.env (resolve para `https://service.example.invalid`). NUNCA hardcode.
- **API Key (global):** header `apikey: <chave>`. A chave fica no MASTER.env. **TODO a confirmar ao vivo:** ler o nome exato da variável `EVOLUTION_*` no MASTER.env (o nome usado nas memórias é genérico "API Key"; confirmar se é `EVOLUTION_API_KEY` antes de scriptar). NUNCA imprimir a chave em resposta, log ou commit.

```bash
# Carregar credenciais (não ecoar o conteúdo)
set -a && source "${HAOS_PRIVATE_ROOT}" && set +a

# Smoke test: a API responde?
curl -s "$EVOLUTION_API_URL/" -H "apikey: $EVOLUTION_API_KEY"
```

> A apikey global do header dá acesso a todas as instâncias. Toda chamada de instância leva a apikey no header; a instância vai no **path** (`/{instancia}`), não no corpo.

---

## Instâncias

- **TODO a confirmar ao vivo:** o nome da instância tem espaço e pode ter sido renomeado. Antes de scriptar um envio, liste as instâncias (abaixo) e copie o `instanceName` exato. Não chute. Na URL, o nome com espaços precisa de URL-encoding (`%20`).

```bash
# Listar instâncias e ver status de conexão de cada uma
curl -s "$EVOLUTION_API_URL/instance/fetchInstances" \
     -H "apikey: $EVOLUTION_API_KEY" | jq '.[] | {name: .name, status: .connectionStatus}'
```

> Os nomes de campo (`name`/`instanceName`, `connectionStatus`/`state`) variam entre versões da Evolution (v1 x v2). Se o `jq` vier vazio, rode sem filtro (`| jq .`) e leia o shape real antes de seguir. Marcar como verificação ao vivo, não assumir o schema.

### Status de uma instância (está conectada?)

```bash
curl -s "$EVOLUTION_API_URL/instance/connectionState/$(jq -rn --arg s "$INST" '$s|@uri')" \
     -H "apikey: $EVOLUTION_API_KEY" | jq .
```

Estado esperado de número saudável: `open` (conectado). `connecting`/`close` = caiu o pareamento, precisa reparear pelo QR no `evolution-manager`.


Conectar um número novo é ação que pareia um WhatsApp real (QR code) e pode afetar a sessão de outro número. Prefira fazer pelo painel `evolution-manager`. Por API:

```bash
curl -s -X POST "$EVOLUTION_API_URL/instance/create" \
  -H "apikey: $EVOLUTION_API_KEY" -H "Content-Type: application/json" \
  -d '{"instanceName":"NomeNovo","qrcode":true,"integration":"WHATSAPP-BAILEYS"}' | jq .
```

> NÃO recriar nem deletar a instância existente para "resetar". Recriar perde o login do número. Reparear sempre pelo QR, sem destruir a instância. Restart de container do WhatsApp em sequência derruba a sessão (regra do `haos-hetzner-map`).

---

## Enviar mensagem de texto

Endpoint canônico da Evolution v2: `POST /message/sendText/{instancia}`.

```bash
curl -s -X POST "$EVOLUTION_API_URL/message/sendText/$(jq -rn --arg s "$INST" '$s|@uri')" \
  -H "apikey: $EVOLUTION_API_KEY" -H "Content-Type: application/json" \
  -d '{
        "number": "${RESOURCE_ID}",
        "text": "Mensagem de teste do HAOS."
      }' | jq '{status: .status, id: .key.id}'
```

- `number`: telefone em formato internacional **sem** `+`, `(`, `)`, espaço ou hífen. BR = `55` + DDD + número (ex: `${RESOURCE_ID}`). Para grupo, usa o JID do grupo (`contact@example.invalid`).
- `text`: o corpo da mensagem.
- Alguns deploys aninham os campos sob `textMessage` (v1) em vez de planos (v2). Se der `400`, é provável diferença de versão: testar o formato alternativo `{"number":"...","textMessage":{"text":"..."}}` antes de desistir.

### Código copiável: separar contexto e payload

Quando o destinatário precisar copiar e colar um código técnico — por exemplo, PIX Copia e Cola, token temporário, protocolo ou código de ativação — não misture o código com explicações, assinatura ou Markdown.

Use esta sequência:

1. mensagem de contexto: finalidade, referência e orientação curta; aplicar a assinatura institucional quando ela fizer parte do padrão do agente;
2. mensagem de payload: somente o código exato, sem rótulo, aspas, crase, assinatura, emoji ou quebra de linha extra;
3. para vários códigos, repetir `contexto -> payload` na ordem pedida, com pequeno intervalo entre os envios;
4. antes do envio, validar o payload pelo mecanismo adequado ao formato. Para BR Code/PIX, validar estrutura EMV e CRC16; não reconstruir nem corrigir manualmente um código inválido;
5. preservar o código somente em memória de execução. Não gravar o payload real em skill, memória, journal, log público ou commit.


### Evidência em três níveis

Não confunda aceitação da API com entrega no WhatsApp:

| Nível | Evidência | O que prova |
|---|---|---|
| fila | resposta HTTP bem-sucedida e `key.id` | a Evolution aceitou a requisição |
| entrega | `DELIVERY_ACK` ou ACK equivalente da versão ativa | o WhatsApp entregou ao destinatário |
| leitura | `READ` ou ACK equivalente | o destinatário abriu/leu quando o recurso está disponível |

`SERVER_ACK`, `PENDING`, HTTP `200/201` ou apenas `key.id` não provam entrega. Depois do envio, consultar o estado pelo ID da mensagem na fonte viva e reportar o maior nível comprovado. Se a consulta de ACK não estiver disponível, declarar somente `aceito pela API`, nunca `entregue`.

### Outros tipos (referência rápida)

| Ação | Endpoint |
|---|---|
| Texto | `POST /message/sendText/{instancia}` |
| Mídia (imagem/doc/vídeo) | `POST /message/sendMedia/{instancia}` |
| Áudio (PTT) | `POST /message/sendWhatsAppAudio/{instancia}` |
| Botões/lista | `POST /message/sendButtons/{instancia}` (depende da versão) |

---

## Número de alerta (NÃO errar)


### Disparar um alerta (1 chamada)

```bash
ALERT_TO="${RESOURCE_ID}"
MSG="[HAOS] $(date '+%d/%m %H:%M'): <descrição curta do alerta>"

curl -s -X POST "$EVOLUTION_API_URL/message/sendText/$(jq -rn --arg s "$INST" '$s|@uri')" \
  -H "apikey: $EVOLUTION_API_KEY" -H "Content-Type: application/json" \
  -d "$(jq -nc --arg n "$ALERT_TO" --arg t "$MSG" '{number:$n, text:$t}')" \
  | jq '{ok: (.status // .key.id != null)}'
```

---

## Integração com n8n

- A Evolution é a camada de WhatsApp dos workflows n8n da casa. O n8n bate na mesma base (`evo.${USER_BRAND}.com.br`) por HTTP Request node, com o header `apikey`.
- Existe um nó/credencial Evolution dedicado em alguns workflows; em outros é HTTP Request cru. Para criar/editar esses fluxos, combinar com a skill `haos-n8n-api` (pegadinhas de credencial e do HTTP Request node estão lá).
- `wa-monitor` (container próprio) já usa esta instância para notificar eventos de Meta Ads. Não conflitar: é o mesmo número.

> SendFlow é OUTRA API de WhatsApp do grupo (Bearer token, `sendflow.pro`), usada para disparo em massa de campanha. Para ALERTA operacional e mensagem transacional, o padrão é a Evolution. Não confundir.

---

## Regras de segurança

- Nunca expor a apikey em resposta, log, commit ou screenshot.
- Não recriar/deletar instância para "resetar" (perde o login do número).
- Não reiniciar o container de WhatsApp em sequência (derruba a sessão pareada).

---

## Saída esperada

Conforme a tarefa, a skill entrega uma destas, sempre com evidência verificável (AGENTS.md §13):

- **Envio/alerta:** a resposta da API com `key.id` ou `status` da mensagem (prova de que entrou na fila), mais o número e a instância usados. Para alerta, confirmar que o destino foi `${RESOURCE_ID}`.
- **Entrega:** ACK consultado na fonte viva. Só usar `entregue` com `DELIVERY_ACK` (ou equivalente comprovado na versão ativa) e `lido` com `READ`; sem ACK, reportar apenas `aceito pela API`.
- **Status:** o `connectionState` de cada instância consultada (`open` = saudável).
- **Listagem:** os `instanceName` reais com seu status de conexão.

Nunca declarar "mensagem entregue" apenas com a resposta da API. `200/201` com `key.id` prova entrada na fila; `400`/`401`/`404` = parar e diagnosticar (auth, nome de instância, formato do payload), não reportar sucesso.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
