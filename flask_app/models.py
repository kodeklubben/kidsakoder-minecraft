# -*- coding: utf-8 -*-
"""
flask_app.models
~~~~~~~~~~~~~~~~

Database models
"""

from flask_security import UserMixin, RoleMixin
from database import db
from flask_app import app
import pytz


# Table definition for many-many relation between role and user
roles_users = db.Table(
        'roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
        )


class User(db.Model, UserMixin):
    """ User model """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    # active and confirmed_at fields are required by Flask-Security
    active = db.Column(db.Boolean, nullable=False)
    confirmed_at = db.Column(db.DateTime)
    # A name or short description of the account
    name = db.Column(db.String(255), server_default='')
    # Playername and uuid is for Minecraft server operator access
    mojang_playername = db.Column(db.String(255), server_default='')
    mojang_uuid = db.Column(db.String(64))

    @classmethod
    def get_by_id(cls, user_id=None):
        """
        Get a user by user ID from the database
        :param user_id: ID of the user to get
        :return: A user object
        """
        if user_id is None:
            return None
        return cls.query.get(user_id)

    def store(self):
        """ Store this user to database """
        db.session.add(self)
        db.session.commit()


class Role(db.Model, RoleMixin):
    """ User role model """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # Required to display name of role in a way that is actually readable in admin panel
    def __str__(self):
        return self.name


class Meeting(db.Model):
    """ Meeting model """
    id = db.Column(db.Integer, primary_key=True)
    # ID of the user that created the meeting
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(50), nullable=False)
    # Start and end time for meeting
    # This should govern the automatic startup and shutdown of Minecraft servers
    _start_time = db.Column('start_time', db.DateTime)  # YYYY-MM-DD HH:MM:SS.SSS
    _end_time = db.Column('end_time', db.DateTime)
    # The number of Minecraft server instances for meeting
    participant_count = db.Column(db.Integer)
    # The Minecraft world to use for meetings Minecraft servers
    _world_id = db.Column('world_id', db.Integer, db.ForeignKey('world.id'))

    @classmethod
    def get_user_meetings(cls, user_id=None):
        """
        Get a list of all meetings for a specified user
        :param user_id: The users ID
        :return: List of meetings
        """
        if user_id is None:
            return None
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_meeting_by_id(cls, meeting_id=None):
        """
        Get a meeting by its ID
        :param meeting_id: The meetings ID
        :return: A meeting object
        """
        if meeting_id is None:
            return None
        return cls.query.get(meeting_id)

    @property
    def world_id(self):
        """
        Get ID of the Minecraft world associated with this meeting
        :return: integer world ID
        """
        return self._world_id

    @world_id.setter
    def world_id(self, value):
        """
        Set Minecraft world to use for this meeting
        :param value: Minecraft world ID
        """
        try:
            int_val = int(value)
        except ValueError:
            # If value is not an int, set to None so that we can check later
            int_val = None
        self._world_id = int_val

    @staticmethod
    def _is_naive_datetime(value):
        return value.tzinfo is None or value.tzinfo.utcoffset(value) is None

    @staticmethod
    def _datetime_to_utc(value):
        """
        Convert naive datetime to application set timezone
        Then store as UTC in model / database

        :param value: datetime object
        :return: UTC datetime object
        """
        if Meeting._is_naive_datetime(value):
            # Is naive. Assume app config timezone
            tz = pytz.timezone(app.config['TIMEZONE'])
            value = tz.localize(value, is_dst=None)

        return value.astimezone(pytz.utc)

    @staticmethod
    def _datetime_to_local(value):
        """
        Read out UTC datetime as application set timezone
        :param value: datetime object
        :return: Local datetime object
        """
        if Meeting._is_naive_datetime(value):
            tz = pytz.utc
            value = tz.localize(value, is_dst=None)

        return value.astimezone(pytz.timezone(app.config['TIMEZONE']))

    @property
    def start_time(self):
        """
        Meeting start time
        :return: datetime object
        """
        return Meeting._datetime_to_local(self._start_time)

    @start_time.setter
    def start_time(self, value):
        """
        Set meeting start time
        :param value: datetime object
        """
        self._start_time = Meeting._datetime_to_utc(value)

    @property
    def end_time(self):
        """
        Meeting end time
        :return: datetime object
        """
        return Meeting._datetime_to_local(self._end_time)

    @end_time.setter
    def end_time(self, value):
        """
        Set meeting end time
        :param value: datetime object
        """
        self._end_time = Meeting._datetime_to_utc(value)

    def store(self):
        """ Store this meeting to the database """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete this meeting from the database """
        db.session.delete(self)
        db.session.commit()


class World(db.Model):
    """ Minecraft world model """
    _id = db.Column('id', db.Integer, primary_key=True)
    # ID of the user that created the Minecraft world
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # A name or short description of the Minecraft world
    description = db.Column(db.String(512), server_default='')
    # The filename of the zipped Minecraft world
    file_ref = db.Column(db.String(255), unique=True)
    # Whether a preview for this world should have been generated already
    # If True; a preview may or may not actually exist
    preview = db.Column(db.Boolean)
    # Intended for a random or specified seed for procedural world generation
    # if this feature is implemented in the future
    seed = db.Column(db.String(100))
    # Favourite worlds will not be deleted automatically if an associated meeting is deleted
    favourite = db.Column(db.Boolean)

    @classmethod
    def get_user_worlds(cls, user_id=None):
        """
        Get a list of Minecraft worlds for a specified user
        :param user_id: The users ID
        :return: List of Minecraft worlds
        """
        if user_id is None:
            return None
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_id(cls, world_id):
        """
        Get a Minecraft world by its ID
        :param world_id: The worlds ID
        :return: A world object
        """
        return cls.query.get(world_id)

    @classmethod
    def exists(cls, world_id):
        """
        Check if a Minecraft world exists in the database
        :param world_id: The ID of the Minecraft world
        :return: True if exists, False if not
        """
        return cls.query.get(world_id) is not None

    @property
    def id(self):
        """
        Get this worlds ID.
        Fetches new ID from database if it does not exist
        :return: Autoincremented ID
        """
        if not self._id:
            # If new world, _id must be auto-incremented in db
            db.session.add(self)
            db.session.flush()
        return self._id

    def store(self):
        """ Save this Minecraft world to the database """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete this Minecraft world from the database
        Checks if the world is in use by a meeting, so meetings must be deleted first.
        Also tries to delete files related to this world
        :return: True if deleted, False if not
        """
        meeting_count = Meeting.query.filter_by(_world_id=self.id).count()
        if meeting_count > 0:
            # Do not delete if in use by a meeting
            return False

        if self.file_ref:
            # Delete related world file and preview
            import files
            files.delete_world_file(self.file_ref)
            files.delete_world_preview(self.file_ref)

        db.session.delete(self)
        db.session.commit()
        return True
