[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$skillRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $skillRoot 'scripts\haos-ralph-loop.ps1'
$fakeCodex = Join-Path $PSScriptRoot 'fixtures\fake-codex.cmd'
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("haos-ralph-loop-test-" + [guid]::NewGuid().ToString('N'))

try {
    New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
    & git -C $tempRoot init -q

    $dryRun = & pwsh -NoProfile -File $runner -Cwd $tempRoot -Objective 'Verify dry-run.' -AcceptanceCriteria 'The runner prints a safe configuration.' -DryRun
    if (($dryRun -join "`n") -notmatch '"dangerous_bypass":\s*false') { throw 'Dry-run did not preserve the dangerous bypass invariant.' }

    $result = & pwsh -NoProfile -File $runner -Cwd $tempRoot -Objective 'Verify the fake loop.' -AcceptanceCriteria 'The fake worker reports completion.' -CodexBinary $fakeCodex -HardTimeoutSeconds 60 -Run
    if (($result -join "`n") -notmatch 'task_complete') { throw 'Expected task_complete from fake loop.' }
    $summary = Get-Content -Raw -LiteralPath (Join-Path $tempRoot '.codex\haos-ralph-loop\run-summary.md')
    if ($summary -notmatch 'Automatic commit/push: false') { throw 'Summary did not preserve no-push invariant.' }
    Write-Output 'PASS: HAOS Ralph Loop dry-run and work/review completion path verified.'
} finally {
    if (Test-Path -LiteralPath $tempRoot) { Remove-Item -LiteralPath $tempRoot -Recurse -Force }
}
