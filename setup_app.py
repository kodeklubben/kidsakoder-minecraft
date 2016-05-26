""" Script to set up application """

import argparse
import os

# Parse arguments passed on command line
parser = argparse.ArgumentParser()
parser.add_argument("-q", "--quiet",
                    help="Run quietly and force new secret key and db",
                    action="store_true")
parser.add_argument("--testing",
                    help='Set test mode to True',
                    action="store_true")
args = parser.parse_args()

config_path = 'flask_app/config/'


def generate_new_secret(force=False):
    """ Generates a new secret key in config dir """
    key_file_path = config_path + 'secret_key.py'
    if force or not os.path.isfile(key_file_path):
        secret_key = os.urandom(24).encode('hex').strip()
        with open(key_file_path, 'w') as key_file:
            key_file.write('""" Auto generated secret key file """\n\n' +
                           'SECRET_KEY = "' + secret_key + '".decode("hex")\n')


def copy_secret_config():
    """ Make a copy of secret_config.py.template if secret_config.py does not exist """
    if not os.path.isfile(config_path + 'secret_config.py'):
        with open(config_path + 'secret_config.py', 'w') as secret_config_file:
            with open(config_path + 'secret_config.py.template') as secret_config_file_template:
                secret_config_file.write(secret_config_file_template.read())


def initialize_db():
    """ Initializes a new database """
    from flask_app import init_security
    from flask_app.database import create_db
    # Initialize database context
    init_security()
    # Drop and create tables
    create_db()


if args.testing:
    with open(config_path + 'configuration.py', 'a') as test_config:
        test_config.write('\nTESTING = True\n')

copy_secret_config()
if args.quiet:
    generate_new_secret()
    initialize_db()
else:
    if os.path.isfile(config_path + 'secret_key.py'):
        # Ask for permission to overwrite
        input_answer = raw_input('Generate new secret key and overwrite existing? (y, n)\n')
        if input_answer.strip() == 'y':
            generate_new_secret(True)
    else:
        generate_new_secret()

    input_answer = raw_input('Initialize database (drops all tables)? (y, n)\n')
    if input_answer.strip() == 'y':
        initialize_db()
