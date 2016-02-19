"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, g
from flask_app import app


@app.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Hjem',
        year=datetime.now().year,
    )


@app.route('/kontakt')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Kontakt',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page """
    if request.method == 'POST':
        processLogin()
    else:
        return render_template(
            'login.html',
            title='Logg inn',
            year=datetime.now().year
        )


@app.route('/database', methods=['GET'])
def database():
    """ Test page for database """
    cur = g.db.execute("select title, text from entries order by id desc")
    meetings = [dict(time=row[1]) for row in cur.fetchall]
    render_template('database.html', meetings)
