"""_summary_

    Returns:
        _type_: _description_
"""
from django.http import JsonResponse,Http404#, HttpResponse
from injector import inject
from rest_framework.views import APIView
from rest_framework import status

from ..services.user_service import UserService
from ..services.liked_track_service import LikedTrackService
from ..serializers import UserSerializer, LikedTrackSerializer,UserWithTracksSerializer


#i want CBV but also want DI
#best of both worlds is wrapping the creation of a CBV with a
#function that gets the service bean injected
@inject
def create_user_view(user_service: UserService,liked_track_service:LikedTrackService):
    """_summary_

    Args:
        user_service (UserService): _description_

    Returns:
        _type_: _description_
    """
    return UserView.as_view(user_service=user_service, liked_track_service=liked_track_service)
class UserView(APIView):
    """_summary_

    Args:
        APIView (_type_): _description_
    """

    def __init__(self, user_service: UserService,liked_track_service:LikedTrackService, *args, **kwargs):
        self.user_service = user_service
        self.liked_track_service=liked_track_service
        super().__init__(*args, **kwargs)
    def get(self,request,user_id):
        """
            Retrieve a user by ID.

            Args:
                request (rest_framework.request.Request): The HTTP request object.
                user_id (int): The ID of the user to retrieve.

            Returns:
                rest_framework.response.Response: The HTTP response object.
        """
        user=self.user_service.get_user(user_id=user_id)
        if user:
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404("User does not exist")
        # try:
        #     user = self.user_service.get_user(user_id)
        # except User.DoesNotExist:  # Or whatever exception your service throws
        #     raise Http404("User does not exist")

        # serializer = UserSerializer(user)
        # return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        """
            Handle POST request to create a user.

            Args:
                request (rest_framework.request.Request): The HTTP request object.

            Returns:
                rest_framework.response.Response: The HTTP response object.
        """
        # Handle POST request
        serializer=UserSerializer(request.data)
        if serializer.is_valid():
            user=self.user_service.create_user(user_data=serializer.validated_data)
            return JsonResponse(UserSerializer(user).data,status=status.HTTP_201_CREATED)
        #return JsonResponse({"message": "This is a POST request"})
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, user_id):
        """
            Update a user based on user_id and request data

            Args:
                request (rest_framework.request.Request): HTTP request
                user_id (int): Identifier for the user to update

            Returns:
                JsonResponse: HTTP response indicating the outcome of the operation
        """
        serializer = UserSerializer(request.data)
        if serializer.is_valid():
            user=self.user_service.update_user(user_id=user_id,
                                                user_data=serializer.validated_data)
            if user:
                return JsonResponse(UserSerializer(user).data,status=status.HTTP_200_OK)
            else:
                raise Http404("User does not exist")
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        """Delete a user by ID.

        Args:
            request (rest_framework.request.Request): The HTTP request object.
            user_id (int): The ID of the user to delete.

        Returns:
            rest_framework.response.Response: The HTTP response object.
        """
        user = self.user_service.delete_user(user_id=user_id)

        if not user:
            raise Http404("User does not exist")
        else:
            return JsonResponse({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    def get_user_liked_tracks(self, request, user_id):
        """_summary_

        Args:
            request (_type_): _description_
            user_id (_type_): _description_

        Raises:
            Http404: _description_

        Returns:
            _type_: _description_
        """
        user=self.user_service.get_user(user_id=user_id)
        if user:
            serializer = UserWithTracksSerializer(user)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404("User does not exist")
    def like_track(self,request):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
    
        serializer =LikedTrackSerializer(request.data) 
        if serializer.is_valid():
            liked_track=self.liked_track_service.like_track(liked_track_data=serializer.validated_data)
            return JsonResponse(UserSerializer(liked_track).data,status=status.HTTP_201_CREATED)
        #return JsonResponse({"message": "This is a POST request"})
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

