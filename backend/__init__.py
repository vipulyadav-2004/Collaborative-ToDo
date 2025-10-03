# backend/__init__.py
import os
from flask import Flask
from .models import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with the app
    db.init_app(app)
    Migrate(app, db)

    
    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

    