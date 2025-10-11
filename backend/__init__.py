import os
from flask import Flask
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect # <-- 1. Import CSRFProtect

login_manager = LoginManager()
login_manager.login_view = 'main.Login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    # --- Configurations ---
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///../instance/site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Initialize Extensions ---
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    CSRFProtect(app) # <-- 2. Initialize it with your app

    # --- Register Blueprints ---
    from .app import main
    app.register_blueprint(main)

    return app