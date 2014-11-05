from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
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
            if main.config['FLASKY_ADMIN']:
                send_email(main.config['FLASKY_ADMIN'], 'New user',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        # in this case url_for needs the namespace of the blueprint
        # can also be shortened in .index
        return redirect(url_for('main.index'))
    return render_template('index.html', current_time=datetime.utcnow(),
                           form=form, name=session.get('name'),
                           known=session.get('known', False))
