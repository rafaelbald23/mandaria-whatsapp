"""
Script para adicionar usuário admin
"""
from auth import AuthManager

# Cria instância do gerenciador
auth = AuthManager()

# Adiciona usuário admin
auth.adicionar_usuario("admin", "admin123")

print("✅ Usuário 'admin' adicionado com sucesso!")
print("   Usuário: admin")
print("   Senha: admin123")
