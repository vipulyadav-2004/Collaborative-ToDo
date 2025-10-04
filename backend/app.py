# backend/app.py

from flask import render_template, url_for, flash, redirect, session, Blueprint
from .models import db, User
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

<<<<<<< HEAD
@main_blueprint.route('/Todo')
=======
@main.route('/Logout')
def Logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main.route('/History', methods=['GET','POST'])
def History():
    return render_template('history.html' , title = 'History')

@main.route('/Todo')
>>>>>>> 5f242e70f30ccf5b46f6a52b0298674612bda889
def Todo():
    return render_template('todo.html', title='Todo')