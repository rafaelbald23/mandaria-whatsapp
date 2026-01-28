# 🚀 Guia de Início - Robô WhatsApp monitorIA

## 📌 Passo a Passo Simples

### 1️⃣ Abrir Terminal

Pressione `Win + R`, digite `cmd` e pressione Enter.

### 2️⃣ Navegar para a Pasta

```bash
cd "Robo - Usuario\web"
```

### 3️⃣ Instalar Dependências

```bash
instalar_dependencias.bat
```

**OU:**

```bash
pip install -r requirements.txt
```

### 4️⃣ Executar o Sistema

```bash
python app.py
```

### 5️⃣ Abrir no Navegador

Abra: **http://localhost:5000**

### 6️⃣ Fazer Login

- **Usuário:** `admin`
- **Senha:** `admin123`

---

## ✅ Pronto!

Agora você pode:
1. Enviar planilhas Excel
2. Disparar mensagens em massa
3. Acompanhar progresso em tempo real
4. Ver histórico de envios

---

## 🎯 Comandos Rápidos

### Instalar tudo de uma vez:

```bash
cd "Robo - Usuario\web"
pip install -r requirements.txt
python app.py
```

### Testar se está tudo OK:

```bash
python testar_instalacao.py
```

---

## 📱 Como Usar

### 1. Preparar Planilha

Crie um arquivo Excel (.xlsx) com:

| Contato       | Nome    |
|---------------|---------|
| 11999999999   | João    |
| 11988888888   | Maria   |

- **Contato:** Número com DDD (sem espaços ou caracteres)
- **Nome:** Nome do contato (opcional)

### 2. Enviar Mensagens

1. Acesse: http://localhost:5000
2. Faça login
3. Clique em "Enviar Mensagens"
4. Faça upload da planilha
5. Digite a mensagem (use `{nome}` para personalizar)
6. Clique em "Iniciar Envio"
7. Escaneie o QR Code do WhatsApp Web
8. Aguarde o envio

### 3. Acompanhar

- Veja o progresso em tempo real
- Mensagens enviadas aparecem em verde
- Erros aparecem em vermelho
- Ao final, baixe o relatório

---

## 🐛 Problemas Comuns

### ❌ "No module named 'flask'"

**Solução:**
```bash
pip install -r requirements.txt
```

### ❌ "python não é reconhecido"

**Solução:**
1. Instale Python: https://www.python.org/downloads/
2. Durante instalação, marque "Add Python to PATH"
3. Reinicie o terminal

### ❌ "Porta 5000 em uso"

**Solução:**
```bash
# Matar processo na porta 5000
netstat -ano | findstr :5000
taskkill /PID <número> /F

# Ou mudar a porta em app.py (última linha)
```

### ❌ Outros erros

Consulte: `SOLUCAO_ERROS.md`

---

## 🧪 Verificar Instalação

Execute:
```bash
python testar_instalacao.py
```

Isso vai mostrar:
- ✅ O que está instalado
- ❌ O que está faltando
- 📁 Estrutura de pastas
- 📄 Arquivos principais

---

## 📚 Mais Informações

- **README.md** - Visão geral
- **COMO_EXECUTAR.md** - Guia completo
- **SOLUCAO_ERROS.md** - Solução de problemas
- **ESTRUTURA.md** - Arquitetura do sistema

---

## 🎨 Recursos

- ✅ Interface moderna (design monitorIA)
- ✅ Envio em massa
- ✅ Personalização com nome
- ✅ Progresso em tempo real
- ✅ Histórico de envios
- ✅ Relatórios Excel
- ✅ Sistema de login
- ✅ Logs detalhados

---

## 🔐 Segurança

⚠️ **IMPORTANTE:**
- Altere a senha após primeiro login
- Não compartilhe suas credenciais
- Use apenas para fins legítimos
- Respeite a privacidade dos contatos

---

## 💡 Dicas

1. **Teste primeiro:** Envie para poucos contatos antes de enviar em massa
2. **Intervalo:** O sistema aguarda 8 segundos entre mensagens (evita bloqueio)
3. **Planilha:** Mantenha os números limpos (apenas números)
4. **Personalização:** Use `{nome}` na mensagem para personalizar
5. **Backup:** Salve suas planilhas antes de enviar

---

## 📞 Suporte

Problemas? Siga esta ordem:

1. ✅ Execute `python testar_instalacao.py`
2. ✅ Consulte `SOLUCAO_ERROS.md`
3. ✅ Verifique os logs em `Logs/`
4. ✅ Entre em contato com o T.I

---

**Desenvolvido por monitorIA - Departamento de T.I**  
**Versão:** 3.0.0 - Sistema 100% Web
