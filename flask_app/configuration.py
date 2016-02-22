"""
Configuration file

Change what configuration is used in __init__.py
"""

from secret_key import secret_key

class Production(object):
    APP_NAME = 'Minecraft Madness'
    DEBUG = False
    SECRET_KEY = secret_key
    #DATABASE = 'path/to/database.db'
    #SESSION_COOKIE_SECURE = True # Should be set when using https

class Development(Production):
    DEBUG = True
    DATABASE = 'database.db'

#class VM_dev(Development):
    #SERVER_NAME = '0.0.0.0'
