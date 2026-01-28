# Robô WhatsApp Web - Docker com Node.js e Python

FROM python:3.11-slim

# Instala Node.js e dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia package.json e instala dependências Node.js
COPY baileys_package.json package.json
RUN npm install

# Copia requirements Python
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia aplicação
COPY . .

# Torna o script executável
RUN chmod +x start.sh

# Cria diretórios necessários
RUN mkdir -p Planilhas Logs baileys_session

# Expõe portas (Flask e Baileys)
EXPOSE 5000 3000

# Comando de inicialização
CMD ["./start.sh"]
