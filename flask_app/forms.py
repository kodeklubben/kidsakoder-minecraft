"""
Flask-WTF form controller
"""

from flask_wtf import Form
from wtforms import StringField, DateTimeField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length

class RegisterForm(Form):
    email = StringField('E-post: ')
    password = PasswordField('Passord: ')
    roles = SelectField(u'Rolle: ', choices=[('instructor', 'Instructor'), ('admin', 'Admin')])
    

class MeetingForm(Form):
    title = StringField('Navn', [Length(min=4, max=25)])
    start_time = DateTimeField('Starttidspunkt')
    end_time = DateTimeField('Sluttidspunkt')
    participant_count = IntegerField('Antall deltakere')
    world_ref = StringField('Minecraft verden')
