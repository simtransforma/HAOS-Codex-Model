@echo off
setlocal
set SCRIPT_DIR=%~dp0
python "%SCRIPT_DIR%audit_skill.py" %*
if %errorlevel% gtr 1 (
  echo [BLOCKED] Risk too high. Do not install.
  exit /b %errorlevel%
)
echo [REVIEW] Audit finished. Review findings before install.
exit /b %errorlevel%
