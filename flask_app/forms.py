# -*- coding: utf-8 -*-
"""
Flask-WTF form controller
"""

from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import StringField, DateTimeField, IntegerField, TextAreaField, HiddenField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class MeetingForm(Form):
    title = StringField(u'Tittel', [Length(min=4, max=50)])
    start_time = DateTimeField(u'Starttidspunkt', [InputRequired()], format='%d.%m.%Y %H:%M')
    end_time = DateTimeField(u'Sluttidspunkt', [InputRequired()], format='%d.%m.%Y %H:%M')
    participant_count = IntegerField(u'Antall deltakere', [InputRequired()])
    world_id = HiddenField(u'Verden ID')


class WorldForm(Form):
    is_world_form = HiddenField(u'Er verden', [InputRequired()], default='True')
    world_id = HiddenField(u'Verden ID', [InputRequired()])
    description = TextAreaField(u'Beskrivelse')


class ChangeEmail(Form):
    new_email = EmailField(u'Ny e-post adresse', [Email()])
    confirm_email = EmailField(u'Bekreft e-post adressen',
                               [Email(), EqualTo('new_email', u'E-post adressene er ikke like')])
    password = PasswordField(u'Skriv inn passordet ditt for å bekrefte endringen', [InputRequired()])


class ChangeName(Form):
    new_name = StringField(u'Nytt navn / beskrivelse for denne brukeren', [InputRequired()])


class ChangePassword(Form):
    # TODO password length requirements?
    old_password = PasswordField(u'Gammelt passord', [InputRequired()])
    new_password = PasswordField(u'Nytt passord', [InputRequired()])
    confirm_password = PasswordField(u'Bekreft nytt passord',
                                     [InputRequired(), EqualTo('new_password', u'Passordene er ikke like')])


class ChangePlayername(Form):
    playername = StringField(u'Ditt minecraft spillernavn', [InputRequired()])
    uuid = StringField(u'Mojang UUID', [InputRequired()])
    password = PasswordField(u'Skriv inn passordet ditt for å bekrefte endringen', [InputRequired()])
