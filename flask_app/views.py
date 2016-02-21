"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, session, escape, redirect, url_for
from flask_app import app
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        session['redirect_page'] = request.url
        return redirect(url_for('login'))
    
    return decorated_function

@app.route('/')
@login_required
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title = 'Hjem',
        year = datetime.now().year,
        app_name = app.config['APP_NAME']
    )

@app.route('/kontakt')
@login_required
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title = 'Kontakt',
        year = datetime.now().year,
        message = 'Your contact page.',
        app_name = app.config['APP_NAME']
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page """
    if 'username' in session:
        # If user is already logged in, redirect to home
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        #processLogin()
        session['username'] = request.form.get('username', None)
        
        return redirect( session.pop('redirect_page', url_for('home')) )
    return render_template(
        'login.html',
        title = 'Logg inn',
        year = datetime.now().year,
        app_name = app.config['APP_NAME']
    )

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
