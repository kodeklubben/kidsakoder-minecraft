
import os
from flask_app.database import init_db

# Generate new secret key
secret_key = os.urandom(24).encode('hex').strip()
with open('flask_app/secret_key.py', 'w') as key_file:
    key_file.write('secret_key = """' + secret_key + '""".decode("hex")')

# Initialize database
init_db()
