"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, g, redirect, url_for, flash
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


@app.route('/database', methods=['GET', 'POST'])
def database():
    """ Test page for database """

    cur = g.db.execute("select title, time from meetings order by id desc")
    meetings = [dict(title=row[0], time=row[1]) for row in cur.fetchall()]
    return render_template('database.html', meetings=meetings)


@app.route('/add_meeting', methods=['POST'])
def add_meeting():
    g.db.execute("insert into meetings (title, time, map_id) VALUES (?, ?, ?)",
                 [request.form['title'], request.form['time'], request.form['map_id']])
    g.db.commit()
    flash('Nytt møte lagt til!')
    return redirect(url_for('database'))
