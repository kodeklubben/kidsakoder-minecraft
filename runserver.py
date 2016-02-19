"""
This script runs the flask_app application using a development server.
"""
import sqlite3
from contextlib import closing

from flask import g

from flask_app import app

app.config.from_envvar('APP_SETTINGS', silent=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('flask_app/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
