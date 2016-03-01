
from flask_security import UserMixin, RoleMixin
from flask_app import db, roles_users


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    
    #first_name = db.Column(db.String(100), nullable=False, server_default='')
    #last_name = db.Column(db.String(100), nullable=False, server_default='')
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from flask_app.database import Base

    def __repr__(self):
        return "<User(username='%s', fullname='%s', email='%s', pw_hash='%s', reset='%s')>" % (self.username,
                                                                                               self.fullname,
                                                                                               self.email,
                                                                                               self.pw_hash,
                                                                                               self.reset)
"""


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Meeting(Base):
    __tablename__ = 'meeting'

    id = Column('id', Integer, primary_key=True)
    creator_id = Column('creator_id', None, ForeignKey('user.id'))
    title = Column('title', String(50), nullable=False)
    time = Column('time', String(23))  # YYYY-MM-DD HH:MM:SS.SSS
    participants = Column('participants', Integer)
    world_id = Column('world_id', None, ForeignKey('world.id'))

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
    __tablename__ = 'world'

    id = Column('id', Integer, primary_key=True)
    reference = Column('reference', String(60))

    def __init__(self, reference):
        self.reference = reference
