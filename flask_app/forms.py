"""
Flask-WTF form controller
"""

from flask_wtf import Form
from wtforms import StringField, IntegerField, HiddenField, DateTimeField
from wtforms.validators import DataRequired, Length


class MeetingForm(Form):
    title = StringField('Navn', [Length(min=4, max=25)])
    start_time = DateTimeField('Starttidspunkt', format='%d.%m.%Y %H:%M')
    end_time = DateTimeField('Sluttidspunkt', format='%d.%m.%Y %H:%M')
    participant_count = IntegerField('Antall deltakere')
    world_ref = HiddenField('Minecraft verden')
