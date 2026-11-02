@echo off
setlocal EnableExtensions
set "out="
set "sandbox="
:args
if "%~1"=="" goto write
if "%~1"=="--output-last-message" (
  set "out=%~2"
  shift
)
if "%~1"=="--sandbox" (
  set "sandbox=%~2"
  shift
)
shift
goto args
:write
if "%out%"=="" exit /b 2
if /I "%sandbox%"=="read-only" (
  > "%out%" echo {"decision":"SHIP","assessment":"Acceptance criteria verified.","feedback":"Ready to ship.","evidence":["fake reviewer evidence"]}
) else (
  > "%out%" echo {"status":"COMPLETE","assessment":"Objective completed.","evidence":["fake worker evidence"],"next_step":"None"}
)
exit /b 0
