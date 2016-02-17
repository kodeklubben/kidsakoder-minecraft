"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
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
			title = 'Logg inn',
			year=datetime.now().year
			)
	






