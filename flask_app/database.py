# -*- coding: utf-8 -*-
""" The database controller """

from flask_app import app
from flask_sqlalchemy import SQLAlchemy


# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Many-many relation between role and user
roles_users = db.Table(
        'roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
        )


def init_db():
    """ Initialize new database """
    from flask_app import user_datastore
    db.drop_all()  # Empty database
    db.create_all()  # Creates all tables from models
    user_datastore.create_role(name='instructor',
                               description='Code club instructor'
                               )
    user_datastore.create_role(name='admin',
                               description='Site administrator'
                               )
    user_datastore.create_user(email='admin@mail.com', password='adminpass123')
    user_datastore.add_role_to_user('admin@mail.com', 'admin')
    db.session.commit()
