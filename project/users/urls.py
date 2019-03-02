from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from .views import users as user_views

from project.users.views.profiles import ProfileDetail
from .views import users as user_views

router = DefaultRouter()
router.register(r"users", user_views.UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
]
