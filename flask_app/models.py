from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from flask_app.database import Base
from werkzeug.security import generate_password_hash, \
    check_password_hash


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String(50))
    fullname = Column('fullname', String(50))
    email = Column('email', String(50))
    pw_hash = Column('pw_hash', String(250))
    reset = Column('reset', Boolean)

    def __repr__(self):
        return "<User(username='%s', fullname='%s', email='%s', pw_hash='%s', reset='%s')>" % (self.username,
                                                                                               self.fullname,
                                                                                               self.email,
                                                                                               self.pw_hash,
                                                                                               self.reset)

    def __init__(self, username, password, fullname, email, reset):
        self.username = username
        self.fullname = fullname
        self.set_password(password)
        self.email = email
        self.reset = reset

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password, method='pbkdf2:sha512:100000', salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


# Hot to test:
# me = User('yourusername', 'password12345678987654321')
# me.pw_hash
# me.check_password('password12345678987654321')
# me.check_password('password1234567890987654321')

class Meeting(Base):
    __tablename__ = 'meetings'

    id = Column('id', Integer, primary_key=True)
    creator_id = Column('creator_id', None, ForeignKey('users.id'))
    title = Column('title', String(50), nullable=False)
    time = Column('time', String(23))  # YYYY-MM-DD HH:MM:SS.SSS
    participants = Column('participants', Integer)
    world_id = Column('world_id', None, ForeignKey('worlds.id'))

    def __repr__(self):
        return "<Meeting(creator_id='%s', title='%s'," \
               " time='%s', participants='%s', world_id='%s')>" % (self.creator_id,
                                                                   self.title,
                                                                   self.time,
                                                                   self.participants,
                                                                   self.world_id)

    def __init__(self, creator_id, title, time, participants, world_id):
        self.creator_id = creator_id
        self.title = title
        self.time = time
        self.participants = participants
        self.world_id = world_id


class World(Base):
    __tablename__ = 'worlds'

    id = Column('id', Integer, primary_key=True)
    reference = Column('reference', String(60))

    def __init__(self, reference):
        self.reference = reference
