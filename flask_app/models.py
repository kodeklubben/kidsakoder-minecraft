from werkzeug.security import generate_password_hash, check_password_hash

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
    
    def get(cls, username):
        # Get user details from db
        # Return None if invalid user
        password = 'jalla'
        return cls(username, password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password, method='pbkdf2:sha512:100000', salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
    
    # Flask-Login methods:
    def is_authenticated():
        return True
    def is_active():
        return True
    def is_anonymous():
        return False
    def get_id():
        # Must return Unicode string
        return self.username

#Hot to test:        
# me = User('yourusername', 'password12345678987654321')
# me.pw_hash
# me.check_password('password12345678987654321')
# me.check_password('password1234567890987654321')