"""
Configuration file

Change what configuration is used in __init__.py
"""

from secret_key import secret_key
import urllib


class Production(object):
    APP_NAME = 'Minecraft Madness'
    DEBUG = False
    SECRET_KEY = secret_key
    # SESSION_COOKIE_SECURE = True # Should be set when using https
    CSRF_ENABLED = True

    # SQLALCHEMY_DATABASE_URI = 'path/to/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'mssql://kodeadmin:7eddsmiSQLadmin@kode-kidza.database.windows.net:1433/kode-kidza'
    db_params = urllib.quote_plus('Driver={SQL Server Native Client 11.0};Server=tcp:kode-kidza.database.windows.net,1433;Database=kode-kidza;Uid=kodeadmin@kode-kidza;Pwd=7eddsmiSQLadmin;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect=' + db_params

    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'salt'


class Development(Production):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    WORLD_UPLOAD_PATH = 'world_storage'

#class VM_dev(Development):
    #SERVER_NAME = '0.0.0.0'
