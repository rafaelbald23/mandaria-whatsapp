@echo off
chcp 65001 >nul
title MandarIA - Instalador do Agente Local

echo.
echo ╔═══════════════════════════════════════╗
echo ║   MandarIA - Instalador Agente Local ║
echo ║   Versão 3.0 - MonitorIA             ║
echo ╚═══════════════════════════════════════╝
echo.

echo [1/3] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo Por favor, instale o Python 3.11 ou superior:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo [2/3] Instalando dependências...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)
echo ✅ Dependências instaladas

echo.
echo [3/3] Configurando agente...
python agente_local.py
if errorlevel 1 (
    echo ❌ Erro ao configurar agente
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════╗
echo ║   ✅ Instalação concluída!           ║
echo ╚═══════════════════════════════════════╝
echo.
echo Para iniciar o agente, execute: iniciar_agente.bat
echo.
pause
