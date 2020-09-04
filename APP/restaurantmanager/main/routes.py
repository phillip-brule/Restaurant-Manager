from flask import render_template, request, Blueprint
from restaurantmanager.models import Task, Role, Report
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


'''
#Role Management
from flask.ext.principal import identity_loaded, RoleNeed, UserNeed

@identity_loaded.connect_via()
def on_identity_loaded(sender, identity):
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
'''



@main.route('/home')
@login_required
def home():
    tasks = Task.query.all()
    user_role = Role.query.filter_by(user_id=current_user.id).first()
    r_id = user_role.r_id
    reports = Report.query.filter_by(r_id=r_id)
    return render_template('home.html', tasks=tasks, reports=reports)



@main.route('/')
@main.route('/about')
def about():
    return render_template('about.html', title='About')
