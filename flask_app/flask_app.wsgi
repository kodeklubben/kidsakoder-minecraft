"""
WSGI entrypoint for Flask application
"""
import sys
sys.path.insert(0, '/opt/kidsakoder-minecraft')
from flask_app import app as application, init_flask_app
init_flask_app()
