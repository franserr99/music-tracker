from flask import Blueprint

history_blueprint = Blueprint('history_blueprint', __name__, template_folder='templates')

from . import routes