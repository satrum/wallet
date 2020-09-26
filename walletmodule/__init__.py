"""Initialize app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import datetime

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from .assets import compile_static_assets
        from . import models

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        # Create Default Bank Account
        email = app.config['BANK_EMAIL']
        password = app.config['BANK_PASS']
        if models.User.query.filter_by(email=email).first() is None:
            bank_user = models.User(name='bank', email=email, created_on=datetime.datetime.utcnow())
            bank_user.set_password(password)
            db.session.add(bank_user)
            db.session.commit()
            print('bank user created')
        else:
            print('bank user already exists')

        # Compile static assets
        if app.config['FLASK_ENV'] == 'development':
            compile_static_assets(app)

        return app
