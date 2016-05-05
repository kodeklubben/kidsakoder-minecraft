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

    name = db.Column(db.String(255), server_default='')
    mojang_playername = db.Column(db.String(255), server_default='')
    mojang_uuid = db.Column(db.String(64))
    
    @classmethod
    def get_all_as_dict(cls):
        """
        :return:  All users as list of dictionaries with all fields
        """
        user_list = cls.query.all()
        return [vars(user) for user in user_list]

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    def store(self):
        """ Store itself to database """
        db.session.add(self)
        db.session.commit()

    def is_admin(self):
        return self.admin


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
        db.session.delete(self)
        db.session.commit()


class World(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(512), server_default='')
    file_ref = db.Column(db.String(255), unique=True)
    preview = db.Column(db.Boolean)
    seed = db.Column(db.String(100))
    favourite = db.Column(db.Boolean)

    @classmethod
    def get_user_worlds(cls, user_id=None):
        if user_id is None:
            return None
        return cls.query.filter_by(user_id=user_id).all()

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

    @classmethod
    def exists(cls, world_id):
        return cls.query.get(world_id) is not None

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
        meeting_count = Meeting.query.filter_by(_world_id=self.id).count()
        if meeting_count > 0:
            # Do not delete if in use
            return False

        if self.file_ref:
            import files
            files.delete_world_file(self.file_ref)
            files.delete_world_preview(self.file_ref)

        db.session.delete(self)
        db.session.commit()
        return True
