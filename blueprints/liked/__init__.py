from flask import Blueprint

liked_blueprint = Blueprint('liked', __name__, template_folder='templates')

from . import routes