from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt

debug_toolbar = DebugToolbarExtension()

db = SQLAlchemy()

mail = Mail()

login_manager = LoginManager()

bcrypt = Bcrypt()

from .models import User


@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()
