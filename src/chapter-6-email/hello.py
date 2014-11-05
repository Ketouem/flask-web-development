import os
# By default Flask looks for templates in a templates subfolder located inside
# the app folder
from flask import Flask, render_template, session, redirect, url_for
# Wraps Twitter bootstrap to use them inside templates
from flask.ext.bootstrap import Bootstrap
# Wraps moment.js, a JS library to handle dates and times. Depends on jquery.js
# already available through bootstrap
from flask.ext.moment import Moment
# Auto generate HTML forms with validators
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
# SQLAlchemy Wrapper
from flask.ext.sqlalchemy import SQLAlchemy
# For debugging, adding imports to the shell
from flask.ext.script import Shell, Manager
# Database migration, wrapper around Alembic
from flask.ext.migrate import Migrate, MigrateCommand
# Email handling
from flask.ext.mail import Mail, Message
# User for sending async email (mail.send is blocking)
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime

app = Flask(__name__)
# To implement CSRF protection, Flask-WTF needs the application to configure an
# encryption key.
app.config['SECRET_KEY'] = "supersecretkey"
# ORM Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'\
                                        + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# Email configuration
app.config.update(
    MAIL_SERVER='smtp.googlemail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]',
    FLASKY_MAIL_SENDER='Flasky Admin <flasky@example.com>',
    FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')
)


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
mail = Mail(app)


# SQLAlchemy model
class Role(db.Model):
    # Define the name of the table
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # One to many relationship, request that the query is not automatically
    # executed.
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r>" % self.username


# WTF form definition
class NameForm(Form):
    # Represents an <input type="text">
    # Required validator ensures that the field is not submitted empty
    name = StringField('What is your name ?', validators=[Required()])
    # Represents an <input type="submit">
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    # Handling the Post/Redirect/Get pattern and the refresh of the page
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            # Known session variable used for template customization after
            # the redirection
            session['known'] = False
            # Send an email to the admin when a new user registers
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New user',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(),
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# Custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
# Expose the database migration command to the manager
# ex: python hello.py db init
manager.add_command("db", MigrateCommand)

# The migrate subcommand creates an automatic migration script
# ex: python hello.py db migrate -m "initial migration"

# Upgrade a database
# ex: python hello.py db upgrade


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + " " + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # mail.send(msg) => is blocking
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

if __name__ == "__main__":
    # Launch app with python hello.py runserver
    # manager.run()
    app.run(debug=True)
