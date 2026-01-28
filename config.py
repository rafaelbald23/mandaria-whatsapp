# Configurações do Robô de WhatsApp Web
import os
from pathlib import Path

# Diretórios (relativos à pasta web)
BASE_DIR = Path(__file__).parent
PLANILHAS_DIR = BASE_DIR / "Planilhas"
LOGS_DIR = BASE_DIR / "Logs"
IMAGENS_DIR = BASE_DIR / "static" / "images"

# Criar diretórios se não existirem
PLANILHAS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
IMAGENS_DIR.mkdir(exist_ok=True)

# Configurações de envio
MAX_TENTATIVAS = 3
TIMEOUT_CARREGAMENTO = 20
TIMEOUT_ELEMENTO = 15
TIMEOUT_LOGIN = 120  # 2 minutos para escanear QR Code
INTERVALO_ENTRE_MENSAGENS = 5  # Intervalo entre mensagens
LIMITE_NUMEROS_AVISO = 200

# Configurações de interface
WINDOW_TITLE = "Robô de Disparo WhatsApp - monitorIA"
THEME_COLOR_PRIMARY = "#201D2E"
THEME_COLOR_SECONDARY = "#A4832B"
THEME_COLOR_SUCCESS = "#2a9d8f"
THEME_COLOR_ERROR = "#e76f51"
THEME_COLOR_WARNING = "#FF5733"

# Arquivo de usuários (será criado se não existir)
USUARIOS_FILE = BASE_DIR / "usuarios.json"

# XPaths do WhatsApp Web
XPATH_SEND_BUTTON = "//span[@data-icon='send']"
XPATH_INVALID_NUMBER = "//*[contains(text(), 'O número de telefone compartilhado por url é inválido')]"
XPATH_CHAT_LOADED = "//div[@contenteditable='true'][@data-tab='10']"
