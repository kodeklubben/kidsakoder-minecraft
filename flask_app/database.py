# -*- coding: utf-8 -*-
""" The database controller """


db = None


def init(app):
    """ Initialize Flask-SQLAlchemy """
    from flask_sqlalchemy import SQLAlchemy
    global db
    db = SQLAlchemy(app)
    return db


def create_db():
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
