"""
API para comunicação com Agente Local
Rotas para o agente buscar fila e enviar resultados
"""

from flask import Blueprint, request, jsonify
from functools import wraps
import json
from pathlib import Path
from datetime import datetime
import uuid

api_agente = Blueprint('api_agente', __name__)

# Armazena fila de envios
FILA_FILE = Path('fila_envios.json')
RESULTADOS_FILE = Path('resultados_envios.json')

def carregar_fila():
    """Carrega fila de envios"""
    if FILA_FILE.exists():
        return json.loads(FILA_FILE.read_text())
    return []

def salvar_fila(fila):
    """Salva fila de envios"""
    FILA_FILE.write_text(json.dumps(fila, indent=2))

def carregar_resultados():
    """Carrega resultados"""
    if RESULTADOS_FILE.exists():
        return json.loads(RESULTADOS_FILE.read_text())
    return {}

def salvar_resultados(resultados):
    """Salva resultados"""
    RESULTADOS_FILE.write_text(json.dumps(resultados, indent=2))

def verificar_api_key(f):
    """Decorator para verificar API Key"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'API Key inválida'}), 401
        
        # Por enquanto, aceita qualquer key (você pode adicionar validação)
        return f(*args, **kwargs)
    
    return decorated

@api_agente.route('/api/agente/fila', methods=['GET'])
@verificar_api_key
def buscar_fila():
    """Retorna envios pendentes na fila"""
    fila = carregar_fila()
    
    # Filtra apenas pendentes
    pendentes = [e for e in fila if e.get('status') == 'pendente']
    
    return jsonify({'envios': pendentes})

@api_agente.route('/api/agente/status', methods=['POST'])
@verificar_api_key
def atualizar_status():
    """Atualiza status de um envio"""
    data = request.get_json()
    envio_id = data.get('envio_id')
    status = data.get('status')
    mensagem = data.get('mensagem', '')
    
    fila = carregar_fila()
    
    for envio in fila:
        if envio['id'] == envio_id:
            envio['status'] = status
            envio['mensagem'] = mensagem
            envio['atualizado_em'] = datetime.now().isoformat()
            break
    
    salvar_fila(fila)
    
    return jsonify({'success': True})

@api_agente.route('/api/agente/progresso', methods=['POST'])
@verificar_api_key
def enviar_progresso():
    """Recebe progresso do envio"""
    data = request.get_json()
    envio_id = data.get('envio_id')
    
    # Emite via SocketIO para atualizar interface em tempo real
    from app import socketio
    socketio.emit('progresso_update', {
        'session_id': envio_id,
        'atual': data.get('atual'),
        'total': data.get('total'),
        'contato': data.get('numero')
    })
    
    return jsonify({'success': True})

@api_agente.route('/api/agente/resultado', methods=['POST'])
@verificar_api_key
def enviar_resultado():
    """Recebe resultado individual"""
    data = request.get_json()
    envio_id = data.get('envio_id')
    
    # Salva resultado
    resultados = carregar_resultados()
    
    if envio_id not in resultados:
        resultados[envio_id] = []
    
    resultados[envio_id].append({
        'numero': data.get('numero'),
        'sucesso': data.get('sucesso'),
        'motivo': data.get('motivo'),
        'timestamp': datetime.now().isoformat()
    })
    
    salvar_resultados(resultados)
    
    # Emite via SocketIO
    from app import socketio
    socketio.emit('mensagem_enviada', {
        'session_id': envio_id,
        'contato': data.get('numero'),
        'sucesso': data.get('sucesso'),
        'motivo': data.get('motivo')
    })
    
    return jsonify({'success': True})

@api_agente.route('/api/agente/finalizar', methods=['POST'])
@verificar_api_key
def finalizar_envio():
    """Finaliza um envio"""
    data = request.get_json()
    envio_id = data.get('envio_id')
    
    fila = carregar_fila()
    
    for envio in fila:
        if envio['id'] == envio_id:
            envio['status'] = 'concluido'
            envio['total'] = data.get('total')
            envio['enviados'] = data.get('enviados')
            envio['falhas'] = data.get('falhas')
            envio['finalizado_em'] = datetime.now().isoformat()
            break
    
    salvar_fila(fila)
    
    # Emite via SocketIO
    from app import socketio
    socketio.emit('envio_concluido', {
        'session_id': envio_id,
        'total': data.get('total'),
        'enviados': data.get('enviados'),
        'falhas': data.get('falhas')
    })
    
    return jsonify({'success': True})

@api_agente.route('/api/agente/adicionar', methods=['POST'])
def adicionar_fila():
    """Adiciona envio na fila (chamado pela interface web)"""
    data = request.get_json()
    
    envio = {
        'id': str(uuid.uuid4()),
        'usuario': data.get('usuario'),
        'numeros': data.get('numeros'),
        'mensagens': data.get('mensagens'),
        'imagem': data.get('imagem'),
        'status': 'pendente',
        'criado_em': datetime.now().isoformat()
    }
    
    fila = carregar_fila()
    fila.append(envio)
    salvar_fila(fila)
    
    return jsonify({'success': True, 'envio_id': envio['id']})
