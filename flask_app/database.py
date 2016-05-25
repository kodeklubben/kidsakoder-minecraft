# -*- coding: utf-8 -*-
"""
flask_app.database
~~~~~~~~~~~~~~~~~~

The database controller
"""


db = None


def init(app):
    """
    Initialize Flask-SQLAlchemy
    :param app: The Flask application to create database for
    :return: SQLAlchemy database reference
    """
    from flask_sqlalchemy import SQLAlchemy
    global db  # Keep local reference to db
    db = SQLAlchemy(app)
    # Import models so that they are defined in db context
    return db


def create_db():
    """ Initialize new database """
    from flask_app import user_datastore
    db.drop_all()  # Empty database
    db.create_all()  # Creates all tables from models
    # Create roles to separate between administrators and regular users
    user_datastore.create_role(name='instructor',
                               description='Code club instructor'
                               )
    user_datastore.create_role(name='admin',
                               description='Site administrator'
                               )
    # Create a default admin user to start off with
    # This should only be used to create a new admin user in production and then deleted
    user_datastore.create_user(email='admin@mail.com', password='adminpass123')
    user_datastore.add_role_to_user('admin@mail.com', 'admin')
    db.session.commit()  # Commit changes to database
