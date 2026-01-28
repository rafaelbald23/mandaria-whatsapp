# 🚀 Opções de Execução - Robô WhatsApp monitorIA

## 🎯 Escolha Seu Método

### ⚡ Método 1: Automático (RECOMENDADO)

```bash
iniciar.bat
```

**O que faz:**
- ✅ Verifica Python
- ✅ Verifica dependências
- ✅ Instala se necessário
- ✅ Cria diretórios
- ✅ Inicia servidor

**Melhor para:** Iniciantes

---

### 🔧 Método 2: Instalador + Execução

```bash
# 1. Instalar
instalar_dependencias.bat

# 2. Executar
python app.py
```

**O que faz:**
- ✅ Instala todas as dependências
- ✅ Cria estrutura de pastas
- ✅ Verifica instalação
- ✅ Inicia servidor

**Melhor para:** Primeira instalação

---

### 💻 Método 3: Manual (Python)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar
python app.py
```

**O que faz:**
- ✅ Controle total
- ✅ Sem scripts intermediários

**Melhor para:** Desenvolvedores

---

### 📦 Método 4: Com npm

```bash
# 1. Setup (primeira vez)
npm run setup

# 2. Executar
npm run dev
```

**O que faz:**
- ✅ Usa scripts npm
- ✅ Padrão moderno

**Melhor para:** Quem tem Node.js

---

## 📊 Comparação

| Método | Dificuldade | Velocidade | Requer |
|--------|-------------|------------|--------|
| **Automático** | ⭐ Fácil | ⚡ Rápido | Python |
| **Instalador** | ⭐⭐ Médio | ⚡⚡ Médio | Python |
| **Manual** | ⭐⭐⭐ Difícil | ⚡⚡⚡ Lento | Python + pip |
| **npm** | ⭐⭐ Médio | ⚡⚡ Médio | Python + Node.js |

---

## 🎯 Qual Escolher?

### Primeira Vez?
```bash
iniciar.bat
```

### Já Instalou Antes?
```bash
python app.py
```

### Desenvolvedor?
```bash
npm run dev
```

### Problemas?
```bash
instalar_dependencias.bat
```

---

## 🔄 Fluxo Completo

### Instalação Inicial

```bash
# Opção A: Automático
iniciar.bat

# Opção B: Manual
instalar_dependencias.bat
python app.py

# Opção C: npm
npm run setup
npm run dev
```

### Uso Diário

```bash
# Opção A: Simples
iniciar.bat

# Opção B: Direto
python app.py

# Opção C: npm
npm run dev
```

---

## 🧪 Testar Instalação

Antes de executar, teste:

```bash
python testar_instalacao.py
```

Isso mostra:
- ✅ Dependências instaladas
- ❌ Dependências faltando
- 📁 Estrutura de pastas
- 📄 Arquivos principais

---

## 🐛 Solução de Problemas

### ❌ "No module named 'flask'"

```bash
pip install -r requirements.txt
```

### ❌ "python não é reconhecido"

1. Instale Python: https://www.python.org/downloads/
2. Marque "Add Python to PATH"
3. Reinicie terminal

### ❌ "npm não é reconhecido"

Use Python direto:
```bash
python app.py
```

### ❌ "Porta 5000 em uso"

Mude a porta em `app.py` (última linha):
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

---

## 📝 Comandos Úteis

### Parar Servidor
```
Ctrl + C
```

### Ver Logs
```bash
type Logs\web_app_*.log
```

### Limpar Cache
```bash
del /s /q __pycache__
```

### Reinstalar Dependências
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## 🎨 Após Iniciar

1. **Abra o navegador:** http://localhost:5000
2. **Faça login:**
   - Usuário: `admin`
   - Senha: `admin123`
3. **Use o sistema:**
   - Upload de planilhas
   - Envio de mensagens
   - Acompanhamento em tempo real

---

## 📚 Documentação

- **LEIA-ME-PRIMEIRO.txt** - Início super rápido
- **INICIO.md** - Guia completo
- **COMO_EXECUTAR.md** - Instruções detalhadas
- **SOLUCAO_ERROS.md** - Problemas comuns
- **README.md** - Visão geral

---

## ✅ Checklist

Antes de executar:

- [ ] Python 3.8+ instalado
- [ ] pip funcionando
- [ ] Dependências instaladas
- [ ] Porta 5000 disponível
- [ ] Google Chrome instalado

---

## 🎯 Resumo Rápido

### Para Iniciantes
```bash
iniciar.bat
```

### Para Desenvolvedores
```bash
npm run dev
```

### Para Produção
```bash
npm run prod
```

---

**Desenvolvido por monitorIA - Departamento de T.I**  
**Versão:** 3.0.0 - Sistema 100% Web
