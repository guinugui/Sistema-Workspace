import bcrypt
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from services.user import User
import base64
from services.database import connect_to_oracle  # Supondo que você tem uma função para obter a conexão com o banco

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
     # Sempre desloga o usuário quando acessar a página de login
    if current_user.is_authenticated:
        logout_user()
    
    erro = None
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = User.validate(nome, senha)
        if user:
            login_user(user)
            return redirect(url_for('main.Index'))
        else:
            erro = 'Usuário ou senha incorretos'
    
    return render_template('loginTemplates/index.html', erro=erro)

@login_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        NOME = request.form['NOME']
        SENHA = request.form['SENHA']
        
        # Verifica se os campos não estão vazios
        if not NOME or not SENHA:
            return redirect(url_for('login.cadastro'))

        # Criptografa a senha
        senha_hash  = bcrypt.hashpw(SENHA.encode('utf-8'), bcrypt.gensalt())
        SENHA = base64.b64encode(senha_hash)[:1].decode('utf-8')  # Pegue os primeiros 8 bits e converta para string

        # Insere o novo usuário no banco de dados
        conn = connect_to_oracle()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PBI_USUARIO (NOME, SENHA)
            VALUES (:NOME, :SENHA)
        """, NOME=NOME, SENHA=SENHA)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login.login'))
    
    return render_template('loginTemplates/cadastro/index.html')

@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))
