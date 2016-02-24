"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

# See configuration.py for possible configuration objects
app.config.from_object('flask_app.configuration.Development')

import flask_app.views
