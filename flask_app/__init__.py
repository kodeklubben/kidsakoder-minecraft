"""
The flask application package.
"""

from flask import Flask
from datetime import datetime
from wtforms.fields import PasswordField
from flask_security import current_user
from flask.ext.security import utils
# Required imports for Admin panel
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

# See configuration.py for possible configuration objects
app.config.from_object('flask_app.configuration.Development')

# Initialize Flask-Security
from database import db
from flask_security import Security, SQLAlchemyUserDatastore
from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)



# Initialize Flask-Admin and add needed views/pages
admin = Admin(app)

#Configurations to a view for displaying, deleting, adding and editing users.
class UserView(ModelView):
    column_exclude_list = ['password', 'first_name', 'last_name']
    column_auto_select_related = True
    #Makes sure only admins can make changes to anything concerning users through the admin panel
    def is_accessible(self):
        return current_user.has_role('admin')
    #Replaces Flask's standard textfield for passwords with an actual password field
    def scaffold_form(self):
        form_class = super(UserView, self).scaffold_form()
        form_class.password2 = PasswordField('Nytt passord')
        return form_class
    #Makes sure the data from the new PW field is sent to the DB
    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = utils.encrypt_password(model.password2)
    #Excludes fields we don't want to display. Both fields that are not needed (names, confirmed_at), and fields that we
    #want to avoid using, such as password and (soon) active
    form_excluded_columns = [#'active',
    'confirmed_at',
    'first_name',
    'last_name',
    'password'
    ]

#Adds previously configured userview
admin.add_view(UserView(User, db.session))



#from datetime import datetime
@app.context_processor
def inject_year():
    """ Make year available in templates """
    return dict(year=datetime.now().year)

# Do last
import flask_app.views
