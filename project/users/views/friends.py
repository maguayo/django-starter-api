from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from project.users.models.friends import Friend
from project.users.serializers.friends import FriendModelSerializer
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from project.functions import response_wrapper
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


class FriendsList(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        friends = Friend.objects.filter(
            Q(user=request.user) | Q(friend=request.user)
        ).distinct()
        serialiser = FriendModelSerializer(friends, many=True)
        return Response(response_wrapper(data=serialiser.data, success=True))


class FriendsDetail(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, friend_id):
        try:
            friend = Friend.objects.get(user=request.user, friend_id=friend_id)
            friend.delete()
        except ObjectDoesNotExist:
            friend = Friend.objects.get(user=friend_id, friend_id=request.user)
            friend.delete()

        return Response(
            response_wrapper(data=None, success=True),
            status=status.HTTP_200_OK,
        )

    def post(self, request, friend_id):
        friend = Friend.objects.filter(user=request.user, friend_id=friend_id)
        if friend.exists() or request.user.id == friend_id:
            return Response(
                response_wrapper(
                    data={"detail": "Friend already exists"}, success=False
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            friend = Friend.objects.get(user=friend_id, friend_id=request.user)
        except ObjectDoesNotExist:
            friend = Friend.objects.create(
                user=request.user, friend_id=friend_id
            )
        else:
            friend.accepted = True
            friend.accepted_date = timezone.now()
            friend.save()

        serialiser = FriendModelSerializer(friend)

        return Response(
            response_wrapper(data=serialiser.data, success=True),
            status=status.HTTP_201_CREATED,
        )
