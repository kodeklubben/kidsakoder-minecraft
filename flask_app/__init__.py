"""
The flask application package.
"""

from flask import Flask
#from flask.ext import login

app = Flask(__name__)

# Flask-Login initialization
"""
login_manager = login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return models.User.get(user_id)
"""

# See configuration.py for possible configuration objects
app.config.from_object('flask_app.configuration.Development')

from flask_sqlalchemy import SQLAlchemy
from flask_user import SQLAlchemyAdapter, UserManager
db = SQLAlchemy(app)
from models import User
db.create_all()
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)

# Do last
import flask_app.views
