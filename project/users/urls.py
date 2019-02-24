from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from .views import users as user_views
from project.users.views import UserList



urlpatterns = [
    path('login/', view=obtain_jwt_token, name="login"),
    path('signup/', view=UserList.as_view(), name="signup"),
    path('token/refresh/', view=refresh_jwt_token, name="token_refresh"),
    path('token/verify/', view=verify_jwt_token, name="token_refresh"),
]
