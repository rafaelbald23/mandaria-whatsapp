@echo off
chcp 65001 >nul
cls
color 0B
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║        INSTALADOR DE DEPENDÊNCIAS - monitorIA              ║
echo ║        Robô WhatsApp Web v3.0                              ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Este script vai instalar todas as dependências necessárias.
echo.
timeout /t 2 >nul
echo.

echo ┌─────────────────────────────────────────────────────────┐
echo │ [1/5] Verificando Python...                            │
echo └─────────────────────────────────────────────────────────┘
python --version 2>nul
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Por favor, instale Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo ⚠️  IMPORTANTE: Durante a instalação, marque
    echo    a opção "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo ✅ Python encontrado!
echo.
timeout /t 1 >nul

echo ┌─────────────────────────────────────────────────────────┐
echo │ [2/5] Verificando pip...                               │
echo └─────────────────────────────────────────────────────────┘
pip --version 2>nul
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ ERRO: pip não encontrado!
    echo.
    echo Tentando instalar pip...
    python -m ensurepip --default-pip
    if errorlevel 1 (
        echo.
        echo ❌ Falha ao instalar pip.
        echo Por favor, reinstale o Python.
        pause
        exit /b 1
    )
)
echo ✅ pip encontrado!
echo.
timeout /t 1 >nul

echo ┌─────────────────────────────────────────────────────────┐
echo │ [3/5] Atualizando pip...                               │
echo └─────────────────────────────────────────────────────────┘
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo ⚠️  Aviso: Não foi possível atualizar pip
    echo    Continuando mesmo assim...
) else (
    echo ✅ pip atualizado!
)
echo.
timeout /t 1 >nul

echo ┌─────────────────────────────────────────────────────────┐
echo │ [4/5] Instalando dependências...                       │
echo └─────────────────────────────────────────────────────────┘
echo.
echo Isso pode levar alguns minutos...
echo Por favor, aguarde...
echo.

pip install -r requirements.txt --quiet --disable-pip-version-check

if errorlevel 1 (
    color 0E
    echo.
    echo ⚠️  Aviso: Algumas dependências podem ter falhado.
    echo    Tentando instalar uma por uma...
    echo.
    
    pip install Flask==3.0.0 --quiet
    pip install Flask-SocketIO==5.3.5 --quiet
    pip install python-socketio==5.10.0 --quiet
    pip install python-engineio==4.8.0 --quiet
    pip install selenium==4.16.0 --quiet
    pip install pandas==2.1.4 --quiet
    pip install openpyxl==3.1.2 --quiet
    pip install Pillow==10.1.0 --quiet
    pip install gunicorn==21.2.0 --quiet
    pip install eventlet==0.33.3 --quiet
    pip install python-dotenv==1.0.0 --quiet
)

echo.
echo ✅ Dependências instaladas!
echo.
timeout /t 1 >nul

echo ┌─────────────────────────────────────────────────────────┐
echo │ [5/5] Criando estrutura de pastas...                   │
echo └─────────────────────────────────────────────────────────┘
if not exist "Planilhas" mkdir "Planilhas"
if not exist "Logs" mkdir "Logs"
if not exist "static" mkdir "static"
if not exist "static\css" mkdir "static\css"
if not exist "static\js" mkdir "static\js"
if not exist "static\images" mkdir "static\images"
if not exist "templates" mkdir "templates"
echo ✅ Estrutura criada!
echo.
timeout /t 1 >nul

echo.
echo ┌─────────────────────────────────────────────────────────┐
echo │ Verificando instalação...                              │
echo └─────────────────────────────────────────────────────────┘
echo.

python -c "import flask; print('✅ Flask:', flask.__version__)" 2>nul || echo ❌ Flask não instalado
python -c "import flask_socketio; print('✅ Flask-SocketIO instalado')" 2>nul || echo ❌ Flask-SocketIO não instalado
python -c "import selenium; print('✅ Selenium instalado')" 2>nul || echo ❌ Selenium não instalado
python -c "import pandas; print('✅ Pandas instalado')" 2>nul || echo ❌ Pandas não instalado

echo.
color 0A
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✅ INSTALAÇÃO CONCLUÍDA!                      ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Para executar o sistema, use um dos comandos:
echo.
echo   📌 npm run dev
echo   📌 python app.py
echo.
echo Depois acesse no navegador:
echo   🌐 http://localhost:5000
echo.
echo Login padrão:
echo   👤 Usuário: admin
echo   🔑 Senha: admin123
echo.
echo ════════════════════════════════════════════════════════════
echo.
pause
