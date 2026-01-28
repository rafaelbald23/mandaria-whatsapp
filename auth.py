import json
import hashlib
from pathlib import Path
from datetime import datetime
import config

class AuthManager:
    def __init__(self):
        self.usuarios_file = config.USUARIOS_FILE
        self.clientes_file = config.BASE_DIR / "clientes.json"
        self._criar_arquivo_padrao()
    
    def _criar_arquivo_padrao(self):
        """Cria arquivo de usuários padrão se não existir"""
        if not self.usuarios_file.exists():
            usuarios_padrao = {
                "admin": {
                    "senha": self._hash_senha("admin123"),
                    "tipo": "admin",
                    "nome_completo": "Administrador",
                    "email": "admin@monitoria.com",
                    "criado_em": datetime.now().isoformat()
                }
            }
            self._salvar_usuarios(usuarios_padrao)
        
        # Cria arquivo de clientes se não existir
        if not self.clientes_file.exists():
            self._salvar_clientes({})
    
    def _hash_senha(self, senha):
        """Gera hash SHA256 da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def _carregar_usuarios(self):
        """Carrega usuários do arquivo"""
        try:
            with open(self.usuarios_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _salvar_usuarios(self, usuarios):
        """Salva usuários no arquivo"""
        with open(self.usuarios_file, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)
    
    def _carregar_clientes(self):
        """Carrega clientes do arquivo"""
        try:
            with open(self.clientes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _salvar_clientes(self, clientes):
        """Salva clientes no arquivo"""
        with open(self.clientes_file, 'w', encoding='utf-8') as f:
            json.dump(clientes, f, indent=4, ensure_ascii=False)
    
    def validar_login(self, usuario, senha):
        """Valida credenciais de login"""
        usuarios = self._carregar_usuarios()
        
        if usuario not in usuarios:
            return False, None
        
        user_data = usuarios[usuario]
        senha_hash = self._hash_senha(senha)
        
        # Verifica senha
        if user_data["senha"] != senha_hash:
            return False, None
        
        # Se for cliente, verifica se está ativo
        if user_data["tipo"] == "cliente":
            if not user_data.get("ativo", False):
                return False, "Cliente desativado. Entre em contato com o suporte."
            
            if user_data.get("bloqueado", False):
                return False, "Acesso bloqueado por falta de pagamento."
        
        return True, user_data
    
    def is_admin(self, usuario):
        """Verifica se usuário é admin"""
        usuarios = self._carregar_usuarios()
        if usuario in usuarios:
            return usuarios[usuario].get("tipo") == "admin"
        return False
    
    def adicionar_cliente(self, usuario, senha, nome_completo, email, empresa="", telefone=""):
        """Adiciona novo cliente"""
        usuarios = self._carregar_usuarios()
        
        if usuario in usuarios:
            return False, "Usuário já existe"
        
        usuarios[usuario] = {
            "senha": self._hash_senha(senha),
            "tipo": "cliente",
            "nome_completo": nome_completo,
            "email": email,
            "empresa": empresa,
            "telefone": telefone,
            "ativo": True,
            "bloqueado": False,
            "criado_em": datetime.now().isoformat(),
            "ultimo_acesso": None,
            "total_envios": 0
        }
        
        self._salvar_usuarios(usuarios)
        return True, "Cliente cadastrado com sucesso"
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        usuarios = self._carregar_usuarios()
        clientes = []
        
        for usuario, dados in usuarios.items():
            if dados.get("tipo") == "cliente":
                clientes.append({
                    "usuario": usuario,
                    **dados
                })
        
        return clientes
    
    def obter_cliente(self, usuario):
        """Obtém dados de um cliente"""
        usuarios = self._carregar_usuarios()
        if usuario in usuarios and usuarios[usuario].get("tipo") == "cliente":
            return usuarios[usuario]
        return None
    
    def atualizar_cliente(self, usuario, dados):
        """Atualiza dados de um cliente"""
        usuarios = self._carregar_usuarios()
        
        if usuario not in usuarios or usuarios[usuario].get("tipo") != "cliente":
            return False, "Cliente não encontrado"
        
        # Atualiza apenas campos permitidos
        campos_permitidos = ["nome_completo", "email", "empresa", "telefone", "ativo", "bloqueado"]
        for campo in campos_permitidos:
            if campo in dados:
                usuarios[usuario][campo] = dados[campo]
        
        usuarios[usuario]["atualizado_em"] = datetime.now().isoformat()
        self._salvar_usuarios(usuarios)
        return True, "Cliente atualizado com sucesso"
    
    def ativar_cliente(self, usuario):
        """Ativa um cliente"""
        return self.atualizar_cliente(usuario, {"ativo": True, "bloqueado": False})
    
    def desativar_cliente(self, usuario):
        """Desativa um cliente"""
        return self.atualizar_cliente(usuario, {"ativo": False})
    
    def bloquear_cliente(self, usuario):
        """Bloqueia um cliente por falta de pagamento"""
        return self.atualizar_cliente(usuario, {"bloqueado": True})
    
    def desbloquear_cliente(self, usuario):
        """Desbloqueia um cliente"""
        return self.atualizar_cliente(usuario, {"bloqueado": False})
    
    def remover_cliente(self, usuario):
        """Remove um cliente"""
        usuarios = self._carregar_usuarios()
        
        if usuario in usuarios and usuarios[usuario].get("tipo") == "cliente":
            del usuarios[usuario]
            self._salvar_usuarios(usuarios)
            return True, "Cliente removido com sucesso"
        
        return False, "Cliente não encontrado"
    
    def alterar_senha_cliente(self, usuario, senha_nova):
        """Altera senha de um cliente"""
        usuarios = self._carregar_usuarios()
        
        if usuario in usuarios and usuarios[usuario].get("tipo") == "cliente":
            usuarios[usuario]["senha"] = self._hash_senha(senha_nova)
            usuarios[usuario]["senha_alterada_em"] = datetime.now().isoformat()
            self._salvar_usuarios(usuarios)
            return True, "Senha alterada com sucesso"
        
        return False, "Cliente não encontrado"
    
    def registrar_acesso(self, usuario):
        """Registra último acesso do cliente"""
        usuarios = self._carregar_usuarios()
        
        if usuario in usuarios:
            usuarios[usuario]["ultimo_acesso"] = datetime.now().isoformat()
            self._salvar_usuarios(usuarios)
    
    def incrementar_envios(self, usuario):
        """Incrementa contador de envios do cliente"""
        usuarios = self._carregar_usuarios()
        
        if usuario in usuarios:
            usuarios[usuario]["total_envios"] = usuarios[usuario].get("total_envios", 0) + 1
            self._salvar_usuarios(usuarios)
