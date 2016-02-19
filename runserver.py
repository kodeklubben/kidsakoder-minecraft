"""
This script runs the flask_app application using a development server.
"""
import sqlite3
from contextlib import closing

from flask import g

from flask_app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

