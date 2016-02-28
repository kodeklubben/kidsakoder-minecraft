"""
Configuration file

Change what configuration is used in __init__.py
"""

from secret_key import secret_key

class Production(object):
    APP_NAME = 'Minecraft Madness'
    DEBUG = False
    SECRET_KEY = secret_key
    #DATABASE = 'path/to/database.db'
    #SESSION_COOKIE_SECURE = True # Should be set when using https
    CSRF_ENABLED = True
    
"""
    # Flask-User Features
    USER_ENABLE_CHANGE_PASSWORD    = True      # Allow users to change their password
    USER_ENABLE_CHANGE_USERNAME    = False      # Allow users to change their username
                                               # Requires USER_ENABLE_USERNAME=True
    USER_ENABLE_CONFIRM_EMAIL      = False      # Force users to confirm their email
                                               # Requires USER_ENABLE_EMAIL=True
    USER_ENABLE_FORGOT_PASSWORD    = True      # Allow users to reset their passwords
                                               # Requires USER_ENABLE_EMAIL=True
    USER_ENABLE_LOGIN_WITHOUT_CONFIRM = True  # Allow users to login without a
                                               # confirmed email address
                                               # Protect views using @confirm_email_required
    USER_ENABLE_EMAIL              = True      # Register with Email
                                               # Requires USER_ENABLE_REGISTRATION=True
    USER_ENABLE_MULTIPLE_EMAILS    = False     # Users may register multiple emails
                                               # Requires USER_ENABLE_EMAIL=True
    USER_ENABLE_REGISTRATION       = True      # Allow new users to register
    USER_ENABLE_RETYPE_PASSWORD    = True      # Prompt for `retype password` in:
                                               #   - registration form,
                                               #   - change password form, and
                                               #   - reset password forms.
    USER_ENABLE_USERNAME           = False      # Register and Login with username
    
    # Flask-User Settings
    USER_APP_NAME                    = APP_NAME   # Used by email templates
    USER_AUTO_LOGIN                  = False
    USER_AUTO_LOGIN_AFTER_CONFIRM    = USER_AUTO_LOGIN
    USER_AUTO_LOGIN_AFTER_REGISTER   = USER_AUTO_LOGIN
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = USER_AUTO_LOGIN
    USER_AUTO_LOGIN_AT_LOGIN         = USER_AUTO_LOGIN
    USER_CONFIRM_EMAIL_EXPIRATION    = 2*24*3600   # Confirmation expiration in seconds
                                                   # (2*24*3600 represents 2 days)
    USER_INVITE_EXPIRATION           = 90*24*3600  # Invitation expiration in seconds
                                                   # (90*24*3600 represents 90 days)
                                                   # v0.6.2 and up
    USER_PASSWORD_HASH               = 'bcrypt'    # Any passlib crypt algorithm
    USER_PASSWORD_HASH_MODE          = 'passlib'   # Set to 'Flask-Security' for
                                                   # Flask-Security compatible hashing
    SECURITY_PASSWORD_SALT           =None              # Only needed for
                                                   # Flask-Security compatible hashing
    USER_REQUIRE_INVITATION          = False       # Registration requires invitation
                                                   # Not yet implemented
                                                   # Requires USER_ENABLE_EMAIL=True
    USER_RESET_PASSWORD_EXPIRATION   = 2*24*3600   # Reset password expiration in seconds
                                                   # (2*24*3600 represents 2 days)
    USER_SEND_PASSWORD_CHANGED_EMAIL = False        # Send registered email
                                                   # Requires USER_ENABLE_EMAIL=True
    USER_SEND_REGISTERED_EMAIL       = False        # Send registered email
                                                   # Requires USER_ENABLE_EMAIL=True
    USER_SEND_USERNAME_CHANGED_EMAIL = False        # Send registered email
                                                   # Requires USER_ENABLE_EMAIL=True
    USER_SHOW_USERNAME_EMAIL_DOES_NOT_EXIST = USER_ENABLE_REGISTRATION
                                                   # Show 'Username/Email does not exist' error message
                                                   # instead of 'Incorrect Username/Email and/or password'
"""

class Development(Production):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

#class VM_dev(Development):
    #SERVER_NAME = '0.0.0.0'
