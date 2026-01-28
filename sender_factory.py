"""
Factory para criar o sender apropriado (Selenium ou Baileys)
"""

import os
from utils import configurar_logger

logger = configurar_logger("sender_factory")

def criar_sender():
    """
    Cria o sender apropriado baseado nas variáveis de ambiente
    
    Se USE_BAILEYS=true ou está no Railway, usa Baileys
    Caso contrário, usa Selenium (para desenvolvimento local)
    """
    use_baileys = os.environ.get('USE_BAILEYS', 'true').lower() == 'true'
    
    # Detecta automaticamente se está no Railway
    is_railway = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_PROJECT_ID')
    
    if use_baileys or is_railway:
        logger.info("Usando Baileys Sender (100% Web)")
        from baileys_sender import BaileysSender
        return BaileysSender()
    else:
        logger.info("Usando Selenium Sender (desenvolvimento local)")
        from whatsapp_sender import WhatsAppSender
        return WhatsAppSender()
