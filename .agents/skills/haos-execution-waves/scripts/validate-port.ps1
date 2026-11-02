[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$commandsRoot = Join-Path $repoRoot 'commands/gsd'
$commandFiles = @(Get-ChildItem -LiteralPath $commandsRoot -File -Filter '*.md' | Sort-Object Name)
$errors = [System.Collections.Generic.List[string]]::new()

if ($commandFiles.Count -ne 31) {
    $errors.Add("Esperados 31 comandos Markdown; encontrados $($commandFiles.Count).")
}

$active = 0
$quarantine = 0
foreach ($file in $commandFiles) {
    $content = Get-Content -LiteralPath $file.FullName -Raw
    if ($content -match '(?im)^status:\s*active\s*$') { $active++ }
    if ($content -match '(?im)^status:\s*quarantine\s*$') { $quarantine++ }
    if ($content -match '(?i)\.claude[\\/]get-shit-done|get-shit-done[\\/]|gsd-tools\.cjs|\.claude[\\/]agents[\\/]gsd-') {
        $errors.Add("Referência executável legada em $($file.Name).")
    }
}

if ($active -ne 2) { $errors.Add("Esperados 2 comandos ativos; encontrados $active.") }
if ($quarantine -ne 29) { $errors.Add("Esperados 29 comandos em quarentena; encontrados $quarantine.") }

foreach ($required in @('plan-phase.md', 'execute-phase.md')) {
    $content = Get-Content -LiteralPath (Join-Path $commandsRoot $required) -Raw
    if ($content -notmatch '(?im)^skill:\s*haos-execution-waves\s*$') {
        $errors.Add("$required não aponta para haos-execution-waves.")
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "OK: 31 comandos auditados; 2 ativos; 29 em quarentena; zero referência executável ao runtime GSD ausente."
