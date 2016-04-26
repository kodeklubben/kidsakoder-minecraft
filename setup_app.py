""" Script to set up application """


# Generate new secret key
input_answer = raw_input('Generate new secret key? (y, n)\n')
if input_answer.strip() == 'y':
    import os
    key_file_path = 'flask_app/config/secret_key.py'
    secret_key = os.urandom(24).encode('hex').strip()
    with open(key_file_path, 'w') as key_file:
        key_file.write('""" Auto generated secret key file """\n\n' +
                       'SECRET_KEY = "' + secret_key + '".decode("hex")\n')


# Initialize database
input_answer = raw_input('Initialize database? (y, n)\n')
if input_answer.strip() == 'y':
    from flask_app.database import init_db
    init_db()
