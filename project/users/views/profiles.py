from rest_framework.views import APIView
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from project.functions import response_wrapper
from project.users.serializers.profiles import ProfileModelSerializer
from project.users.serializers.users import UserModelSerializer
from project.users.models import User


class ProfileDetail(APIView):
    def patch(self, request, user_id, format=None):
        user = User.objects.get(id=user_id)

        profile = user.profile
        serializer = ProfileModelSerializer(
            profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = UserModelSerializer(user).data
        return Response(response_wrapper(data=data, success=True))
