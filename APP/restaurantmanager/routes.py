import secrets
import os
from PIL import Image
from flask import escape, request, render_template, url_for, flash, redirect, request
from restaurantmanager import app, db, bcrypt
from restaurantmanager.forms import RegistrationForm, LoginForm, UpdateAccountForm, TaskForm
from restaurantmanager.models import User, Task, Completed_Task, Report, Restaurant, Role
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required

'''
#Role Management
from flask.ext.principal import identity_loaded, RoleNeed, UserNeed

@identity_loaded.connect_via(app)
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

@app.route('/')
@app.route('/home')
def home():
    tasks = Task.query.all()
    user_role = Role.query.filter_by(user_id=current_user.id).first()
    r_id = user_role.r_id
    reports = Report.query.filter_by(r_id=r_id)
    return render_template('home.html', tasks=tasks, reports=reports)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    form.restaurant_id.choices = [(r.id, r.name) for r in Restaurant.query.order_by('name')]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        role = Role(user_id=1, r_id=form.restaurant_id.data, role='employee')
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data}! Your account has been created and you are now able to login!', 'success')
        return redirect( url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))




#for editing account picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file=image_file, form=form)



@app.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(user_id=current_user.id).first()
        r_id = role.r_id
        task = Task(name=form.name.data, description=form.description.data, r_id=r_id)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
    return render_template('create_task.html', title = 'New Task', form=form)


@app.route('/task/<int:task_id>')
def task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task.html', title=task.name, task=task)