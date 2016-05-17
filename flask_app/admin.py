# -*- coding: utf-8 -*-

# Required imports for Admin panel
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField
from wtforms import validators
from database import db
from flask_security import current_user
from models import User, Role, Meeting, World
from flask.ext.security import utils
from flask_app import app


def initAdmin():
    # Initialize Flask-Admin and add needed views/pages
    admin = Admin(app)

    # Configurations for admin panel about meetings
    class MeetingView(ModelView):
        def is_accessible(self):
            return current_user.has_role('admin')

    class WorldView(ModelView):
        def is_accessible(self):
            return current_user.has_role('admin')

    # Configurations to a view for displaying, deleting, adding and editing users.
    class UserView(ModelView):
        column_exclude_list = ['password', 'confirmed_at']
        
        # Automatically display readable roles
        column_auto_select_related = True
        
        def index(self):
            self._admin_template_args['active'] = True
        
        # Makes sure only admins can make changes to anything concerning users through the admin panel,
        # by not displaying the User-tab if admin panel is somehow accessed by a regular user.
        def is_accessible(self):
            return current_user.has_role('admin')
        
        # Replaces Flask's standard textfield for passwords with an actual password field
        def scaffold_form(self):
            form_class = super(UserView, self).scaffold_form()
            form_class.password2 = PasswordField('Password', [
                validators.EqualTo('confirm', message='Passwords must match')
            ])
            form_class.confirm = PasswordField('Confirm password')
            return form_class
        
        # Makes sure the data from the new PW field is sent to the DB,
        # so that the new PW field is an actual replacement, and not just a field that says "Password".
        # Also hashes PW's before sending them to the DB. If PW field is blank in edit user,
        # existing PW will be kept. Gives error message when PW field is blank in create - not sure how to fix.
        def on_model_change(self, form, model, is_created):
            if len(model.password2):
                model.password = utils.encrypt_password(model.password2)
        
        # Excludes fields we don't want to display. Both fields that are not needed (names, confirmed_at),
        # and fields that we want to avoid using, such as password and (soon) active.
        # Separated on different lines so singular ones can be commented out, to check what causes errors.
        form_excluded_columns = [
            'confirmed_at',
            'password',
            'mojang_playername',
            'mojang_uuid'
        ]

    # Adds previously configured views
    admin.add_view(UserView(User, db.session))
    admin.add_view(MeetingView(Meeting, db.session))
    admin.add_view(WorldView(World, db.session))
