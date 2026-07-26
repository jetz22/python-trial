from flask_security import Security, SQLAlchemySessionUserDatastore

from app import db
from app.models import User, Role

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security()
