from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from .views import users as user_views
from project.users.views.users import UserList, UserDetail, UserLogin
from project.users.views.profiles import ProfileDetail


urlpatterns = [
    path("login/", view=UserLogin.as_view(), name="login"),
    path("signup/", view=UserList.as_view(), name="signup"),
    path("token/refresh/", view=refresh_jwt_token, name="token_refresh"),
    path("token/verify/", view=verify_jwt_token, name="token_verify"),
    path("<int:user_id>/", view=UserDetail.as_view(), name="user-detail"),
    path(
        "<int:user_id>/profile/",
        view=ProfileDetail.as_view(),
        name="profile-detail",
    ),
]
