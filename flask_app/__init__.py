"""
The flask application package.
"""

from flask import Flask
#import configuration
app = Flask(__name__)

# See configuration.py for possible configuration objects
app.config.from_object('configuration.Development')

import flask_app.views
