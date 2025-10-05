# backend/app.py

from flask import render_template, url_for, flash, redirect, session, Blueprint,request,jsonify
from .models import db, User ,Task
from .forms import RegistrationForms, LoginForm

# Create a Blueprint
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    username = session.get('username')
    return render_template('index.html',  username=username)

@main_blueprint.route('/SignUp', methods=['GET', 'POST'])
def Signup():
    form = RegistrationForms()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('main.Login'))
    return render_template('signup.html', title='Signup', form=form)

@main_blueprint.route('/Login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['username'] = user.username
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@main_blueprint.route('/Logout')
def Logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main_blueprint.route('/Todo')
def Todo():
    # Get the username from the session
    username = session.get('username')
    # Pass it to the template
    return render_template('todo.html', title='Todo', username=username)

@main_blueprint.route('/History', methods=['GET','POST'])
def History():
    if 'username' in session:
        # Get the username from the session
        username = session.get('username') 
        user = User.query.filter_by(username=username).first()
        # Pass the username to the template
        return render_template('history.html', title='Task History', tasks=user.tasks, username=username)
    else:
        flash('You need to be logged in to see your history.', 'danger')
        return redirect(url_for('main.Login'))
  
@main_blueprint.route('/get_tasks')
def get_tasks():
    if 'username' not in session:
        return jsonify([])
    user = User.query.filter_by(username=session['username']).first()
    tasks = Task.query.filter_by(author=user, status='active').all()
    return jsonify([{'id': task.id, 'content': task.content} for task in tasks])

@main_blueprint.route('/add_task', methods=['POST'])
def add_task():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    user = User.query.filter_by(username=session['username']).first()
    
    new_task = Task(content=data['content'], author=user)
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({'id': new_task.id, 'content': new_task.content})

@main_blueprint.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    task_to_delete = Task.query.get(task_id)
    if task_to_delete and task_to_delete.author.username == session['username']:
        # We change the status instead of deleting forever
        task_to_delete.status = 'deleted'
        db.session.commit()
        return jsonify({'message': 'Task marked as deleted'})
    
    return jsonify({'error': 'Task not found or unauthorized'}), 404