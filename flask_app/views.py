"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, session, escape, redirect, url_for
from flask_app import app
import var_file

app.secret_key = var_file.secret_key

@app.route('/')
def home():
    """Renders the home page."""
    if 'username' in session:
        return 'jalla ' + escape(session['username'])
    else:
        return redirect(url_for('login'))
    
    return render_template(
        'index.html',
        title='Hjem',
        year=datetime.now().year,
        app_name = var_file.app_name
    )

@app.route('/kontakt')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Kontakt',
        year=datetime.now().year,
        message='Your contact page.',
        app_name = var_file.app_name
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page """
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        return redirect(url_for('home'))
        #processLogin()
    else:
        
        return render_template(
            'login.html',
            title = 'Logg inn',
            year=datetime.now().year,
            app_name = var_file.app_name
        )








