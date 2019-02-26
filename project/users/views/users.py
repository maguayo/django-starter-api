from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from project.users.permissions import IsAccountOwner
from project.users.serializers.profiles import ProfileModelSerializer
from project.users.serializers import (
    AccountVerificationSerializer,
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
)
from project.users.models import User
from rest_framework.exceptions import NotFound


class UserList(APIView):
    def post(self, request, format=None):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class UserDetail(APIView):
    def patch(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise NotFound

        serializer = UserModelSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = UserModelSerializer(user).data
        return Response(data)


class UserProfile(APIView):
    def patch(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise NotFound

        profile = user.profile
        serializer = ProfileModelSerializer(
            profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = UserModelSerializer(user).data
        return Response(data)
