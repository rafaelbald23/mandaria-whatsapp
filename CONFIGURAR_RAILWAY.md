# 🚀 Configurar MandarIA no Railway

## Passo 1: Deploy da Evolution API

1. Acesse: https://railway.app/template/evolution-api
2. Clique em "Deploy Now"
3. Conecte sua conta GitHub
4. Configure as variáveis:
   - `AUTHENTICATION_API_KEY`: Crie uma senha forte (ex: `minha-chave-secreta-123`)
   - Deixe as outras no padrão
5. Clique em "Deploy"
6. Aguarde 2-3 minutos

## Passo 2: Obter URL da Evolution API

1. No Railway, clique no projeto Evolution API
2. Vá em "Settings" → "Domains"
3. Clique em "Generate Domain"
4. Copie a URL (ex: `https://evolution-api-production-xxxx.up.railway.app`)

## Passo 3: Configurar MandarIA

1. No Railway, vá no projeto MandarIA
2. Clique em "Variables"
3. Adicione estas variáveis:

```
USE_EVOLUTION_API=true
EVOLUTION_API_URL=https://evolution-api-production-xxxx.up.railway.app
EVOLUTION_API_KEY=minha-chave-secreta-123
EVOLUTION_INSTANCE=mandaria
```

**IMPORTANTE:** Use a mesma chave que você criou no Passo 1!

## Passo 4: Fazer Deploy

O Railway vai fazer o deploy automaticamente quando você adicionar as variáveis.

## Passo 5: Testar

1. Acesse seu MandarIA: `https://seu-mandaria.railway.app`
2. Faça login
3. Vá em "Enviar Mensagens"
4. Preencha os dados
5. Clique em "Iniciar Envio"
6. Um QR Code será exibido
7. Escaneie com seu WhatsApp
8. Pronto! 🎉

## Troubleshooting

### Erro: "Falha ao inicializar navegador"
- Verifique se as variáveis estão corretas
- Confirme que a Evolution API está rodando
- Teste a URL da Evolution API no navegador

### QR Code não aparece
- Verifique os logs do Railway
- Confirme que a API Key está correta
- Tente recriar a instância

### Mensagens não enviam
- Verifique se o WhatsApp está conectado
- Confira os logs da Evolution API
- Teste enviar uma mensagem manualmente pela API

## Links Úteis

- Evolution API Docs: https://doc.evolution-api.com
- Railway Docs: https://docs.railway.app
- Suporte: Abra uma issue no GitHub

## Custos Estimados

- Evolution API: Gratuita
- Railway (ambos projetos): ~$10-15/mês
- Total: ~$10-15/mês

## Alternativa: Usar Evolution API Externa

Se preferir, pode usar uma Evolution API hospedada em outro lugar:
- Render (gratuito)
- Heroku
- VPS própria
- Servidor local

Basta mudar a `EVOLUTION_API_URL` para apontar para ela.
