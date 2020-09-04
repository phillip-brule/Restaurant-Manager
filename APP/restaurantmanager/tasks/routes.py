from flask import (render_template, url_for, flash,
                    redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from restaurantmanager import db
from restaurantmanager.models import Task, Role, Report, Restaurant
from restaurantmanager.tasks.forms import TaskForm

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks')
@login_required
def list_of_tasks():
    page = request.args.get('page', 1, type=int)
    user_role = Role.query.filter_by(user_id=current_user.id).first()
    r_id = user_role.r_id
    tasks = Task.query.filter_by(r_id=r_id).order_by(Task.name.asc()).paginate(page=page, per_page = 10)
    return render_template('tasks.html', tasks=tasks)

@tasks.route('/reports')
@login_required
def reports():
    page = request.args.get('page', 1, type=int)
    user_role = Role.query.filter_by(user_id=current_user.id).first()
    r_id = user_role.r_id
    reports = Report.query.filter_by(r_id=r_id).order_by(Report.report_date.desc()).paginate(page=page, per_page=10)
    return render_template('reports.html', reports=reports)

@tasks.route('/task/new', methods=['GET', 'POST'])
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
    return render_template('create_task.html', title = 'New Task', form=form, legend='New Task')


@tasks.route('/task/<int:task_id>')
@login_required
def task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task.html', title=task.name, task=task)

@tasks.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    role = Role.query.filter_by(user_id=current_user.id).first()
    r_id = role.r_id
    if task.restaurant.id != r_id:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.name = form.name.data
        task.description = form.description.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('tasks.task', task_id=task.id))
    elif request.method == 'GET':
        form.name.data = task.name
        form.description.data = task.description    
    return render_template('create_task.html', title = 'Edit Task', form=form, legend='Edit Task')

@tasks.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    role = Role.query.filter_by(user_id=current_user.id).first()
    r_id = role.r_id
    if task.restaurant.id != r_id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('main.home'))



@tasks.route('/report/<string:report_id>')
@login_required
def report_page(report_id):
    report = Report.query.filter_by(id = report_id).first_or_404()
    return render_template('report_page.html', report=report, completed_tasks = report.completed_tasks)
