from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from project.users.models.friends import Friend
from project.users.serializers.friends import FriendModelSerializer
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from project.functions import response_wrapper


class FriendsList(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        friends = Friend.objects.filter(user=request.user)
        serialiser = FriendModelSerializer(friends, many=True)
        return Response(response_wrapper(data=serialiser.data, success=True))

    def post(self, request):
        serialiser = FriendModelSerializer(data=request.data)
        serialiser.is_valid(raise_exception=True)
        serialiser.save()

        return Response(
            response_wrapper(data=serialiser.data, success=True),
            status=status.HTTP_201_CREATED,
        )
