from flask import Blueprint, render_template
from flask_security import auth_required

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
@auth_required('session')
def home():
    return render_template('home.html', title="Home")

@views_bp.route('/about')
def about():
    return render_template('about.html', title="About")
