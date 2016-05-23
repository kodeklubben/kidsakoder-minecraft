# -*- coding: utf-8 -*-
"""
flask_app
~~~~~~~~~

The flask application package initialization
"""

from flask import Flask
import logging
import os


# Create Flask app context
app = Flask(__name__)

# pre_logger logs messages before file logging is initialized.
# Contains tuples of log level integer and message
pre_logger = [(logging.WARNING, '### Starting app ###')]


# Externally visible objects
############################
user_datastore = None


def config_loader():
    """ Load configuration files """
    try:  # Load secret key
        app.config.from_pyfile('config/secret_key.py')  # Load first in case we want to use in other config opt
    except IOError:
        app.config['SECRET_KEY'] = 'secret_key'  # Default setting in case file does not exist yet
        pre_logger.append((logging.WARNING, 'secret_key not found. Setting secret_key as default secret_key'))

    # Load main configuration
    app.config.from_pyfile('config/configuration.py')

    try:  # Load settings that should be kept secret
        app.config.from_pyfile('config/secret_config.py')
    except IOError:
        pre_logger.append((logging.WARNING, 'Secret config file not found. Skipping'))

    try:  # Load development configuration overrides
        app.config.from_pyfile('config/development.py')
        pre_logger.append((logging.WARNING, 'Loading development config'))
    except IOError:
        pre_logger.append((logging.DEBUG, 'Development config not found'))


def main():
    """ Main app init function """

    # Initialize file logging
    #########################
    if not app.testing:
        import logging.handlers
        file_handler = logging.handlers.RotatingFileHandler(app.config['APP_LOG_FILE'], maxBytes=8192, backupCount=5)
        if app.debug:  # Log everything in debug mode
            file_handler.setLevel(logging.DEBUG)
        else:
            file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)-8s: %(message)s',
                                                    datefmt='%Y-%m-%d %H:%M'))
        app.logger.addHandler(file_handler)

        # Log pre_logger
        for log in pre_logger:
            app.logger.log(log[0], log[1])

    # Set locale for datetime format
    ################################
    import locale

    def try_locale(locale_list):
        """ Recursively try locales from a list """
        if not locale_list:
            app.logger.warning('Locale not found')
            return
        head, tail = locale_list[0], locale_list[1:]
        try:
            locale.setlocale(locale.LC_TIME, head)
            app.logger.info('Locale set to ' + head)
        except locale.Error:
            try_locale(tail)

    our_locales = ('nb_NO.utf8', 'nb_NO', 'no_NO', 'norwegian-bokmal')
    try_locale(our_locales)
    app.logger.debug('Preferred locale encoding: ' + locale.getpreferredencoding())

    # Initialize database
    #####################
    import database
    db = database.init(app)
    import models

    # Initialize Flask-Security
    ###########################
    from flask_security import Security, SQLAlchemyUserDatastore
    global user_datastore
    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    security = Security(app, user_datastore)

    # Initialize Flask-Admin
    ########################
    from admin import init_admin
    init_admin(app)

    # Context processors
    ####################
    @app.context_processor
    def inject_year():
        """ Make year available in templates """
        from datetime import datetime
        return dict(year=datetime.now().year)

    # Do last
    #########
    import flask_app.views

config_loader()
# If files don't exist, assume setup_app.py has not been run
config_path = os.path.join(app.root_path, 'config')
if (os.path.isfile(os.path.join(config_path, 'secret_key.py')) and
        os.path.isfile(os.path.join(config_path, 'secret_config.py'))):
    main()
else:
    print '#########################################'
    print '# Did you forget to run setup_app.py??? #'
    print '#########################################'
