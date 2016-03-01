"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

# See configuration.py for possible configuration objects
app.config.from_object('flask_app.configuration.Development')


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from flask_security import Security, SQLAlchemyUserDatastore
roles_users = db.Table(
        'roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
        )
from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def datadatadata():
    db.create_all()
    #user_datastore.create_user(email='jall@jall.com', password='password123')
    #db.session.commit()

# Do last
import flask_app.views
