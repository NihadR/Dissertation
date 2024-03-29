from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dissertation.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    '''
    Initialises the entire app 
    '''
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Registers the different blueprints created for the 
    # mini packages in the system
    from dissertation.users.routes import users
    from dissertation.admin.routes import admin
    from dissertation.main.routes import main
    from dissertation.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app