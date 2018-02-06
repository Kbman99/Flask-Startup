from flask import Flask

from .core import db, login_manager, debug_toolbar, bcrypt
from .helpers import register_blueprints


def create_app(package_name, package_path, settings=None):
    app = Flask(package_name,
                template_folder='templates')

    app.config.from_pyfile('config.py')

    if settings:
        app.config.update(settings)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'user.signin'

    bcrypt.init_app(app)

    app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    debug_toolbar.init_app(app)

    register_blueprints(app, package_name, package_path)

    return app
