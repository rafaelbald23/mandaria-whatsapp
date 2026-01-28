# 👥 Sistema de Gerenciamento de Clientes

## 📋 Visão Geral

Sistema completo de gerenciamento de clientes com controle de acesso, bloqueio por falta de pagamento e administração centralizada.

---

## 🔐 Tipos de Usuário

### 1. Administrador
- Acesso total ao sistema
- Gerencia clientes
- Cria/edita/remove usuários
- Controla acesso e bloqueios

### 2. Cliente
- Acesso ao sistema de envio
- Histórico próprio
- Configurações limitadas

---

## 🎯 Funcionalidades Admin

### Painel de Gerenciamento
Acesse: **http://localhost:5000/admin/clientes**

### Cadastrar Cliente
1. Clique em "Adicionar Cliente"
2. Preencha os dados:
   - **Usuário** (login) *
   - **Senha** *
   - **Nome Completo** *
   - **Email**
   - **Empresa**
   - **Telefone**
3. Clique em "Adicionar"

### Controlar Acesso

#### Ativar Cliente
- Cliente pode fazer login
- Acesso total ao sistema

#### Desativar Cliente
- Cliente não pode fazer login
- Mensagem: "Cliente desativado"

#### Bloquear Cliente
- Bloqueio por falta de pagamento
- Cliente não pode fazer login
- Mensagem: "Acesso bloqueado por falta de pagamento"

#### Desbloquear Cliente
- Remove bloqueio
- Cliente volta a ter acesso

### Alterar Senha
1. Clique em "Senha" no card do cliente
2. Digite a nova senha
3. Confirme

### Remover Cliente
1. Clique em "Remover"
2. Confirme a ação
3. Cliente é permanentemente removido

---

## 📊 Estatísticas

O painel mostra:
- **Total de Clientes**: Todos os cadastrados
- **Clientes Ativos**: Com acesso liberado
- **Bloqueados**: Por falta de pagamento

---

## 🎨 Status dos Clientes

### 🟢 Ativo
- Cliente pode acessar normalmente
- Cor: Verde

### 🔴 Inativo
- Cliente desativado pelo admin
- Não pode fazer login
- Cor: Vermelho

### 🟠 Bloqueado
- Bloqueado por falta de pagamento
- Não pode fazer login
- Cor: Laranja

---

## 🔄 Fluxo de Uso

### Para Admin

1. **Login**
   ```
   Usuário: admin
   Senha: admin123
   ```

2. **Acessar Painel**
   - Menu lateral → "Gerenciar Clientes"

3. **Cadastrar Cliente**
   - Botão "Adicionar Cliente"
   - Preencher formulário
   - Salvar

4. **Gerenciar Cliente**
   - Ativar/Desativar
   - Bloquear/Desbloquear
   - Alterar senha
   - Remover

### Para Cliente

1. **Receber Credenciais**
   - Admin fornece usuário e senha

2. **Fazer Login**
   - Acessar http://localhost:5000
   - Inserir credenciais

3. **Usar Sistema**
   - Enviar mensagens
   - Ver histórico
   - Configurações

---

## 🛡️ Segurança

### Senhas
- Armazenadas com hash SHA256
- Nunca salvas em texto puro
- Admin pode alterar quando necessário

### Controle de Acesso
- Verificação em cada login
- Bloqueio imediato quando necessário
- Logs de todas as ações

### Auditoria
- Registro de último acesso
- Contador de envios
- Histórico de alterações

---

## 📁 Estrutura de Dados

### Arquivo: `usuarios.json`

```json
{
  "admin": {
    "senha": "hash_sha256",
    "tipo": "admin",
    "nome_completo": "Administrador",
    "email": "admin@monitoria.com",
    "criado_em": "2026-01-27T17:00:00"
  },
  "cliente1": {
    "senha": "hash_sha256",
    "tipo": "cliente",
    "nome_completo": "João Silva",
    "email": "joao@empresa.com",
    "empresa": "Empresa XYZ",
    "telefone": "11999999999",
    "ativo": true,
    "bloqueado": false,
    "criado_em": "2026-01-27T17:30:00",
    "ultimo_acesso": "2026-01-27T18:00:00",
    "total_envios": 5
  }
}
```

---

## 🔧 API Endpoints

### Listar Clientes
```
GET /api/admin/clientes
```

### Adicionar Cliente
```
POST /api/admin/clientes/adicionar
Body: {
  "usuario": "cliente1",
  "senha": "senha123",
  "nome_completo": "João Silva",
  "email": "joao@empresa.com",
  "empresa": "Empresa XYZ",
  "telefone": "11999999999"
}
```

### Ativar Cliente
```
POST /api/admin/clientes/{usuario}/ativar
```

### Desativar Cliente
```
POST /api/admin/clientes/{usuario}/desativar
```

### Bloquear Cliente
```
POST /api/admin/clientes/{usuario}/bloquear
```

### Desbloquear Cliente
```
POST /api/admin/clientes/{usuario}/desbloquear
```

### Alterar Senha
```
POST /api/admin/clientes/{usuario}/alterar-senha
Body: {
  "senha_nova": "nova_senha123"
}
```

### Remover Cliente
```
POST /api/admin/clientes/{usuario}/remover
```

---

## 💡 Casos de Uso

### Caso 1: Novo Cliente
1. Admin cadastra cliente
2. Cliente recebe credenciais
3. Cliente faz login
4. Cliente usa sistema

### Caso 2: Falta de Pagamento
1. Admin bloqueia cliente
2. Cliente tenta login
3. Recebe mensagem de bloqueio
4. Cliente regulariza pagamento
5. Admin desbloqueia
6. Cliente volta a acessar

### Caso 3: Cliente Inativo
1. Admin desativa cliente
2. Cliente não pode mais acessar
3. Quando necessário, admin reativa

### Caso 4: Esqueceu Senha
1. Cliente solicita nova senha
2. Admin altera senha
3. Admin envia nova senha
4. Cliente faz login

---

## 📝 Boas Práticas

### Para Admin

1. **Senhas Fortes**
   - Mínimo 8 caracteres
   - Letras, números e símbolos

2. **Documentação**
   - Anote quando criar clientes
   - Registre motivos de bloqueio

3. **Comunicação**
   - Avise cliente antes de bloquear
   - Explique motivo do bloqueio

4. **Backup**
   - Faça backup do `usuarios.json`
   - Guarde em local seguro

### Para Clientes

1. **Segurança**
   - Não compartilhe senha
   - Faça logout após usar

2. **Suporte**
   - Entre em contato com admin
   - Relate problemas

---

## 🚨 Mensagens de Erro

### "Cliente desativado"
- **Causa**: Admin desativou o acesso
- **Solução**: Contatar admin

### "Acesso bloqueado por falta de pagamento"
- **Causa**: Pagamento pendente
- **Solução**: Regularizar pagamento

### "Usuário ou senha incorretos"
- **Causa**: Credenciais inválidas
- **Solução**: Verificar dados ou solicitar nova senha

---

## 🔄 Migração de Usuários Antigos

Se você tinha usuários no formato antigo, execute:

```bash
python recriar_usuarios.py
```

Isso recria o arquivo com o novo formato.

---

## 📞 Suporte

### Para Admin
- Acesse: `/admin/clientes`
- Gerencie todos os clientes
- Controle total do sistema

### Para Clientes
- Entre em contato com admin
- Relate problemas de acesso
- Solicite alterações

---

## ✅ Checklist Admin

- [ ] Fez login como admin
- [ ] Acessou painel de clientes
- [ ] Cadastrou primeiro cliente
- [ ] Testou ativar/desativar
- [ ] Testou bloquear/desbloquear
- [ ] Alterou senha de teste
- [ ] Verificou estatísticas

---

## 🎯 Próximos Passos

1. **Login como Admin**
   ```
   Usuário: admin
   Senha: admin123
   ```

2. **Acessar Painel**
   - http://localhost:5000/admin/clientes

3. **Cadastrar Clientes**
   - Adicione seus clientes
   - Configure acessos

4. **Gerenciar**
   - Controle acessos
   - Bloqueie quando necessário
   - Mantenha sistema organizado

---

**Desenvolvido por monitorIA - Departamento de T.I**  
**Versão:** 3.1.0 - Sistema com Gerenciamento de Clientes  
**Data:** Janeiro 2026
