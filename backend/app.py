# backend/app.py

from flask import render_template, url_for, flash, redirect, session, Blueprint
from .models import db, User
from .forms import RegistrationForms, LoginForm

# Create a Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    username = session.get('username')
    return render_template('index.html',  username=username)

@main.route('/SignUp', methods=['GET', 'POST'])
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

@main.route('/Login', methods=['GET', 'POST'])
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

@main.route('/Logout')
def Logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main.route('/History', methods=['GET','POST'])
def History():
    return render_template('history.html' , title = 'History')

@main.route('/Todo')
def Todo():
    return render_template('todo.html', title='Todo')