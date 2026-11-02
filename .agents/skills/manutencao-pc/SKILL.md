---
name: manutencao-pc
description: "Manutencao e diagnostico do PC de trabalho do usuario: notebook Dell G15 5530 (badge Alienware) rodando Windows 11 com Atlas OS, OneDrive pesado e o ambiente de dev do HAOS (Codex, Codex-mem, chroma). Use SEMPRE que o assunto for o PC local travando, lento, esquentando ou com algo parado. Gatilhos do usuario: \"meu pc ta travando\", \"o pc ta lento\", \"ta uma bosta\", \"trava tudo\", \"limpa o disco\", \"o disco encheu\", \"o onedrive parou de sincronizar\", \"onedrive crashando\", \"atualiza os drivers\", \"reinstala driver Dell\", \"DCU\", \"cpu a 100\", \"ta esquentando\", \"manutencao do pc\", \"o whatsapp fica abrindo e fechando\", \"explorer travado\", \"o turbo nao liga\", \"monitor nao pega 165hz\". Use tambem implicitamente quando o usuario descrever sintomas de hardware/SO local sem nomear a causa. NAO use para servidores (Hetzner/Hostinger = @devops); aqui e so a maquina local do usuario.\n"
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

# Manutencao do PC local do usuario

Skill interna e pessoal. Trata SO a maquina de trabalho do usuario. Toda causa-raiz aqui
ja foi diagnosticada ao vivo, nao re-investigar do zero: ler o sintoma, aplicar o fix.

## Saida esperada desta skill

Sempre entregar nesta forma:
1. **Diagnostico**: o que esta acontecendo, com a causa-raiz nomeada (sintoma -> causa).
2. **Acao**: o comando/fix exato a rodar (ou "REBOOT resolve", quando for o caso).
3. Se a acao for elevada (admin) ou destrutiva, mostrar antes e esperar OK do usuario.

## REGRA DE OURO

Quando o PC "fica uma bosta" (trava, WhatsApp abre/fecha, Explorer congela): NAO remendar
processo por processo. Primeiro medir **uptime + RAM livre**. Se uptime alto + RAM baixa,
**REBOOT resolve**, e a resposta certa. So caca processo individual se o uptime for baixo.

```powershell
# diagnostico rapido de "pc travando"
$os = Get-CimInstance Win32_OperatingSystem
$up = (Get-Date) - $os.LastBootUpTime
"Uptime: {0:N1} h" -f $up.TotalHours
"RAM livre: {0:N1} GB de {1:N0} GB" -f ($os.FreePhysicalMemory/1MB), ($os.TotalVisibleMemorySize/1MB)
Get-Process | Sort-Object WS -Descending | Select-Object -First 8 Name, @{n='RAM_MB';e={int (user-supplied dependency; see PORTABILITY.md)}}, @{n='CPU_s';e={[int]$_.CPU}}
```

## Fluxo de diagnostico: "pc travando / lento"

1. **Uptime + RAM** (script acima). Uptime alto + RAM baixa -> **REBOOT** e parar aqui.
2. **Temperatura** (so se "esquentando" ou throttle): medir no HWiNFO. **100C com a maquina
   IDLE = contato termico ruim** (pasta termica demais), NAO defeito de CPU. Ver secao Termica.
3. **Processos vilao conhecidos** (uptime baixo, RAM subindo): checar nesta ordem
   `ServiceShell.exe` (Realtek leak) -> `python` com CPU alta (chroma loop) -> `OneDrive.exe`
   (reconciliando pin/unpin). Ver tabela de fixes.
4. **Turbo/lentidao sob carga**: se a CPU parece travada na base, e o **perfil do AWCC**, nao
   a BIOS. Ver secao Turbo.

## Tabela: sintoma -> causa -> fix

| Sintoma | Causa-raiz | Fix |
|---|---|---|
| RAM cai sozinha em horas, fica lento | **Realtek leak**: `ServiceShell.exe` (RealtekAudioControl) vaza ate 3-4GB | `taskkill /F /IM ServiceShell.exe` (admin; audio nao para). Ja existe tarefa `HAOS_AntiRealtekLeak` (SYSTEM, mata a cada 4h). Cura: atualizar pela MS Store. |
| Chrome perde logins apos shutdown (exit_type=Crashed) | **Atlas reduz timeout de shutdown p/ 2000ms** (padrao 20000), mata apps antes de salvar | `WaitToKillAppTimeout=20000` em HKCU (ja aplicado). Pendente HKLM `WaitToKillServiceTimeout` (admin). |
| WhatsApp Desktop abre e fecha / crasha | **WebView2** com cache `EBWebView` corrompido | Limpar Cache/Code Cache/Service Worker CacheStorage/GPUCache em `...WhatsAppDesktop...\LocalCache\EBWebView`. **NAO** tocar IndexedDB (e o login). **NUNCA** usar `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--disable-gpu` (quebra). |
| CPU alta continua sem motivo, varios `python` | **chroma-mcp (Codex-mem) loop**: acumulo de instancias | Reboot normaliza. Se voltar, matar o `python` com CPU alta (dados intactos em `~/.Codex-mem`). Tem supervisor (1 worker + 1 mcp). |
| Explorer congela ao abrir pasta sincronizada; CPU alta no OneDrive | **OneDrive reconciliando muito pin/unpin** | Pausar/matar `OneDrive.exe` alivia; reinicia limpo no boot. Evitar "tornar tudo disponivel". |
| OneDrive crasha em loop (Event 1000, `0xc0000409`), hidratacao trava | **DB de sync corrompido** (o `/reset` sozinho NAO basta) | Ver secao "OneDrive crash loop" (reset profundo dos .db). |
| Disco enche a cada poucos dias e "volta no reboot" | **Logs do OneDrive** acumulam ~1,4 GB/dia (projeto vive no OneDrive) | Ja tem tarefa `HAOS_LimparLogsOneDrive` (diaria 13h). Manual: apagar `.odl/.odlgz/.odlsent/.aodl/.etl/.log` +2d em `%LOCALAPPDATA%\Microsoft\OneDrive\logs` (regeneram). |
| OneDrive torra 1 nucleo direto | **`Codex-mem.db` (~200MB) sincronizando** (SQLite no OneDrive e pessimo) | Ja resolvido: .db fora do OneDrive (`~/.Codex-mem`); `mirror_memory.ps1` so copia .md. Nao por .db de volta no OneDrive. |
| CPU a 100C com a maquina parada | **Pasta termica demais** (camada grossa isola) | Ate refazer: ficar no perfil **Silencioso** (~71C). Conserto fisico = limpar e por POUCA pasta. Ver secao Termica. |
| Turbo da CPU nao liga (trava na base ~2400MHz) | **Perfil termico do AWCC** (Silencioso/Equilibrado limitam), NAO BIOS/XTU | Mudar p/ **Desempenho/Equilibrado** no AWCC libera na hora. Ver secao Turbo. |
| Scroll do Chrome engasgado no monitor externo | **Renderiza na GPU errada** (Intel) num monitor que esta na NVIDIA | `HKCU\SOFTWARE\Microsoft\DirectX\UserGpuPreferences` Chrome/Edge = `GpuPreference=2;` (Alto desempenho) e reiniciar o browser. |
| Monitor externo so pega 60Hz no nativo | **G15 nao tem DisplayPort**; HDMI 2.0 limita 3440@60 | Usar cabo **USB-C -> DisplayPort** (USB-C sai da NVIDIA, DP 1.4 = 3440x1440 @165Hz com DSC). |

## Turbo (medir certo)

- O turbo e controlado pelo **AWCC**, nao pela BIOS, nao pelo Intel XTU. Silencioso/Equilibrado
  podem capar; **Desempenho** libera (3.7-4.6GHz).
- **`CurrentClockSpeed` do WMI MENTE** (congela na base). Para medir turbo real:

```powershell
Get-CimInstance Win32_PerfFormattedData_Counters_ProcessorInformation -Filter "Name='_Total'" |
  Select-Object PercentProcessorPerformance   # >100 = turbo ativo
```

- AWCC = NECESSARIO (controla turbo + PL + ventilador). Fechar a JANELA do app economiza
  ~500MB; o servico continua. NAO confundir com **Alienware Arena** (bloatware, pode remover).

## Pegadinhas do Atlas OS

Atlas e debloat agressivo. Tres efeitos que atrapalham manutencao:

1. **UAC escondido**: `PromptOnSecureDesktop=0` faz o prompt de UAC virar janela normal e ficar
   ATRAS das outras. O usuario nunca ve, parece que "nao apareceu". Para rodar algo elevado: criar
   **atalho .lnk na Area de Trabalho marcado como admin** (o UAC ganha foco quando o usuario CLICA).
   `Start-Process -Verb RunAs` disparado pela sessao deixa o UAC atras das janelas.
2. **Instaladores OEM quebram** (Dell, etc.): `AppCompat\DisableEngine=1` faz TODO instalador
   achar que e Windows 8.1 (`VersionNT=603`) e abortar (`UnSupportedOSDetected`, exit 1602).
   Contorno sem reboot: cirurgia no MSI removendo as custom actions de OS-check. Detalhe completo
   em `./references/atlas-os.md`. Alternativa simples (aceita reboot): `DisableEngine=0` -> reboot
   -> instalar -> `DisableEngine=1`.
3. **Timeout de shutdown curto** (2000ms): ver Chrome perdendo login na tabela acima.

## Drivers Dell (DCU)

- Automacao montada: tarefa `HAOS_DellDriverUpdate_Monthly` (dia 1, 15h, SYSTEM, AC-only).
  Auto-aplica DRIVERS + APPS; BIOS/firmware so geram relatorio em
  `.maintenance\dcu-updates\ACAO-MANUAL-<mes>.txt` para revisao manual.
- `dcu-cli.exe` exige elevacao. **3005 / 3003 = servico ocupado** (cada `/scan` dispara ~60s;
  chamadas rapidas colidem). **Reboot pendente BLOQUEIA o apply** -> reiniciar antes de aplicar.
- Servico `DellClientManagementService` fica Manual + parado (Atlas-friendly); a tarefa faz
  Manual->Start->run->Stop sob demanda.
- BIOS ja na ultima (1.31.0). NVIDIA dGPU se auto-atualiza. MSI patchado guardado em
  `.maintenance\dcu-installer\msi\` para reinstalar.

## OneDrive crash loop (reset profundo)

Quando o `OneDrive /reset` simples nao basta (crash em loop, hidratacao travando):

1. `Stop-Process` no OneDrive.
2. Mover/apagar `OCSI.db`, `SyncEngineDatabase.db`, `SafeDelete.db` (+ `-wal`/`-shm`) de
   `%LOCALAPPDATA%\Microsoft\OneDrive\settings\Personal\`.
3. Reabrir o OneDrive. Re-sync pos-reset demora (conta grande) mas converge sem crash.

**Cofre Pessoal**: o `.vhdx` vive em `${USER_WORKSPACE_ROOT}<SID>\{GUID}.vhdx`. `${USER_WORKSPACE_ROOT}`
NAO e lixo, contem o cofre. Confirmar GUID em `HKCU\...\OneDrive\Accounts\Personal` (`VaultBackupGuid`)
antes de qualquer limpeza ali.

## Pegadinha de PowerShell ao automatizar

Virgula em argumento de comando nativo quebra o parsing (o pwsh trata como operador de array e
o script "abre e fecha"). Passar args via array + splatting:

```powershell
$a = @('/applyUpdates','-updateType=driver,application','-reboot=disable',"-outputLog=$log")
& $dcu @a
# validar sintaxe antes de o usuario rodar:
[Management.Automation.Language.Parser]::ParseFile($path,[ref]$null,[ref]$err)
```

## Terminal piscando nos hooks Claude-Mem/Codex

Quando janelas ou abas de terminal aparecem durante cada ferramenta, auditar primeiro o
lançador do Claude-Mem. No Windows, `where bun` com `shell: true` e a execução por
`bun.cmd` criam `cmd.exe`/`conhost.exe` transitórios. A correção é preferir um caminho
absoluto para `bun.exe` e usar `spawn(..., { shell: false, windowsHide: true })`.

Também evitar que `<USER_DEPENDENCY:.codex/hooks.json>` invoque `powershell.exe` dentro do `pwsh.exe` já
criado pelo Codex: chamar o script diretamente com `& ".codex\\hooks\\script.ps1"` reduz
processos e flashes. Validar as duas instâncias independentes (Claude Code e Codex) por
suas portas/healthchecks; nunca encerrar uma para corrigir a outra. O procedimento completo
está em `./references/claude-mem-terminal-flash-playbook.md`.

## Referencias

- `./references/atlas-os.md`: cirurgia no MSI para instalar OEM sob Atlas (passo a passo completo).
- Runbook de disco: `Obsidian/Codex-Vault/02-Arquitetura/Rotina-Saudavel-Disco-XTremeNote3.md`.
- As causas-raiz acima ja foram diagnosticadas ao vivo. Nao re-diagnosticar; aplicar o fix.
- `./references/claude-mem-terminal-flash-playbook.md`: diagnóstico, correção e validação do
  terminal transitório gerado pelos hooks de memória.

