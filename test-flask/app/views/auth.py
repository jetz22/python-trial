from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.verify_and_update_password(password):
            login_user(user)
            return redirect(url_for('views.home'))
        error = 'Invalid credentials'
    return render_template('login.html', error=error)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
