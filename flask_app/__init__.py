# -*- coding: utf-8 -*-
"""
The flask application package.
"""

from flask import Flask, g


app = Flask(__name__)

# Load configurations
app.config.from_pyfile('config/secret_key.py')  # Load first in case we want to use in other config opt
app.config.from_pyfile('config/configuration.py')
app.config.from_pyfile('config/secret_config.py')
# Development configuration overrides. Comment out for production
app.config.from_pyfile('config/development.py')

# Initialize logger
import logging.handlers
file_handler = logging.handlers.RotatingFileHandler(app.config['APP_LOG_FILE'])
if app.debug:  # Log everything in debug mode
    file_handler.setLevel(logging.DEBUG)
else:
    file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)


# Set locale for datetime format
import locale
def try_locale(locale_list):
    """ Recursively try locales from a list """
    if not locale_list:
        app.logger.warning('Locale not found')
        return
    head, tail = locale_list[0], locale_list[1:]
    try:
        locale.setlocale(locale.LC_TIME, head)
        app.logger.info('Locale set to ' + head)
    except locale.Error:
        try_locale(tail)

our_locales = ('nb_NO.utf8', 'nb_NO', 'no_NO', 'norwegian-bokmal')
try_locale(our_locales)
app.logger.debug('Preferred locale encoding: ' + locale.getpreferredencoding())


# Initialize Flask-Security
from database import db, roles_users
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Initialize Flask-Admin
from admin import init_admin
init_admin()


from datetime import datetime
@app.context_processor
def inject_year():
    """ Make year available in templates """
    return dict(year=datetime.now().year)


# Do last
import flask_app.views
