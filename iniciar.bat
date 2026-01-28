@echo off
chcp 65001 >nul
cls
color 0B
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║        ROBÔ WHATSAPP WEB - monitorIA                       ║
echo ║        Sistema de Disparo v3.0                             ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Iniciando sistema...
echo.
timeout /t 2 >nul

echo Verificando Python...
python --version 2>nul
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Por favor, instale Python 3.8+:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✅ Python OK
echo.

echo Verificando dependências...
python -c "import flask" 2>nul
if errorlevel 1 (
    color 0E
    echo.
    echo ⚠️  Dependências não instaladas!
    echo.
    echo Deseja instalar agora? (S/N)
    set /p resposta=
    if /i "%resposta%"=="S" (
        echo.
        echo Instalando dependências...
        pip install -r requirements.txt --quiet
        if errorlevel 1 (
            color 0C
            echo.
            echo ❌ Erro ao instalar dependências!
            echo.
            echo Execute manualmente:
            echo   pip install -r requirements.txt
            echo.
            pause
            exit /b 1
        )
        echo ✅ Dependências instaladas!
    ) else (
        echo.
        echo Execute primeiro:
        echo   pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)
echo ✅ Dependências OK
echo.

echo Criando diretórios...
if not exist "Planilhas" mkdir "Planilhas"
if not exist "Logs" mkdir "Logs"
if not exist "static\images" mkdir "static\images"
echo ✅ Diretórios OK
echo.

color 0A
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✅ INICIANDO SERVIDOR...                      ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Acesse no navegador:
echo   🌐 http://localhost:5000
echo.
echo Login padrão:
echo   👤 Usuário: admin
echo   🔑 Senha: admin123
echo.
echo Para parar o servidor: Ctrl + C
echo.
echo ════════════════════════════════════════════════════════════
echo.

python app.py
