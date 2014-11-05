from flask import Blueprint

"""
    A blueprint is similar to an application in that it can define routes.
    The difference is that the routes associated with a blueprint are in a
    'dormant' state until the blueprint is registered with an application, at
    which point the routes become part of it.
"""

main = Blueprint('main', __name__)

# These modules are imported at the bottom to avoid circular dependencies
# because views and errors need to import the main blueprint
from . import views, errors
# The routes of the application are stored in app/main/views.py
# The error handlers are in app/main/errors.py
