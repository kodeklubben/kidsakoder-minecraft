"""
WSGI entrypoint for Flask application
"""
import sys
sys.path.insert(0, '/vagrant')
from flask_app import app as application
