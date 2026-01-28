"""
Factory para criar o sender apropriado (Selenium ou Evolution API)
"""

import os
from utils import configurar_logger

logger = configurar_logger("sender_factory")

def criar_sender():
    """
    Cria o sender apropriado baseado nas variáveis de ambiente
    
    Se USE_EVOLUTION_API=true, usa Evolution API
    Caso contrário, usa Selenium (para desenvolvimento local)
    """
    use_evolution = os.environ.get('USE_EVOLUTION_API', 'false').lower() == 'true'
    
    # Detecta automaticamente se está no Railway
    is_railway = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_PROJECT_ID')
    
    if use_evolution or is_railway:
        logger.info("Usando Evolution API Sender")
        from evolution_api_sender import EvolutionAPISender
        return EvolutionAPISender()
    else:
        logger.info("Usando Selenium Sender (desenvolvimento local)")
        from whatsapp_sender import WhatsAppSender
        return WhatsAppSender()
