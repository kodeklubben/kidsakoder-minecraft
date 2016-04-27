# -*- coding: utf-8 -*-
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
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    first_name = db.Column(db.String(100), server_default='')  # Do we need - or even want - to register our users with names?
    last_name = db.Column(db.String(100), server_default='')  # Removed from user registration for now
    
    def is_admin(self):
        return self.admin
        
    @classmethod
    def store(self):
        """ Store itself to database """
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_all_as_dict(cls):
        """
        :return:  All users as list of dictionaries with all fields
        """
        user_list = cls.query.all()
        return [vars(user) for user in user_list]


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # Required to display name of role in a way that is actually readable in admin panel
    def __str__(self):
        return self.name

    # (Apparently) required to avoid TypeError: Unhashable when saving users
    def __hash__(self):
        return hash(self.name)


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime)  # YYYY-MM-DD HH:MM:SS.SSS
    end_time = db.Column(db.DateTime)
    participant_count = db.Column(db.Integer)
    _world_id = db.Column('world_id', db.Integer, db.ForeignKey('world.id'))

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
        return [vars(meeting) for meeting in meeting_list.order_by(Meeting.start_time)]

    @classmethod
    def get_meeting_by_id(cls, meeting_id):
        meeting = cls.query.get(meeting_id)
        return meeting

    @property
    def world_id(self):
        return self._world_id

    @world_id.setter
    def world_id(self, value):
        try:
            int_val = int(value)
        except ValueError:
            int_val = None
        self._world_id = int_val

    def store(self):
        """ Store itself to database """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete itself from the database """
        if self.world_id:
            # Check if world is favoured and delete if not
            # TODO only if meeting user is also owner of world
            # TODO maybe check if world is used in other meetings?
            # meetings = Meeting.query.filter_by(self.world_id)
            world = World.get_by_id(self.world_id)
            if not world.favourite:
                world.delete()
        db.session.delete(self)
        db.session.commit()


class World(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(512), server_default='')
    file_ref = db.Column(db.String(255), unique=True)
    seed = db.Column(db.String(100))
    favourite = db.Column(db.Boolean)

    @classmethod
    def get_all_as_dict(cls):
        """
        :return:  All worlds as list of dictionaries with all fields
        """
        world_list = cls.query.all()
        return [vars(world) for world in world_list]

    @classmethod
    def get_by_id(cls, world_id):
        return cls.query.get(world_id)

    @property
    def id(self):
        if not self._id:
            # If new world, _id must be auto-incremented in db
            db.session.add(self)
            db.session.flush()
        return self._id

    def store(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        if self.file_ref:
            # TODO delete file in file_ref
            pass
        db.session.delete(self)
        db.session.commit()
