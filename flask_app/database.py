from flask import g
from sqlalchemy import create_engine

from flask.ext.app import app
from flask.ext.app.schema import metadata

engine = create_engine(app.config['DATABASE_ALCHEMY'], echo=True)


def connect_db():
    return engine.connect()


def init_db():
    metadata.drop_all(engine)  # Empties the database
    metadata.create_all(engine)  # Creates all tables from metadata definition


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
