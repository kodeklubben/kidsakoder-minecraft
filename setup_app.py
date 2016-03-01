
import os
from flask_app.database import init_db

# Generate new secret key
key_file_path = 'flask_app/secret_key.py'
if not os.path.isfile(key_file_path):
    secret_key = os.urandom(24).encode('hex').strip()
    with open(key_file_path, 'w') as key_file:
        key_file.write('secret_key = """' + secret_key + '""".decode("hex")')

# Initialize database
init_db()
