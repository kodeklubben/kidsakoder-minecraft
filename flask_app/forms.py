"""
Flask-WTF form controller
"""

from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import StringField, DateTimeField, IntegerField, TextAreaField, HiddenField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class MeetingForm(Form):
    title = StringField('Navn', [Length(min=4, max=50)])
    start_time = DateTimeField('Starttidspunkt', [InputRequired()], format='%d.%m.%Y %H:%M')
    end_time = DateTimeField('Sluttidspunkt', [InputRequired()], format='%d.%m.%Y %H:%M')
    participant_count = IntegerField('Antall deltakere', [InputRequired()])
    # TODO set ID as required
    world_id = HiddenField('Verden ID')


class WorldForm(Form):
    is_world_form = HiddenField('Er verden', [InputRequired()], default='True')
    world_id = HiddenField('Verden ID', [InputRequired()])
    description = TextAreaField('Beskrivelse')


class ChangeEmail(Form):
    new_email = EmailField('Ny e-post adresse', [Email()])
    confirm_email = EmailField('Bekreft e-post adresse',
                               [Email(), EqualTo('new_email', 'E-post adressene er ikke like')])
    password = PasswordField('Skriv inn passordet ditt for å bekrefte endringen', [InputRequired()])


class ChangeName(Form):
    new_name = StringField('Nytt navn / beskrivelse for denne brukeren', [InputRequired()])


class ChangePassword(Form):
    # TODO password length requirements?
    old_password = PasswordField('Gammelt passord', [InputRequired()])
    new_password = PasswordField('Nytt passord', [InputRequired()])
    confirm_password = PasswordField('Bekreft passordet', [InputRequired()])


class ChangePlayername(Form):
    playername = StringField('Ditt minecraft spillernavn', [InputRequired()])
    uuid = StringField('Mojang UUID', [InputRequired()])
