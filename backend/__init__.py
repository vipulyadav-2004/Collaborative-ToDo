import os
from flask import Flask
from .models import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    # --- Configurations ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Initialize Extensions ---
    db.init_app(app)
    Migrate(app, db)

    # --- Register Blueprints ---
    from .app import main_blueprint
    app.register_blueprint(main_blueprint)

    return app

    