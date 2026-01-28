# 📁 Estrutura do Projeto Web

## Sistema 100% Web - Sem Desktop

Este projeto é **exclusivamente web**. Não há versão desktop.

---

## 🗂️ Estrutura de Arquivos

```
web/                                    # Raiz do projeto
│
├── 🐍 Backend (Python/Flask)
│   ├── app.py                         # Aplicação Flask principal
│   ├── config.py                      # Configurações
│   ├── auth.py                        # Autenticação
│   ├── utils.py                       # Utilitários
│   └── whatsapp_sender.py             # Lógica de envio
│
├── 🎨 Frontend
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css             # Estilos globais
│   │   │   ├── login.css             # Login
│   │   │   ├── dashboard.css         # Dashboard
│   │   │   └── enviar.css            # Envio
│   │   │
│   │   ├── js/
│   │   │   └── enviar.js             # JavaScript + Socket.IO
│   │   │
│   │   └── images/
│   │       └── monitoria-logo.png    # Logo oficial
│   │
│   └── templates/
│       ├── login.html                 # Tela de login
│       ├── dashboard.html             # Dashboard
│       ├── enviar.html                # Envio de mensagens
│       ├── historico.html             # Histórico
│       ├── configuracoes.html         # Configurações
│       │
│       └── partials/
│           └── sidebar.html           # Sidebar reutilizável
│
├── 📦 Configuração
│   ├── package.json                   # Scripts npm
│   ├── requirements.txt               # Dependências Python
│   ├── .env.example                   # Variáveis de ambiente
│   ├── .npmrc                         # Configuração npm
│   ├── .gitignore                     # Git ignore
│   │
│   ├── Dockerfile                     # Container Docker
│   └── docker-compose.yml             # Orquestração
│
├── 🚀 Scripts
│   ├── dev.bat                        # Desenvolvimento (Windows)
│   ├── setup.bat                      # Setup inicial (Windows)
│   └── iniciar.bat                    # Inicializador (Windows)
│
├── 📚 Documentação
│   ├── README.md                      # Visão geral
│   ├── README_WEB.md                  # Documentação completa
│   ├── COMO_EXECUTAR.md               # Guia de execução
│   ├── COMANDOS.md                    # Lista de comandos
│   ├── ESTRUTURA.md                   # Este arquivo
│   ├── LOGO_MONITORIA.md              # Sobre a logo
│   └── SOBRE_MONITORIA.md             # Design monitorIA
│
├── 📊 Dados (Criados automaticamente)
│   ├── Planilhas/                     # Planilhas de entrada/saída
│   ├── Logs/                          # Logs de execução
│   ├── usuarios.json                  # Usuários e senhas
│   └── chrome_profile/                # Perfil do Chrome
│
└── 🧪 Testes (Futuro)
    └── tests/                         # Testes automatizados
```

---

## 📦 Arquivos Principais

### Backend

#### `app.py` (Principal)
- Aplicação Flask
- Rotas e endpoints
- Socket.IO para real-time
- Lógica de sessões

#### `config.py`
- Configurações centralizadas
- Caminhos de diretórios
- Timeouts e intervalos
- XPaths do WhatsApp

#### `auth.py`
- Sistema de autenticação
- Criptografia SHA256
- CRUD de usuários
- Validação de login

#### `utils.py`
- Funções utilitárias
- Validação de dados
- Manipulação de planilhas
- Configuração de logs

#### `whatsapp_sender.py`
- Lógica de envio
- Selenium WebDriver
- Retry automático
- Tratamento de erros

---

### Frontend

#### Templates HTML

- **login.html** - Tela de login com design monitorIA
- **dashboard.html** - Dashboard com estatísticas
- **enviar.html** - Página de envio com real-time
- **historico.html** - Lista de envios anteriores
- **configuracoes.html** - Configurações do sistema
- **partials/sidebar.html** - Sidebar reutilizável

#### CSS

- **style.css** - Estilos globais, variáveis, componentes
- **login.css** - Estilos específicos do login
- **dashboard.css** - Estilos do dashboard e sidebar
- **enviar.css** - Estilos da página de envio

#### JavaScript

- **enviar.js** - Lógica de envio, Socket.IO, upload

---

## 🔄 Fluxo de Dados

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  login.html     │ ──→ auth.py ──→ usuarios.json
└─────────┬───────┘
          │
          ▼ (Login OK)
┌─────────────────┐
│ dashboard.html  │ ──→ app.py ──→ Estatísticas
└─────────┬───────┘
          │
          ▼ (Enviar)
┌─────────────────┐
│  enviar.html    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Upload xlsx    │ ──→ utils.py ──→ Validação
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ whatsapp_sender │ ──→ Selenium ──→ WhatsApp Web
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Socket.IO      │ ──→ Real-time updates
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Resultado.xlsx │ ──→ Planilhas/
└─────────────────┘
```

---

## 🚀 Como Executar

### Primeira Vez

```bash
cd web
npm run setup
```

### Desenvolvimento

```bash
npm run dev
```

### Produção

```bash
npm run prod
```

---

## 📊 Tamanho dos Arquivos

```
Backend Python:     ~15 KB
Frontend HTML:      ~25 KB
CSS:               ~20 KB
JavaScript:        ~10 KB
Documentação:      ~150 KB
─────────────────────────
Total:             ~220 KB
```

---

## 🎯 Características

### ✅ Sistema 100% Web
- Sem código desktop
- Sem Tkinter
- Sem dependências desktop
- Apenas navegador

### ✅ Modular
- Backend separado do frontend
- Componentes reutilizáveis
- Fácil manutenção

### ✅ Profissional
- Código limpo
- Documentação completa
- Padrões de mercado

---

## 🔧 Tecnologias

### Backend
- Python 3.8+
- Flask 3.0
- Flask-SocketIO 5.3
- Selenium 4.16
- Pandas 2.1

### Frontend
- HTML5
- CSS3 (Glassmorphism)
- JavaScript ES6+
- Socket.IO Client

### DevOps
- npm scripts
- Docker
- Gunicorn

---

## 📝 Notas

- **Não há versão desktop** - Sistema exclusivamente web
- **Logo monitorIA** integrada em `static/images/`
- **Dados locais** em `Planilhas/` e `Logs/`
- **Sessão persistente** do Chrome em `chrome_profile/`

---

**Desenvolvido por monitorIA - Departamento de T.I**  
**Versão:** 3.0.0 Web Only  
**Arquitetura:** 100% Web
