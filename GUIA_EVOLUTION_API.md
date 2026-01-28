# Guia: Instalar Evolution API no Railway

## Passo 1: Deploy da Evolution API

1. Acesse: https://railway.app
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo"
4. Busque por: `EvolutionAPI/evolution-api`
5. Ou use o template direto: https://railway.app/template/evolution-api

## Passo 2: Configurar Variáveis de Ambiente

No Railway, adicione estas variáveis:

```env
AUTHENTICATION_API_KEY=sua-chave-secreta-aqui
SERVER_URL=https://seu-dominio-evolution.railway.app
```

## Passo 3: Obter URL da Evolution API

Após o deploy, copie a URL pública da Evolution API.
Exemplo: `https://evolution-api-production-xxxx.up.railway.app`

## Passo 4: Configurar MandarIA

No projeto MandarIA, adicione estas variáveis de ambiente no Railway:

```env
EVOLUTION_API_URL=https://evolution-api-production-xxxx.up.railway.app
EVOLUTION_API_KEY=sua-chave-secreta-aqui
EVOLUTION_INSTANCE=mandaria
USE_EVOLUTION_API=true
```

## Passo 5: Testar

1. Acesse o MandarIA
2. Clique em "Enviar Mensagens"
3. Um QR Code será gerado
4. Escaneie com seu WhatsApp
5. Pronto! Agora funciona no Railway

## Vantagens

✅ Funciona perfeitamente no Railway
✅ Não precisa de Chrome/Selenium
✅ Mais rápido e estável
✅ Suporta múltiplas instâncias
✅ API REST completa

## Custos

- Evolution API: Gratuita (open source)
- Railway: ~$5-10/mês (dependendo do uso)

## Alternativa Rápida

Se preferir, posso adaptar o código para usar a Evolution API hospedada em outro lugar (Render, Heroku, VPS própria).

## Documentação

- Evolution API: https://doc.evolution-api.com
- GitHub: https://github.com/EvolutionAPI/evolution-api
