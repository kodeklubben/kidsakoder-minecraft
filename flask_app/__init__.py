# -*- coding: utf-8 -*-
"""
The flask application package.
"""

from flask import Flask, g
from datetime import datetime


app = Flask(__name__)

# Load configurations
app.config.from_pyfile('config/configuration.py')
app.config.from_pyfile('config/secret_key.py')
app.config.from_pyfile('config/secret_config.py')
# Development configuration. Comment out for production
app.config.from_pyfile('config/development.py')


# Set locale for datetime format
import locale
try:
    # For UNIX(-like) if the locale is installed
    locale.setlocale(locale.LC_TIME, 'nb_NO')
    print 'Locale set to nb_NO'
except locale.Error:
    try:
        # This might be generally more default installed
        locale.setlocale(locale.LC_TIME, 'no_NO')
        print 'Locale set to no_NO'
    except locale.Error:
        try:
            # Should work for windows
            locale.setlocale(locale.LC_TIME, 'norwegian-bokmal')
            print 'Locale set to norwegian-bokmal'
        except locale.Error:
            print 'Norwegian locale not found'


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
