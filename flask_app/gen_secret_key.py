# Generate new secret key

import os

key_file = open('secret_key.py', 'w')
secret_key = os.urandom(24).encode('base-64').strip()
key_file.write('secret_key = """' + secret_key + '"""')
key_file.close
