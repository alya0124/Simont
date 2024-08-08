from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return redirect(url_for('auth.iniciar_sesion'))

@main_bp.route('/inicio')
@login_required
def inicio():
    admin = current_user.admin
    return render_template('index.html', user=current_user.username, admin=admin)
