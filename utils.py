import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
import re
import config

def configurar_logger(nome="whatsapp_bot"):
    """Configura o sistema de logs"""
    log_file = config.LOGS_DIR / f"{nome}_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(nome)

def validar_numero_telefone(numero):
    """Valida e formata número de telefone"""
    if pd.isna(numero):
        return None
    
    # Remove caracteres não numéricos
    numero_limpo = re.sub(r'\D', '', str(numero))
    
    # Verifica se tem tamanho válido (10-15 dígitos)
    if len(numero_limpo) < 10 or len(numero_limpo) > 15:
        return None
    
    return numero_limpo

def carregar_planilha(caminho):
    """Carrega e valida planilha de contatos"""
    try:
        df = pd.read_excel(caminho)
        
        # Verifica colunas obrigatórias
        if 'Contato' not in df.columns:
            raise ValueError("Planilha deve conter coluna 'Contato'")
        
        # Adiciona coluna Nome se não existir
        if 'Nome' not in df.columns:
            df['Nome'] = ''
        
        # Valida e limpa números
        df['Contato'] = df['Contato'].apply(validar_numero_telefone)
        df = df.dropna(subset=['Contato'])
        
        # Remove duplicatas
        df = df.drop_duplicates(subset=['Contato'])
        
        return df
    
    except Exception as e:
        raise Exception(f"Erro ao carregar planilha: {str(e)}")

def salvar_resultados(planilha, numeros_nao_enviados, caminho_saida=None):
    """Salva planilha com status de envio"""
    if caminho_saida is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        caminho_saida = config.PLANILHAS_DIR / f"Resultado_{timestamp}.xlsx"
    
    # Cria cópia da planilha para não modificar a original
    df_resultado = planilha.copy()
    
    # Adiciona colunas de status
    df_resultado['Status'] = 'Enviado'
    df_resultado['Motivo'] = 'Enviado com sucesso'
    df_resultado['Data_Envio'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Marca números não enviados
    for numero in numeros_nao_enviados:
        mask = df_resultado['Contato'] == numero
        df_resultado.loc[mask, 'Status'] = 'Não Enviado'
        df_resultado.loc[mask, 'Motivo'] = 'Falha no envio'
    
    # Salva arquivo
    df_resultado.to_excel(caminho_saida, index=False)
    
    return caminho_saida

def formatar_mensagem_whatsapp(mensagem, nome=''):
    """Formata mensagem para URL do WhatsApp"""
    # Substitui placeholder pelo nome
    if '{}' in mensagem and nome:
        mensagem = mensagem.replace('{}', nome)
    
    # Codifica para URL
    mensagem_codificada = mensagem.replace('\n', '%0A')
    
    return mensagem_codificada

def validar_mensagem(mensagem):
    """Valida se a mensagem está no formato correto"""
    if not mensagem or not mensagem.strip():
        return False, "Mensagem não pode estar vazia"
    
    if len(mensagem) > 4096:
        return False, "Mensagem muito longa (máximo 4096 caracteres)"
    
    return True, ""
