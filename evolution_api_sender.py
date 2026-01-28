"""
WhatsApp Sender usando Evolution API
Substitui o Selenium para funcionar no Railway
"""

import requests
import time
import base64
from pathlib import Path
from utils import configurar_logger, formatar_mensagem_whatsapp
import config
import os

logger = configurar_logger("evolution_api_sender")

class EvolutionAPISender:
    def __init__(self):
        # Configurações da Evolution API (via variáveis de ambiente)
        self.base_url = os.environ.get('EVOLUTION_API_URL', 'http://localhost:8080')
        self.api_key = os.environ.get('EVOLUTION_API_KEY', '')
        self.instance_name = os.environ.get('EVOLUTION_INSTANCE', 'mandaria')
        
        self.headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        
        self.connected = False
        
    def inicializar_driver(self):
        """Verifica se a instância existe e está conectada"""
        try:
            logger.info("Verificando conexão com Evolution API...")
            
            # Verifica status da instância
            response = requests.get(
                f"{self.base_url}/instance/connectionState/{self.instance_name}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                state = data.get('instance', {}).get('state')
                
                if state == 'open':
                    logger.info("Instância já conectada!")
                    self.connected = True
                    return True
                else:
                    logger.info(f"Instância em estado: {state}")
                    return True  # Retorna True para permitir aguardar login
            else:
                logger.warning(f"Instância não encontrada, criando nova...")
                return self._criar_instancia()
                
        except Exception as e:
            logger.error(f"Erro ao verificar instância: {e}")
            return False
    
    def _criar_instancia(self):
        """Cria uma nova instância na Evolution API"""
        try:
            payload = {
                "instanceName": self.instance_name,
                "qrcode": True,
                "integration": "WHATSAPP-BAILEYS"
            }
            
            response = requests.post(
                f"{self.base_url}/instance/create",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                logger.info("Instância criada com sucesso!")
                return True
            else:
                logger.error(f"Erro ao criar instância: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao criar instância: {e}")
            return False
    
    def aguardar_login(self):
        """Aguarda o usuário escanear o QR Code"""
        try:
            logger.info("Aguardando login via QR Code...")
            
            # Obtém QR Code
            qr_code = self._obter_qr_code()
            if not qr_code:
                logger.error("Não foi possível obter QR Code")
                return False
            
            # Aguarda conexão (máximo 2 minutos)
            tempo_inicio = time.time()
            timeout = config.TIMEOUT_LOGIN
            
            while (time.time() - tempo_inicio) < timeout:
                # Verifica status da conexão
                response = requests.get(
                    f"{self.base_url}/instance/connectionState/{self.instance_name}",
                    headers=self.headers,
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    state = data.get('instance', {}).get('state')
                    
                    if state == 'open':
                        logger.info("Login realizado com sucesso!")
                        self.connected = True
                        return True
                
                time.sleep(2)  # Verifica a cada 2 segundos
            
            logger.error("Timeout ao aguardar login")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao aguardar login: {e}")
            return False
    
    def _obter_qr_code(self):
        """Obtém o QR Code da instância"""
        try:
            response = requests.get(
                f"{self.base_url}/instance/connect/{self.instance_name}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                qr_code = data.get('qrcode', {}).get('base64')
                
                if qr_code:
                    logger.info("QR Code obtido com sucesso")
                    # Aqui você pode salvar o QR Code ou enviá-lo via websocket
                    return qr_code
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter QR Code: {e}")
            return None
    
    def enviar_mensagem(self, numero, mensagem, nome=''):
        """Envia uma mensagem para um número específico"""
        try:
            if not self.connected:
                logger.error("Instância não conectada")
                return False, "Não conectado"
            
            # Formata mensagem
            mensagem_formatada = formatar_mensagem_whatsapp(mensagem, nome)
            
            # Formata número (remove caracteres especiais)
            numero_limpo = ''.join(filter(str.isdigit, numero))
            
            # Adiciona código do país se não tiver
            if not numero_limpo.startswith('55'):
                numero_limpo = '55' + numero_limpo
            
            # Payload para enviar mensagem
            payload = {
                "number": numero_limpo,
                "text": mensagem_formatada
            }
            
            # Envia mensagem
            response = requests.post(
                f"{self.base_url}/message/sendText/{self.instance_name}",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"Mensagem enviada para {numero} ({nome})")
                time.sleep(config.INTERVALO_ENTRE_MENSAGENS)
                return True, "Enviado com sucesso"
            else:
                logger.error(f"Erro ao enviar para {numero}: {response.text}")
                return False, f"Erro: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return False, str(e)
    
    def enviar_imagem(self, caminho_imagem):
        """Envia uma imagem"""
        try:
            if not self.connected:
                logger.error("Instância não conectada")
                return False
            
            # Lê imagem e converte para base64
            with open(caminho_imagem, 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Obtém extensão do arquivo
            extensao = Path(caminho_imagem).suffix.lower()
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif'
            }
            mime_type = mime_types.get(extensao, 'image/jpeg')
            
            # Payload para enviar imagem
            payload = {
                "mediatype": "image",
                "mimetype": mime_type,
                "media": img_base64,
                "fileName": Path(caminho_imagem).name
            }
            
            # Envia imagem
            response = requests.post(
                f"{self.base_url}/message/sendMedia/{self.instance_name}",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                logger.info("Imagem enviada com sucesso")
                return True
            else:
                logger.error(f"Erro ao enviar imagem: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar imagem: {e}")
            return False
    
    def fechar(self):
        """Fecha a conexão (logout)"""
        try:
            # Não fazemos logout automático para manter a sessão
            logger.info("Mantendo sessão ativa")
        except Exception as e:
            logger.error(f"Erro ao fechar: {e}")
