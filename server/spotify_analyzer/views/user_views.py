from django.http import JsonResponse, HttpResponse
from django.views import View
from injector import inject

from server.spotify_analyzer.services.user_service import UserService


#i want CBV but also want DI
#best of both worlds is wrapping the creation of a CBV with a 
#function that gets the service bean injected
@inject
def create_user_view(user_service: UserService):
    return UserView.as_view(user_service=user_service)
class UserView(View):

    def __init__(self, user_service, *args, **kwargs):
        self.user_service = user_service
        super().__init__(*args, **kwargs)
    
    def get(self, request):
        # Handle GET request
        return JsonResponse({"message": "This is a GET request"})

    def post(self, request):
        # Handle POST request
        return JsonResponse({"message": "This is a POST request"})

    def put(self, request):
        # Handle PUT request
        return JsonResponse({"message": "This is a PUT request"})

    def delete(self, request):
        # Handle DELETE request
        return JsonResponse({"message": "This is a DELETE request"})

