from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.routes.auth import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/panel-control')
@login_required
@admin_required
def admin():
    return render_template('admin/panel_control_admin.html', user=current_user.username)