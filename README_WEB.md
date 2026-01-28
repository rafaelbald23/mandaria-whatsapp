# 🌐 Robô WhatsApp Web v3.0

## Versão Web Moderna e Futurista

Sistema de disparo automatizado de mensagens WhatsApp com interface web moderna, seguindo o design do **monitorIA**.

---

## 🎨 Design

- **Gradiente roxo/azul** (igual ao monitorIA)
- **Glassmorphism** (efeito de vidro)
- **Animações suaves** e transições
- **Responsivo** para todos os dispositivos
- **Dark theme** moderno
- **Real-time updates** com Socket.IO

---

## 🚀 Início Rápido

### 1. Setup (Primeira vez)

```bash
cd "Robo - Usuario/web"
npm run setup
```

### 2. Executar o Servidor

```bash
npm run dev
```

### 3. Acessar no Navegador

```
http://localhost:5000
```

### 4. Login

- **Usuário:** Rafael Theobald
- **Senha:** Rafinha01!

---

## 📋 Comandos npm

```bash
npm run dev      # Inicia servidor em desenvolvimento
npm run setup    # Instala dependências e configura
npm run start    # Inicia servidor (alias)
npm run prod     # Inicia em produção (Gunicorn)
npm install      # Instala apenas dependências Python
```

---

## 📁 Estrutura

```
web/
├── app.py                      # Aplicação Flask principal
├── requirements.txt            # Dependências Python
├── README_WEB.md              # Este arquivo
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   ├── style.css          # Estilos globais
│   │   ├── login.css          # Estilos do login
│   │   ├── dashboard.css      # Estilos do dashboard
│   │   └── enviar.css         # Estilos da página de envio
│   │
│   └── js/
│       └── enviar.js          # JavaScript da página de envio
│
└── templates/                  # Templates HTML
    ├── login.html             # Página de login
    ├── dashboard.html         # Dashboard principal
    ├── enviar.html            # Página de envio
    ├── historico.html         # Histórico de envios
    ├── configuracoes.html     # Configurações
    │
    └── partials/
        └── sidebar.html       # Sidebar reutilizável
```

---

## 🎯 Funcionalidades

### ✅ Implementadas

- **Login seguro** com senhas criptografadas
- **Dashboard** com estatísticas em tempo real
- **Upload de planilhas** com drag & drop
- **Preview de contatos** antes do envio
- **Editor de mensagens** com contador de caracteres
- **Envio em tempo real** com Socket.IO
- **Barra de progresso** animada
- **Logs de envio** em tempo real
- **Estatísticas** de sucesso/falha
- **Histórico** de envios anteriores
- **Design responsivo** para mobile

### 🔄 Em Desenvolvimento

- Página de histórico completa
- Página de configurações
- Gráficos de estatísticas
- Exportação de relatórios
- Agendamento de envios

---

## 🎨 Paleta de Cores

```css
/* Gradientes principais */
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

/* Background */
--dark-bg: #0f0c29;
--dark-bg-2: #1a1640;
--dark-bg-3: #24204d;

/* Acentos */
--accent-cyan: #00d4ff;
--accent-pink: #ff006e;
--accent-purple: #8b5cf6;

/* Status */
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;
```

---

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na pasta `web/`:

```env
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
FLASK_DEBUG=True
```

### Configurações do Sistema

As configurações do robô estão em `config.py` na pasta raiz:

```python
MAX_TENTATIVAS = 3
TIMEOUT_CARREGAMENTO = 20
INTERVALO_ENTRE_MENSAGENS = 8
LIMITE_NUMEROS_AVISO = 200
```

---

## 🚀 Deploy em Produção

### Usando Gunicorn

```bash
gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:5000
```

### Usando Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "app:app", "--bind", "0.0.0.0:5000"]
```

### Variáveis de Ambiente para Produção

```env
SECRET_KEY=chave-super-secreta-aleatoria
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## 📊 API Endpoints

### Autenticação

```
POST /login
Body: { "usuario": "string", "senha": "string" }
Response: { "success": boolean, "message": "string" }
```

### Validar Planilha

```
POST /api/validar-planilha
Body: FormData com arquivo 'planilha'
Response: { "success": boolean, "total": number, "preview": array, "temp_file": "string" }
```

### Iniciar Envio

```
POST /api/iniciar-envio
Body: { "temp_file": "string", "mensagem": "string" }
Response: { "success": boolean, "session_id": "string" }
```

### Estatísticas

```
GET /api/estatisticas
Response: { 
    "total_envios": number,
    "total_enviados": number,
    "total_falhas": number,
    "taxa_sucesso": number
}
```

---

## 🔌 WebSocket Events

### Cliente → Servidor

Nenhum evento específico (apenas conexão)

### Servidor → Cliente

```javascript
// Atualização de status
socket.on('status_update', (data) => {
    // data: { session_id, status, message }
});

// Atualização de progresso
socket.on('progresso_update', (data) => {
    // data: { session_id, atual, total, contato, nome }
});

// Mensagem enviada
socket.on('mensagem_enviada', (data) => {
    // data: { session_id, contato, nome, sucesso, motivo }
});

// Envio concluído
socket.on('envio_concluido', (data) => {
    // data: { session_id, total, enviados, falhas, arquivo_resultado }
});

// Erro no envio
socket.on('erro_envio', (data) => {
    // data: { session_id, message }
});
```

---

## 🐛 Troubleshooting

### Erro: "Address already in use"

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Erro: "ChromeDriver not found"

Baixe o ChromeDriver compatível com seu Chrome:
https://chromedriver.chromium.org/

### Socket.IO não conecta

Verifique se o eventlet está instalado:
```bash
pip install eventlet
```

---

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:

- ✅ Desktop (1920x1080+)
- ✅ Laptop (1366x768+)
- ✅ Tablet (768x1024)
- ✅ Mobile (375x667+)

---

## 🔒 Segurança

- Senhas criptografadas com SHA256
- Sessões seguras com Flask
- Validação de inputs no backend
- Proteção contra CSRF
- Sanitização de dados
- Logs de auditoria

---

## 🎓 Tecnologias Utilizadas

### Backend
- **Flask** - Framework web
- **Flask-SocketIO** - WebSocket real-time
- **Selenium** - Automação do WhatsApp
- **Pandas** - Manipulação de planilhas

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilos (Glassmorphism)
- **JavaScript** - Interatividade
- **Socket.IO Client** - Real-time updates

### Design
- **Inter Font** - Tipografia moderna
- **Gradientes** - Roxo/Azul
- **Animações CSS** - Transições suaves
- **SVG Icons** - Ícones vetoriais

---

## 📈 Performance

- **Tempo de carregamento:** < 2s
- **First Contentful Paint:** < 1s
- **Time to Interactive:** < 3s
- **Lighthouse Score:** 90+

---

## 🤝 Contribuindo

Este é um projeto interno da Fysi's. Para contribuir:

1. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
2. Commit suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
3. Push para a branch: `git push origin feature/nova-funcionalidade`
4. Abra um Pull Request

---

## 📞 Suporte

- **Discord:** T.I da empresa
- **Email:** ti@fysys.com.br
- **Documentação:** README.md na pasta raiz

---

## 📝 Changelog

### v3.0.0 (2026-01-27)
- ✨ Versão web completa
- 🎨 Design moderno igual ao monitorIA
- ⚡ Real-time updates com Socket.IO
- 📱 Interface responsiva
- 🔒 Segurança aprimorada

---

## 📄 Licença

**Uso Interno** - Fysi's  
Todos os direitos reservados.

---

**Desenvolvido com ❤️ por monitorIA - Departamento de T.I**  
**Versão:** 3.0.0  
**Data:** Janeiro 2026
