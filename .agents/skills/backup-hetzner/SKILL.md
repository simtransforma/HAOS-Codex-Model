---
name: backup-hetzner
description: "Operar e auditar o sistema de backup do servidor Hetzner (example.invalid) e do n8n do grupo ${USER_BRAND}: backup geral diario, backup n8n semanal pro Google Drive, encryption key do n8n, restore e disaster recovery. Use SEMPRE que o usuario pedir \"faz backup do hetzner\", \"backup do n8n\", \"roda o backup agora\", \"o backup rodou?\", \"cade o backup de ontem\", \"restaura o backup\", \"preciso recuperar o n8n\", \"qual a chave de encryption do backup\", \"testa o disaster recovery\", \"o off-site ta funcionando?\", \"o backup foi pro Drive?\", \"checa a retencao do backup\". Tambem aciona implicitamente quando a tarefa envolver recuperar workflows/credentials do n8n, mexer no banco antes de uma operacao destrutiva (backup verificado ANTES), ou diagnosticar por que o backup off-site quebrou (causa-raiz tipica = troca de senha Google revoga o OAuth do rclone). NAO pule esta skill quando o assunto for proteger ou restaurar dados do Hetzner/n8n: a chave de encryption fica FORA do pacote (de proposito) e o off-site tem pegadinha de token que ja custou tempo. NAO use para o backup da memoria eterna do Codex (isso e o finish_task.ps1, outro mecanismo).\n"
---

# Backup Hetzner / n8n



## Regras de ouro (nao violar)

1. **Read-only primeiro.** Listar, ler manifesto e checar log sao seguros. Restaurar, podar ou rodar backup manual = confirmar intencao antes.
2. **A `N8N_ENCRYPTION_KEY` fica FORA do pacote de backup, de proposito.** Sem ela os ${USER_INVENTORY} do n8n nao descriptografam. Ela vive SO no `MASTER.env` local (campo `N8N_ENCRYPTION_KEY`) e numa copia-cofre no Bitwarden (item "N8N_ENCRYPTION_KEY"). NUNCA jogar essa chave pro servidor nem pro pacote: isso anula a protecao DR validada. (Por isso o `sync-secrets.py` exclui ela do espelho pro Hetzner.)
3. **Nunca expor o valor da chave** em resposta, log ou commit. So por nome de variavel.
4. **Backup verificado ANTES de mexer em banco/volume.** Antes de qualquer operacao destrutiva no Hetzner (drop, migration, recriar volume), confirmar que ha backup recente e integro.
5. **SSH do Hetzner e instavel** -> comandos curtos e individuais, nao encadear pipeline longo.
6. **Off-site quebra silenciosamente quando trocam a senha do Google.** Ver causa-raiz abaixo. Por isso ha alerta WhatsApp em falha.

## Acesso

```bash
ssh -i "${HAOS_PRIVATE_ROOT}" -o StrictHostKeyChecking=no -o ConnectTimeout=15 root@example.invalid "CMD"
```

Carregar o `MASTER.env` antes de qualquer coisa que precise de credencial (caminho em `project_credentials.md`):

```bash
set -a && source "${HAOS_PRIVATE_ROOT}" && set +a
```

## Arquitetura (dois fluxos independentes)

| | Backup GERAL | Backup n8n especifico |
|---|---|---|
| Script | `${HAOS_PRIVATE_ROOT}` | `${HAOS_PRIVATE_ROOT}` (perm 700) |
| Cron | diario **03:00 BRT** (`/etc/cron.d/...`) | semanal **domingo `30 6 * * 0` UTC = 03:30 BRT** (`/etc/cron.d/n8n-backup`) |
| Conteudo | `pg_dumpall` + `pg_dump` (n8n/typebot/evolution) + `mysqldump` Mautic + Redis + volumes Docker + configs `/opt` | ${USER_INVENTORY} JSON + ${USER_INVENTORY} + dump do banco n8n + MANIFEST |
| Destino Drive | remote `gdrive_oauth:` -> pasta "servidor-hetzner" (root_folder_id `${RESOURCE_ID}`) | pasta **N8N** (folder ID `${RESOURCE_ID}`) -> `N8N/<DATA>/n8n-backup-<DATA>.tar.gz` |
| Retencao local | **3 dias** (`backup.sh` linha 16 `RETENTION_DAYS=3`, poda na linha 139; `${HAOS_PRIVATE_ROOT}` ~18G) | 7 dias |
| Retencao Drive | diaria, inalterada (copia segura off-site) | 90 dias |



## Encryption key

- Variavel: `N8N_ENCRYPTION_KEY` (${USER_INVENTORY}), no `MASTER.env` local. **Fora do pacote de backup** (protecao validada por teste negativo: sem a chave, os credentials nao decriptam).
- O `${HAOS_PRIVATE_ROOT}` do Hetzner NAO tem essa chave (e a unica que o `sync-secrets.py` exclui do espelho). Se ela voltar pro servidor, vai parar dentro do backup geral e mata a separacao -> NAO fazer.

## Checar se o backup rodou (read-only, fazer SEMPRE primeiro)

Backup geral (ultimo arquivo local + tamanho + data):
```bash
ssh ... "ls -lh ${HAOS_PRIVATE_ROOT} | tail -5"
```

Backup n8n (ultimo manifesto local):
```bash
ssh ... "ls -lt ${HAOS_PRIVATE_ROOT} 2>/dev/null | head -5"   # [CONFIRMAR caminho local exato]
```

Confirmar que subiu pro Drive (off-site e a parte que mais quebra):
```bash
ssh ... "rclone lsl gdrive_oauth:servidor-hetzner | tail -5"
ssh ... "rclone lsl gdrive_oauth:N8N | tail -10"
```

Log do cron / ultima execucao:
```bash
ssh ... "tail -40 /var/log/backup.log 2>/dev/null || grep -i backup /var/log/syslog | tail -20"   # [CONFIRMAR nome do log]
```

Se o `rclone lsl` falhar com erro de auth/token -> e a causa-raiz historica (proxima secao), nao um backup vazio.

## Causa-raiz do off-site quebrar (NAO esquecer)


**Regra duravel:** toda vez que a senha de uma conta Google e trocada, TODAS as integracoes OAuth daquela conta morrem. Apos troca de senha Google, reautorizar proativamente: rclone (este backup) + credenciais Google no n8n.


## Restore / Disaster Recovery

- Runbook: `${HAOS_PRIVATE_ROOT}` (no servidor) + copia em `HAO IA Operation System\_backups\n8n\RESTORE-RUNBOOK.md` (local). **Seguir o runbook, nao improvisar.**

Fluxo de restore do n8n (resumo; o runbook manda):
1. Pegar o `.tar.gz` do dia desejado: `rclone copy gdrive_oauth:N8N/<DATA>/n8n-backup-<DATA>.tar.gz <destino>`.
2. Extrair, conferir o MANIFEST (deve listar os ${USER_INVENTORY} + ${USER_INVENTORY} + dump).
3. Garantir que o n8n alvo esta com a MESMA `N8N_ENCRYPTION_KEY` (do `MASTER.env` ou Bitwarden) ANTES de importar credentials, senao o decrypt falha.
4. Restaurar conforme o runbook (import dos workflows + restore do dump do banco).
5. Validar com turno real: abrir o n8n, conferir workflows ativos e disparar 1 fluxo de teste. Nao declarar restaurado so porque o import "nao deu erro".

Para o backup geral, a restauracao e por componente (Postgres via `pg_restore`/`psql`, Mautic via `mysql`, volumes Docker, configs `/opt`) seguindo o mesmo runbook.

## TODOs a confirmar ao vivo antes de afirmar como fato

- Caminhos exatos: `${HAOS_PRIVATE_ROOT}`, `${HAOS_PRIVATE_ROOT}`, `${HAOS_PRIVATE_ROOT}` (existem? linhas 16/139 ainda valem?).
- Nomes de arquivo de cron em `/etc/cron.d/` (geral e `n8n-backup`) e horarios.
- `RETENTION_DAYS` atual (3 local geral; 7 local n8n; 90 Drive n8n).
- Folder IDs do Drive ainda corretos (`${RESOURCE_ID}` servidor-hetzner; `${RESOURCE_ID}` N8N).
- Numeros ${USER_INVENTORY} / ${USER_INVENTORY} mudaram desde 2026-05-18.
- Nome/caminho do log de backup e do destino local do n8n (`${HAOS_PRIVATE_ROOT}` e palpite).
- Remote `gdrive_oauth:` ainda autorizado (rodar um `rclone lsd gdrive_oauth:` read-only).

## Saida esperada

Ao responder uma demanda de backup, entregar de forma objetiva (PT-BR, sem em-dash):
- **Status:** rodou / nao rodou, com a EVIDENCIA (saida do `ls`/`rclone lsl`, data e tamanho do ultimo pacote local e do Drive).
- **Off-site:** confirmado no Drive (pasta + data) ou sinalizar quebra de token com o proximo passo (reautorizar rclone).
- **Em restore/DR:** o passo do runbook em que esta, com a `N8N_ENCRYPTION_KEY` referida so por nome, e a validacao por turno real.
- Citar a fonte quando o dado vier da memoria e ainda nao foi confirmado ao vivo (marcar [CONFIRMAR]).

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
