@echo off
setlocal EnableDelayedExpansion

rem Ir para o diretório do .bat
cd /d "%~dp0"

rem Lista de comandos possíveis
set PY_CMDS=py python python3

for %%C in (%PY_CMDS%) do (
    where %%C >nul 2>&1
    if not errorlevel 1 (
        rem Tenta achar o pythonw equivalente
        if exist "%%~dp$PATH:C\pythonw.exe" (
            start "" "%%~dp$PATH:C\pythonw.exe" main.py
        ) else (
            start "" %%C main.py
        )
        exit
    )
)

echo Nenhuma instalacao do Python foi encontrada.
pause
