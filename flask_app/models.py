
from flask_security import UserMixin, RoleMixin
from database import db, roles_users


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    #first_name = db.Column(db.String(100), server_default='')
    #last_name = db.Column(db.String(100), server_default='')
"""
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


class Meeting(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column('title', db.String(50), nullable=False)
    time = db.Column('time', db.String(23))  # YYYY-MM-DD HH:MM:SS.SSS
    participants = db.Column('participants', db.Integer)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'))

    def __repr__(self):
        return "<Meeting(user_id='%s', title='%s'," \
               " time='%s', participants='%s', world_id='%s')>" % (self.user_id,
                                                                   self.title,
                                                                   self.time,
                                                                   self.participants,
                                                                   self.world_id)

    def __init__(self, user_id, title, time, participants, world_id):
        self.user_id = user_id
        self.title = title
        self.time = time
        self.participants = participants
        self.world_id = world_id


class World(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    reference = db.Column('reference', db.String(60))

    def __init__(self, reference):
        self.reference = reference
