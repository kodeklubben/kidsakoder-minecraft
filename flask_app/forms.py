"""
Flask-WTF form controller
"""

from flask_wtf import Form
from wtforms import StringField, DateTimeField
from wtforms.validators import DataRequired, Length


class MeetingForm(Form):
    title = StringField('Navn', [Length(min=4, max=25)])
    start_time = DateTimeField('Starttidspunkt')
    end_time = DateTimeField('Sluttidspunkt')
    participant_count = StringField('Antall deltakere')
    world_ref = StringField('Minecraft verden')
