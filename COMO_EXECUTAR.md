# 🚀 Como Executar o Sistema

## ⚡ Início Rápido (3 Passos)

### 1️⃣ Instalar Dependências

Abra o terminal na pasta `web/` e execute:

```bash
pip install -r requirements.txt
```

**OU** execute o instalador automático:

```bash
instalar_dependencias.bat
```

### 2️⃣ Executar o Sistema

```bash
npm run dev
```

**OU** diretamente com Python:

```bash
python app.py
```

### 3️⃣ Acessar no Navegador

Abra: **http://localhost:5000**

---

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

- **Python 3.8+** → [Download](https://www.python.org/downloads/)
- **Google Chrome** → [Download](https://www.google.com/chrome/)
- **Node.js** (opcional) → [Download](https://nodejs.org/)

---

## 🔧 Instalação Detalhada

### Passo 1: Verificar Python

```bash
python --version
```

Deve mostrar: `Python 3.8` ou superior

Se não funcionar, instale Python e marque "Add Python to PATH" durante a instalação.

### Passo 2: Navegar para a Pasta

```bash
cd "Robo - Usuario/web"
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

Isso vai instalar:
- Flask (servidor web)
- Flask-SocketIO (comunicação real-time)
- Selenium (automação do WhatsApp)
- Pandas (manipulação de planilhas)
- E outras dependências necessárias

### Passo 4: Executar

```bash
python app.py
```

Você verá:
```
 * Running on http://0.0.0.0:5000
```

### Passo 5: Acessar

Abra o navegador em: **http://localhost:5000**

---

## 🎯 Comandos Disponíveis

### Com npm (recomendado)

```bash
npm run dev      # Inicia servidor em modo desenvolvimento
npm run setup    # Instala tudo automaticamente
npm run start    # Inicia servidor
npm run prod     # Inicia em modo produção
```

### Com Python direto

```bash
python app.py                    # Inicia servidor
pip install -r requirements.txt  # Instala dependências
```

---

## 🐛 Problemas Comuns

### ❌ "No module named 'flask'"

**Solução:**
```bash
pip install -r requirements.txt
```

### ❌ "npm não é reconhecido"

**Solução:** Use Python direto:
```bash
python app.py
```

### ❌ "python não é reconhecido"

**Solução:** Instale Python e adicione ao PATH

### ❌ "Porta 5000 em uso"

**Solução:** Mude a porta em `app.py` (última linha):
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

---

## 📁 Estrutura de Pastas

Após a instalação, você terá:

```
web/
├── app.py                 # Servidor principal
├── requirements.txt       # Dependências
├── package.json          # Scripts npm
├── Planilhas/            # Planilhas (criado automaticamente)
├── Logs/                 # Logs (criado automaticamente)
├── templates/            # Páginas HTML
│   ├── login.html
│   ├── dashboard.html
│   └── ...
└── static/               # CSS, JS, Imagens
    ├── css/
    ├── js/
    └── images/
```

---

## 🔐 Login Padrão

**Usuário:** `admin`  
**Senha:** `admin123`

⚠️ **IMPORTANTE:** Altere a senha após o primeiro login!

---

## 📱 Como Usar

1. **Login:** Acesse http://localhost:5000 e faça login
2. **Upload:** Envie uma planilha Excel (.xlsx) com colunas:
   - `Contato` (obrigatório) - Número com DDD
   - `Nome` (opcional) - Nome do contato
3. **Mensagem:** Digite a mensagem (use `{nome}` para personalizar)
4. **Enviar:** Clique em "Iniciar Envio"
5. **WhatsApp:** Escaneie o QR Code no WhatsApp Web
6. **Acompanhar:** Veja o progresso em tempo real

---

## 🎨 Recursos

- ✅ Interface moderna (design monitorIA)
- ✅ Envio em massa de mensagens
- ✅ Personalização com nome
- ✅ Progresso em tempo real
- ✅ Histórico de envios
- ✅ Relatórios em Excel
- ✅ Sistema de login
- ✅ Logs detalhados

---

## 🆘 Precisa de Ajuda?

Consulte os guias:
- `SOLUCAO_ERROS.md` - Soluções para erros comuns
- `ESTRUTURA.md` - Arquitetura do sistema
- `COMANDOS.md` - Lista de comandos

---

**Desenvolvido por monitorIA - Departamento de T.I**  
**Versão:** 3.0.0 - Sistema 100% Web
