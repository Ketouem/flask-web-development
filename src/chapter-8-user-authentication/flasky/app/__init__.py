from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

"""
    Single file app has a big drawback, because the app is created in the
    global scope, there is no way to apply configuration changes dynamically.
    The solution to this problem is to delay the creation of the application by
    moving it into a factory function that can be invoked from the script.
    This gives the ability to set the configuration but also be able to create
    multiple application instances (for testing purposes).
"""

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
"""
    Provides security against session tampering. With the 'strong' setting,
    Flask-Login will keep track of the client's IP address and user agent and
    will log the user out if it detects a change.
"""
login_manager.session_protection = 'strong'
# Sets the endpoint for the login page
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Attach routes and custom error pages
    from main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    # Registering the auth blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    """
        The `url_prefix` argument in the blueprint registration is optional.
        When used, all the routes defined in the blueprint will be registered
        with the given prefix, in this case '/auth'.
        Ex: the /login route will be registered as '/auth/login'
    """

    return app
