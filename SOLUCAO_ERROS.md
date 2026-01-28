# 🔧 Solução de Erros Comuns

## ❌ Erro: "No module named 'flask'"

### Causa
As dependências Python não foram instaladas.

### Solução

#### Opção 1: Usar o setup automático
```bash
npm run setup
```

#### Opção 2: Instalar manualmente
```bash
pip install -r requirements.txt
```

#### Opção 3: Instalar uma por uma
```bash
pip install Flask==3.0.0
pip install Flask-SocketIO==5.3.5
pip install selenium==4.16.0
pip install pandas==2.1.4
pip install openpyxl==3.1.2
pip install Pillow==10.1.0
pip install gunicorn==21.2.0
pip install eventlet==0.33.3
pip install python-dotenv==1.0.0
```

---

## ❌ Erro: "npm não é reconhecido"

### Causa
Node.js não está instalado.

### Solução

#### Opção 1: Instalar Node.js
1. Baixe em: https://nodejs.org/
2. Instale a versão LTS
3. Reinicie o terminal
4. Execute: `npm run setup`

#### Opção 2: Usar Python direto (sem npm)
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar servidor
python app.py
```

---

## ❌ Erro: "python não é reconhecido"

### Causa
Python não está no PATH do sistema.

### Solução

#### Opção 1: Reinstalar Python
1. Baixe em: https://www.python.org/
2. Durante instalação, marque "Add Python to PATH"
3. Instale
4. Reinicie o terminal

#### Opção 2: Adicionar ao PATH manualmente
1. Encontre onde Python está instalado
2. Adicione ao PATH do Windows
3. Reinicie o terminal

---

## ❌ Erro: "Porta 5000 em uso"

### Causa
Outro processo está usando a porta 5000.

### Solução

#### Opção 1: Matar o processo
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

#### Opção 2: Mudar a porta
Edite `app.py` (última linha):
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

Depois acesse: `http://localhost:5001`

---

## ❌ Erro: "ChromeDriver not found"

### Causa
ChromeDriver não está instalado ou não está no PATH.

### Solução

#### Opção 1: Baixar ChromeDriver
1. Verifique versão do Chrome: Menu → Ajuda → Sobre
2. Baixe ChromeDriver compatível: https://chromedriver.chromium.org/
3. Extraia o arquivo
4. Coloque em uma das opções:
   - Na pasta do projeto
   - Em `C:\Windows\System32\`
   - Em qualquer pasta no PATH

#### Opção 2: Usar webdriver-manager (automático)
```bash
pip install webdriver-manager
```

Depois edite `whatsapp_sender.py`:
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# No método inicializar_driver:
service = Service(ChromeDriverManager().install())
self.driver = webdriver.Chrome(service=service, options=chrome_options)
```

---

## ❌ Erro: "Permission denied"

### Causa
Falta de permissões para criar diretórios ou arquivos.

### Solução

#### Windows
Execute o terminal como Administrador:
1. Clique com botão direito no CMD/PowerShell
2. "Executar como administrador"
3. Execute os comandos novamente

---

## ❌ Erro: "Template not found"

### Causa
Flask não está encontrando os templates.

### Solução

Verifique se a estrutura está correta:
```
web/
├── app.py
└── templates/
    ├── login.html
    ├── dashboard.html
    └── ...
```

Se estiver errado, reorganize os arquivos.

---

## ❌ Erro: "Static files not found"

### Causa
Flask não está encontrando arquivos CSS/JS.

### Solução

Verifique se a estrutura está correta:
```
web/
├── app.py
└── static/
    ├── css/
    ├── js/
    └── images/
```

---

## ❌ Erro: "Database/File locked"

### Causa
Arquivo `usuarios.json` está sendo usado por outro processo.

### Solução

1. Feche todos os editores de texto
2. Feche o navegador
3. Reinicie o servidor

---

## 🔄 Processo Completo de Instalação

### Passo a Passo Garantido

```bash
# 1. Verificar Python
python --version
# Deve mostrar: Python 3.8 ou superior

# 2. Verificar pip
pip --version
# Deve mostrar a versão do pip

# 3. Atualizar pip
python -m pip install --upgrade pip

# 4. Navegar para a pasta
cd "Robo - Usuario/web"

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Verificar instalação
pip list | findstr Flask
# Deve mostrar: Flask 3.0.0

# 7. Executar servidor
python app.py

# 8. Acessar no navegador
# http://localhost:5000
```

---

## 🧪 Testar Instalação

### Script de Teste

Crie um arquivo `test_install.py`:

```python
print("Testando instalação...")

try:
    import flask
    print("✅ Flask instalado")
except ImportError:
    print("❌ Flask NÃO instalado")

try:
    import flask_socketio
    print("✅ Flask-SocketIO instalado")
except ImportError:
    print("❌ Flask-SocketIO NÃO instalado")

try:
    import selenium
    print("✅ Selenium instalado")
except ImportError:
    print("❌ Selenium NÃO instalado")

try:
    import pandas
    print("✅ Pandas instalado")
except ImportError:
    print("❌ Pandas NÃO instalado")

print("\nSe todos estiverem ✅, você pode executar: python app.py")
```

Execute:
```bash
python test_install.py
```

---

## 📞 Ainda com Problemas?

### Informações para Suporte

Ao pedir ajuda, forneça:

1. **Versão do Python:**
```bash
python --version
```

2. **Versão do pip:**
```bash
pip --version
```

3. **Sistema Operacional:**
```bash
# Windows
ver

# Linux/Mac
uname -a
```

4. **Erro completo:**
Copie e cole o erro completo do terminal

5. **Pacotes instalados:**
```bash
pip list
```

---

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Python no PATH
- [ ] pip funcionando
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] ChromeDriver baixado
- [ ] Porta 5000 disponível
- [ ] Estrutura de pastas correta
- [ ] Executou `python app.py`
- [ ] Acessou `http://localhost:5000`

---

## 🎯 Solução Rápida (Tudo de Uma Vez)

```bash
# Copie e cole tudo de uma vez:

cd "Robo - Usuario/web"
python -m pip install --upgrade pip
pip install Flask==3.0.0 Flask-SocketIO==5.3.5 selenium==4.16.0 pandas==2.1.4 openpyxl==3.1.2 Pillow==10.1.0 gunicorn==21.2.0 eventlet==0.33.3 python-dotenv==1.0.0
python app.py
```

Depois acesse: `http://localhost:5000`

---

**Desenvolvido por monitorIA - Departamento de T.I**  
**Suporte:** Discord do T.I
