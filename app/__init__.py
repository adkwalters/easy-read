import logging
from logging.handlers import SMTPHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from config import Config

# Instantiate app database engine
db = SQLAlchemy()

# Instatiate and configure login manager 
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access that page.'
login.login_message_category = 'error'

# Instantiate flask-mail
mail = Mail()


def create_app(config_class=Config):

    # Create Flask app
    app = Flask(__name__)    

    # Configure app from config class
    app.config.from_object(config_class)

    # Initialise extensions
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Email all errors to all admins while in production
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling 
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='EasyRead Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app


from app import models