# Runbook por destino

Comandos exatos para replicar em cada um dos 8 destinos. Carregar `haos-hetzner-map` antes. Confirmar caminhos ao vivo na primeira execução (ver checklist do SKILL.md). Credenciais sempre por nome de variável ou caminho, nunca valor.

SSH base (do AGENTS.md):
```
ssh -i "<.../_secrets/ssh/hetzner_ed25519>" -o StrictHostKeyChecking=no root@example.invalid
```

---

## Destino 1: Claude Code LOCAL (Windows) = a ORIGEM

Para recurso PÚBLICO, edite na fonte da verdade e versione:
```
git add -A
git commit -m "feat: <descricao>"
git push
```
Para uso local imediato, a skill também pode ser copiada para `${HAOS_PRIVATE_ROOT}`.
Recurso INTERNO: NÃO vai pro HAOS_CC. Fica em `${HAOS_PRIVATE_ROOT}` e é copiado por SSH (ver seção INTERNOS).

## Destino 2: ${HAOS_PRIVATE_ROOT} (clone Hetzner, pull-only)

```
cd ${HAOS_PRIVATE_ROOT} && git pull --ff-only
```
Confirma com `git log -1 --oneline`. NUNCA `git push` ou editar aqui.

## Destino 3: Claude Code HETZNER (host)

Skills do superset chegam via plugin que aponta para `${HAOS_PRIVATE_ROOT}`. Para skills de usuário:
```
cp -r ${HAOS_PRIVATE_ROOT}<skill> ${HAOS_PRIVATE_ROOT}<skill>
```
Agentes: o roster são 29 arquivos `.md` em `${HAOS_PRIVATE_ROOT}` (formato subagent: frontmatter `name/description/tools` + SOUL), lidos via plugin `haos@hau-solucoes-digitais`. Roster PRÓPRIO do Claude Code Hetzner.
- Agente PÚBLICO: entra pelo plugin (chega via `git pull` no `${HAOS_PRIVATE_ROOT}`).
- Agente INTERNO/sensível (ex: SOUL com faturamento): NÃO vai pro `${HAOS_PRIVATE_ROOT}` público. Criar como agente nativo de usuário em `${HAOS_PRIVATE_ROOT}` (frontmatter `name/description/model` + SOUL embutido). Montar o `.md` localmente e `scp`; criar o dir antes:
```
ssh ... 'mkdir -p ${HAOS_PRIVATE_ROOT}'
scp -i "<chave>" cfo-nativo-hetzner.md root@example.invalid:${HAOS_PRIVATE_ROOT}
```
Verificar: `ls ${HAOS_PRIVATE_ROOT}<skill>` e `head ${HAOS_PRIVATE_ROOT}<nome>.md`.

## Destino 4: OpenClaw (container) = o ÚNICO do sync script

```
bash ${HAOS_PRIVATE_ROOT}
```
Lê de `${HAOS_PRIVATE_ROOT}` e entrega nas pastas do OpenClaw (`${HAOS_PRIVATE_ROOT}` e `${HAOS_PRIVATE_ROOT}`, bind-mount, on-demand, sem restart). Agentes em `${HAOS_PRIVATE_ROOT}`.
NÃO reiniciar o container em cascata. Verificar: `ls ${HAOS_PRIVATE_ROOT} | wc -l`.
TODO ao vivo: ler o script antes (`cat ${HAOS_PRIVATE_ROOT}`) para saber exatamente o que ele cobre.

## Destino 5: Codex (do OpenClaw)

É o MOTOR de LLM (vendorizado, `which codex` é vazio no host), NÃO tem roster próprio nem pasta `agents/`. Não "usa o roster do OpenClaw": o OpenClaw é quem tem o roster e invoca o Codex como backend. Recebe só SKILLS por cópia direta (o sync NÃO cobre):
```
cp -r ${HAOS_PRIVATE_ROOT}<skill> ${HAOS_PRIVATE_ROOT}<skill>
```
No container resolve como `${HAOS_PRIVATE_ROOT}`. Verificar: `ls ${HAOS_PRIVATE_ROOT}<skill>`.

## Destino 6: Hermes (CLI Python on-demand)

NÃO é container (`docker ps` vazio é normal). Home `${HAOS_PRIVATE_ROOT}`.

Skills (lê só `${HAOS_PRIVATE_ROOT}`, reindexa no boot via `.skills_prompt_snapshot.json`):
```
cp -r ${HAOS_PRIVATE_ROOT}<skill> ${HAOS_PRIVATE_ROOT}<skill>
```
Agentes = PERFIL (diretório `${HAOS_PRIVATE_ROOT}` com config.yaml + .env + SOUL.md):
```
hermes profile create <nome> --clone-from sm-social
# depois sobrescrever o SOUL:
cp ${HAOS_PRIVATE_ROOT}<nome>/SOUL.md ${HAOS_PRIVATE_ROOT}<nome>/SOUL.md
```
config.yaml fica idêntico (provider openai-codex / gpt-5.5 via OpenRouter). SOUL recarrega a cada mensagem, sem restart.
Verificar: `hermes --version`, `ls ${HAOS_PRIVATE_ROOT}<skill>`, `ls ${HAOS_PRIVATE_ROOT}<nome>`.

## Destino 7: Paperclip (container) = o MAIS complexo

Copiar pra pasta NÃO ativa. Resolução real = registry no banco. 3 passos:
```
# (a) levar o markdown da skill pro dir-fonte estável (o hash depende do path absoluto):
docker cp <skill>/ paperclip:/paperclip/company-skills/haos/<skill>/

# (b) registrar no DB rodando com tsx (node puro da ERR_MODULE_NOT_FOUND):
#     companySkillService(db).importFromSource(companyId, dir)  em /app/server
#     companyId SIM = ${RESOURCE_ID}

# (c) atribuir por agente em adapter_config.paperclipSkillSync.desiredSkills (jsonb_set)
```
Chave canônica = `local/<sha256(path absoluto)[:10]>/<slug>`, slug do `name` do frontmatter (NÃO do dir). Agente só dispara com Assignee. Curadoria de skill POR PAPEL (blanket degrada recall).
TODO ao vivo: reconfirmar companyId, nome do service e o resolver antes de repetir. Frágil e específico de versão.

## Destino opcional: sandbox privado (modelo condicional)

Se houver sandbox no escopo aprovado, confirmar seu estado ativo ou pausado, o responsavel autorizado e o runtime usado. Selecionar o metodo de entrega compativel, preservar outras skills e verificar o resultado no destino. Nao propagar conteudo para ambiente pessoal, pausado ou nao autorizado por presuncao.
---

## INTERNOS (skills com infra/segredo + SOUL completo): cópia direta SSH

Não passam pelo git. Do host (ou via `scp` da máquina local para o host, depois distribuir):
```
# do local para o host (skill interna):
scp -i "<chave>" -r "${HAOS_PRIVATE_ROOT}" root@example.invalid:${HAOS_PRIVATE_ROOT}<skill>
# (usar um diretório privado no host como staging, NÃO ${HAOS_PRIVATE_ROOT} que é o repo público)

# do host para cada runtime, mesmos caminhos das seções acima:
cp -r ${HAOS_PRIVATE_ROOT}<skill> ${HAOS_PRIVATE_ROOT}<skill>            # Claude Code Hetzner
cp -r ${HAOS_PRIVATE_ROOT}<skill> ${HAOS_PRIVATE_ROOT}<skill>        # OpenClaw
cp -r ${HAOS_PRIVATE_ROOT}<skill> ${HAOS_PRIVATE_ROOT}<skill>  # Codex
cp -r ${HAOS_PRIVATE_ROOT}<skill> ${HAOS_PRIVATE_ROOT}<skill>             # Hermes
docker cp ${HAOS_PRIVATE_ROOT}<skill> paperclip:/paperclip/company-skills/haos/<skill>/  # + registry
```
SOUL completo do agente: mesmo princípio (cópia direta para `${HAOS_PRIVATE_ROOT}` se público, ou diretório privado se o SOUL tiver algo sensível; depois perfil no Hermes, import no Paperclip).
TODO ao vivo: confirmar se existe um diretório de staging privado no host ou criar um (ex: `${HAOS_PRIVATE_ROOT}`), e garantir que ele NÃO é o repo público.

