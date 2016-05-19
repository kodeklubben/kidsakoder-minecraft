"""
This script runs the flask_app application using a development server.
"""

import __builtin__
# Set development mode before importing flask_app
__builtin__.flask_app_development_mode = True

from flask_app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
