"""
The flask application package.
"""

from flask import Flask

DEBUG = True
app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS', silent=False)


import flask_app.database
import flask_app.views
