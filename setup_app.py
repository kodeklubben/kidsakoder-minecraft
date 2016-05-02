""" Script to set up application """

# Parse arguments passed on command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-q", "--quiet", 
        help="Run quietly and force new secret key and db", 
        action="store_true")
args = parser.parse_args()


""" Generates a new secret key in config dir """
def generate_new_secret():
    import os
    key_file_path = 'flask_app/config/secret_key.py'
    secret_key = os.urandom(24).encode('hex').strip()
    with open(key_file_path, 'w') as key_file:
        key_file.write('""" Auto generated secret key file """\n\n' +
                       'SECRET_KEY = "' + secret_key + '".decode("hex")\n')


""" Initializes a new database """
def initialize_db():
    from flask_app.database import init_db
    init_db()


if args.quiet:
    generate_new_secret()
    initialize_db()
else:
    input_answer = raw_input('Generate new secret key? (y, n)\n')
    if input_answer.strip() == 'y':
        generate_new_secret()

    input_answer = raw_input('Initialize database? (y, n)\n')
    if input_answer.strip() == 'y':
        initialize_db()
