from sqlalchemy import create_engine
from sqlalchemy.dialects import sqlite

from flask.ext.app.alchemy_schema import metadata


def init_db():
    engine = create_engine('sqlite:\\\\\\:memory:', echo=True)
    metadata.create_all(engine)
