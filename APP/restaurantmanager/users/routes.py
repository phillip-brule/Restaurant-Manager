from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from restaurantmanager import db, bcrypt
from restaurantmanager.models import User, Task, Completed_Task, Report, Restaurant, Role
from restaurantmanager.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from restaurantmanager.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    form.restaurant_id.choices = [(r.id, r.name) for r in Restaurant.query.order_by('name')]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        role = Role(user_id=1, r_id=form.restaurant_id.data, role='employee')
        db.session.add(user)
        db.session.add(role)
        db.session.commit()
        flash(f'Welcome {form.name.data}! Your account has been created and you are now able to login!', 'success')
        return redirect( url_for('users.login'))
    return render_template('register.html', title = 'Register', form = form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.tasks'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.about'))


@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file=image_file, form=form)


#page that shows all the tasks an employee has completed
#this page will show analytics on how well this employee is performing
@users.route('/employee/<string:user_id>')
@login_required
def employee_page(user_id):
    user = User.query.filter_by(id = user_id).first_or_404()
    page = request.args.get('page', 1, type=int)
    completed_tasks = Completed_Task.query.filter_by(user_id=user_id)\
        .order_by(Completed_Task.date_completed.desc())\
        .paginate(page=page, per_page = 10)
    return render_template('employee_page.html', completed_tasks=completed_tasks, user=user)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.tasks'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        message = "An email with reset instructions has been sent to " + user.email + "."
        flash(message, 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('tasks.tasks'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated and you are now able to login!', 'success')
        return redirect( url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)