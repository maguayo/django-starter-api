import jwt
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings
from project.users.models import User, Profile
from project.users.serializers.profiles import ProfileModelSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserModelSerializer(serializers.ModelSerializer):
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile",
        )


class UserSignUpSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )
    phone_number = serializers.CharField(
        validators=[phone_regex], required=False
    )
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    first_name = serializers.CharField(
        min_length=2, max_length=30, required=False
    )
    last_name = serializers.CharField(
        min_length=2, max_length=30, required=False
    )

    def validate(self, data):
        """Verify passwords match."""
        passwd = data["password"]
        passwd_conf = data["password_confirmation"]
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop("password_confirmation")
        user = User.objects.create_user(
            **data, is_verified=False, is_client=True
        )
        Profile.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(email=data["email"], password=data["password"])

        if not user:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        self.context["user"] = user

        return data

    def create(self, data):
        """Handle user and profile creation."""
        user = self.context["user"]
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)


class TokenSerialiser(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, data):
        try:
            payload = jwt.decode(
                data, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link has expired.")
        except jwt.PyJWTError:
            raise serializers.ValidationError("Invalid token")

        self.context["payload"] = payload
        return data

    def save(self):
        payload = self.context["payload"]
        user = User.objects.get(email=payload["email"])
        return jwt_encode_handler(jwt_payload_handler(user))
