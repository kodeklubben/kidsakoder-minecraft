"""
Configuration file

Change what configuration is used in __init__.py
"""

APP_NAME = 'Minecraft Madness'
DEBUG = False
# SESSION_COOKIE_SECURE = True # Should be set when using https
CSRF_ENABLED = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
WORLD_UPLOAD_PATH = 'world_storage'

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
