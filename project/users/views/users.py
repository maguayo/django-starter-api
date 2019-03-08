from rest_framework import mixins, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from project.functions import response_wrapper
from project.users.serializers.profiles import ProfileModelSerializer
from project.users.serializers.users import (
    TokenSerialiser,
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
)
from project.users.models import User
from project.users.permissions import ActionBasedPermission
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: [
            "update",
            "partial_update",
            "destroy",
            "list",
            "retrieve",
            "profile",
        ],
        permissions.AllowAny: [
            "login",
            "signup",
            "token_verify",
            "token_refresh",
        ],
    }

    @action(detail=False, methods=["post"])
    def login(self, request):
        token_login = UserLoginSerializer(data=request.data)
        token_login.is_valid(raise_exception=True)
        token = token_login.save()

        return Response(response_wrapper(data={"token": token}, success=True))

    @action(detail=False, methods=["post"])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(
            response_wrapper(data=data, success=True),
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], url_path="token/refresh")
    def token_refresh(self, request):
        token_refresh = TokenSerialiser(data=request.data)
        token_refresh.is_valid(raise_exception=True)
        token = token_refresh.save()
        return Response(response_wrapper(data={"token": token}, success=True))

    @action(detail=False, methods=["post"], url_path="token/verify")
    def token_verify(self, request):
        token_refresh = TokenSerialiser(data=request.data)
        token_refresh.is_valid(raise_exception=True)

        token = token_refresh.data["token"]

        return Response(response_wrapper(data={"token": token}, success=True))

    @action(detail=True, methods=["put", "patch"])
    def profile(self, request, *args, **kwargs):
        user = self.get_object()

        profile = user.profile
        serializer = ProfileModelSerializer(
            profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = UserModelSerializer(user).data
        return Response(response_wrapper(data=data, success=True))

    def update(self, request, *args, **kwargs):
        response = super(UserViewSet, self).update(request, *args, **kwargs)
        data = UserModelSerializer(response.data).data
        return Response(response_wrapper(data=data, success=True))

    def retrieve(self, request, pk) -> Response:
        user = self.get_object()
        serialiser = UserModelSerializer(user)
        return Response(response_wrapper(data=serialiser.data, success=True))
