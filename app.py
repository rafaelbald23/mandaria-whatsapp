"""
MandarIA - Flask Application
Versão Web 3.0 - Desenvolvido por MonitorIA
Sistema 100% Web - Sem Desktop
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
from functools import wraps
import os
from pathlib import Path
import time

# Importa módulos locais
from auth import AuthManager
from utils import carregar_planilha, salvar_resultados, validar_mensagem, validar_numero_telefone, configurar_logger
from sender_factory import criar_sender
from api_agente import api_agente
import config
import pandas as pd
from datetime import datetime
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'monitoria-whatsapp-robot-secret-key-2026'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Registra blueprint da API do agente
app.register_blueprint(api_agente)

# Configuração do SocketIO para produção
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)

# Inicializa componentes
auth_manager = AuthManager()
logger = configurar_logger("web_app")

# Armazena sessões ativas de envio
active_sessions = {}

# Filtro customizado para formatar timestamp
@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    """Converte timestamp para data formatada"""
    try:
        from datetime import datetime
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%d/%m/%Y às %H:%M')
    except:
        return 'Data desconhecida'

def login_required(f):
    """Decorator para rotas que requerem login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator para rotas que requerem admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        if not auth_manager.is_admin(session['usuario']):
            return jsonify({'success': False, 'message': 'Acesso negado'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Redireciona para login ou dashboard"""
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        data = request.get_json()
        usuario = data.get('usuario', '').strip()
        senha = data.get('senha', '')
        
        sucesso, resultado = auth_manager.validar_login(usuario, senha)
        
        if sucesso:
            session['usuario'] = usuario
            session['tipo'] = resultado['tipo']
            session['nome_completo'] = resultado.get('nome_completo', usuario)
            
            # Registra acesso
            auth_manager.registrar_acesso(usuario)
            
            logger.info(f"Login bem-sucedido: {usuario} ({resultado['tipo']})")
            return jsonify({
                'success': True, 
                'message': 'Login realizado com sucesso!',
                'tipo': resultado['tipo']
            })
        else:
            logger.warning(f"Tentativa de login falhou: {usuario}")
            mensagem = resultado if resultado else 'Usuário ou senha incorretos'
            return jsonify({'success': False, 'message': mensagem}), 401
    
    # Passa timestamp atual para forçar reload da logo
    return render_template('login.html', cache_buster=int(time.time() * 1000))

@app.route('/logout')
def logout():
    """Logout do usuário"""
    usuario = session.get('usuario', 'Desconhecido')
    session.pop('usuario', None)
    logger.info(f"Logout: {usuario}")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    is_admin = auth_manager.is_admin(session['usuario'])
    return render_template('dashboard.html', 
                         usuario=session['usuario'],
                         nome_completo=session.get('nome_completo', session['usuario']),
                         is_admin=is_admin)

@app.route('/enviar')
@login_required
def enviar():
    """Página de envio de mensagens"""
    is_admin = auth_manager.is_admin(session['usuario'])
    return render_template('enviar_novo.html', 
                         usuario=session['usuario'],
                         is_admin=is_admin)

@app.route('/relatorios')
@login_required
def relatorios():
    """Página de relatórios detalhados"""
    is_admin = auth_manager.is_admin(session['usuario'])
    return render_template('relatorios.html',
                         usuario=session['usuario'],
                         is_admin=is_admin)

@app.route('/api/relatorios/dados')
@login_required
def api_relatorios_dados():
    """API: Retorna dados para relatórios"""
    try:
        dados = []
        planilhas_dir = config.PLANILHAS_DIR
        
        if planilhas_dir.exists():
            for arquivo in sorted(planilhas_dir.glob('Resultado_*.xlsx'), reverse=True):
                try:
                    df = pd.read_excel(arquivo)
                    data_arquivo = datetime.fromtimestamp(arquivo.stat().st_mtime).strftime('%d/%m/%Y %H:%M')
                    
                    for _, row in df.iterrows():
                        dados.append({
                            'contato': str(row.get('Contato', '')),
                            'nome': str(row.get('Nome', '')),
                            'status': str(row.get('Status', '')),
                            'motivo': str(row.get('Motivo', '')),
                            'data': data_arquivo
                        })
                except Exception as e:
                    logger.error(f"Erro ao ler {arquivo}: {e}")
        
        return jsonify({'success': True, 'dados': dados})
    except Exception as e:
        logger.error(f"Erro ao carregar dados de relatórios: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/historico')
@login_required
def historico():
    """Página de histórico de envios"""
    is_admin = auth_manager.is_admin(session['usuario'])
    # Lista arquivos de resultado
    resultados = []
    planilhas_dir = config.PLANILHAS_DIR
    
    if planilhas_dir.exists():
        for arquivo in sorted(planilhas_dir.glob('Resultado_*.xlsx'), reverse=True):
            try:
                df = pd.read_excel(arquivo)
                total = len(df)
                enviados = len(df[df['Status'] == 'Enviado'])
                data_timestamp = arquivo.stat().st_mtime
                data_formatada = datetime.fromtimestamp(data_timestamp).strftime('%d/%m/%Y às %H:%M')
                
                resultados.append({
                    'arquivo': arquivo.name,
                    'data': data_formatada,
                    'total': total,
                    'enviados': enviados,
                    'falhas': total - enviados
                })
            except Exception as e:
                logger.error(f"Erro ao ler {arquivo}: {e}")
    
    return render_template('historico.html', 
                         usuario=session['usuario'], 
                         resultados=resultados,
                         is_admin=is_admin)

@app.route('/api/relatorios/listar')
@login_required
def api_listar_relatorios():
    """API: Lista todos os relatórios disponíveis"""
    try:
        relatorios = []
        planilhas_dir = config.PLANILHAS_DIR
        
        if planilhas_dir.exists():
            for arquivo in sorted(planilhas_dir.glob('Resultado_*.xlsx'), reverse=True):
                try:
                    df = pd.read_excel(arquivo)
                    total = len(df)
                    enviados = len(df[df['Status'] == 'Enviado'])
                    falhas = total - enviados
                    
                    relatorios.append({
                        'arquivo': arquivo.name,
                        'data': arquivo.stat().st_mtime,
                        'total': total,
                        'enviados': enviados,
                        'falhas': falhas,
                        'taxa_sucesso': round((enviados / total * 100) if total > 0 else 0, 2)
                    })
                except Exception as e:
                    logger.error(f"Erro ao ler {arquivo}: {e}")
        
        return jsonify({'success': True, 'relatorios': relatorios})
    except Exception as e:
        logger.error(f"Erro ao listar relatórios: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/relatorios/detalhes/<arquivo>')
@login_required
def api_detalhes_relatorio(arquivo):
    """API: Retorna detalhes de um relatório específico"""
    try:
        arquivo_path = config.PLANILHAS_DIR / arquivo
        
        if not arquivo_path.exists():
            return jsonify({'success': False, 'message': 'Arquivo não encontrado'}), 404
        
        df = pd.read_excel(arquivo_path)
        
        # Converte para lista de dicionários
        dados = df.to_dict('records')
        
        return jsonify({
            'success': True,
            'dados': dados,
            'total': len(dados),
            'enviados': len(df[df['Status'] == 'Enviado']),
            'falhas': len(df[df['Status'] != 'Enviado'])
        })
    except Exception as e:
        logger.error(f"Erro ao obter detalhes do relatório: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/relatorios/exportar/<arquivo>')
@login_required
def api_exportar_csv(arquivo):
    """API: Exporta relatório para CSV"""
    try:
        from flask import send_file
        import io
        
        arquivo_path = config.PLANILHAS_DIR / arquivo
        
        if not arquivo_path.exists():
            return jsonify({'success': False, 'message': 'Arquivo não encontrado'}), 404
        
        # Lê Excel
        df = pd.read_excel(arquivo_path)
        
        # Aplica filtros se fornecidos
        status_filtro = request.args.get('status')
        if status_filtro:
            if status_filtro == 'enviado':
                df = df[df['Status'] == 'Enviado']
            elif status_filtro == 'falha':
                df = df[df['Status'] != 'Enviado']
        
        # Converte para CSV
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)
        
        # Cria arquivo em memória
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8-sig'))
        mem.seek(0)
        
        # Nome do arquivo
        nome_csv = arquivo.replace('.xlsx', '.csv')
        if status_filtro:
            nome_csv = arquivo.replace('.xlsx', f'_{status_filtro}.csv')
        
        return send_file(
            mem,
            mimetype='text/csv',
            as_attachment=True,
            download_name=nome_csv
        )
    except Exception as e:
        logger.error(f"Erro ao exportar CSV: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/configuracoes')
@login_required
def configuracoes():
    """Página de configurações"""
    is_admin = auth_manager.is_admin(session['usuario'])
    return render_template('configuracoes.html', 
                         usuario=session['usuario'],
                         is_admin=is_admin)

# ==================== ROTAS ADMINISTRATIVAS ====================

@app.route('/admin/clientes')
@admin_required
def admin_clientes():
    """Página de gerenciamento de clientes (apenas admin)"""
    clientes = auth_manager.listar_clientes()
    return render_template('admin_clientes.html', 
                         usuario=session['usuario'],
                         nome_completo=session.get('nome_completo'),
                         clientes=clientes)

@app.route('/api/admin/clientes', methods=['GET'])
@admin_required
def api_listar_clientes():
    """API: Lista todos os clientes"""
    clientes = auth_manager.listar_clientes()
    return jsonify({'success': True, 'clientes': clientes})

@app.route('/api/admin/clientes/adicionar', methods=['POST'])
@admin_required
def api_adicionar_cliente():
    """API: Adiciona novo cliente"""
    try:
        data = request.get_json()
        
        usuario = data.get('usuario', '').strip()
        senha = data.get('senha', '').strip()
        nome_completo = data.get('nome_completo', '').strip()
        email = data.get('email', '').strip()
        empresa = data.get('empresa', '').strip()
        telefone = data.get('telefone', '').strip()
        
        if not usuario or not senha or not nome_completo:
            return jsonify({'success': False, 'message': 'Preencha todos os campos obrigatórios'}), 400
        
        sucesso, mensagem = auth_manager.adicionar_cliente(
            usuario, senha, nome_completo, email, empresa, telefone
        )
        
        if sucesso:
            logger.info(f"Cliente adicionado: {usuario} por {session['usuario']}")
            return jsonify({'success': True, 'message': mensagem})
        else:
            return jsonify({'success': False, 'message': mensagem}), 400
            
    except Exception as e:
        logger.error(f"Erro ao adicionar cliente: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/clientes/<usuario>', methods=['GET'])
@admin_required
def api_obter_cliente(usuario):
    """API: Obtém dados de um cliente"""
    cliente = auth_manager.obter_cliente(usuario)
    if cliente:
        return jsonify({'success': True, 'cliente': cliente})
    return jsonify({'success': False, 'message': 'Cliente não encontrado'}), 404

@app.route('/api/admin/clientes/<usuario>/atualizar', methods=['POST'])
@admin_required
def api_atualizar_cliente(usuario):
    """API: Atualiza dados de um cliente"""
    try:
        data = request.get_json()
        sucesso, mensagem = auth_manager.atualizar_cliente(usuario, data)
        
        if sucesso:
            logger.info(f"Cliente atualizado: {usuario} por {session['usuario']}")
            return jsonify({'success': True, 'message': mensagem})
        else:
            return jsonify({'success': False, 'message': mensagem}), 400
            
    except Exception as e:
        logger.error(f"Erro ao atualizar cliente: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/clientes/<usuario>/ativar', methods=['POST'])
@admin_required
def api_ativar_cliente(usuario):
    """API: Ativa um cliente"""
    sucesso, mensagem = auth_manager.ativar_cliente(usuario)
    if sucesso:
        logger.info(f"Cliente ativado: {usuario} por {session['usuario']}")
        return jsonify({'success': True, 'message': mensagem})
    return jsonify({'success': False, 'message': mensagem}), 400

@app.route('/api/admin/clientes/<usuario>/desativar', methods=['POST'])
@admin_required
def api_desativar_cliente(usuario):
    """API: Desativa um cliente"""
    sucesso, mensagem = auth_manager.desativar_cliente(usuario)
    if sucesso:
        logger.info(f"Cliente desativado: {usuario} por {session['usuario']}")
        return jsonify({'success': True, 'message': mensagem})
    return jsonify({'success': False, 'message': mensagem}), 400

@app.route('/api/admin/clientes/<usuario>/bloquear', methods=['POST'])
@admin_required
def api_bloquear_cliente(usuario):
    """API: Bloqueia um cliente por falta de pagamento"""
    sucesso, mensagem = auth_manager.bloquear_cliente(usuario)
    if sucesso:
        logger.info(f"Cliente bloqueado: {usuario} por {session['usuario']}")
        return jsonify({'success': True, 'message': mensagem})
    return jsonify({'success': False, 'message': mensagem}), 400

@app.route('/api/admin/clientes/<usuario>/desbloquear', methods=['POST'])
@admin_required
def api_desbloquear_cliente(usuario):
    """API: Desbloqueia um cliente"""
    sucesso, mensagem = auth_manager.desbloquear_cliente(usuario)
    if sucesso:
        logger.info(f"Cliente desbloqueado: {usuario} por {session['usuario']}")
        return jsonify({'success': True, 'message': mensagem})
    return jsonify({'success': False, 'message': mensagem}), 400

@app.route('/api/admin/clientes/<usuario>/alterar-senha', methods=['POST'])
@admin_required
def api_alterar_senha_cliente(usuario):
    """API: Altera senha de um cliente"""
    try:
        data = request.get_json()
        senha_nova = data.get('senha_nova', '').strip()
        
        if not senha_nova:
            return jsonify({'success': False, 'message': 'Senha não pode ser vazia'}), 400
        
        sucesso, mensagem = auth_manager.alterar_senha_cliente(usuario, senha_nova)
        
        if sucesso:
            logger.info(f"Senha alterada para cliente: {usuario} por {session['usuario']}")
            return jsonify({'success': True, 'message': mensagem})
        else:
            return jsonify({'success': False, 'message': mensagem}), 400
            
    except Exception as e:
        logger.error(f"Erro ao alterar senha: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/clientes/<usuario>/remover', methods=['POST'])
@admin_required
def api_remover_cliente(usuario):
    """API: Remove um cliente"""
    sucesso, mensagem = auth_manager.remover_cliente(usuario)
    if sucesso:
        logger.info(f"Cliente removido: {usuario} por {session['usuario']}")
        return jsonify({'success': True, 'message': mensagem})
    return jsonify({'success': False, 'message': mensagem}), 400

# ==================== FIM ROTAS ADMINISTRATIVAS ====================

@app.route('/api/enviar-novo', methods=['POST'])
@login_required
def api_enviar_novo():
    """API: Novo sistema de envio (adiciona na fila para agente processar)"""
    try:
        import json
        from werkzeug.utils import secure_filename
        from api_agente import adicionar_fila
        
        # Recebe dados
        numeros_json = request.form.get('numeros')
        mensagens_json = request.form.get('mensagens')
        imagem = request.files.get('imagem')
        
        if not numeros_json or not mensagens_json:
            return jsonify({'success': False, 'message': 'Dados incompletos'}), 400
        
        numeros = json.loads(numeros_json)
        mensagens = json.loads(mensagens_json)
        
        if not numeros or not mensagens:
            return jsonify({'success': False, 'message': 'Adicione números e mensagens'}), 400
        
        # Limpa números
        numeros_limpos = []
        for numero in numeros:
            numero_limpo = ''.join(filter(str.isdigit, numero))
            if numero_limpo:
                numeros_limpos.append(numero_limpo)
        
        # Salva imagem se houver e gera URL
        imagem_url = None
        if imagem:
            filename = secure_filename(imagem.filename)
            imagem_path = config.PLANILHAS_DIR / f"img_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            imagem.save(imagem_path)
            # URL relativa para o agente baixar
            imagem_url = f"/static/uploads/{imagem_path.name}"
        
        # Adiciona na fila
        envio_data = {
            'usuario': session['usuario'],
            'numeros': numeros_limpos,
            'mensagens': mensagens,
            'imagem': imagem_url
        }
        
        # Chama função da API do agente
        response = adicionar_fila()
        data = response.get_json()
        
        if data.get('success'):
            session_id = data.get('envio_id')
            
            # Cria sessão ativa para acompanhamento
            active_sessions[session_id] = {
                'usuario': session['usuario'],
                'total': len(numeros_limpos) * len(mensagens),
                'processados': 0,
                'enviados': 0,
                'falhas': 0,
                'status': 'aguardando_agente'
            }
            
            # Incrementa contador de envios do cliente
            auth_manager.incrementar_envios(session['usuario'])
            
            # Emite status inicial
            socketio.emit('status_update', {
                'session_id': session_id,
                'status': 'aguardando_agente',
                'message': 'Aguardando agente local processar...'
            })
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'message': 'Envio adicionado na fila com sucesso'
            })
        else:
            return jsonify({'success': False, 'message': 'Erro ao adicionar na fila'}), 500
        
    except Exception as e:
        logger.error(f"Erro ao iniciar envio novo: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

def processar_envio_novo(session_id, planilha, mensagens, imagem_path, temp_path):
    """Processa envio com múltiplas mensagens e imagem"""
    sender = None
    numeros_nao_enviados = []
    
    try:
        # Atualiza status
        active_sessions[session_id]['status'] = 'inicializando'
        socketio.emit('status_update', {
            'session_id': session_id,
            'status': 'inicializando',
            'message': 'Inicializando navegador...'
        })
        
        # Inicializa sender
        sender = criar_sender()
        if not sender.inicializar_driver():
            raise Exception("Falha ao inicializar navegador")
        
        # Aguarda login
        active_sessions[session_id]['status'] = 'aguardando_login'
        socketio.emit('status_update', {
            'session_id': session_id,
            'status': 'aguardando_login',
            'message': 'Aguardando login no WhatsApp Web...'
        })
        
        if not sender.aguardar_login():
            raise Exception("Falha ao fazer login no WhatsApp Web")
        
        logger.info("Login detectado! Iniciando envio de mensagens...")
        
        # Envia mensagens
        active_sessions[session_id]['status'] = 'enviando'
        socketio.emit('status_update', {
            'session_id': session_id,
            'status': 'enviando',
            'message': 'Enviando mensagens...'
        })
        
        total_envios = len(planilha) * len(mensagens)
        envio_atual = 0
        
        for index, row in planilha.iterrows():
            nome = row.get('Nome', '')
            contato = row['Contato']
            
            # Envia cada mensagem
            for idx_msg, mensagem in enumerate(mensagens):
                envio_atual += 1
                active_sessions[session_id]['processados'] = envio_atual
                
                socketio.emit('progresso_update', {
                    'session_id': session_id,
                    'atual': envio_atual,
                    'total': total_envios,
                    'contato': contato,
                    'mensagem': idx_msg + 1
                })
                
                # Envia mensagem
                sucesso, motivo = sender.enviar_mensagem(contato, mensagem, nome)
                
                if sucesso:
                    active_sessions[session_id]['enviados'] += 1
                else:
                    active_sessions[session_id]['falhas'] += 1
                    if contato not in numeros_nao_enviados:
                        numeros_nao_enviados.append(contato)
                
                socketio.emit('mensagem_enviada', {
                    'session_id': session_id,
                    'contato': contato,
                    'mensagem_num': idx_msg + 1,
                    'sucesso': sucesso,
                    'motivo': motivo
                })
            
            # Envia imagem por último, após todas as mensagens deste contato
            if imagem_path and active_sessions[session_id]['enviados'] > 0:
                logger.info(f"Enviando imagem para {contato} (após todas as mensagens)...")
                time.sleep(2)  # Aguarda a última mensagem ser enviada
                sucesso_imagem = sender.enviar_imagem(imagem_path)
                if sucesso_imagem:
                    logger.info(f"Imagem enviada para {contato}")
                else:
                    logger.warning(f"Falha ao enviar imagem para {contato}")
        
        # Salva resultados
        arquivo_resultado = salvar_resultados(planilha, numeros_nao_enviados)
        
        # Finaliza
        active_sessions[session_id]['status'] = 'concluido'
        socketio.emit('envio_concluido', {
            'session_id': session_id,
            'total': total_envios,
            'enviados': active_sessions[session_id]['enviados'],
            'falhas': active_sessions[session_id]['falhas'],
            'arquivo_resultado': arquivo_resultado.name
        })
        
        logger.info(f"Envio concluído: {session_id}")
        
    except Exception as e:
        logger.error(f"Erro no envio {session_id}: {e}")
        active_sessions[session_id]['status'] = 'erro'
        socketio.emit('erro_envio', {
            'session_id': session_id,
            'message': str(e)
        })
        
    finally:
        if sender:
            sender.fechar()
        
        # Remove arquivos temporários
        try:
            if temp_path.exists():
                temp_path.unlink()
            if imagem_path and imagem_path.exists():
                imagem_path.unlink()
        except Exception as e:
            logger.error(f"Erro ao remover arquivos temporários: {e}")

@app.route('/api/validar-planilha', methods=['POST'])
@login_required
def validar_planilha():
    """Valida planilha enviada"""
    try:
        if 'planilha' not in request.files:
            return jsonify({'success': False, 'message': 'Nenhum arquivo enviado'}), 400
        
        arquivo = request.files['planilha']
        
        if arquivo.filename == '':
            return jsonify({'success': False, 'message': 'Nenhum arquivo selecionado'}), 400
        
        if not arquivo.filename.endswith('.xlsx'):
            return jsonify({'success': False, 'message': 'Apenas arquivos .xlsx são aceitos'}), 400
        
        # Salva temporariamente
        temp_path = config.PLANILHAS_DIR / f"temp_{session['usuario']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        arquivo.save(temp_path)
        
        # Valida
        df = carregar_planilha(temp_path)
        
        # Preview dos dados
        preview = []
        for idx, row in df.head(5).iterrows():
            preview.append({
                'nome': row.get('Nome', ''),
                'contato': row['Contato']
            })
        
        return jsonify({
            'success': True,
            'total': len(df),
            'preview': preview,
            'temp_file': temp_path.name
        })
        
    except Exception as e:
        logger.error(f"Erro ao validar planilha: {e}")
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/iniciar-envio', methods=['POST'])
@login_required
def iniciar_envio():
    """Inicia processo de envio"""
    try:
        data = request.get_json()
        temp_file = data.get('temp_file')
        mensagem = data.get('mensagem', '').strip()
        
        # Validações
        valido, erro = validar_mensagem(mensagem)
        if not valido:
            return jsonify({'success': False, 'message': erro}), 400
        
        # Carrega planilha
        temp_path = config.PLANILHAS_DIR / temp_file
        if not temp_path.exists():
            return jsonify({'success': False, 'message': 'Planilha não encontrada'}), 400
        
        df = carregar_planilha(temp_path)
        
        # Cria sessão de envio
        session_id = f"{session['usuario']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Inicia thread de envio
        thread = threading.Thread(
            target=processar_envio,
            args=(session_id, df, mensagem, temp_path),
            daemon=True
        )
        thread.start()
        
        active_sessions[session_id] = {
            'usuario': session['usuario'],
            'total': len(df),
            'processados': 0,
            'enviados': 0,
            'falhas': 0,
            'status': 'iniciando'
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Envio iniciado com sucesso'
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar envio: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

def processar_envio(session_id, planilha, mensagem, temp_path):
    """Processa envio em background"""
    sender = None
    numeros_nao_enviados = []
    
    try:
        # Atualiza status
        active_sessions[session_id]['status'] = 'inicializando'
        socketio.emit('status_update', {
            'session_id': session_id,
            'status': 'inicializando',
            'message': 'Inicializando navegador...'
        })
        
        # Inicializa sender
        sender = criar_sender()
        if not sender.inicializar_driver():
            raise Exception("Falha ao inicializar navegador")
        
        # Aguarda login
        active_sessions[session_id]['status'] = 'aguardando_login'
        socketio.emit('status_update', {
            'session_id': session_id,
            'status': 'aguardando_login',
            'message': 'Aguardando login no WhatsApp Web...'
        })
        
        if not sender.aguardar_login():
            raise Exception("Falha ao fazer login no WhatsApp Web")
        
        # Envia mensagens
        active_sessions[session_id]['status'] = 'enviando'
        total = len(planilha)
        
        for index, row in planilha.iterrows():
            nome = row.get('Nome', '')
            contato = row['Contato']
            
            # Callback de progresso
            active_sessions[session_id]['processados'] = index + 1
            
            socketio.emit('progresso_update', {
                'session_id': session_id,
                'atual': index + 1,
                'total': total,
                'contato': contato,
                'nome': nome
            })
            
            # Envia mensagem
            sucesso, motivo = sender.enviar_mensagem(contato, mensagem, nome)
            
            if sucesso:
                active_sessions[session_id]['enviados'] += 1
            else:
                active_sessions[session_id]['falhas'] += 1
                numeros_nao_enviados.append(contato)
            
            socketio.emit('mensagem_enviada', {
                'session_id': session_id,
                'contato': contato,
                'nome': nome,
                'sucesso': sucesso,
                'motivo': motivo
            })
        
        # Salva resultados
        arquivo_resultado = salvar_resultados(planilha, numeros_nao_enviados)
        
        # Finaliza
        active_sessions[session_id]['status'] = 'concluido'
        socketio.emit('envio_concluido', {
            'session_id': session_id,
            'total': total,
            'enviados': active_sessions[session_id]['enviados'],
            'falhas': active_sessions[session_id]['falhas'],
            'arquivo_resultado': arquivo_resultado.name
        })
        
        logger.info(f"Envio concluído: {session_id}")
        
    except Exception as e:
        logger.error(f"Erro no envio {session_id}: {e}")
        active_sessions[session_id]['status'] = 'erro'
        socketio.emit('erro_envio', {
            'session_id': session_id,
            'message': str(e)
        })
        
    finally:
        if sender:
            sender.fechar()
        
        # Remove arquivo temporário
        try:
            if temp_path.exists():
                temp_path.unlink()
        except Exception as e:
            logger.error(f"Erro ao remover arquivo temporário: {e}")

@app.route('/api/status-envio/<session_id>')
@login_required
def status_envio(session_id):
    """Retorna status de um envio"""
    if session_id in active_sessions:
        return jsonify(active_sessions[session_id])
    return jsonify({'error': 'Sessão não encontrada'}), 404

@app.route('/api/estatisticas')
@login_required
def estatisticas():
    """Retorna estatísticas gerais"""
    try:
        planilhas_dir = config.PLANILHAS_DIR
        
        total_envios = 0
        total_enviados = 0
        total_falhas = 0
        
        if planilhas_dir.exists():
            for arquivo in planilhas_dir.glob('Resultado_*.xlsx'):
                try:
                    df = pd.read_excel(arquivo)
                    total_envios += len(df)
                    total_enviados += len(df[df['Status'] == 'Enviado'])
                except Exception:
                    pass
        
        total_falhas = total_envios - total_enviados
        taxa_sucesso = (total_enviados / total_envios * 100) if total_envios > 0 else 0
        
        return jsonify({
            'total_envios': total_envios,
            'total_enviados': total_enviados,
            'total_falhas': total_falhas,
            'taxa_sucesso': round(taxa_sucesso, 2)
        })
        
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Cria diretórios necessários
    config.PLANILHAS_DIR.mkdir(exist_ok=True)
    config.LOGS_DIR.mkdir(exist_ok=True)
    
    # Porta do Railway ou local
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Iniciando servidor web na porta {port}...")
    socketio.run(app, debug=False, host='0.0.0.0', port=port)
