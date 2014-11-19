from datetime import datetime
from flask import (render_template, session, redirect, url_for, current_app,
                   abort, flash)
from flask.ext.login import login_required, current_user
from . import main
from .forms import NameForm, EditProfileForm
from .. import db
from ..models import User, Permission
from ..email import send_email
from ..decorators import admin_required, permission_required


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
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New user',
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


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

"""
    If this route is accessed by a user who is not authenticated , Flask-Login
    will intercept the request and send the user to the login page instead.
"""


@main.route('/secret')
@login_required
def secret():
    return "Super secret stuff !"


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators !"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators !"
