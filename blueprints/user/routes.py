from . import user_blueprint
from db.queries.user_queries import user_id_list
from db.queries.user_queries import create_user
from db.queries.user_queries import users_list


@user_blueprint.route('user_id_list')
def user_list():
    pass

@user_blueprint.route('create_user')
def add_user():
    pass

#@user_blueprint.route('create_user')
#def add_user():
#    pass

