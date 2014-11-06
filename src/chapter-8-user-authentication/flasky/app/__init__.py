from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
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


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # Attach routes and custom error pages
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
