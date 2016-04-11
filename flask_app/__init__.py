"""
The flask application package.
"""

from flask import Flask
from flask_admin import Admin

app = Flask(__name__)

# See configuration.py for possible configuration objects
app.config.from_object('flask_app.configuration.Development')

# Initialize Flask-Security
from database import db
from flask_security import Security, SQLAlchemyUserDatastore
from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Initialize Flask-Admin and add needed views/pages
admin = Admin(app)

from datetime import datetime
@app.context_processor
def inject_year():
    """ Make year available in templates """
    return dict(year=datetime.now().year)

# Do last
import flask_app.views
