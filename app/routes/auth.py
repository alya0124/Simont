from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        user = User.get_by_username(user_name)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.inicio'))
        else:
            flash('La contraseña o usuario no es valido')
            return redirect(url_for('auth.iniciar_sesion'))
    return "Acción no autorizada", 405

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.iniciar_sesion'))

@auth_bp.route('/iniciar-sesion')
def iniciar_sesion():
    return render_template('login.html')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.admin:
             flash('No tienes acceso a esta página.')
             return redirect(url_for('auth.iniciar_sesion'))
        return f(*args, **kwargs)
    return decorated_function