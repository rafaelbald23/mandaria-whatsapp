#!/bin/bash

# Script de inicialização para Railway
# Inicia o servidor Baileys (Node.js) e o Flask (Python) simultaneamente

echo "🚀 Iniciando MandarIA..."

# Inicia servidor Baileys em background
echo "📱 Iniciando servidor WhatsApp Baileys..."
node whatsapp_baileys.js &
BAILEYS_PID=$!

# Aguarda 3 segundos para o Baileys iniciar
sleep 3

# Inicia servidor Flask
echo "🌐 Iniciando servidor Flask..."
python app.py &
FLASK_PID=$!

# Função para encerrar processos ao receber SIGTERM
cleanup() {
    echo "🛑 Encerrando servidores..."
    kill $BAILEYS_PID $FLASK_PID
    exit 0
}

trap cleanup SIGTERM SIGINT

# Aguarda os processos
wait
