from flask import Blueprint

history_blueprint = Blueprint('history', __name__, template_folder='templates')

from . import routes