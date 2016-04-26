
import os

# Generate new secret key
key_file_path = 'flask_app/secret_key.py'
if not os.path.isfile(key_file_path):
    secret_key = os.urandom(24).encode('hex').strip()
    with open(key_file_path, 'w') as key_file:
        key_file.write('""" Auto generated secret key file """\n\n' +
                       'secret_key = "' + secret_key + '".decode("hex")\n')

# Initialize database
from flask_app.database import init_db
init_db()
