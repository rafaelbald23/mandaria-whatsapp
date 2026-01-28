from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import config
from utils import configurar_logger, formatar_mensagem_whatsapp

logger = configurar_logger("whatsapp_sender")

class WhatsAppSender:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def inicializar_driver(self):
        """Inicializa o Chrome WebDriver com configurações otimizadas"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Mantém sessão do WhatsApp
            user_data_dir = config.BASE_DIR / "chrome_profile"
            user_data_dir.mkdir(exist_ok=True)
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, config.TIMEOUT_ELEMENTO)
            
            logger.info("Driver inicializado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar driver: {e}")
            return False
    
    def aguardar_login(self):
        """Aguarda o usuário fazer login no WhatsApp Web"""
        try:
            self.driver.get("https://web.whatsapp.com/")
            logger.info("Aguardando login no WhatsApp Web...")
            
            # Cria um wait especial com timeout maior para login
            wait_login = WebDriverWait(self.driver, config.TIMEOUT_LOGIN)
            
            # Aguarda até que o chat esteja carregado (indica login bem-sucedido)
            logger.info(f"Você tem {config.TIMEOUT_LOGIN} segundos para escanear o QR Code...")
            
            # Tenta múltiplos seletores para detectar login
            login_detectado = False
            tempo_inicio = time.time()
            
            while not login_detectado and (time.time() - tempo_inicio) < config.TIMEOUT_LOGIN:
                try:
                    # Verifica se o QR Code ainda está presente
                    qr_code = self.driver.find_elements(By.XPATH, "//canvas[@aria-label='Scan me!']")
                    
                    # Se não há QR Code, provavelmente já logou
                    if not qr_code:
                        # Verifica se a interface principal está carregada
                        elementos_principais = [
                            "//div[@id='side']",  # Sidebar de conversas
                            "//div[@contenteditable='true'][@data-tab='3']",  # Campo de busca
                            "//div[contains(@class, 'landing-main')]",  # Tela principal
                            "//header[contains(@class, 'header')]"  # Header
                        ]
                        
                        for xpath in elementos_principais:
                            elementos = self.driver.find_elements(By.XPATH, xpath)
                            if elementos:
                                logger.info("Login detectado! Interface principal carregada.")
                                login_detectado = True
                                break
                    
                    if not login_detectado:
                        time.sleep(1)  # Aguarda 1 segundo antes de verificar novamente
                        
                except Exception as e:
                    logger.debug(f"Verificando login: {e}")
                    time.sleep(1)
            
            if login_detectado:
                logger.info("Login realizado com sucesso!")
                time.sleep(3)  # Aguarda estabilização
                return True
            else:
                logger.error(f"Timeout ao aguardar login - {config.TIMEOUT_LOGIN} segundos excedidos")
                return False
            
        except TimeoutException:
            logger.error(f"Timeout ao aguardar login - {config.TIMEOUT_LOGIN} segundos excedidos")
            return False
        except Exception as e:
            logger.error(f"Erro ao aguardar login: {e}")
            return False
    
    def enviar_imagem(self, caminho_imagem):
        """Envia uma imagem colando no campo de texto"""
        try:
            logger.info(f"Enviando imagem: {caminho_imagem}")
            
            # Encontra o botão de anexo (clipe)
            xpaths_anexo = [
                "//span[@data-icon='plus']",
                "//span[@data-icon='clip']",
                "//button[@aria-label='Anexar']",
                "//*[@data-icon='plus']"
            ]
            
            botao_anexo = None
            for xpath in xpaths_anexo:
                try:
                    botao_anexo = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    if botao_anexo:
                        logger.info(f"Botão de anexo encontrado: {xpath}")
                        botao_anexo.click()
                        time.sleep(1)
                        break
                except:
                    continue
            
            if not botao_anexo:
                logger.warning("Botão de anexo não encontrado")
                return False
            
            # Encontra o input de arquivo para imagens
            try:
                input_arquivo = self.driver.find_element(By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
                input_arquivo.send_keys(str(caminho_imagem))
                time.sleep(2)
                logger.info("Imagem carregada")
            except Exception as e:
                logger.error(f"Erro ao carregar imagem: {e}")
                return False
            
            # Aguarda preview e clica no botão de enviar
            xpaths_enviar = [
                "//span[@data-icon='send']",
                "//button[@aria-label='Enviar']",
                "//*[@data-icon='send']"
            ]
            
            for xpath in xpaths_enviar:
                try:
                    botao_enviar = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    botao_enviar.click()
                    logger.info("Imagem enviada com sucesso")
                    time.sleep(2)
                    return True
                except:
                    continue
            
            logger.warning("Botão de enviar imagem não encontrado")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao enviar imagem: {e}")
            return False
    
    def enviar_mensagem(self, numero, mensagem, nome=''):
        """Envia uma mensagem para um número específico"""
        tentativas = 0
        
        while tentativas < config.MAX_TENTATIVAS:
            try:
                # Formata mensagem
                mensagem_formatada = formatar_mensagem_whatsapp(mensagem, nome)
                
                # Monta URL com a mensagem na URL
                url = f'https://web.whatsapp.com/send?phone={numero}&text={mensagem_formatada}'
                
                # Navega para o chat
                self.driver.get(url)
                
                # Aguarda carregamento
                time.sleep(config.TIMEOUT_CARREGAMENTO / 2)
                
                # Verifica se número é inválido
                try:
                    self.driver.find_element(By.XPATH, config.XPATH_INVALID_NUMBER)
                    logger.warning(f"Número inválido: {numero}")
                    return False, "Número inválido"
                except NoSuchElementException:
                    pass
                
                # Aguarda botão de enviar
                logger.info(f"Procurando botão de enviar para {numero}...")
                
                botao_encontrado = False
                xpaths_botao = [
                    "//span[@data-icon='send']",
                    "//button[@aria-label='Enviar']",
                    "//button[contains(@aria-label, 'Send')]",
                    "//*[@data-icon='send']",
                    "//button[contains(@class, 'send')]"
                ]
                
                for xpath in xpaths_botao:
                    try:
                        botao_enviar = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        if botao_enviar:
                            logger.info(f"Botão encontrado com xpath: {xpath}")
                            botao_enviar.click()
                            botao_encontrado = True
                            break
                    except:
                        continue
                
                if not botao_encontrado:
                    logger.warning(f"Botão de enviar não encontrado para {numero}")
                    tentativas += 1
                    continue
                
                # Aguarda confirmação de envio
                time.sleep(2)
                
                logger.info(f"Mensagem enviada para {numero} ({nome})")
                return True, "Enviado com sucesso"
                
            except TimeoutException:
                tentativas += 1
                logger.warning(f"Timeout ao enviar para {numero} - Tentativa {tentativas}/{config.MAX_TENTATIVAS}")
                
                if tentativas < config.MAX_TENTATIVAS:
                    time.sleep(3)
                    
            except Exception as e:
                tentativas += 1
                logger.error(f"Erro ao enviar para {numero}: {e} - Tentativa {tentativas}/{config.MAX_TENTATIVAS}")
                
                if tentativas < config.MAX_TENTATIVAS:
                    time.sleep(3)
        
        return False, f"Falha após {config.MAX_TENTATIVAS} tentativas"
    
    def enviar_lote(self, planilha, mensagem, callback_progresso=None):
        """Envia mensagens para um lote de contatos"""
        numeros_nao_enviados = []
        total = len(planilha)
        
        for index, row in planilha.iterrows():
            nome = row.get('Nome', '')
            contato = row['Contato']
            
            # Callback de progresso
            if callback_progresso:
                callback_progresso(index + 1, total, contato, nome)
            
            # Envia mensagem
            sucesso, motivo = self.enviar_mensagem(contato, mensagem, nome)
            
            if not sucesso:
                numeros_nao_enviados.append(contato)
            
            # Intervalo entre mensagens
            if index < total - 1:
                time.sleep(config.INTERVALO_ENTRE_MENSAGENS)
        
        return numeros_nao_enviados
    
    def enviar_lote(self, planilha, mensagem, callback_progresso=None):
        """Envia mensagens para um lote de contatos"""
        numeros_nao_enviados = []
        total = len(planilha)
        
        for index, row in planilha.iterrows():
            nome = row.get('Nome', '')
            contato = row['Contato']
            
            # Callback de progresso
            if callback_progresso:
                callback_progresso(index + 1, total, contato, nome)
            
            # Envia mensagem
            sucesso, motivo = self.enviar_mensagem(contato, mensagem, nome)
            
            if not sucesso:
                numeros_nao_enviados.append(contato)
            
            # Intervalo entre mensagens
            if index < total - 1:
                time.sleep(config.INTERVALO_ENTRE_MENSAGENS)
        
        return numeros_nao_enviados
    
    def fechar(self):
        """Fecha o driver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Driver fechado")
            except Exception as e:
                logger.error(f"Erro ao fechar driver: {e}")
