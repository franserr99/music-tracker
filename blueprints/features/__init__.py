# Inside your_blueprint/__init__.py

from flask import Blueprint

feature_blueprint = Blueprint('feature_blueprint', __name__, template_folder='templates')

from . import routes