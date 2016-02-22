"""
The flask application package.
"""

from flask import Flask
from flask.ext import login
import models

app = Flask(__name__)

# Flask-Login initialization
login_manager = login.LoginManager()
login_manager.init_app(app)
@login_manager.user_user_loader
def load_user(user_id):
    return models.User.get(user_id)

# See configuration.py for possible configuration objects
app.config.from_object('flask_app.configuration.Development')

import flask_app.database
import flask_app.views
