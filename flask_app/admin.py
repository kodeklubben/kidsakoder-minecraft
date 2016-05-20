# -*- coding: utf-8 -*-
""" Flask-Admin """

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import validators, PasswordField
from flask_security import current_user, utils
from database import db
from models import User, Meeting, World


class MeetingView(ModelView):
    """ Configuration for admin panel Meeting tab """

    # Meetings should only be listed in admin panel
    # Edit, create or delete will break integrity
    can_create = False
    can_edit = False
    can_delete = False

    # Tried to get meeting creators email, but relations in models are not properly configured
    # # column_auto_select_related = True
    # form_ajax_refs = {
    #     'user_id': {
    #         'fields': ['email']
    #     }
    # }

    # View is acessible only to admins
    def is_accessible(self):
        return current_user.has_role('admin')


class WorldView(ModelView):
    """ Configuration for admin panel World tab """

    # Worlds should only be listed in admin panel
    # Edit, create or delete will break integrity
    can_create = False
    can_edit = False
    can_delete = False

    # Columns to exclude from list view
    column_exclude_list = ['preview', 'seed']

    # View is accessible only to admins
    def is_accessible(self):
        return current_user.has_role('admin')


class UserView(ModelView):
    """ Configuration for admin panel User tab """
    # Columns to exclude from list view
    column_exclude_list = ['password', 'confirmed_at']
    # Fields to exclude from user register / edit form
    form_excluded_columns = [
        'confirmed_at',
        'password',
        'mojang_playername',
        'mojang_uuid'
    ]

    # Automatically display readable roles
    column_auto_select_related = True

    def index(self):
        self._admin_template_args['active'] = True

    # Make sure only admins can make changes to anything concerning users through the admin panel,
    def is_accessible(self):
        return current_user.has_role('admin')

    # Replaces standard textfield for passwords with an actual password field
    def scaffold_form(self):
        form_class = super(UserView, self).scaffold_form()
        form_class.password2 = PasswordField('Password', [
            validators.EqualTo('confirm', message='Passwords must match')
        ])
        form_class.confirm = PasswordField('Confirm password')
        return form_class

    # Hash password and store hash in user object.
    # If PW field is blank in edit user existing PW will be kept.
    # Gives error message when PW field is blank in create - not sure how to fix.
    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = utils.encrypt_password(model.password2)


def init_admin(app):
    """ Initialize Flask-Admin """
    admin = Admin(app)
    # Adds previously configured views
    admin.add_view(UserView(User, db.session))
    admin.add_view(MeetingView(Meeting, db.session))
    admin.add_view(WorldView(World, db.session))

    return admin
