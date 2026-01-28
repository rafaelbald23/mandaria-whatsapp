@echo off
echo ========================================
echo   SETUP - ROBO WHATSAPP monitorIA
echo ========================================
echo.

echo [1/3] Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ em: https://www.python.org/
    pause
    exit /b 1
)
echo OK: Python encontrado
echo.

echo [2/3] Instalando dependencias Python...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)
echo OK: Dependencias instaladas
echo.

echo [3/3] Criando diretorios...
if not exist "Planilhas" mkdir "Planilhas"
if not exist "Logs" mkdir "Logs"
if not exist "static\images" mkdir "static\images"
echo OK: Diretorios criados
echo.

echo ========================================
echo   SETUP CONCLUIDO!
echo ========================================
echo.
echo Agora voce pode executar:
echo   npm run dev
echo.
echo Ou:
echo   python app.py
echo.
pause
