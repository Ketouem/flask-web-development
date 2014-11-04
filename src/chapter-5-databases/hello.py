import os
# By default Flask looks for templates in a templates subfolder located inside
# the app folder
from flask import Flask, render_template, session, redirect, url_for, flash
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

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

# SQLAlchemy model
# TODO: finish model definition

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
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            # Feedback message when the form is submitted
            # also need a part in the template itself.
            flash("Looks like you've changed your name!")
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(),
                           form=form, name=session.get('name'))


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

if __name__ == "__main__":
    app.run(debug=True)
