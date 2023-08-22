# Inside your_blueprint/__init__.py

from flask import Blueprint

feature_blueprint = Blueprint('feature', __name__, template_folder='templates')

from . import routes