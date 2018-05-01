import logging
import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.tasks import generate_coords

#from app.config_common import *


class base_config(object):
    SITE_NAME = 'Flask-Startup'

    SECRET_KEY = 'houdini'

    ADMIN_CREDENTIALS = ('admin', 'pa$$word')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_BINDS = {
    #     # These binds allow you to add in multiple databases
    #     'alias': 'postgresql://postgres:password@localhost:5432/alias'
    # }

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'lorabeaconbase@gmail.com'
    MAIL_PASSWORD = 'loralora'

    ADMINS = ['kylebowman99@gmail.com']

    BCRYPT_LOG_ROUNDS = 13

    WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
    CLIENT_AUTH_TIMEOUT = 9999

    LOG_LEVEL = logging.INFO
    LOG_FILENAME = 'activity.log'

    JOBS = [
        {
            'id': 'job1',
            'func': generate_coords,
            'trigger': 'interval',
            'seconds': 10,
            'replace_existing': True
        }
    ]

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///app.db')
    }

    SCHEDULER_API_ENABLED = True


class dev_config(base_config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    WTF_CSRF_ENABLED = False
