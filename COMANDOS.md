# 📋 Comandos do Sistema

## 🚀 Comandos Principais

### Desenvolvimento

```bash
npm run dev
```
Inicia o servidor em modo desenvolvimento.
- ✅ Auto-reload habilitado
- ✅ Debug mode ativo
- ✅ Logs detalhados
- 🌐 Acesso: http://localhost:5000

---

### Setup Inicial

```bash
npm run setup
```
Configura o ambiente pela primeira vez.
- ✅ Verifica Python
- ✅ Instala dependências
- ✅ Cria diretórios
- ✅ Prepara ambiente

---

### Produção

```bash
npm run prod
```
Inicia o servidor em modo produção.
- ✅ Gunicorn worker
- ✅ Otimizado para performance
- ✅ Sem debug
- 🌐 Acesso: http://0.0.0.0:5000

---

## 📦 Instalação

### Instalar Dependências

```bash
npm install
```
Instala apenas as dependências Python.

Equivalente a:
```bash
pip install -r requirements.txt
```

---

## 🧪 Testes e Qualidade

### Executar Testes

```bash
npm test
```
Executa a suite de testes.

### Verificar Código

```bash
npm run lint
```
Verifica qualidade do código com flake8.

### Formatar Código

```bash
npm run format
```
Formata código com black.

---

## 🔧 Comandos Alternativos

### Sem npm

Se você não tem npm instalado, pode usar:

#### Windows
```bash
dev.bat          # Desenvolvimento
setup.bat        # Setup inicial
```

#### Python Direto
```bash
python app.py    # Inicia servidor
```

---

## 📊 Comparação de Comandos

| Ação | npm | Alternativa |
|------|-----|-------------|
| **Desenvolvimento** | `npm run dev` | `dev.bat` ou `python app.py` |
| **Setup** | `npm run setup` | `setup.bat` |
| **Produção** | `npm run prod` | `gunicorn ...` |
| **Instalar** | `npm install` | `pip install -r requirements.txt` |

---

## 🎯 Fluxo de Trabalho

### Primeira Vez

```bash
# 1. Navegue até a pasta
cd "Robo - Usuario/web"

# 2. Configure o ambiente
npm run setup

# 3. Inicie o servidor
npm run dev
```

### Dia a Dia

```bash
# Apenas inicie o servidor
npm run dev
```

### Deploy em Produção

```bash
# Use o modo produção
npm run prod
```

---

## 🔥 Atalhos Úteis

### Parar o Servidor
```
Ctrl + C
```

### Reiniciar o Servidor
```
Ctrl + C
npm run dev
```

### Ver Logs em Tempo Real
```bash
# Windows
type ..\Logs\web_app_*.log

# Linux/Mac
tail -f ../Logs/web_app_*.log
```

---

## 🐛 Troubleshooting

### Erro: "npm não é reconhecido"

**Solução:** Instale o Node.js
```
https://nodejs.org/
```

### Erro: "python não é reconhecido"

**Solução:** Instale o Python 3.8+
```
https://www.python.org/
```

### Erro: "No module named 'flask'"

**Solução:** Execute o setup
```bash
npm run setup
```

### Erro: "Porta 5000 em uso"

**Solução:** Mude a porta no `app.py`
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

---

## 📱 Acesso Remoto

### Descobrir seu IP

```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

### Acessar de Outro Dispositivo

```
http://SEU_IP:5000
```

Exemplo: `http://192.168.1.100:5000`

---

## 🎨 Variáveis de Ambiente

Crie um arquivo `.env`:

```env
SECRET_KEY=sua-chave-secreta
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000
```

---

## 📚 Documentação Completa

- **COMO_EXECUTAR.md** - Guia detalhado de execução
- **README_WEB.md** - Documentação completa
- **WEB_INICIO_RAPIDO.md** - Início rápido

---

## ✅ Checklist

Antes de executar:

- [ ] Python 3.8+ instalado
- [ ] Node.js instalado (opcional)
- [ ] Executou `npm run setup`
- [ ] ChromeDriver no PATH
- [ ] Porta 5000 disponível

---

## 🎉 Pronto!

Agora você pode usar:

```bash
npm run dev
```

E começar a desenvolver! 🚀

---

**Desenvolvido por monitorIA - Departamento de T.I**  
**Versão:** 3.0.0  
**Suporte:** Discord do T.I
