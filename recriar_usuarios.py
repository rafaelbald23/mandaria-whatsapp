"""
Script para recriar arquivo de usuários com novo formato
"""
import json
import hashlib
from datetime import datetime
from pathlib import Path

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Novo formato de usuários
usuarios = {
    "admin": {
        "senha": hash_senha("admin123"),
        "tipo": "admin",
        "nome_completo": "Administrador",
        "email": "admin@monitoria.com",
        "criado_em": datetime.now().isoformat()
    }
}

# Salva arquivo
with open('usuarios.json', 'w', encoding='utf-8') as f:
    json.dump(usuarios, f, indent=4, ensure_ascii=False)

print("✅ Arquivo de usuários recriado com sucesso!")
print()
print("Login Admin:")
print("  Usuário: admin")
print("  Senha: admin123")
