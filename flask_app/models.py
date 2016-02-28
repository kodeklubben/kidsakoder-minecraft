from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import UserMixin, RoleMixin
from flask_app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.Relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    
    #username = db.Column(db.String(50), nullable=False, unique=True)
    #reset_password_token = db.Column(db.String(100), nullable=False)
    #first_name = db.Column(db.String(100), nullable=False, server_default='')
    #last_name = db.Column(db.String(100), nullable=False, server_default='')
"""
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
    
    @classmethod
    def get(cls, username):
        # Get user details from db
        # Return None if invalid user
        if username == 'admin':
            password = 'laOssKodeIminecraft'
            return cls(username, password)
        
        return None

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password, method='pbkdf2:sha512:100000', salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
    
    # Flask-Login methods:
    def is_authenticated():
        return True
    def is_active():
        return True
    def is_anonymous():
        return False
    def get_id():
        # Must return Unicode string
        return self.username
"""

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

#Hot to test:        
# me = User('yourusername', 'password12345678987654321')
# me.pw_hash
# me.check_password('password12345678987654321')
# me.check_password('password1234567890987654321')