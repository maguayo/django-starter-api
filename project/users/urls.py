from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import users as user_views
from project.users.views.friends import FriendsList, FriendsDetail

router = DefaultRouter()
router.register(r"users", user_views.UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("friends/", view=FriendsList.as_view(), name="friends-list"),
    path(
        "friends/<uuid:friend_id>/",
        view=FriendsDetail.as_view(),
        name="friends-detail",
    ),
]
