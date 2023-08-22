from . import user_blueprint

from db.queries.user_queries import create_user
from db.queries.user_queries import users_list


@user_blueprint.route('users_list')
def user_list():
    return user_list()

@user_blueprint.route('create_user')
def add_user(id):
    create_user(id)
