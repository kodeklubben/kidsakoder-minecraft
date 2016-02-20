"""
The flask application package.
"""

from flask import Flask

DATABASE = 'C:\\Users\\Andreas\\dev\\kidsakoder-minecraft\\flask_app\\tmp\\database.db'
SECRET_KEY = 'development key'
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


import flask_app.database
import flask_app.views
