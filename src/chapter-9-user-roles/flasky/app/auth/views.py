from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from . import auth
from ..models import User
from ..email import send_email
from .. import db
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # Post/Redirect/Get pattern
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    # The folder auth that will host the templates must be created under
    # app/templates (Blueprints can also be configured to have their own
    # independent folder for template)
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    # Remove and reset the user session
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm',
                   user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


"""
    The before_app_request handler will intercept a request when three
    conditions are true:
        -   a user is logged in
        -   the account for the user is not confirmed
        -   the requested endpoint is outside of the authentication blueprint
"""


@auth.before_app_request
def before_request():
    if current_user.is_authenticated() \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    user = current_user
    send_email(user.email, 'Confirm Your Account', 'auth/email/confirm',
               user=user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
