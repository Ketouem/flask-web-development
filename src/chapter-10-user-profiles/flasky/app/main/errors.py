# Blueprint with error handlers

from flask import render_template
from . import main


# Need to user app_errorhandler and not errorhandler because the later will
# only be invoked for errors that originate in the blueprint
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
