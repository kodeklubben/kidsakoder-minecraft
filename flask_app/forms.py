"""
Flask-WTF form controller
"""

from flask_wtf import Form
from wtforms import StringField, DateTimeField, IntegerField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length


class MeetingForm(Form):
    title = StringField('Navn', [Length(min=4, max=25)])
    start_time = DateTimeField('Starttidspunkt')
    end_time = DateTimeField('Sluttidspunkt')
    participant_count = IntegerField('Antall deltakere')
    world_id = HiddenField('Verden ID')
    world_ref = StringField('Minecraft verden')


class WorldForm(Form):
    world_id = HiddenField('Verden ID')
    description = TextAreaField('Beskrivelse')
