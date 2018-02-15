from flask import Flask

from .core import db, login_manager, debug_toolbar, bcrypt, scheduler
from .helpers import register_blueprints
from app import config


def create_app(package_name, package_path, settings=None):
    app = Flask(package_name,
                template_folder='templates')

    app.config.from_object(config.dev_config)

    if settings:
        app.config.update(settings)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'user.signin'

    scheduler.init_app(app)
    scheduler.start()

    bcrypt.init_app(app)

    debug_toolbar.init_app(app)

    register_blueprints(app, package_name, package_path)

    return app
