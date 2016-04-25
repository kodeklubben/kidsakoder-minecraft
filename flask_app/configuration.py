"""
Configuration file

Change what configuration is used in __init__.py
"""

from secret_key import secret_key

class Production(object):
    APP_NAME = 'Minecraft Madness'
    DEBUG = False
    SECRET_KEY = secret_key
    #SESSION_COOKIE_SECURE = True # Should be set when using https
    CSRF_ENABLED = True

    #SQLALCHEMY_DATABASE_URI = 'path/to/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'salt'


class Development(Production):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    WORLD_UPLOAD_PATH = 'world_storage'
    PREVIEW_STORAGE_PATH = 'preview_storage'

#class VM_dev(Development):
    #SERVER_NAME = '0.0.0.0'
