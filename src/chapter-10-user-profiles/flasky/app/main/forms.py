# Auto generate HTML forms with validators
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length


# WTF form definition
class NameForm(Form):
    # Represents an <input type="text">
    # Required validator ensures that the field is not submitted empty
    name = StringField('What is your name ?', validators=[Required()])
    # Represents an <input type="submit">
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
