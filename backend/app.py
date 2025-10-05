from flask import render_template, url_for, flash, redirect, Blueprint, request, jsonify
from .models import db, User, Task
from .forms import RegistrationForms, LoginForm, DeleteTaskForm
from flask_login import login_user, logout_user, login_required, current_user

# The name of the blueprint variable is now 'main' to match the import
main = Blueprint('main', __name__)

@main.route('/')
def index():
    # No need to pass username; current_user is available in all templates
    return render_template('index.html')

@main.route('/SignUp', methods=['GET', 'POST'])
def Signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForms()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('main.Login'))
    return render_template('signup.html', title='Signup', form=form)

@main.route('/Login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Use login_user to manage the session and "Remember Me"
            login_user(user, remember=form.remember.data)
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/Logout')
@login_required # Protect this route
def Logout():
    logout_user() # Use logout_user to properly clear the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main.route('/Todo')
@login_required # Protect this route
def Todo():
    return render_template('todo.html', title='Todo')

@main.route('/History', methods=['GET','POST'])
@login_required # Protect this route
def History():
    tasks = Task.query.filter_by(author=current_user).order_by(Task.date_created.desc()).all()
    delete_form = DeleteTaskForm()
    return render_template('history.html', title='Task History', tasks=tasks, delete_form=delete_form)

# --- TASK API ROUTES ---

@main.route('/get_tasks')
@login_required
def get_tasks():
    tasks = Task.query.filter_by(author=current_user, status='active').all()
    return jsonify([{'id': task.id, 'content': task.content} for task in tasks])

@main.route('/add_task', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    new_task = Task(content=data['content'], author=current_user)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'content': new_task.content})

@main.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    if task_to_delete and task_to_delete.author == current_user:
        task_to_delete.status = 'deleted'
        db.session.commit()
        return jsonify({'message': 'Task marked as deleted'})
    return jsonify({'error': 'Task not found or unauthorized'}), 404

@main.route('/delete_history/<int:task_id>', methods=['POST'])
@login_required
def delete_history(task_id):
    task_to_delete = Task.query.get(task_id)
    if not task_to_delete:
        flash('Task history not found.', 'danger')
        return redirect(url_for('main.History'))
    if task_to_delete.author != current_user:
        flash('You are not authorized to delete this task.', 'danger')
        return redirect(url_for('main.History'))
    db.session.delete(task_to_delete)
    db.session.commit()
    flash('Task history permanently deleted.', 'success')
    return redirect(url_for('main.History'))