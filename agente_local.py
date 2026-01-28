"""
Agente Local MandarIA
Roda na máquina do cliente e executa disparos
Sincroniza com o servidor web (Railway)
"""

import requests
import time
import json
from pathlib import Path
from whatsapp_sender import WhatsAppSender
from utils import configurar_logger
import sys
import os

logger = configurar_logger("agente_local")

class AgenteLocal:
    def __init__(self, servidor_url, api_key):
        self.servidor_url = servidor_url.rstrip('/')
        self.api_key = api_key
        self.sender = None
        self.rodando = True
        
        logger.info(f"Agente Local iniciado - Servidor: {self.servidor_url}")
    
    def conectar_whatsapp(self):
        """Conecta ao WhatsApp Web"""
        try:
            logger.info("Conectando ao WhatsApp Web...")
            self.sender = WhatsAppSender()
            
            if not self.sender.inicializar_driver():
                logger.error("Falha ao inicializar navegador")
                return False
            
            if not self.sender.aguardar_login():
                logger.error("Falha ao fazer login")
                return False
            
            logger.info("✅ WhatsApp conectado com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao conectar WhatsApp: {e}")
            return False
    
    def buscar_fila(self):
        """Busca mensagens pendentes no servidor"""
        try:
            response = requests.get(
                f"{self.servidor_url}/api/agente/fila",
                headers={'Authorization': f'Bearer {self.api_key}'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('envios', [])
            
            return []
            
        except Exception as e:
            logger.error(f"Erro ao buscar fila: {e}")
            return []
    
    def processar_envio(self, envio):
        """Processa um envio da fila"""
        try:
            envio_id = envio['id']
            numeros = envio['numeros']
            mensagens = envio['mensagens']
            imagem = envio.get('imagem')
            
            logger.info(f"Processando envio {envio_id}: {len(numeros)} números, {len(mensagens)} mensagens")
            
            # Atualiza status para "processando"
            self.atualizar_status(envio_id, 'processando')
            
            total = len(numeros) * len(mensagens)
            processados = 0
            enviados = 0
            falhas = 0
            
            for numero in numeros:
                for mensagem in mensagens:
                    processados += 1
                    
                    # Envia progresso
                    self.enviar_progresso(envio_id, processados, total, numero)
                    
                    # Envia mensagem
                    sucesso, motivo = self.sender.enviar_mensagem(numero, mensagem)
                    
                    if sucesso:
                        enviados += 1
                    else:
                        falhas += 1
                    
                    # Envia resultado individual
                    self.enviar_resultado_individual(envio_id, numero, sucesso, motivo)
                
                # Envia imagem se houver
                if imagem and enviados > 0:
                    # Download da imagem
                    img_path = self.baixar_imagem(imagem)
                    if img_path:
                        self.sender.enviar_imagem(img_path)
                        os.remove(img_path)
            
            # Finaliza envio
            self.finalizar_envio(envio_id, total, enviados, falhas)
            logger.info(f"✅ Envio {envio_id} concluído: {enviados}/{total} enviados")
            
        except Exception as e:
            logger.error(f"Erro ao processar envio: {e}")
            self.atualizar_status(envio['id'], 'erro', str(e))
    
    def atualizar_status(self, envio_id, status, mensagem=''):
        """Atualiza status do envio no servidor"""
        try:
            requests.post(
                f"{self.servidor_url}/api/agente/status",
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={
                    'envio_id': envio_id,
                    'status': status,
                    'mensagem': mensagem
                },
                timeout=5
            )
        except Exception as e:
            logger.error(f"Erro ao atualizar status: {e}")
    
    def enviar_progresso(self, envio_id, atual, total, numero):
        """Envia progresso do envio"""
        try:
            requests.post(
                f"{self.servidor_url}/api/agente/progresso",
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={
                    'envio_id': envio_id,
                    'atual': atual,
                    'total': total,
                    'numero': numero
                },
                timeout=5
            )
        except Exception as e:
            logger.error(f"Erro ao enviar progresso: {e}")
    
    def enviar_resultado_individual(self, envio_id, numero, sucesso, motivo):
        """Envia resultado individual"""
        try:
            requests.post(
                f"{self.servidor_url}/api/agente/resultado",
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={
                    'envio_id': envio_id,
                    'numero': numero,
                    'sucesso': sucesso,
                    'motivo': motivo
                },
                timeout=5
            )
        except Exception as e:
            logger.error(f"Erro ao enviar resultado: {e}")
    
    def finalizar_envio(self, envio_id, total, enviados, falhas):
        """Finaliza envio"""
        try:
            requests.post(
                f"{self.servidor_url}/api/agente/finalizar",
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={
                    'envio_id': envio_id,
                    'total': total,
                    'enviados': enviados,
                    'falhas': falhas
                },
                timeout=5
            )
        except Exception as e:
            logger.error(f"Erro ao finalizar envio: {e}")
    
    def baixar_imagem(self, url_imagem):
        """Baixa imagem do servidor"""
        try:
            response = requests.get(url_imagem, timeout=10)
            if response.status_code == 200:
                temp_path = Path('temp_image.jpg')
                temp_path.write_bytes(response.content)
                return temp_path
            return None
        except Exception as e:
            logger.error(f"Erro ao baixar imagem: {e}")
            return None
    
    def executar(self):
        """Loop principal do agente"""
        logger.info("🚀 Agente Local em execução...")
        
        # Conecta ao WhatsApp
        if not self.conectar_whatsapp():
            logger.error("❌ Falha ao conectar WhatsApp. Encerrando...")
            return
        
        # Loop de verificação
        while self.rodando:
            try:
                # Busca fila
                envios = self.buscar_fila()
                
                if envios:
                    logger.info(f"📬 {len(envios)} envio(s) na fila")
                    
                    for envio in envios:
                        self.processar_envio(envio)
                
                # Aguarda 5 segundos antes de verificar novamente
                time.sleep(5)
                
            except KeyboardInterrupt:
                logger.info("⏹️ Encerrando agente...")
                self.rodando = False
            except Exception as e:
                logger.error(f"Erro no loop principal: {e}")
                time.sleep(10)
        
        # Fecha WhatsApp
        if self.sender:
            self.sender.fechar()
        
        logger.info("👋 Agente Local encerrado")


def main():
    """Função principal"""
    print("""
    ╔═══════════════════════════════════════╗
    ║   MandarIA - Agente Local v3.0       ║
    ║   Desenvolvido por MonitorIA         ║
    ╚═══════════════════════════════════════╝
    """)
    
    # Configurações
    servidor_url = input("URL do servidor (ex: https://seu-mandaria.railway.app): ").strip()
    api_key = input("Chave de API: ").strip()
    
    if not servidor_url or not api_key:
        print("❌ URL e API Key são obrigatórios!")
        return
    
    # Salva configurações
    config_file = Path('agente_config.json')
    config_file.write_text(json.dumps({
        'servidor_url': servidor_url,
        'api_key': api_key
    }))
    
    print("\n✅ Configurações salvas!")
    print("🚀 Iniciando agente...\n")
    
    # Inicia agente
    agente = AgenteLocal(servidor_url, api_key)
    agente.executar()


if __name__ == '__main__':
    # Verifica se tem configuração salva
    config_file = Path('agente_config.json')
    
    if config_file.exists():
        config = json.loads(config_file.read_text())
        agente = AgenteLocal(config['servidor_url'], config['api_key'])
        agente.executar()
    else:
        main()
