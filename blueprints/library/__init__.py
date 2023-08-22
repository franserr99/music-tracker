from flask import Blueprint

library_blueprint = Blueprint('library', __name__, template_folder='templates')

from . import routes