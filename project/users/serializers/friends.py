from rest_framework import serializers
from project.users.models import User, Friend
from django.utils import timezone


class FriendModelSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()
    friend_id = serializers.UUIDField()
    accepted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Friend
        fields = ("user_id", "friend_id", "accepted")

    def validate(self, data):
        if (
            not User.objects.filter(id=data["friend_id"]).exists()
            or not User.objects.filter(id=data["user_id"]).exists()
        ):
            raise serializers.ValidationError("User does not exist")

        friend = Friend.objects.filter(
            user_id=data["user_id"], friend_id=data["friend_id"]
        )

        if friend.exists():
            raise serializers.ValidationError("Invitation already exists.")

        return data

    def create(self, validated_data):
        try:
            friend = Friend.objects.get(
                user_id=validated_data["friend_id"],
                friend_id=validated_data["user_id"],
            )
        except Exception:
            friend = Friend.objects.create(**validated_data)
        else:
            friend.accepted = True
            friend.accepted_date = timezone.now()
            friend.save()

        return friend
