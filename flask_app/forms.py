"""
Flask-WTF form controller
"""

from flask_wtf import Form
from wtforms import StringField, IntegerField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


class MeetingForm(Form):
    title = StringField('Navn', [Length(min=4, max=25)])
    start_time = DateField('Starttidspunkt', format='%Y-%m-%d')
    end_time = DateField('Sluttidspunkt', format='%Y-%m-%d')
    participant_count = IntegerField('Antall deltakere')
    world_ref = HiddenField('Minecraft verden')
