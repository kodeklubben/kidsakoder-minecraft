# -*- coding: utf-8 -*-
"""
Configuration file

Change what configuration is used in __init__.py
"""

from flask_app import app


APP_NAME = 'Kodeklubben Minecraft'
DEBUG = False
# SESSION_COOKIE_SECURE = True # Should be set when using https
CSRF_ENABLED = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
WORLD_UPLOAD_PATH = 'world_storage'
PREVIEW_STORAGE_PATH = 'static/preview_storage'
TEXTUREPACK_PATH = 'static/texturepack'

# Flask Security
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_REMEMBER_SALT = app.config['SECRET_KEY']
SECURITY_DEFAULT_REMEMBER_ME = False

SECURITY_MSG_DISABLED_ACCOUNT = (u'Denne kontoen er deaktivert', 'error')
SECURITY_MSG_EMAIL_NOT_PROVIDED = (u'E-post adresse mangler', 'error')
SECURITY_MSG_USER_DOES_NOT_EXIST = (u'Feil brukernavn og / eller passord', 'error')
SECURITY_MSG_INVALID_PASSWORD = SECURITY_MSG_USER_DOES_NOT_EXIST
SECURITY_MSG_LOGIN = (u'Venligst logg inn for å få tilgang til denne siden', 'info')
SECURITY_MSG_PASSWORD_NOT_PROVIDED = (u'Passord mangler', 'error')
SECURITY_MSG_UNAUTHORIZED = (u'Du har ikke tilgang til å se denne ressursen', 'error')

# Celery
CELERY_BROKER_URL = 'amqp://guest@master//'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_TRACK_STARTED = True
CELERY_TASK_SERIALIZER = 'json'
