from flask import Flask

app = Flask(__name__)

app.config.from_object('app.config')

from app.logger_setup import logger


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_mail import Mail
mail = Mail(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = DebugToolbarExtension(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from app.views import main, user, error
app.register_blueprint(user.userbp)

from flask_login import LoginManager
from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'


@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()
