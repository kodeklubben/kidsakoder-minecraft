"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, session, escape, redirect, url_for
from flask_app import app
import var_file

app.secret_key = var_file.secret_key

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        return redirect(url_for('login', next_page=request.url))
    return decorated_function

@app.route('/')
@login_required
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title = 'Hjem',
        year = datetime.now().year,
        app_name = var_file.app_name
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
        app_name = var_file.app_name
    )

@app.route('/login', methods=['GET', 'POST'])
def login(next_page = url_for('home')):
    """ Login page """
    if 'username' in session:
        # If user is already logged in, redirect to home
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        #processLogin()
        session['username'] = request.form.get('username', None)
        return redirect(next_page)
    else:
        return render_template(
            'login.html',
            title = 'Logg inn',
            year = datetime.now().year,
            app_name = var_file.app_name
        )








