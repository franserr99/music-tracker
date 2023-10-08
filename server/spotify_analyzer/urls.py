from django.urls import include, path


app_name = 'your_app'

urlpatterns = [
    path('api-auth/', include('rest_framework.urls'))
]