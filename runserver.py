"""
This script runs the flask_app application using a development server.
"""

from flask_app import app

if __name__ == '__main__':
    from flask_app import init_flask_app
    # Fully initialize app before running dev server
    init_flask_app()
    app.run(host='0.0.0.0', port=5000)
