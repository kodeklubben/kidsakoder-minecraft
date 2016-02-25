# Generate new secret key

import os

secret_key = os.urandom(24).encode('hex').strip()
with open('secret_key.py', 'w') as key_file:
    key_file.write('secret_key = """' + secret_key + '""".decode("hex")')
