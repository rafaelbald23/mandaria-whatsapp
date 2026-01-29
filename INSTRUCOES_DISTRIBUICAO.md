# MandarIA - Instruções de Distribuição do Agente Local

## Pacote Criado

**Arquivo:** `C:\Users\rafae\Desktop\MandarIA-Agente-v3.1.zip`  
**Tamanho:** ~10 KB  
**Data:** 29/01/2026

## Conteúdo do Pacote

```
MandarIA-Agente-v3.1.zip
├── agente_local.py          # Agente principal (9.9 KB)
├── whatsapp_sender.py       # Envio de mensagens (13.6 KB)
├── utils.py                 # Utilitários (3.4 KB)
├── config.py                # Configurações (1.1 KB) ✅ CORRIGIDO
├── requirements.txt         # Dependências Python (343 bytes)
├── instalar_agente.bat      # Instalador (1.5 KB)
├── iniciar_agente.bat       # Inicializador (560 bytes)
└── LEIA-ME.txt             # Instruções (3.1 KB)
```

## Correções Aplicadas (v3.1)

### Problema Resolvido
O `config.py` original tentava criar a pasta `static/images` que não existe no agente, causando erro:
```
FileNotFoundError: [WinError 3] O sistema não pode encontrar o caminho especificado: 
'C:\\Users\\rafae\\Desktop\\MandarIA-Agente-v3.0\\static\\images'
```

### Solução Implementada
- Criado `config_agente.py` simplificado
- Remove referências a `IMAGENS_DIR` e pasta `static`
- Mantém apenas diretórios necessários: `Planilhas/` e `Logs/`
- Copiado como `config.py` no pacote final

## Instruções para o Cliente

### 1. Extração
```
1. Extrair MandarIA-Agente-v3.1.zip em qualquer pasta
2. Recomendado: C:\MandarIA
```

### 2. Instalação
```
1. Executar: instalar_agente.bat
2. Informar URL do servidor: https://mandaria.up.railway.app
3. Informar API Key: monitoria-api-key-2026
```

### 3. Uso
```
1. No sistema web: criar envio e clicar em "Iniciar Envio"
2. Executar: iniciar_agente.bat
3. Escanear QR Code do WhatsApp
4. Aguardar processamento
```

## Requisitos do Cliente

- ✅ Python 3.11 ou superior
- ✅ Google Chrome instalado
- ✅ Conexão com internet
- ✅ Windows 10/11

## Estrutura Criada Automaticamente

Após a primeira execução, o agente cria:

```
MandarIA-Agente-v3.1/
├── Planilhas/              # Planilhas temporárias
├── Logs/                   # Logs do sistema
├── chrome_profile/         # Perfil do Chrome (sessão WhatsApp)
└── agente_config.json      # Configurações salvas
```

## Logs

Os logs são salvos em:
```
Logs/agente_local_AAAAMMDD.log
```

Exemplo:
```
Logs/agente_local_20260129.log
```

## Configuração do Servidor

O agente se conecta ao servidor Railway:

**URL:** https://mandaria.up.railway.app  
**API Key:** monitoria-api-key-2026  
**Endpoint:** `/api/agente/fila`

## Fluxo de Funcionamento

1. Cliente acessa sistema web (Railway)
2. Cliente cria envio (planilha + mensagens)
3. Sistema adiciona envio na fila (`fila_envios.json`)
4. Cliente executa `iniciar_agente.bat`
5. Agente conecta ao WhatsApp Web
6. Agente busca fila no servidor a cada 5 segundos
7. Agente processa envios e envia resultados ao servidor
8. Sistema web atualiza status em tempo real

## Distribuição

### Para Clientes Individuais
Enviar o arquivo `MandarIA-Agente-v3.1.zip` por:
- Email
- Google Drive
- Dropbox
- WeTransfer

### Para Múltiplos Clientes
Hospedar em:
- GitHub Releases
- Google Drive (link público)
- Servidor próprio

## Suporte

Em caso de problemas:

1. Verificar logs em `Logs/`
2. Verificar se Chrome está instalado
3. Verificar conexão com internet
4. Confirmar URL do servidor
5. Verificar API Key

## Versões

- **v3.0** - Sistema híbrido inicial (com erro no config.py)
- **v3.1** - Correção do config.py + instruções completas ✅

## Próximos Passos

1. ✅ Pacote criado e testado
2. ⏳ Distribuir para clientes
3. ⏳ Coletar feedback
4. ⏳ Ajustes conforme necessário

---

**Desenvolvido por MonitorIA**  
**Janeiro 2026**
