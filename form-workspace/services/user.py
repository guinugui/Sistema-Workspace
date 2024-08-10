import bcrypt
import base64
from services.database import connect_to_oracle

class User:
    def __init__(self, id_usuario, nome):
        self.id = id_usuario
        self.nome = nome

    @staticmethod
    def validate(nome, senha):
        conn = connect_to_oracle()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_USUARIO, NOME, SENHA FROM PBI_USUARIO WHERE NOME = :nome", nome=nome)
        user_row = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_row:
            user_id, user_nome, hashed_password = user_row
            # Hash a senha fornecida e compare apenas os primeiros 8 bits
            senha_hash = base64.b64encode(bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()))[:1].decode('utf-8')
            if senha_hash == hashed_password:
                return User(user_id, user_nome)
        
        return None

    @staticmethod
    def get(user_id):
        conn = connect_to_oracle()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_USUARIO, NOME FROM PBI_USUARIO WHERE ID_USUARIO = :user_id", user_id=user_id)
        user_row = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_row:
            user_id, user_nome = user_row
            return User(user_id, user_nome)
        
        return None

    # Métodos necessários para Flask-Login
    def is_active(self):
        return True  # Substitua por lógica adequada se necessário

    def is_authenticated(self):
        return True if hasattr(self, 'id') else False

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # Converta para string se necessário
