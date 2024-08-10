from flask import Flask, redirect, url_for
from flask_login import LoginManager
from login.login import login_bp
from formWorkspace.main import main_bp
from services.user import User

app = Flask(__name__, template_folder='templates')
app.secret_key = 'sua_chave_secreta_aqui'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(main_bp, url_prefix='/main')

@app.route('/')
def home():
    return redirect(url_for('login.login'))

if __name__ == '__main__':
    app.run(debug=True)
