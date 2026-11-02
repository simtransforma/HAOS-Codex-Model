---
name: openclaw-ops
description: "Use when maintaining, diagnosing, or recovering the self-hosted OpenClaw instance on the Hetzner server (container `openclaw`, 192.0.2.1) \u2014 agent stuck on \"...\", OAuth/codex auth failures (token_expired/auth_permanent), health checks, lock issues, gateway/restart, or any OpenClaw server troubleshooting. Read-only first; state changes need usuario's OK."
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

# OpenClaw Ops — Diagnóstico e Recuperação (Hetzner)

Manutenção da instância OpenClaw self-hosted (Docker, container `openclaw`,
192.0.2.1, versão 2026.5.12, modelo `openai-codex/gpt-5.5` via OAuth ChatGPT
subscription da conta user-000020@account.example.invalid).

**KB completa (Obsidian):** `OpenClaw-Hetzner-Vault/KB-OpenClaw-2026-05/00-Indice.md`
**Runbook detalhado:** `OpenClaw-Hetzner-Vault/Codex-OAuth-Relogin-Runbook.md`
**Memória de bolso:** `<USER_DEPENDENCY:withheld-artifact-7155d086af11>`

## Regras de ouro (não violar)
1. **Read-only primeiro.** Diagnosticar antes de mexer. `openclaw doctor` sem `--fix`,
   `status`, `logs`, `health`, `models auth list` são seguros.
2. **Mudança de estado = OK do usuario.** `docker restart`, `openclaw ... login`,
   `doctor --fix`, `config set`, `update`, deletar lock → confirmar antes.
3. **`/health` não é prova.** Validar sempre com turno real:
   `openclaw agent --agent main --session-id test -m "responda OK"`.
4. **`pkill -f "<padrão>"` se auto-mata** se o padrão estiver na própria cmdline
   (exit 143). Matar por PID/pidfile.
5. **Caminho no container = `${USER_SERVICE_ROOT}/resource`** (`${USER_SERVICE_ROOT}/resource` é o lado HOST).
6. SSH do Hetzner instável → comandos **curtos e individuais**.

## Acesso
```
ssh -i "${USER_WORKSPACE_ROOT}" -o StrictHostKeyChecking=no -o ConnectTimeout=15 root@192.0.2.1 "CMD"
```
No container: `docker exec openclaw bash -lc 'CMD'`.

## Passo 1 — Diagnóstico (read-only, sempre primeiro)
```
docker exec openclaw curl -s --max-time 5 http://127.0.0.1:18789/health
docker exec openclaw curl -s --max-time 5 http://127.0.0.1:37777/health   # claude-mem
docker exec openclaw bash -lc 'openclaw models auth list --agent main'
docker logs --since 5m openclaw 2>&1 | grep -iE 'token_expired|auth_permanent|file lock|401'
docker exec openclaw bash -lc 'openclaw doctor 2>&1 | tail -40'
```

## Passo 2 — Classificar a falha de auth (decisão crítica)
| Log | Cenário | Fix |
|---|---|---|
| `file lock timeout for auth-profiles.json` | **lock stale** | deletar `*.json.lock` órfão + restart (selfheal já faz isso) |
| `(401) token_expired` + `reason=auth_permanent` + `next=none` | **refresh morto** | **re-login OAuth PKCE** (Passo 3). Recriar referência do profile NÃO resolve |
| `Profiles: (none)` no `models auth list` | profile ausente | re-login OAuth PKCE (Passo 3) |

`setup-token` e `paste-token` NÃO servem para codex (OAuth). `migrate codex` não migra auth.
O `~/.codex` do codex CLI estar válido NÃO conserta o agente (stores separados).

## Passo 3 — Re-login OAuth codex (refresh morto) — requer usuario no browser
Driver pty incluído nesta skill: `codex_login_driver.py`.

```bash
# 1. Subir o driver no container
cat <skill>/codex_login_driver.py | ssh ... 'docker exec -i openclaw tee /tmp/codex_login_driver.py >/dev/null'
ssh ... 'docker exec openclaw bash -lc "setsid bash -c \"python3 /tmp/codex_login_driver.py\" >/dev/null 2>&1 &"'

# 2. Pegar a URL (esperar ~13s)
ssh ... 'docker exec openclaw bash -lc "sed -e \"s/\x1b\[[0-9;?]*[a-zA-Z]//g\" /tmp/codex_login2.out | tr -d \"\r\" | grep -aoE \"https://service.example.invalid ]*\" | head -1"'

# 3. usuario abre a URL no browser dele, conta user-000020@account.example.invalid, autoriza.
#    Cai em localhost:1455 com ERR_CONNECTION_REFUSED (NORMAL). Copia a URL INTEIRA
#    da barra como TEXTO (não print — o code vem cortado). Deve ter o mesmo &state=.

# 4. Injetar a redirect URL (heredoc evita quebra com & + .)
ssh ... 'docker exec -i openclaw bash -lc "cat > /tmp/codex_answer.txt"' <<'X'
<REDIRECT_URL_AQUI>
X

# 5. Conferir
ssh ... 'docker exec openclaw bash -lc "sed -e \"s/\x1b\[[0-9;?]*[a-zA-Z]//g\" /tmp/codex_login2.out | grep -aiE \"ANSWER SENT|Auth profile|error|EXIT\""'
#   Esperado: [DRIVER] ANSWER SENT  +  Auth profile: openai-codex:user-000021@account.example.invalid (openai-codex/oauth)
```
Cada URL tem `state`/`code_challenge` únicos atrelados ao processo VIVO. Reiniciou o
driver → gera URL nova (matar antigo por pidfile: `kill $(cat /tmp/codex_driver.pid)`).
Code OAuth expira rápido → fazer em seguida.

## Passo 4 — Aplicar e verificar (OK do usuario p/ restart)
```
docker restart openclaw && sleep 20
docker exec openclaw curl -s http://127.0.0.1:18789/health                 # {"ok":true}
docker logs --since 2m openclaw 2>&1 | grep -iE 'token_expired|401|auth_permanent'  # vazio
docker exec openclaw bash -lc 'openclaw models auth list --agent main'     # profile presente
docker exec openclaw bash -lc 'timeout 120 openclaw agent --agent main --session-id authtest -m "responda apenas: FUNCIONANDO"'
```
Só declarar resolvido com o **turno real respondendo**.

## Passo 5 — Higiene
```
docker exec openclaw bash -lc 'rm -f /tmp/codex_answer.txt /tmp/codex_login2.out /tmp/codex_login_driver.py /tmp/codex_driver.pid /tmp/codex_login.pid'
```

## Lock stale (caso mais simples)
```
docker exec openclaw bash -lc 'find ${USER_SERVICE_ROOT}/resource -name "auth-profiles.json.lock" -delete -print'
# depois (OK do usuario): docker compose -f ${USER_SERVICE_ROOT}/resource restart openclaw  (ou docker restart openclaw)
```

## Sinais de risco a vigiar (detalhe na KB → 07-Instalacao-Atual-Hetzner)
- Chave de cripto OAuth (`${USER_SERVICE_ROOT}/resource`) NÃO está nos bind-mounts → recriar container = perder profiles OAuth.
- OAuth do profile expira ~2026-05-29 (profile único, sem fallback).
- Bootstrap saturado (IDENTITY/USER/MEMORY 0 chars injetados). Worker claude-mem instável. Versão 2026.5.12 defasada.
Nenhuma mitigação dessas sem OK explícito do usuario (mexe em infra/auth).

## Issues upstream úteis
github.com/openclaw/openclaw — filtrar `impact:auth-provider`+`P1`. Ex.: #53969 (hardening
auth store codex), #81865 (parse JSON OAuth trava), #84218 (heartbeat isolatedSession loop).

