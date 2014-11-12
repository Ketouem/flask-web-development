# Auto generate HTML forms with validators
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


# WTF form definition
class NameForm(Form):
    # Represents an <input type="text">
    # Required validator ensures that the field is not submitted empty
    name = StringField('What is your name ?', validators=[Required()])
    # Represents an <input type="submit">
    submit = SubmitField('Submit')
