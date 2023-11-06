"""_summary_

    Returns:
        _type_: _description_
"""

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ..serializers import UserSerializer
from ...models import User


@method_decorator(csrf_exempt, name='dispatch')
class UserListCreate(ListCreateAPIView):
    queryset = User.objects.all()  # Adjust the queryset to your needs
    serializer_class = UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()  # Adjust the queryset to your needs
    serializer_class = UserSerializer
    lookup_field = 'id'  # The field in the URL to look up by
