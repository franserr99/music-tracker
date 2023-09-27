from .models import User
from django_injector import provider, singleton

@provider
@singleton
def provide_user_model() -> User:
    return User
