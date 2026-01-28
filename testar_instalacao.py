"""
Script de Teste de Instalação
Robô WhatsApp Web - monitorIA
"""

import sys

def testar_modulo(nome_modulo, nome_exibicao=None):
    """Testa se um módulo está instalado"""
    if nome_exibicao is None:
        nome_exibicao = nome_modulo
    
    try:
        modulo = __import__(nome_modulo)
        versao = getattr(modulo, '__version__', 'versão desconhecida')
        print(f"✅ {nome_exibicao}: {versao}")
        return True
    except ImportError:
        print(f"❌ {nome_exibicao}: NÃO INSTALADO")
        return False

def main():
    print("=" * 60)
    print("  TESTE DE INSTALAÇÃO - Robô WhatsApp monitorIA")
    print("=" * 60)
    print()
    
    # Testa Python
    print(f"🐍 Python: {sys.version}")
    print()
    
    # Lista de módulos para testar
    modulos = [
        ('flask', 'Flask'),
        ('flask_socketio', 'Flask-SocketIO'),
        ('socketio', 'python-socketio'),
        ('engineio', 'python-engineio'),
        ('selenium', 'Selenium'),
        ('pandas', 'Pandas'),
        ('openpyxl', 'OpenPyXL'),
        ('PIL', 'Pillow'),
        ('eventlet', 'Eventlet'),
        ('dotenv', 'python-dotenv'),
    ]
    
    print("Testando dependências:")
    print("-" * 60)
    
    resultados = []
    for modulo, nome in modulos:
        resultado = testar_modulo(modulo, nome)
        resultados.append(resultado)
    
    print()
    print("=" * 60)
    
    # Resumo
    total = len(resultados)
    instalados = sum(resultados)
    faltando = total - instalados
    
    if faltando == 0:
        print("✅ SUCESSO! Todas as dependências estão instaladas!")
        print()
        print("Você pode executar o sistema:")
        print("  python app.py")
        print()
        print("Depois acesse: http://localhost:5000")
    else:
        print(f"⚠️  ATENÇÃO! {faltando} dependência(s) faltando!")
        print()
        print("Execute para instalar:")
        print("  pip install -r requirements.txt")
        print()
        print("Ou:")
        print("  instalar_dependencias.bat")
    
    print("=" * 60)
    print()
    
    # Testa estrutura de pastas
    print("Verificando estrutura de pastas:")
    print("-" * 60)
    
    from pathlib import Path
    
    pastas = [
        'Planilhas',
        'Logs',
        'static',
        'static/css',
        'static/js',
        'static/images',
        'templates',
    ]
    
    for pasta in pastas:
        caminho = Path(pasta)
        if caminho.exists():
            print(f"✅ {pasta}/")
        else:
            print(f"❌ {pasta}/ (não existe)")
    
    print()
    print("=" * 60)
    
    # Testa arquivos principais
    print("Verificando arquivos principais:")
    print("-" * 60)
    
    arquivos = [
        'app.py',
        'config.py',
        'auth.py',
        'utils.py',
        'whatsapp_sender.py',
        'requirements.txt',
        'package.json',
    ]
    
    for arquivo in arquivos:
        caminho = Path(arquivo)
        if caminho.exists():
            tamanho = caminho.stat().st_size
            print(f"✅ {arquivo} ({tamanho} bytes)")
        else:
            print(f"❌ {arquivo} (não encontrado)")
    
    print()
    print("=" * 60)
    print()
    
    if faltando == 0:
        print("🎉 Sistema pronto para uso!")
    else:
        print("⚠️  Instale as dependências faltando antes de executar.")
    
    print()
    input("Pressione ENTER para sair...")

if __name__ == '__main__':
    main()
