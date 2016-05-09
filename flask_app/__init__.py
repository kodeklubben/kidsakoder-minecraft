# -*- coding: utf-8 -*-
"""
The flask application package.
"""

from flask import Flask, g
from datetime import datetime


app = Flask(__name__)

# Load configurations
app.config.from_pyfile('config/secret_key.py')  # Load first in case we want to use in other config opt
app.config.from_pyfile('config/configuration.py')
app.config.from_pyfile('config/secret_config.py')
# Development configuration overrides. Comment out for production
app.config.from_pyfile('config/development.py')


# Set locale for datetime format
import locale
def try_locale(locale_list):
    """ Recursively try locales from a list """
    if not locale_list:
        print 'Locale not found'
        return
    head, tail = locale_list[0], locale_list[1:]
    try:
        locale.setlocale(locale.LC_TIME, head)
        print 'Locale set to ' + head
    except locale.Error:
        try_locale(tail)

our_locales = ('nb_NO', 'no_NO', 'norwegian-bokmal')
try_locale(our_locales)

print 'Preferred locale encoding: ' + locale.getpreferredencoding()

# Initialize Flask-Security
from database import db, roles_users
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from admin import initAdmin
initAdmin()

#from datetime import datetime
@app.context_processor
def inject_year():
    """ Make year available in templates """
    return dict(year=datetime.now().year)

# Do last
import flask_app.views
