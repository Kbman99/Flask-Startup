import logging

from app.config_common import *


# DEBUG has to be to False in a production environment for security reasons
DEBUG = False

# Secret key for generating tokens
SECRET_KEY = 'houdini'

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'pa$$word')
