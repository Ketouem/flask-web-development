from . import db
# Werkzeug provides facilities for password hashing
from werkzeug.security import generate_password_hash, check_password_hash
# User model for logins
from flask.ext.login import UserMixin
from . import login_manager


# Flask-Login requires a callback function that loads a user given its id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


class User(UserMixin, db.Model):
    """
    To be able to work with the User model, Flask-Login requires a few methods
    to be implemented:
        -   is_authenticated
        -   is_active
        -   is_anonymous
        -   get_id
    Flask-Login provides a base UserMixin that has default implementations that
    are appropriate for most cases.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "<User %r>" % self.username
