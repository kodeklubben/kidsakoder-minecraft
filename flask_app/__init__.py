"""
The flask application package.
"""

from flask import Flask
#from flask.ext import login

app = Flask(__name__)

# See configuration.py for possible configuration objects
app.config.from_object('flask_app.configuration.Development')

# Flask-Login initialization
"""
login_manager = login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return models.User.get(user_id)
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from flask_security import Security, SQLAlchemyUserDatastore
from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('user.id'))
                      )
db.create_all()

"""
from flask_user import SQLAlchemyAdapter, UserManager
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)
"""

# Do last
import flask_app.views
