from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from flask.ext.app.schema import metadata
from flask_app import app

engine = create_engine(app.config['DATABASE'], echo=True, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from flask.ext.app import models
    metadata.drop_all(engine)  # Empties the database
    Base.metadata.create_all(bind=engine)  # Creates all tables from metadata definition
    admin = models.User('admin', 'adminpass1234', 'Administrator', 'admin@mail.com', False)
    db_session.add(admin)
    db_session.commit()
