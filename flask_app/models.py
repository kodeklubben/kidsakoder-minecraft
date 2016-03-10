"""
Database models
"""
from flask_security import UserMixin, RoleMixin
from database import db, roles_users


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    first_name = db.Column(db.String(100), server_default='')
    last_name = db.Column(db.String(100), server_default='')


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime)  # YYYY-MM-DD HH:MM:SS.SSS
    end_time = db.Column(db.DateTime)
    participant_count = db.Column(db.Integer)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'))

    @classmethod
    def get_all_as_dict(cls):
        """
        :return:  All meetings as list of dictionaries with all fields
        """
        meeting_list = cls.query.all()
        return [vars(meeting) for meeting in meeting_list]

    @classmethod
    def get_user_meetings_as_dict(cls, user_id=None):
        if user_id is None:
            return None
        meeting_list = cls.query.filter_by(user_id=user_id)
        return [vars(meeting) for meeting in meeting_list]

    def store(self):
        """ Store itself to database """
        db.session.add(self)
        db.session.commit()

# Is this needed?
"""
    def __repr__(self):
        return "<Meeting(user_id='%s', title='%s'," \
               " time='%s', participants='%s', world_id='%s')>" % (self.user_id,
                                                                   self.title,
                                                                   self.time,
                                                                   self.participants,
                                                                   self.world_id)"""


class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_ref = db.Column(db.String(100), unique=True)
