from rest_framework import serializers
from project.users.models import User, Friend


class FriendModelSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()
    friend_id = serializers.UUIDField()
    accepted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Friend
        fields = ("user_id", "friend_id", "accepted")

    def validate_friend_id(self, data):
        if not User.objects.filter(id=data).exists():
            raise serializers.ValidationError("User does not exist")
        return data

    def create(self, validated_data):
        friend = Friend.objects.create(**validated_data)
        return friend
