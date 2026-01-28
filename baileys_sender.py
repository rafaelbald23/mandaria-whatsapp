"""
WhatsApp Sender usando Baileys via subprocess
Integra Node.js Baileys com Python Flask
"""

import subprocess
import requests
import time
import json
import os
from pathlib import Path
from utils import configurar_logger, formatar_mensagem_whatsapp
import config

logger = configurar_logger("baileys_sender")

class BaileysSender:
    def __init__(self):
        self.baileys_url = "http://localhost:3000"
        self.baileys_process = None
        self.connected = False
        
    def inicializar_driver(self):
        """Inicia o servidor Baileys"""
        try:
            logger.info("Iniciando servidor Baileys...")
            
            # Verifica se já está rodando
            try:
                response = requests.get(f"{self.baileys_url}/status", timeout=2)
                if response.status_code == 200:
                    logger.info("Servidor Baileys já está rodando")
                    data = response.json()
                    self.connected = data.get('connected', False)
                    return True
            except:
                pass
            
            # Inicia o servidor Baileys
            baileys_dir = Path(__file__).parent
            
            # Verifica se node_modules existe
            if not (baileys_dir / "node_modules").exists():
                logger.info("Instalando dependências do Baileys...")
                subprocess.run(
                    ["npm", "install", "--prefix", str(baileys_dir)],
                    check=True,
                    capture_output=True
                )
            
            # Inicia servidor em background
            self.baileys_process = subprocess.Popen(
                ["node", "whatsapp_baileys.js"],
                cwd=str(baileys_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Aguarda servidor iniciar
            time.sleep(5)
            
            # Verifica se iniciou
            try:
                response = requests.get(f"{self.baileys_url}/status", timeout=5)
                if response.status_code == 200:
                    logger.info("Servidor Baileys iniciado com sucesso!")
                    return True
            except:
                logger.error("Falha ao iniciar servidor Baileys")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao inicializar Baileys: {e}")
            return False
    
    def aguardar_login(self):
        """Aguarda o usuário escanear o QR Code"""
        try:
            logger.info("Aguardando login via QR Code...")
            
            tempo_inicio = time.time()
            timeout = config.TIMEOUT_LOGIN
            
            while (time.time() - tempo_inicio) < timeout:
                try:
                    response = requests.get(f"{self.baileys_url}/status", timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if data.get('connected'):
                            logger.info("Login realizado com sucesso!")
                            self.connected = True
                            return True
                        
                        # Se tem QR Code, continua aguardando
                        if data.get('hasQR'):
                            logger.debug("QR Code disponível, aguardando scan...")
                    
                except Exception as e:
                    logger.debug(f"Verificando status: {e}")
                
                time.sleep(2)
            
            logger.error("Timeout ao aguardar login")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao aguardar login: {e}")
            return False
    
    def obter_qr_code(self):
        """Obtém o QR Code atual"""
        try:
            response = requests.get(f"{self.baileys_url}/qr", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('qr')
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter QR Code: {e}")
            return None
    
    def enviar_mensagem(self, numero, mensagem, nome=''):
        """Envia uma mensagem para um número específico"""
        try:
            if not self.connected:
                logger.error("WhatsApp não conectado")
                return False, "Não conectado"
            
            # Formata mensagem
            mensagem_formatada = formatar_mensagem_whatsapp(mensagem, nome)
            
            # Formata número (remove caracteres especiais)
            numero_limpo = ''.join(filter(str.isdigit, numero))
            
            # Adiciona código do país se não tiver
            if not numero_limpo.startswith('55'):
                numero_limpo = '55' + numero_limpo
            
            # Envia mensagem
            payload = {
                "number": numero_limpo,
                "message": mensagem_formatada
            }
            
            response = requests.post(
                f"{self.baileys_url}/send",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"Mensagem enviada para {numero} ({nome})")
                time.sleep(config.INTERVALO_ENTRE_MENSAGENS)
                return True, "Enviado com sucesso"
            else:
                error_msg = response.json().get('error', 'Erro desconhecido')
                logger.error(f"Erro ao enviar para {numero}: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return False, str(e)
    
    def enviar_imagem(self, caminho_imagem):
        """Envia uma imagem"""
        try:
            if not self.connected:
                logger.error("WhatsApp não conectado")
                return False
            
            # Lê imagem e converte para base64
            import base64
            with open(caminho_imagem, 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Envia imagem
            payload = {
                "image": img_base64,
                "caption": ""
            }
            
            response = requests.post(
                f"{self.baileys_url}/send-image",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("Imagem enviada com sucesso")
                return True
            else:
                logger.error(f"Erro ao enviar imagem: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar imagem: {e}")
            return False
    
    def fechar(self):
        """Fecha o servidor Baileys"""
        try:
            # Não fecha o servidor para manter a sessão
            logger.info("Mantendo servidor Baileys ativo")
        except Exception as e:
            logger.error(f"Erro ao fechar: {e}")
