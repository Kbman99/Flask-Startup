from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from flask_apscheduler import APScheduler

debug_toolbar = DebugToolbarExtension()

db = SQLAlchemy()

mail = Mail()

login_manager = LoginManager()

bcrypt = Bcrypt()

scheduler = APScheduler()

from .models import User


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()
