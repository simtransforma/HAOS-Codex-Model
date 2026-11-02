# Atlas OS: instalar instalador OEM (InstallShield) que o Atlas bloqueia

Vale para qualquer instalador OEM InstallShield que o Atlas trava (Dell Command Update e o caso
de referencia). O usuario validou esse metodo ao vivo em 11/06/2026.

## Por que quebra

- Atlas seta `HKLM\SOFTWARE\Policies\Microsoft\Windows\AppCompat\DisableEngine = 1` (corta
  PCA/telemetria/inventory).
- O motor AppCompat e quem honra o manifesto `supportedOS`. Desligado, `GetVersionEx` ignora o
  manifesto e retorna a versao legada (6.3.9600 = Win8.1) para TODO processo, inclusive `msiexec`.
- Sintoma no log MSI: `VersionNT = 603`, `WindowsBuild = 9600` (mesmo sendo Win11 26200 real).
  O instalador aborta com `UnSupportedOSDetected` (exit 1602).
- `6.3/9600` (e nao `6.2/9200`) confirma o motor desligado caindo no fallback legado.
- NAO adianta: patch no registry `CurrentVersion` (o MSI le do GetVersionEx); setar
  `DisableEngine=0` SEM reboot (so re-inicializa no boot); mexer em `__COMPAT_LAYER`/Layers/SDB.

## Metodo que funciona (sem reboot, sem mexer no Atlas): cirurgia no MSI

1. `winget download --id Dell.CommandUpdate.Universal -d <dir>` (baixa o EXE, nao instala).
2. Extrair o EXE com 7zip -> tem `DellCommandUpdateApp_Setup.exe` (InstallShield real) dentro.
3. InstallShield nao extrai limpo com 7zip. Truque: rodar o setup `/s` e capturar o MSI que ele
   joga no `%TEMP%` durante a execucao (poll por `*.msi` novo >1MB, copiar, matar o setup).
   MSI self-contained ~96MB.
4. Abrir o MSI via COM (`WindowsInstaller.Installer` -> `OpenDatabase` mode 1) e **DELETAR as
   custom actions de OS-check** do `InstallExecuteSequence` E do `InstallUISequence`, depois
   `Commit`:
   - `CheckOSIsWin10`, `CheckSystemOS`, `CheckFrameworkSupported`, `ShowIdenticalAppMssg`
     (todas Type 257 = DLL `ISSetup.dll` que chama GetVersionEx e aborta com a versao fake).
   - A LaunchCondition padrao NAO bloqueia (checa so VersionNT 400-602; 603 passa). Sao as DLLs
     que matam. A maquina ATENDE os requisitos de verdade (Win11, .NET 8, admin), so o check e
     enganado pelo spoof.
5. `msiexec /i DellCommandUpdate_patched.msi /qn /norestart` (elevado) -> exit 0, instala.

MSI patchado guardado em `${USER_WORKSPACE_ROOT}`
(reusar em reinstalacao).

## Alternativa simples (se aceitar reboot)

`DisableEngine=0` -> reboot -> instalar normalmente -> `DisableEngine=1`.

## DCU CLI: codigos e pegadinhas

- `dcu-cli.exe` exige elevacao sempre.
- **3005** = "Dell Client Management Service instalando atualizacoes pendentes". **3003** =
  "operacao em andamento". Ambos = servico ocupado. Cada `/scan` dispara ~60s; chamadas rapidas
  colidem. Helper tem retry nesses codigos.
- **Reboot pendente BLOQUEIA o apply** (`MsiSystemRebootPending=1` + `.tmp` em DriverStore ->
  PendingFileRename). Reiniciar o PC antes de aplicar.
- `/help` funciona mesmo com servico ocupado (nao toca no servico).
- Apos reinstalar o servico: `dcu-cli /configure -scheduleManual -updatesNotification=disable`
  para ele parar de competir com a tarefa agendada.

