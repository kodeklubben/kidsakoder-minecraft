"""
Flask-WTF form controller
"""

from flask_wtf import Form
from wtforms import StringField, DateTimeField, IntegerField, TextAreaField, HiddenField
from wtforms.validators import InputRequired, Length


class MeetingForm(Form):
    title = StringField('Navn', [Length(min=4, max=25)])
    start_time = DateTimeField('Starttidspunkt', [InputRequired()], format='%d.%m.%Y %H:%M')
    end_time = DateTimeField('Sluttidspunkt', [InputRequired()], format='%d.%m.%Y %H:%M')
    participant_count = IntegerField('Antall deltakere', [InputRequired()])
    # TODO set ID as required
    world_id = HiddenField('Verden ID')


class WorldForm(Form):
    is_world_form = HiddenField('Er verden', [InputRequired()], default='True')
    world_id = HiddenField('Verden ID', [InputRequired()])
    description = TextAreaField('Beskrivelse')
