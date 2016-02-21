"""
Configuration file

Change configuration in __init__.py
"""

from secret_key import secret_key

class Production(object):
    APP_NAME = 'Minecraft Madness'
    DEBUG = False
    SECRET_KEY = secret_key

class Development(Production):
    DEBUG = True
    #SERVER_NAME

class VM_dev(Development):
    #SERVER_NAME