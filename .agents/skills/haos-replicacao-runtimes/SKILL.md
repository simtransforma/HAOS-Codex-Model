---
name: haos-replicacao-runtimes
description: "Runbook para REPLICAR e PROPAGAR recursos do HAOS (skills, agentes SOUL.md, wrappers nativos, hooks, configs como AGENTS.md e bootstrap) para os runtimes que rodam no servidor Hetzner. Cada runtime recebe de um jeito diferente (uns por git, uns por cópia direta, o Paperclip por registry no banco). Use SEMPRE que a tarefa for \"replica essa skill no Hetzner\", \"propaga o agente pros runtimes\", \"sincroniza as skills no OpenClaw / Codex / Hermes / Paperclip\", \"atualiza o Codex do Hetzner com a skill nova\", \"distribui o HAOS_CC pros runtimes\", \"roda o sync de skills\", ou qualquer variação. Também aciona implicitamente logo depois de criar ou editar uma skill, um agente ou um config que precisa valer no servidor. NÃO improvise a propagação: cada destino tem caminho e método próprios. Siga o runbook daqui e carregue a skill haos-hetzner-map ANTES de tocar no servidor.\n"
---

# haos-replicacao-runtimes

Modelo condicional para replicar recursos entre runtimes, somente quando existirem no ambiente do usuario e houver autorizacao para a acao e os destinos. Os gatilhos da descricao selecionam este runbook; nao autorizam propagacao implicita, SSH, push, instalacao de hooks ou alteracao global. Ler `references/runbook-por-destino.md` e adaptar os comandos ao mapa real, sem presumir configuracao instalada.

## Pré-requisitos (obrigatório, nesta ordem)

1. **Carregar a skill `haos-hetzner-map`** antes de qualquer ação no servidor (fonte da verdade do mapa: caminhos, containers, portas).
2. **Classificar o recurso: PÚBLICO ou INTERNO.** Público = genérico e sanitizado (vai pelo git/HAOS_CC). Interno = toca infra, segredo, IP, container, cliente, ou é SOUL completo (vai só por cópia direta SSH, NUNCA pro HAOS_CC público).
3. **SSH instável:** usar comandos curtos e individuais. Rodar `df -h` antes de operação pesada. Chave em `_secrets/ssh/hetzner_ed25519`, host `root@example.invalid` (formato completo no AGENTS.md, sem expor segredo).

## Pipeline geral

```
[1] EDITAR na fonte da verdade
         | commit + push
         v
[2] <USER_PUBLIC_REPOSITORY>   (superset PUBLICO, sanitizado; push exige OK)
         | git pull (ff-only)
         v
[3] ${HAOS_PRIVATE_ROOT}   (Hetzner, clone que SÓ recebe pull, nunca push)
         |
         +--[4a] ${HAOS_PRIVATE_ROOT}  -> sincroniza SÓ o container openclaw
         |
         +--[4b] COPIAS DIRETAS (cp -r / docker cp) -> runtimes e sandboxes autorizados
```

Regra de verificacao: conferir quais destinos o sync script do usuario realmente cobre. Se cobrir apenas OpenClaw, os demais exigem o metodo de copia ou registry validado para cada destino. Material INTERNO nao passa por repositorio publico.

## Destinos possiveis (modelo a confirmar, nao inventario instalado)

| # | Destino | Tipo | Método de entrega | Complexidade |
|---|---|---|---|---|
| 2 | `${HAOS_PRIVATE_ROOT}` (clone Hetzner) | repo (pull-only) | `git pull` ff-only | baixa |
| 3 | Codex HETZNER | CLI host | `cp -r` de `${HAOS_PRIVATE_ROOT}` + plugin | baixa |
| 4 | OpenClaw | container | `${HAOS_PRIVATE_ROOT}` | baixa |
| 5 | Codex (do OpenClaw) | CLI on-demand | `cp -r` para `${HAOS_PRIVATE_ROOT}` | média |
| 6 | Hermes | CLI on-demand | skills por `cp -r`; agentes por PERFIL (`hermes profile create --clone-from`) | média |
| 7 | Paperclip | container | registry no DB (`importFromSource` via tsx) + atribuição por agente | ALTA |

## Duas trilhas

- **INTERNO (skill com infra/segredo, SOUL completo):** NUNCA vai pro HAOS_CC público. Cópia direta servidor-a-servidor: `scp`/`tar | ssh` do host para cada runtime, ou `docker cp` para containers. Para o Paperclip, entra pelo registry do banco.

## Pegadinhas críticas (não esquecer)

1. **Codex e Hermes são CLI on-demand, NÃO containers.** `docker ps`/`ps` vazio é NORMAL. Nunca concluir que "sumiram" por isso. Verificar Hermes com `hermes --version` + `ls ${HAOS_PRIVATE_ROOT}`; Codex pelo path do harness.
2. **Codex é MOTOR de LLM, não tem roster próprio.** `which codex` no host é vazio (vendorizado dentro do OpenClaw e do Paperclip via `@openai/codex-linux-x64`). NÃO "usa o roster do OpenClaw": ele é o backend; o roster é de quem o invoca. Dois contextos: motor do OpenClaw (`${HAOS_PRIVATE_ROOT}`, só `skills/`, sem `agents/`) e o do Paperclip (`/paperclip/.codex`, que executa o roster do Paperclip). Codex recebe só SKILLS por `cp -r`; nunca tente "plugar um agente no Codex".
3. **`${HAOS_PRIVATE_ROOT}` é só pull.** Editar dentro de qualquer runtime/container = perda garantida (o próximo sync sobrescreve). Editar SEMPRE na origem.
4. **Hermes usa PERFIS, não arquivo solto:** perfil = diretório `${HAOS_PRIVATE_ROOT}` com `config.yaml` + `.env` + `SOUL.md`. Criar com `hermes profile create <nome> --clone-from <existente>`, depois sobrescrever o `SOUL.md`.
5. **Paperclip é o mais complexo:** copiar a skill pra pasta NÃO ativa. Precisa registrar no DB (`company_skills` via `importFromSource` rodado com **tsx**, não node puro) e atribuir por agente (`desiredSkills`). E agente só dispara com **Assignee**.
6. **Autenticacao:** conferir usuario, versao e permissao do runtime. Quando suportado e autorizado, preferir login interativo; nao gerar ou exibir token em screenshots ou logs.
7. **Não reiniciar OpenClaw em cascata** (derruba sessão WhatsApp; self-heal cuida). Não reiniciar o daemon Docker à toa.
8. **Adaptação de SO:** host Linux não tem `pwsh`. Scripts `.ps1` precisam de equivalente `.sh`. Python é portável.
9. **Skills core:** conferir a politica de distribuicao do usuario, conflitos entre comandos e skills e exclusoes de cada runtime antes de copiar. Nenhuma contagem de core e presumida a partir de outro ambiente.
10. **Sandbox privado:** se estiver pausado ou fora do escopo autorizado, nao propagar conteudo; confirmar o estado e a aprovacao aplicavel sem identificar ambientes pessoais de terceiros.

## Checklist de verificação ao vivo (confirmar ANTES de declarar concluído)

Contagens, caminhos, versoes e metodos dependem do ambiente do usuario. Confirmar na fonte real antes de cada acao dependente e registrar evidencia local sanitizada; este pacote nao fornece resultados de verificacao ao vivo.

**Checklist condicional, sem resultados previamente confirmados:**
- [ ] Se houver sync por `tar` e `docker exec`, revisar origem, destino, merge e ownership. Preservar outras skills e testar idempotencia na copia autorizada. Nao remover arquivos orfaos, alterar ownership ou reiniciar container sem escopo e rollback aprovados.
- [ ] Confirmar caminhos separados por runtime: Codex host, OpenClaw, motor Codex, Hermes e profiles, quando presentes. Registrar versoes reais; placeholders nao sao um mapa implantado.
- [ ] Se Hermes suportar profiles, conferir `hermes profile create <nome> --clone-from <perfil-base>`, arquivos `config.yaml`, `SOUL.md` e skills. Validar como autenticacao e herdada, sem copiar ou exibir credenciais e sem sobrescrever perfil existente por presuncao.
- [ ] Se necessario, preparar staging INTERNO fora do repo publico. Revisar o transporte autorizado por `scp`, `cp -r` ou equivalente e conferir o conteudo no destino sem levar segredos ao pacote.
- [ ] Conferir main-guard hook por runtime (LOG vs ENFORCE) apenas se fizer parte do escopo; nao instalar nem ativar hooks automaticamente.
- [ ] Se Paperclip estiver no escopo, confirmar registry no DB, identificador da organizacao, `companySkillService.importFromSource`, resolver e atribuicao por agente antes de executar qualquer escrita.

## Saída esperada

Para cada destino autorizado e realmente tocado, confirmar com evidencia que o recurso chegou e e lido pelo runtime. Listar destinos pulados e o motivo sem dados pessoais. Nunca declarar "replicado" sem conferir a skill/agente no destino real; sem teste, manter NAO VERIFICADO.

## Portabilidade

Consultar [dependencias e limites](EXPORT_DEPENDENCIES.md). Procedimento importado, nao prova de integracao instalada. Exemplos .example exigem adaptacao e testes; nao executar comandos com dependencias ausentes.
