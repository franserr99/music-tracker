from flask import Blueprint

library_blueprint = Blueprint('library_blueprint', __name__, template_folder='templates')

from . import routes