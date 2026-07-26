import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_security.utils import hash_password

migrate = Migrate()
db = SQLAlchemy()


def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    instance_path = os.path.join(base_dir, 'instance')
    os.makedirs(instance_path, exist_ok=True)

    app = Flask(__name__, instance_path=instance_path)
    app.config['SECRET_KEY'] = 'this-is-a-test-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(instance_path, 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECURITY_PASSWORD_SALT'] = 'this-is-a-test-salt'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_REGISTERABLE'] = False
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    app.config['SECURITY_LOGIN_URL'] = '/login'
    app.config['SECURITY_POST_LOGIN_VIEW'] = '/'
    app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/login'
    app.config['SQLALCHEMY_ECHO'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.security import security, user_datastore
    from app.views import views_bp
    from app.views.auth import auth_bp

    security.init_app(app, user_datastore, register_blueprint=False)
    app.register_blueprint(views_bp)
    app.register_blueprint(auth_bp)
    app.add_url_rule('/login', endpoint='security.login', view_func=app.view_functions['auth.login'], methods=['GET', 'POST'])
    app.add_url_rule('/logout', endpoint='security.logout', view_func=app.view_functions['auth.logout'])

    with app.app_context():
        db.create_all()
        _create_default_security_users()

    return app


def _create_default_security_users():
    from app.security import user_datastore

    user_role = user_datastore.find_role('user')
    if not user_role:
        user_role = user_datastore.create_role(name='user', description='Regular user')

    admin_role = user_datastore.find_role('admin')
    if not admin_role:
        admin_role = user_datastore.create_role(name='admin', description='Administrator')

    if not user_datastore.find_user(email='user@example.com'):
        user_datastore.create_user(
            email='user@example.com',
            password=hash_password('password'),
            fs_uniquifier='user-1',
            roles=[user_role]
        )

    if not user_datastore.find_user(email='admin@example.com'):
        user_datastore.create_user(
            email='admin@example.com',
            password=hash_password('password'),
            fs_uniquifier='admin-1',
            roles=[admin_role]
        )

    db.session.commit()
