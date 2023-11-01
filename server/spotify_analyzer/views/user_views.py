"""_summary_

    Returns:
        _type_: _description_
"""

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from ..serializers import UserSerializer
from ..models import User


class UserListCreate(ListCreateAPIView):
    queryset = User.objects.all()  # Adjust the queryset to your needs
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()  # Adjust the queryset to your needs
    serializer_class = UserSerializer
    lookup_field = 'user_id'  # The field in the URL to look up by
